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


def get_episode_pub_date(episode_id):
    return episode_col.find_one({"_id": {"$eq": episode_id}}, {"pub_date": 1})['pub_date']


def get_bgm_info():
    result_list = []
    for d in list(col.find({"bangumi_id": {"$ne": 10}}, {"name": 1, "bangumi_id": 1})):
        result_list.append({"title": d['name'],"url": "https://api.bgm.tv/v0/subjects/{}/image?type=common".format(d['bangumi_id'])})
    return result_list


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


def update_sub(data):
    update_query = {"_id": data['_id']}
    new_values = {"$set": {"name": data['name'], "subtitle": data['subtitle'], "link": data['link'],
                           "bangumi_id": data['bangumi_id'], "last_time": data['last_time']}}
    col.update_one(update_query, new_values)


# 增加
def add_sub_anime(data_dict):
    col.insert_one(data_dict)


def add_episode(data_dict):
    episode_col.insert_one(data_dict)


# 删除
def delete_sub_anime(anime_id):
    col.delete_one({"_id": anime_id})


def delete_episode(episode_id):
    episode_col.delete_one({"_id": episode_id})
