from db_util import *
from flask import Flask, jsonify, request

from util import get_episode

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/data/sub_anime')
def get_sub_anime():
    return jsonify(get_all_sub_list())


@app.route('/data/bangumi_info')
def get_bangumi_info():
    return jsonify(get_bgm_info())



@app.route('/data/switch', methods=["post"])
def switch_change():
    anime_id = request.get_json()['id']
    change_status(anime_id)
    msg = {"message": "ok"}
    return jsonify(msg)


@app.route('/data/sub_update', methods=["post"])
def get_new_episode():
    sub_list = get_sub_list()
    for sub in sub_list:
        get_episode(sub)
    return jsonify(get_episode_list())


@app.route('/data/add_sub', methods=["post"])
def add_sub():
    data = request.get_json()
    data['_id'] = int(data['_id'])
    data['last_time'] = 0
    data['status'] = True
    add_sub_anime(data)
    msg = {"message": "ok"}
    return jsonify(msg)


@app.route('/data/delete_sub', methods=["post"])
def del_sub():
    data = request.get_json()
    delete_sub_anime(data['id'])
    msg = {"message": "ok"}
    return jsonify(msg)


@app.route('/data/edit_sub', methods=["post"])
def edit_tran():
    data = request.get_json()['data']
    update_sub(data)
    msg = {"message": "ok"}
    return jsonify(msg)


@app.route('/data/new_episode')
def show_new_episode():
    return jsonify(get_episode_list())


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
