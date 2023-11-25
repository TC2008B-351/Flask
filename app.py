from flask import Flask, request
import json
from trafficSystem.models import TrafficModel
from trafficSystem.map import grid_size

app = Flask(__name__)

model = TrafficModel(grid_size, grid_size, 1)

def carToJSON(lists):
    cars_list = [
        {
        "id": json.dumps(car_data[0]),
        "x1": json.dumps(car_data[1]),
        "z1": json.dumps(car_data[2]),
        "x2": json.dumps(car_data[3]),
        "z2": json.dumps(car_data[4]),
        "x3": json.dumps(car_data[5]),
        "z3": json.dumps(car_data[6])
        }
        for car_data in lists]
    result_dict = {"Items": cars_list}
    return result_dict

def semaphoreToJSON(lists):
    sem_list = [
        {
            "id": json.dumps(sem_data[0]),
            "state": json.dumps(sem_data[1])
        }
        for sem_data in lists]
    result_dict = {"Semaphores": sem_list}
    return result_dict

@app.route('/')
def index():
    return "My API is running!"

@app.route('getSemaphoreState', methods=['GET'])
def getSemaphoreState():
    if request.method == 'GET':
        state = model.getSemaphoreState()
        return carToJSON(state)

@app.route('/getState', methods=['GET'])
def getCarPositions():
    if request.method == 'GET':
        state = model.getCarState()
        model.step()
        #print(toJSON(state))
        return semaphoreToJSON(state)

if __name__ == '__main__':
    intial_state = model.getState()
    #print("Initial State:")
    #print(toJSON(intial_state))
    app.run(debug=True, port=8000)


