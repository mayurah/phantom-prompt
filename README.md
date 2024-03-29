# Phantom Prompt

URL based Phantom Prompt Handler


## Run it on Docker

Using Docker to deploy phantom-prompt

a. Download and Install Docker 🐳

b. In Terminal (Console)

- Verify that the docker is installed: `docker -v`
- Pull docker image locally: `docker pull teamfdse/phantom-prompt:latest`
- Run docker image 📦: `docker run -d -t -i -p 81:80 --restart always teamfdse/phantom-prompt:latest `

## Verify Web Server

> ```curl -vk http://localhost:81/``` should return `root`.

Nginx Reverse Proxy (optional)

# Nginx Higher Level Design

```
User --> Nginx (Port: 443) --upstream--> Containerized URL Prompt App (Port: 81)
```


# Backup existing NGINX
> **cp /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak**

# Modify Nginx Proxy
> **vim /etc/nginx/conf.d/default.conf**

> **Alternative nginx path** `/opt/phantom/usr/nginx/conf/conf.d/phantom-nginx-server.conf`

```conf
http {

  ... put below code inside http {}. (parallel to other *upstream* )
  upstream prompt {
    server 127.0.0.1:81;
  }
  ...
  
  

  server {
    ... put below code inside server {}.  (parallel to other *location* )
    location /prompt {
      proxy_pass http://prompt/prompt;
    }
  }
  ... 

}
```

* The only 

# Restart Nginx
> service nginx restart 
