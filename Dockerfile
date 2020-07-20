FROM python:3.6.8
ADD . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 80
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ls -lah /usr/src/app
# ENTRYPOINT ["export", "FLASK_ENV=development", ";", "python","prompt.py"]

CMD git config --global user.email "docker@example.com"; git config --global user.name "Docker"; git stash; git pull; export FLASK_ENV=development; python prompt.py

# For Bash:
# npm install && cd node_modules/splunk-sdk/ && npm install && cd ./../../ && node app.js && node node_modules/splunk-sdk/sdkdo runserver

# For auto-git updates on docker restart
# Before Build
# git remote set-url origin https://github.com/mayurah/phantom-prompt.git
# git remote set-url upstream https://github.com/mayurah/phantom-prompt.git

# While pushing as a user
# git remote set-url origin git@github.com:mayurah/phantom-prompt.git
# git remote set-url upstream git@github.com:mayurah/phantom-prompt.git

# Build Docker Image from Dockerfile
## docker build https://github.com/mayurah/phantom-prompt.git#master:.
# docker build . -t phantom-prompt
# docker run -t -i -p 81:80 phantom-prompt:latest

## PUSH
# docker login -u teamfdse
# docker tag phantom-prompt teamfdse/phantom-prompt:latest
# docker push teamfdse/phantom-prompt

## PULL
# docker pull teamfdse/phantom-prompt
# docker run -t -i -p 81:80 teamfdse/phantom-prompt:latest
# curl -v loalhost:81