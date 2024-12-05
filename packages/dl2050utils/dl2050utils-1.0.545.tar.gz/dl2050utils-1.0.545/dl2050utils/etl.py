import re
from pathlib import Path
import asyncio
import json
import pandas as pd
from dl2050utils.core import *

def q(db, qss):
    res = None
    for qs in qss.split(';'): res = asyncio.get_event_loop().run_until_complete(db.query(qs))
    return res

def get_model_names(path):
    models = []
    for f in Path(path).glob('*.json'):
        r = re.search('(.*)$', f.stem, re.IGNORECASE)
        if(r is None): continue
        models.append(r.group(1))
    return models

def create_model(db, model, fname=None, path='.'):
    fname = fname or f'{model}.json'
    fname = f'{path}/{fname}'
    try:
        with open(fname) as f: meta=json.load(f)
        q(db, f"insert into models (model,meta) values ('{model}','{json.dumps(meta)}')")
        return False
    except Exception as e:
        print(str(e))
        return True

def update_model(db, model, fname=None, path='.'):
    fname = fname or f'{model}.json'
    fname = f'{path}/{fname}'
    try:
        with open(fname) as f: meta=json.load(f)
        q(db, f"update models set meta='{json.dumps(meta)}' where model='{model}'")
        return False
    except Exception as e:
        print(str(e))
        return True
    
def merge_model(db, model, fname, path='.'):
    fname = f'{path}/{fname}'
    try:
        meta = get_model(db, model)
        with open(fname) as f: meta2=json.load(f)
        meta = {**meta, **meta2}
        q(db, f"update models set meta='{json.dumps(meta)}' where model='{model}'")
        return False
    except Exception as e:
        print(str(e))
        return True

def delete_model(db, model):
    return q(db, f"delete from models where model='{model}'")

def get_all_models(db):
    return [e['model'] for e in q(db,f"select model from models")]

def get_model(db, model):
    try:
        return json.loads(q(db, f"select meta from models where model='{model}'")[0]['meta'])
    except Exception as e:
        return

async def db_insert_df(db, df, tbl, renames={}):
    for _,row in df.iterrows():
        d = {}
        for k,v in row.items(): d[renames[k] if k in renames else k] = v
        await db.insert(tbl, d)

def get_tree_rows(rows, idx, parent, df, cols, level, crank=None, max_level=None):
    if max_level and level>=max_level: return 0
    c1 = cols[level]
    vals = df.groupby(c1).sum().sort_values(crank,ascending=False).index.values
    for v in vals:
        df1 = df[df[c1]==v]
        nodeidx = idx[0]
        idx[0] += 1
        n = get_tree_rows(rows, idx, nodeidx, df1, cols, level+1, crank=crank, max_level=max_level)
        nn = idx[0]-nodeidx-1
        leaf = n==0
        rows.append([nodeidx, parent, level+1, leaf, n, nn, v])
    return len(vals)

def build_tree_tbl(df, cols, vcol, crank=None, max_level=None):
    df1 = df[cols+[vcol]].groupby(cols).sum().reset_index()
    for c in cols: df1.loc[df1[c]=='',c] = 'Etc'
    tcols = ['id', 'parent', 'lv', 'leaf', 'n', 'nn', 'name']
    rows = []
    get_tree_rows(rows, [1], 0, df1, cols, 0, crank=crank, max_level=max_level)
    return pd.DataFrame(rows, columns=tcols).sort_values('id')

def get_tree_json(df, parent=0):
    rows = []
    df1 = df[df['parent']==parent]
    for i in range(len(df1)):
        d = df1.iloc[i].to_dict()
        if d['leaf']!=True: d['children']=get_tree_json(df, parent=d['id'])
        rows.append(d)
    return rows

def get_json(df, cols, key):
    res = []
    while True:
        df1 = df[df['id']==key]
        if len(df1)==0: break
        d = df1.iloc[0].to_dict()
        level = d['level']
        if level>len(cols) or level<0: break
        res.append({'col': cols[level-1], 'id': d['id'], 'name': d['name']})
        key = d['parent']
    return res
