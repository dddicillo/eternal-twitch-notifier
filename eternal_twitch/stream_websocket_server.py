from threading import Thread
from rx.core import Observer
from rx.operators import debounce
from flask import Flask, render_template
from flask_socketio import SocketIO
from logging import getLogger

logger = getLogger('stream_websocket_server')


class StreamWebsocketServer(Thread, Observer):
    '''Sends stream changes to web UI.'''

    def __init__(self, config, store):
        Thread.__init__(self)
        self.app = Flask(__name__)
        self.configure_flask()
        self.socketio = SocketIO(
            self.app, logger=logger, engineio_logger=False)
        self.configure_socketio()
        self.store = store

    def on_next(self, stream_change):
        '''Responds to updates to the stream_changes observable.'''
        logger.debug('Broadcasting stream change to clients...')
        logger.debug(str(stream_change))
        streams = list(map(lambda stream: stream.data,
                           self.store.read_streams()))
        streams = sorted(
            streams, key=lambda stream: stream['viewers'], reverse=True)
        self.socketio.emit('streams', streams, broadcast=True)

    def configure_flask(self):
        self.app.config['SECRET_KEY'] = 'secret!'
        def handler():
            return render_template('eternal-twitch.html')
        self.app.add_url_rule('/', 'eternal_twitch', handler)

    def configure_socketio(self):
        def handle_connection():
            self.on_next({ 'type': 'connection' })
        self.socketio.on_event('connected', handle_connection)

    def run(self):
        '''Subscribes websocket server to changes to the store.'''
        self.disposer = self.store.stream_changes.pipe(
            debounce(1)
        ).subscribe(self)
        self.socketio.run(self.app, host='0.0.0.0',
                          debug=False, use_reloader=False)

    def stop_socketio(self):
        def handler():
            self.socketio.stop()
        self.socketio.on('stop', handler)

    def stop(self):
        '''Stops sending store updates to websocket server.'''
        logger.info('Stopping stream websocket server...')
        if hasattr(self, 'disposer'):
            self.disposer.dispose()
        self.stop_socketio()
