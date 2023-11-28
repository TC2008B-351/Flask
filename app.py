from flask import Flask, request
import json
from trafficSystem.models import TrafficModel
from trafficSystem.map import grid_size

app = Flask(__name__)

model = TrafficModel(grid_size, grid_size, 17)

def initialCarToJSON(lists):
    cars_list = [
        {
        "id": json.dumps(car_data[0]),
        "x": json.dumps(car_data[1]),
        "z": json.dumps(car_data[2]),
        }
        for car_data in lists]
    result_dict = {"Items": cars_list}
    return result_dict

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
            "position": json.dumps(sem_data[1]),
            "state": sem_data[2]
        }
        for sem_data in lists]
    result_dict = {"Semaphores": sem_list}
    return result_dict

@app.route('/')
def index():
    return "My API is running!"

@app.route('/getNumberCars', methods=['GET'])
def getNumberCars():
    if request.method == 'GET':
        n_cars = model.num_cars
        return {'Cars' : json.dumps(n_cars)}

@app.route('/getSemaphoreState', methods=['GET'])
def getSemaphoreState():
    if request.method == 'GET':
        state = model.getSemaphoreState()
        return semaphoreToJSON(state)

@app.route('/getNextCarState', methods=['GET'])
def getCarPositions():
    if request.method == 'GET':
        state = model.getCarState()
        model.step()
        return carToJSON(state)

@app.route('/getInitialCarState', methods=['GET'])
def getInitialCarPositions():
    if request.method == 'GET':
        state = model.getInitialCarState()
        return initialCarToJSON(state)

if __name__ == '__main__':
    """
    intial_car_state = model.getCarState()
    intial_semaphore_state = model.getSemaphoreState()
    print("Initial State:")
    print(carToJSON(intial_car_state))
    print(semaphoreToJSON(intial_semaphore_state))
    """
    app.run(debug=True, port=8000)


