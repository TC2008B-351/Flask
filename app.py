from flask import Flask, request
import json
from trafficSystem.models import TrafficModel
from trafficSystem.map import grid_size

app = Flask(__name__)

model = TrafficModel(grid_size, grid_size, 1)

def toJSON(lists):
    cars = []
    for item in lists:
        cars.append({"id": json.dumps(item[0]),
                     "x": json.dumps(item[1]),
                     "z": json.dumps(item[2]),
                     "rotation": json.dumps(item[3])
                    })
    return cars

@app.route('/')
def index():
    return "My API is running!"

@app.route('/getState', methods=['GET'])
def getPositions():
    if request.method == 'GET':
        state = model.getState()
        model.step()
        print(toJSON(state))
        return toJSON(state)

if __name__ == '__main__':
    intial_state = model.getState()
    # print("Initial State:")
    print(toJSON(intial_state))
    app.run(debug=True, port=8000)

