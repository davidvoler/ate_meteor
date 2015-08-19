from MeteorClient import MeteorClient

client = MeteorClient('ws://127.0.0.1:3000/websocket', auto_reconnect=True, auto_reconnect_timeout=0.3)
client.connect()


def callback_function(error, result):
    if error:
        print(error)
        return

    print(result)

client.call('runServerFixture', ['EK6qPmdg53kcwgZJS'], callback_function)

client.close()