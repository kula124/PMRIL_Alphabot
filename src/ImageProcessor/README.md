# Image processor

Entry point and interface for the application.
Uses the signal from video camera to find the robot and assign goal destination.

Robot detection is implemented with colour-based fast object detection algorithm.

Requires the websocket server to be live and listening on the configured port.

## How to setup the environment
Folder name used by the project for virtual environment is `env`
This folder is ignored by `.gitignore` so keep it consistent.
The environment can be initialized in few steps:
### Linux
```bash
$ python3 -m venv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
$ python3 main.py
```
### Windows
```sh
$ py -m pip install virtualenv
$ py -m venv env
$ .\env\Scripts\activate
$ pip install -r requirements.txt
$ python main.py
```

## Controls
Follow the instructions on screen to initialize the app.

- **Left-click and drag** to capture the markers on the car.
- **Right-click** to reset the markers.
- **Middle mouse button** to mark the goal destination.
- **ALT + middle mouse button** to reset the goal destination  
