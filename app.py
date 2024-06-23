from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

app = Flask(__name__)
CORS(app)

uri = "mongodb+srv://neiracarlosargenis:WSGc5d39D9dJuSV7@cluster0.wr2s1ph.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

routeFiles = "."
# routeFiles = "/home/argenisneira/mysite"

@app.route('/')
def root():
  return "root"

@app.route('/save', methods=['POST'])
def save_data():
  data = request.get_json()
  with open(routeFiles + "/datos.txt", 'w') as archivo:
    # Escribir el contenido en el archivo
    archivo.write(json.dumps(data))
  return jsonify(data)

@app.route('/get_values', methods=['GET'])
def get_data():
  #algo que se puede mejorar es desde el front enviar un objeto con 3 keys
  #pero lo puedo manejar en el backend para que sean leidos por la otra pagina
  result = []
  with open(routeFiles + "/datos.txt", 'r') as archivo:
    contenido = archivo.read()
    dataJson = json.loads(contenido)
    element_count = len(dataJson) // 3
    for i in range(1, element_count + 1):
      result.append({
        "word" : dataJson[f"word{i}"],
        "score" : dataJson[f"score{i}"],
        "show" : dataJson[f"show{i}"],
      })
  #the one who first buzz
  with open(routeFiles + '/buzz.txt', 'r') as archivo:
    first_line = archivo.readline().strip()
    first_buz = first_line if first_line else '{"usuario": ""}'

  #if the button wrong is pressed
  with open(routeFiles + '/wrong.txt', 'r') as archivo:
    wrong = archivo.readline().strip()

  return jsonify({"values": result, "first" : first_buz, "wrong" : wrong})

#handle buzz
@app.route('/buzz', methods=['POST'])
def first_buz():
  data = request.get_json()
  with open(routeFiles + '/buzz.txt', 'a') as archivo:
    archivo.write(json.dumps(data) + "\n")
  return "OK"

@app.route('/reset_buzz', methods=['GET'])
def reset_buzz():
  with open(routeFiles + '/buzz.txt', 'w') as archivo:
    archivo.write('')
  return "OK"

#show wrong for a few seconds
@app.route('/wrong', methods=['POST'])
def show_wrong():
  data = request.get_json()
  number = data['wrong']
  with open(routeFiles + '/wrong.txt', 'w') as archivo:
    archivo.write(str(number))
  return "OK"

#Logica que incluye conectarse a la base de datos
@app.route("/get_games",methods=['GET'])
def get_games():
  t=client.cien_personas_dijeron.matches.find()
  # Convertir cursor a una lista de diccionarios  
  documents = []
  for document in t:
      # Convierte ObjectId a str para evitar el error de serialización
      document['_id'] = str(document['_id'])
      documents.append(document)
  return jsonify(documents), 200

#SEGUNDA APPLICACION
@app.route('/save_canvas', methods=['POST'])
def save_canvas():
  data = request.get_json()
  with open("/home/argenisneira/canvas-form-api/database.txt", 'a') as archivo:
    archivo.write(json.dumps(data) + "\n")
  return "OK"

@app.route('/get_canvas', methods=['GET'])
def get_canvas():
  data = []
  with open("/home/argenisneira/canvas-form-api/database.txt", "r") as archivo:
    for linea in archivo:
      data.append(json.loads(linea))
  return jsonify({"array": data})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080,debug=False)