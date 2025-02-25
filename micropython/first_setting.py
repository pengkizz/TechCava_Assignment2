from flask import Flask,jsonify,request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

uri = "mongodb+srv://Khairunnisaa54:Khay54@techcava.kyln8.mongodb.net/?retryWrites=true&w=majority&appName=TechCava"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['MyDatabase'] # ganti sesuai dengan nama database kalian
my_collections = db['MyCollection'] # ganti sesuai dengan nama collections kalian


# results = my_collections.insert_many([murid_1,murid_2])
# print(results.inserted_ids) # akan menghasilkan ID dari data yang kita masukkan

get_data=my_collections.find()

for x in get_data:
    print(x)
    

app = Flask(__name__)

@app.route('/', methods=['GET'])
def entry_point():
    return jsonify(message='Hello semuanya!')

# @app.route('/tes', methods=['GET', 'POST'])
# def coba():
#     if request.method == 'POST':
#         body = request.get_json()
#         return jsonify(message='you just send POST', data=body['data'])
#     elif request.method == 'GET':
#         return jsonify(message="yuhu udh bisa GET")

@app.route('/api/sensor', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.json  # Menerima data dari request
        # data["timestamp"] = datetime.now()  # Tambahkan timestamp otomatis

        # Simpan ke MongoDB
        result = my_collections.insert_one(data)
        
        return jsonify({"message": "Data berhasil disimpan!", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sensor", methods=["GET"])
def get_sensor_data():
    data = my_collections.find()  # Ambil semua data, tanpa field _id
    return jsonify(data)

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True, port=7000)