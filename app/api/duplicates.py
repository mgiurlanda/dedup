from app.api import bp
from flask import make_response
import pandas as pd
from app import db
import io

@bp.route('/duplicates/<entity>', methods=['GET'])
def get_duplicates(entity):
    df = pd.read_sql("select * from %s" % entity.lower()+"_output", db.engine)
    return _make_csv_response(df)

@bp.route('/duplicates/<entity>/<cluster_id>', methods=['GET'])
def get_duplicates_by_cluster(entity, cluster_id):
    df = pd.read_sql("select * from %s where cluster_id=%s" % (entity.lower()+"_output", cluster_id), db.engine)
    return _make_csv_response(df)
    
def _make_csv_response(df):
    s_buf = io.StringIO()
    df.to_csv(s_buf)
    output = make_response(s_buf.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=output.csv"
    output.headers["Content-type"] = "text/csv"
    return output