# Remote connection with flask and eventlet

## Getting this app running on your server

1. Find some webserver. SSH into it.
2. Get a domain name and make sure you properly point it to your server.
3. Install Nginx, python and pip on the server
4. Clone this repo onto your server. 
5. Use my nginx-config files as a guide to creating your own server configuration on Nginx for your domain. Also note that I used [Let's Encrypt](https://letsencrypt.org/) to manage my ssl cert. SSL cert is manditory when using WebRTC. 
I'd say that the most important peice is the virtualhost segment
```
server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate /etc/certs/server.crt;
    ssl_certificate_key /etc/certs/server.key;
    ssl_trusted_certificate /etc/ssl/certs/GeoTrust_Global_CA.pem;
    
    add_header Strict-Transport-Security max-age=15768000;
    
    ssl_stapling on;
    ssl_stapling_verify on;
    
    location / {
        try_files $uri @webRTCserver;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwared-For $proxy_add_x_forwarded_for;
    }
    
    location @webRTCserver {
        proxy_pass http://127.0.0.1:8080;
    }
    
    location /socket.io/ {
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:8080;
    }   

    if ($scheme != "https") {
        return 301 https://$host$request_uri;
    } # managed by Certbot

}
```
6. Change directory into root file of repository. run `pip install .` to install all needed packages.
7. Run the webRTCserver.py file `python webRTCserver.py` Should be hosted on port 8080 and then Nginx will be using that as the `proxy_pass`

8. Last word I should mention that this has no stun and turn server implementation, only using googles stun server which is not meant for production. More info on [WebRTC in the real world](https://www.html5rocks.com/en/tutorials/webrtc/infrastructure/)
