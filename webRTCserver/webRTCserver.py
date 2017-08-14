from flask import Flask, render_template, url_for
import socketio
import eventlet
import eventlet.wsgi
import datetime

sio = socketio.Server()
app = Flask(__name__)

connected_particpants = {}

def write_log(s):    
    with open('logfile.out', 'a+') as f:
        f.write('time: %s Action: %s \n' % (str(datetime.datetime.now()), s))

@app.route('/')
def index():
    """Serve index page"""
    return render_template('index.html')

@sio.on('message', namespace='/')
def messgage(sid, data):
    sio.emit('message', data=data)

@sio.on('disconnect', namespace='/')
def disconnect(sid):
    write_log("Received Disconnect message from %s" % sid)
    for room in connected_particpants:
        try:
            room.remove(sid)
            write_log("Remove %s from %s" %(sid, room))
        except:
            pass


@sio.on('create or join', namespace='/')
def create_or_join(sid, data):
    sio.enter_room(sid, data)
    try:
        connected_particpants[data].append(sid)
    except KeyError:
        connected_particpants[data] = [sid]
    numClients = len(connected_particpants[data])
    if numClients == 1:
        sio.emit('created', data)
    elif numClients > 2:
        sio.emit('full')
    elif numClients == 2:
        sio.emit('joined')
        sio.emit('join')
    print (sid, data, len(connected_particpants[data]))

@app.route('/<room>')
def room(room):
    return room

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)
