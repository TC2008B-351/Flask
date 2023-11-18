from flask import Flask, request
import json
from mesa.models import TrafficModel

app = Flask(__name__)

model = TrafficModel()

@app.route('/')
def index():
    return "My API is running!"

@app.route('/getPositions', methods=['GET'])
def getPositions():
    if request.method == 'GET':
        positions = model.getPositions()
        model.step()
        print(json.dumps(positions))
        return 0
        # return "{'positions:'"+p2+"}"

if __name__ == '__main__':
    p1 = model.getPositions()
    print(json.dumps(p1))
    app.run(debug=True, port=8000)
