from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
  return "root"

@app.route('/save', methods=['POST'])
def save_data():
  data = request.get_json()
  with open("datos.txt", 'w') as archivo:
    # Escribir el contenido en el archivo
    archivo.write(json.dumps(data))
  return jsonify(data)

@app.route('/get_values', methods=['GET'])
def get_data():
  #algo que se puede mejorar es desde el front enviar un objeto con 3 keys
  #pero lo puedo manejar en el backend para que sean leidos por la otra pagina
  result = []
  with open("datos.txt", 'r') as archivo:
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
  with open('buzz.txt', 'r') as archivo:
    first_line = archivo.readline().strip()
    first_buz = first_line if first_line else '{"usuario": ""}'
  return jsonify({"values": result, "first" : first_buz})

#handle buzz
@app.route('/buzz', methods=['POST'])
def first_buz():
  data = request.get_json()
  with open('buzz.txt', 'a') as archivo:
    archivo.write(json.dumps(data) + "\n")
  return "OK"

@app.route('/reset_buzz', methods=['GET'])
def reset_buzz():
  with open('buzz.txt', 'w') as archivo:
    archivo.write('')
  return "OK"

# @app.route('/get_first_buzz', methods=['GET'])
# def get_first():
#   with open('buzz.txt', 'r') as archivo:
#     first_line = archivo.readline().strip
#     first_buz = first_line if first_line else '{"usuario": ""}'
#   return jsonify(first_buz)

if __name__ == '__main__':
  app.run(debug=False)