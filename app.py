from flask import Flask, request, jsonify, make_response
import pymysql

app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def hello():
    return 'hello world'

mydb = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='mymusic'
)

@app.route('/post_music', method=['POST'])
def post_music():
    hasil = {"status": "gagal"}
    query = "INSERT INTO music(title, artist, rilis) VALUES(%s,%s,%s)"
    try:
        data = request.json
        title = data["title"]
        artist = data["artist"]
        rilis = data.rilis["rilis"]
        value =(title, artist, rilis)
        mycorsor = mydb.cursor()
        mycorsor.execute(query, value)
        mydb.commit()
        hasil = {"status": "berhasil"}
    except Exception as e:
        print("Error: " + str(e))
    
    return jsonify(hasil)

@app.route('/music', methods=['GET'])
def music():
    query = "SELECT * FROM music"

    mycorsor = mydb.cursor()
    mycorsor.execute(query)
    data = mycorsor.fetchall()
    row_headers = [x[0] for x in mycorsor.description]
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    mydb.commit()
    return make_response(jsonify(json_data),200)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5123)