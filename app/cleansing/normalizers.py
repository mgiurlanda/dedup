from unidecode import unidecode
import pandas as pd
import numpy as np
from ast import literal_eval
from pyparsing import Word, alphas, nums, OneOrMore, oneOf, Keyword, Combine, Group, Dict

def _trim(x):
    x = x.split()
    x = ' '.join(x)
    return x  

def clean_punctuation(df):
    for i in df.columns:
        df[i] = df[i].astype(str) 
    df = df.applymap(lambda x: x.lower())
    for i in df.columns:
        df[i] = df[i].str.replace('[^\w\s\.\(\)\,\\\\]','')
    df = df.applymap(lambda x: _trim(x))
    df = df.applymap(lambda x: unidecode(x))
    #for i in df.columns:
    #    df[i] = df[i].replace({'nan': None})
    df.replace('nan', None, inplace=True)
    df.replace('', None, inplace=True)
    df.replace('.', None, inplace=True)
    return df

MONTHS = "months"
HOURS = "hours"
YEARS = "years"
DAYS = "days"
WEEKS = "weeks"
RUNNING_HOURS = "running hours"
HOURS_IN_YEAR = 8760
HOURS_IN_MONTH = 730
HOURS_IN_DAY = 24
HOURS_IN_WEEK = 168

dispatch = {
    MONTHS: lambda value: value * HOURS_IN_MONTH,
    YEARS: lambda value: value * HOURS_IN_YEAR,
    DAYS: lambda value: value * HOURS_IN_DAY,
    WEEKS: lambda value: value * HOURS_IN_WEEK
}

period = Word( nums )
unit = Combine(Keyword( MONTHS ) | Keyword( HOURS ) | Combine(DAYS) | Combine(YEARS) | Combine(RUNNING_HOURS))

frequency = Group(period + unit)

grammar = OneOrMore(frequency)

def frequency_normalizer(df):

    df['Frequency'] = df['Frequency'].map(_frequency_normalizer)
    return df
    

def _frequency_normalizer(frequencyStr):
    if not frequencyStr or not frequencyStr.strip() or frequencyStr == "none":
        return frequencyStr

    tokenized = grammar.parseString(frequencyStr)

    normalized = []
    for f in tokenized:
        periodValue = f[0]
        unitValue = f[1]
        if unitValue == RUNNING_HOURS or unitValue == HOURS:
            normalized.append(periodValue + " " + unitValue)
        else:
            normalizedPeriod = dispatch[unitValue](int(periodValue))
            normalized.append(str(normalizedPeriod) + " hours")
    return ' '.join(normalized)