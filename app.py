from flask import Flask, request
import json
from trafficSystem.models import TrafficModel
from trafficSystem.map import grid_size

app = Flask(__name__)

model = TrafficModel(grid_size, grid_size, 1)

def toJSON(lists):
    result_dict = {"cars": {}}
    for list in lists:
        car_pos = {"x": json.dumps(list[1]), "y": json.dumps(list[2])}
        result_dict["cars"][json.dumps(list[0])] = car_pos
    return result_dict

@app.route('/')
def index():
    return "My API is running!"

@app.route('/getPositions', methods=['GET'])
def getPositions():
    if request.method == 'GET':
        positions = model.getPositions()
        model.step()
        # print(toJSON(positions))
        return toJSON(positions)

if __name__ == '__main__':
    intial_positions = model.getPositions()
    # print("Initial Positions:")
    # print(toJSON(intial_positions))
    app.run(debug=False, port=8000)
