import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['anime']
col = db['sub']
episode_col = db['episode']


# 查询

def get_all_sub_list():
    return list(col.find())


def get_sub_list():
    return list(col.find({"status": {"$eq": True}}))


def get_anime(anime_id):
    return col.find_one({"_id": {"$eq": anime_id}})


def get_anime_name(anime_id):
    return col.find_one({"_id": {"$eq": anime_id}}, {"name": 1})


def get_episode_list():
    return list(episode_col.find({"download_flag": {"$eq": False}}).sort("pub_date", -1))

# 修改

def change_status(anime_id):
    result = col.find_one({"_id": {"$eq": anime_id}}, {"status": 1})
    # print(anime_id)
    if result['status']:
        col.update_one({"_id": {"$eq": anime_id}}, {"$set": {"status": False}})
    else:
        col.update_one({"_id": {"$eq": anime_id}}, {"$set": {"status": True}})


def update_timestamp(anime_id, new_timestamp):
    col.update_one({"_id": {"$eq": anime_id}}, {"$set": {"last_time": new_timestamp}})


# 增加
def add_sub_anime(data_dict):
    col.insert_one(data_dict)


def add_episode(data_dict):
    episode_col.insert_one(data_dict)
