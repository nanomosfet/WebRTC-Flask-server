# Remote connection with flask and eventlet

## Getting this app running on your server

1. Find some webserver. SSH into it.
2. Get a domain name and make sure you properly point it to your server.
3. Install Nginx, virtualenv on the server
4. Clone this repo onto your server. 
5. Use my nginx-config files as a guide to creating your own server configuration on Nginx for your domain. Also note that I used [Let's Encrypt](https://letsencrypt.org/) to manage my ssl cert. SSL cert is manditory when using WebRTC. 
I'd say that the most important peice is the virtualhost segment
```
server {
	listen 80;
	listen [::]:80;

	server_name example.com;
	root /your/root/to/site;


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
    listen 443 ssl; # managed by Certbot
    ssl_certificate /path/to/chain; # managed by Certbot
    ssl_certificate_key /path/to/key; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot


    if ($scheme != "https") {
        return 301 https://$host$request_uri;
    } # managed by Certbot

}
```
6. Run the webRTCserver.py file `python webRTCserver.py` Should be hosted on port 8080 and then Nginx will be using that as the `proxy_pass`
7. Last word I should mention that this has no stun and turn server implementation, only using googles stun server which is not meant for production. More info on [WebRTC in the real world](https://www.html5rocks.com/en/tutorials/webrtc/infrastructure/)
