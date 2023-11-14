from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return "My API is running!"

@app.route('/theChallenge', methods = ['POST', 'GET'])
def theChallenge():
    if request.method == 'GET':
        name = request.args.get('name')
        return 'welcome %s' % name
    else:
        return 'Please use GET!'




if __name__ == '__main__':
    app.run(debug=True, port=8000)
