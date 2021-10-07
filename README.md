# Phantom Prompt

URL based Phantom Prompt Handler


## Run it on Docker

Using Docker to deploy phantom-prompt

a. Download and Install Docker 🐳

b. In Terminal (Console)

- Verify that the docker is installed: `docker -v`
- Pull docker image locally: `docker pull teamfdse/phantom-prompt:latest`
- Run docker image 📦: `docker run -t -i -p 81:80 teamfdse/phantom-prompt:latest`



Nginx Reverse Proxy (optional)

```conf
http {

  upstream prompt {
    server 127.0.0.1:81;
  }

  server {
    ...
    location / {
      proxy_pass http://prompt/prompt;
    }
  }


}
```
