import os
import subprocess
import argparse

PYTHONPATH = ''

# Parse through optional arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--hostname", help="Host URL", required=False, default='0.0.0.0')
parser.add_argument("-p", "--port", help="Port Number", required=False, default=5000)
parser.add_argument("-n", "--containername", help="Docker Container Name", required=False,
                    default="Chemical Transformation Database API")
args = parser.parse_args()

# Build image
docker_build = 'docker build -t pf_chem_trans .'
os.system(docker_build)

# Get image name
image_output = subprocess.check_output(['docker', 'image', 'ls'])
image = str(image_output.split()[8]).split("'")[1]

# Run the docker container from docker image
docker_run = f'docker run --name {args.containername} -e ' \
             f'FLASK_APP=/app/flask-api/main.py -e PYTHONPATH=${PYTHONPATH}:/app/flask-api/' + \
             f' -p {args.port}:5000 -d -it {image}'
os.system(docker_run)

# Get container name
container_output = subprocess.check_output(['docker', 'container', 'ls'])
container = str(container_output.split()[8]).split("'")[1]

# Start Flask
docker_exec = f'docker exec {container} flask run -h {args.hostname} -p 5000'
os.system(docker_exec)
