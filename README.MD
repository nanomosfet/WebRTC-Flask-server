# Remote connection with flask and eventlet

## Getting this app running on your server

1. Find some webserver. SSH into it.
2. Get a domain name and make sure you properly point it to your server.
3. Install Nginx, python and pip on the server
4. Clone this repo onto your server. 
5. Run a HTTPS enabled Nginx reverse proxy for the eventlet WSGI server that will run on localhost:8080. You *need* to have HTTPS configured for your your server in order for this to work as WebRTC will not operate on a HTTP protocol. Use these [nginx-config files](https://github.com/nanomosfet/WebRTC-Flask-server/tree/master/nginx-config) as a guide to creating your own server configuration on Nginx for your domain. Also note that I used [Let's Encrypt](https://letsencrypt.org/) to manage my ssl cert. Look at [these Nginx resources](https://www.nginx.com/resources/admin-guide/) for more information on Nginx server configuration.
6. Change directory into root file of this repository. Run `pip install .` to install all needed packages.
7. Run the webRTCserver.py file `python webRTCserver.py`. You can check now that on your localhost:8080 that a page is loading. Note that if you are on the web you need to have HTTPS set up. 

8. Last word I should mention that this has no stun and turn server implementation, only using googles stun server which is not meant for production. More info on [WebRTC in the real world](https://www.html5rocks.com/en/tutorials/webrtc/infrastructure/)
