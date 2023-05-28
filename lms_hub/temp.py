from flask import Blueprint, send_from_directory

temp = Blueprint("temp", __name__)

@temp.route('/calendar_script/<path:path>')
def send_calendar(path):
    return send_from_directory('templates/lms/calendar_script', path)

@temp.route('/dashboard_script/<path:path>')
def send_dashboard(path):
    return send_from_directory('templates/lms/dashboard_script', path)

@temp.route('/classcard_script/<path:path>')
def send_classcard(path):
    return send_from_directory('templates/lms/classcard_script', path)