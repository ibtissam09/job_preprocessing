import pymongo
import pandas as pd

def select_data():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["jobsDb"]
    mycol = mydb["JobsFrance"]
    documents = mycol.find({})
    df = pd.DataFrame(list(documents))
    return df
def select_data_with_filter(filter,val):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["jobsDb"]
    mycol = mydb["JobsFrance"]
    documents = mycol.find({filter:val})
    df = pd.DataFrame(list(documents))
    return df
def update_value(query_col,query_val, new_query, new_val):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["jobsDb"]
    mycol = mydb["JobsFrance"]
    myquery = { query_col: query_val }
    newvalues = { "$set": {new_query: new_val } }
    mycol.update_one(myquery, newvalues)
