# %%
import pymongo
# %%
myclient = pymongo.MongoClient(
    'localhost'
    # "mongodb+srv://itba:itba_pass@cluster0.6mytljp.mongodb.net/"

)
# %%
myclient.list_database_names()
# %%
mydb = myclient['mlops']
# %%
mydb.list_collection_names()
# %%
mydb.airbyte_raw_scores.count_documents({})
# %%
cursor = mydb.airbyte_raw_scores.find(
    { "_airbyte_data.rating": { "$gte": 5 } }
)
# %%
for c in cursor:
    print(c['_airbyte_data'])
    break
# %%
