# cicd
####
Go to steup.py edit the version
Go to setup edit the user name
######

Step 1: Clean the Workspace 
run:     rm -rf target
run:     rm -rf dist build *.egg-info target

####
Step 2: Build the Project
run:     pyb clean publish
run:     ls target/dist/
#####

after build the artifact to install 
cd target/dist/hello_world_app-0.1.0 
 run:    python setup.py sdist bdist_wheel 
 run:    ls dist 
 ####


 ####
 pip install hello-world-app-betrand
python -m hello_world_app.app
#####

####
Upload to PyPI




#####
to access the application run python -m hello_world_app.app
this name was created automatically ducing the build process