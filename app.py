from datetime import datetime
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
client = MongoClient('mongodb+srv://kentang:eUenw9z4QIlEoGzW@cluster0.mjce1r3.mongodb.net/?retryWrites=true&w=majority')
db = client.dbdiary

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    today = datetime.now()
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    profile_name = f'profile-{mytime}.{extension}'
    save_to = f'static/{profile_name}'
    profile.save(save_to)

    doc = {
        'file': filename,
        'profile': profile_name,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data was saved!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5009, debug=True)