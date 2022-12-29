#!/bin/bash

# create a virtual environment
cd ..
python3 -m venv IEEE_SEMS

# activate the virtual environment 
source IEEE_SEMS/bin/activate


pip install -r requirements.txt
# write the commands that will connect the pi to internet