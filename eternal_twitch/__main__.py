from eventlet import monkey_patch
monkey_patch()
import logging
from signal import signal, SIGINT, pause
from .stream_websocket_server import StreamWebsocketServer
from .stream_notifier import StreamNotifier
from .stream_printer import StreamPrinter
from .twitch_poller import TwitchPoller
from .store import Store
from .logging import configure_logging
from .config import Config


def main():
    '''Main module function.'''
    config = Config()
    configure_logging(config)

    logging.info('Initializing...')
    config.log()

    # Initialize Store
    store = Store(config)

    twitch_poller = TwitchPoller(config, store)
    stream_printer = StreamPrinter(config, store)
    stream_notifier = StreamNotifier(config, store)
    stream_websocket_server = StreamWebsocketServer(config, store)

    # Signal Handler
    def handle_signal(sig, frame):
        stream_notifier.stop()
        stream_printer.stop()
        twitch_poller.stop()
        stream_websocket_server.stop()
        exit(0)
    signal(SIGINT, handle_signal)

    # Run Twitch Poller
    twitch_poller.run()

    # Run Stream Printer
    if config.printer_enabled:
        stream_printer.run()

    # Run Stream Notifier
    if config.notifier_enabled:
        stream_notifier.run()

    # Run Stream Websocket Server
    stream_websocket_server.start()

    # Block Main Thread
    stream_websocket_server.join()
    logging.info('Stopping...')


main()
