from celery import Celery
app = Celery('proj', broker='amqp://localhost//', backend='redis://localhost')
from MeteorClient import MeteorClient
client = MeteorClient('ws://127.0.0.1:3000/websocket', auto_reconnect=True)
client.connect()



@app.task
def notify_meteor(x,y):
    print (client.connected) #Prints True
    client.call('myMetoerMethod', [x,y]) #Raises an exception