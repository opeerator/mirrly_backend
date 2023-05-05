from flask import Flask, render_template, jsonify
from mode_config import ModeManager

app = Flask(__name__)
mode_manager = ModeManager()

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

@app.route("/stop/<mode_name>", methods=['POST'])
def stop(mode_name):
    # Turn off every system.
    mode_manager.stop(mode_name)
    return jsonify({'message': "Stopped"})


app.run(host="0.0.0.0")