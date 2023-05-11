import atexit
import subprocess
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from mode_config import ModeManager
from head_control import HeadMotors
from foot_motors import FootMotors

mode_manager = ModeManager()
head_motors = HeadMotors()
current_move = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somesecret'
socketio = SocketIO(app)

FootMotors()

@socketio.event
def test_connect():
    print("Connected to mirrly")

@app.after_request
def add_header(response):
    """Adding header's for robot's response.

    Returns:
        json: Server's response
    """
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/")
def index():
    """A sample page for 0.0.0.0

    Returns:
        html: An html page. 
    """
    return render_template('index.html')


@app.route("/run/<mode_name>", methods=['POST'])
def run(mode_name):
    # Run different modes.
    mode_manager.run(mode_name)
    response = {'message': f'{mode_name} running'}
    if mode_manager.should_redirect(mode_name):
        response['redirect'] = True
    return jsonify(response)

@app.route("/status")
def status_check():
    battery_level = 90 # Placeholder for battery status.
    if mode_manager.is_running():
        return jsonify({"status": "processing", f"battery_level":"{battery_level}"})
    else:
        return jsonify({"status": "idle", f"battery_level":"{battery_level}"})
    
# @app.route("/head/move/<component>/<gpos>", methods=['POST'])
@socketio.on('move')
def move_head_m(message):
    res = head_motors.move(message['component'], message['gpos'])
    return jsonify({"status": f"{res}"})

# @app.route("/head/getinfo/<component>", methods=['POST'])
@socketio.on('/head/getinfo/all')
def head_info(data):
    res = head_motors.current_pos(data['component'])
    emit('info', {'data': res})

@app.route("/stop/<mode_name>", methods=['POST'])
def stop(mode_name):
    # Turn off every system.
    mode_manager.stop(mode_name)
    return jsonify({'message': "Stopped"})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
    head_motors.close()
