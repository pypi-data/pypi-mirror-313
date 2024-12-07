class WebSocketClosure(Exception):
    pass


class ConnectionClosed(Exception):
    def __init__(self, websocket, close_code):
        self.websocket = websocket
        self.close_code = close_code

        print(self.websocket, self.close_code)


class ReconnectWebsocket(Exception):
    pass
