#!/usr/bin/env bash
# ---------------------------------------------------------------------
# This shell script helps a first time user set up his/her environment
# All it does:
#     - create a virtual env and activate it
#     - pip install all the required files from requirements.txt
# NOTE: YOU NEED TO HAVE PIP3 INSTALLED for this to work. This project
# requires python 3.5 and above
# ---------------------------------------------------------------------
#
clear

echo "----------------------------------------------"
echo " ------ PYTHON VENV PROJECT SETUP-------------"
echo "----------------------------------------------"


echo "This script installs your virtual environment"
sudo virtualenv --no-site-packages --distribute venv
echo "finished installing your virtual environment"

echo "----------------------------------------------"
echo " ------ PIP INSTALL REQUIREMENTS -------------"
echo "----------------------------------------------"


echo "NOTE: you must have pip3 installed for the requirements.txt to be installed"

echo "about to activate your virtual environment"
source ./venv/bin/activate ||  echo "is your virtual environment set up first? Run project_setup.sh"

echo "successfully activated your virtual environment"

echo "about to install from requirements.txt"
sudo ./venv/bin/pip3 install -r ./requirements.txt

echo "finished installing all requirements"