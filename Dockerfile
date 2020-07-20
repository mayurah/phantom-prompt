FROM python:3.6.8
ADD . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 10444
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["export", "FLASK_ENV=development", ";", "python","prompt.py"]

# CMD git config --global user.email "docker@example.com"; git config --global user.name "Docker"; git stash; git pull; npm start

# For Bash:
# npm install && cd node_modules/splunk-sdk/ && npm install && cd ./../../ && node app.js && node node_modules/splunk-sdk/sdkdo runserver

# Build Docker Image from Dockerfile
## docker build https://github.com/mayurah/phantom-prompt.git#master:.
# docker build . -t phantom-prompt
# docker run -t -i -p 80:80 phantom-prompt:latest

## PUSH
# docker login -u teamfdse
# docker tag phantom-prompt teamfdse/phantom-prompt:latest
# docker push teamfdse/phantom-prompt

## PULL
# docker pull teamfdse/phantom-prompt
# docker run -t -i -p 80:80 teamfdse/phantom-prompt:latest