## Python virtual environment
Folder name used by the project for virtual environment is `env`
This folder is ignored by `.gitignore` so keep it consistent.
The environment can be initialized in few steps:
### Linux
```bash
$ python3 -m venv env
$ source ./env/bin/activate
```
### Windows
```sh
$ py -m pip install virtualenv
$ py -m venv env
$ .\env\Scripts\activate
```