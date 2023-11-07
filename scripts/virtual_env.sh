#!/bin/bash
#######################################
# Setup Python virtual environment
#######################################

cd ..


function setup_venv() {
    python -m venv .venv
    source .venv/bin/activate
}


function exit_venv() {
    source deactivate
}


setup_venv
# exit_venv