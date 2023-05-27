LMS Backpack
This is a course requirements for CS191/192 Software Engineering Courses of the Department of Computer Science, College of Engineering, University of the Philippines, Diliman under the guidance of Ma. Rowena C. Solamo for AY 2020-2021.

Amante, David Alexander R.
Caluag, Jose Ellis Miguel C.
Choa, Christian Julien N.

Windows setup
```bash
python3.11 -m pip install virtualenv
python3.11 -m venv venv
.\venv\Scripts\activate
pip install flask flask-login firebase-admin google-auth-oauthlib requests python-dotenv
flask --app lms_hub/app --debug run
```

Linux setup
```bash
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv
source venv/bin/activate
pip install flask flask-login firebase-admin google-auth-oauthlib requests python-dotenv
```

If you want to run the app on debug mode, use
```bash
python3.11 -m lms_hub.app
```
If you want to deploy it to, for example, railway.app, then use
```bash
FLASK_RUN_PORT=$PORT FLASK_RUN_HOST=0.0.0.0 flask --app lms_hub/app run
```