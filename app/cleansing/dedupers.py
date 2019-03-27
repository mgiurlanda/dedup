from config import Config
import os
import dedupe
import app.cleansing.normalizers as normalizers
import pandas as pd
from flask import current_app
#from app import db

def run(config, entity_name):
    matched_entity = {}
    for entity in config['entities']:
        if entity["name"] == entity_name:
            matched_entity = entity
            break
    if (matched_entity):
        entity_df = pd.read_sql_query(matched_entity["query"], current_app.source_connection)
        for normalizer in matched_entity['normalizers']:
            entity_df = getattr(normalizers, normalizer)(entity_df)
        print(entity_df.head(5))
        deduper = EntityDeduper(entity_df, matched_entity)
        if (deduper.need_sampling):
            deduper.sample()
        if (deduper.need_training):
            deduper.train()
        return deduper.cluster()
    else:
        print('Entity %s not found '%(entity_name))



class EntityDeduper:
    
    def __init__(self, dataframe, entity):
        self.settings = entity["name"].lower() + "_settings"
        self.training = entity["name"].lower() + "_training.json"
        self.dictionary = dataframe.to_dict('index') 
        self.dataframe = dataframe
        self.entity = entity
        if os.path.exists(self.settings):
            with open(self.settings, 'rb') as sf :
                self.deduper = dedupe.StaticDedupe(sf, num_cores=4)
        else:
            self.deduper = dedupe.Dedupe(entity["matching_fields"], num_cores=4)

    def sample(self):
        if (type(self.deduper) == dedupe.Dedupe):
            self.deduper.sample(self.dictionary)
        else:
            print("Active Learning Deduplication not active")
            
    def isActiveLearningDeduper(self):
        return type(self.deduper) == dedupe.Dedupe

    def need_sampling(self):
        return self.isActiveLearningDeduper()
    
    def need_training(self):
        return self.isActiveLearningDeduper()

    def train(self):
        if (type(self.deduper) == dedupe.Dedupe):
            if os.path.exists(self.training):
                print('reading labeled examples from ', self.training)
                with open(self.training) as tf :
                    self.deduper.readTraining(tf)
            # use 'y', 'n' and 'u' keys to flag duplicates
            # press 'f' when you are finished
            dedupe.convenience.consoleLabel(self.deduper)
            # When finished, save our labeled, training pairs to disk
            with open(self.training, 'w') as tf:
                self.deduper.writeTraining(tf)
            
            # Notice our the argument here
            #
            # `recall` is the proportion of true dupes pairs that the learned
            # rules must cover. You may want to reduce this if your are making
            # too many blocks and too many comparisons.
            self.deduper.train(recall=0.90)

            with open(self.settings, 'wb') as sf:
                self.deduper.writeSettings(sf)

            # We can now remove some of the memory hobbing objects we used
            # for training
            self.deduper.cleanupTraining()
        else:
            print("Active Learning Deduplication not active")
    
    def cluster(self):
        # Set threshold
        print('threshold...')
        threshold = self.deduper.threshold(self.dictionary, recall_weight=1)

        # ## Clustering

        print('clustering...')
        clustered_dupes = self.deduper.match(self.dictionary, threshold)

        cluster_membership = {}
        cluster_id = 0
        for (cluster_id, cluster) in enumerate(clustered_dupes):
            id_set, scores = cluster
            cluster_d = [self.dictionary[c] for c in id_set]
            canonical_rep = dedupe.canonicalize(cluster_d)
            for record_id, score in zip(id_set, scores):
                cluster_membership[record_id] = {
                    "cluster id" : cluster_id,
                    "canonical representation" : canonical_rep,
                    "confidence": score
                }



        cluster_index=[]
        for i in cluster_membership.items():
            cluster_index.append(i)

        dfa = pd.DataFrame(cluster_index)

        dfa.rename(columns={0: 'Id'}, inplace=True)
            
        dfa['cluster id'] = dfa[1].apply(lambda x: x["cluster id"])
        dfa['confidence'] = dfa[1].apply(lambda x: x["confidence"])

        canonical_list=[]   

        for i in dfa[1][0]['canonical representation'].keys():
            canonical_list.append(i)
            dfa[i + ' - ' + 'canonical'] = None
            dfa[i + ' - ' + 'canonical'] = dfa[1].apply(lambda x: x['canonical representation'][i])

        dfa.set_index('Id', inplace=True)
        self.dataframe = self.dataframe.join(dfa)
        self.dataframe[self.entity["output_fields"] + ['cluster id', 'confidence']].to_csv(self.entity["name"].lower()+"_output.csv")
        #self.dataframe[self.entity["output_fields"] + ['cluster id', 'confidence']].to_sql(self.entity["name"].lower()+"_output", con=db.engine, if_exists='replace')
        return self.dataframe