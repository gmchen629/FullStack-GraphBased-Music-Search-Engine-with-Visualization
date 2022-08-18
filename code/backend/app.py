import flask
from flask import Flask
from flask_cors import CORS
from init_db import query_music_info, init_db, insert_new_feedback, query_recommend_name_list
from feedback import query_user_feedback, query_music_feedback

app = Flask(__name__)
CORS(app)   # restriction recommended


# function for http://127.0.0.1:5000/info/<music>
# for example http://127.0.0.1:5000/info/Danny Boy
@app.route("/info/<music>")
def music_info_result(music):
    data = query_music_info(music)
    json_data = flask.jsonify(data)
    return json_data


# function for http://127.0.0.1:5000/recommend/<music>
# for example http://127.0.0.1:5000/recommend/Danny Boy
@app.route("/recommend/<music_name>")
def music_recommend_result(music_name):
    data = query_recommend_name_list(music_name)
    json_data = flask.jsonify(data)
    return json_data


@app.route('/feedback/user_feedback/<rating>')
def user_feedback(rating):
    insert_new_feedback('user_feedback',[rating])
    # get current average feedback
    system_user_feedback = query_user_feedback()
    json_data = flask.jsonify(system_user_feedback)
    print("get user feedback")
    print(system_user_feedback)
    return json_data


@app.route('/feedback/music_feedback/<rating>')
def music_feedback(rating):
    insert_new_feedback('music_feedback',[rating])
    # get current average feedback
    music_user_feedback = query_music_feedback()
    json_data = flask.jsonify(music_user_feedback)
    print(music_user_feedback)
    return json_data


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3000, debug=True)
    init_db()
    app.run(port=5000, debug=True)
