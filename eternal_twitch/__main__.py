from eventlet import monkey_patch
monkey_patch()
from .config import Config
from .store import Store
from .twitch_poller import TwitchPoller
from .stream_printer import StreamPrinter
from .stream_notifier import StreamNotifier
from .stream_websocket_server import StreamWebsocketServer
from signal import signal, SIGINT, pause
import logging
import logging.config


def main():
    '''Main module function.'''
    config = Config()

    # Configure Logging
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s [%(levelname)s] - %(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'eternal_twitch.log',
                'mode': 'w'
            },
            'stream_notifier_file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'stream_notifier.log',
                'mode': 'w'
            },
            'stream_printer_file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'stream_printer.log',
                'mode': 'w'
            },
            'stream_websocket_server_file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'stream_websocket_server.log',
                'mode': 'w'
            },
            'twitch_poller_file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'twitch_poller.log',
                'mode': 'w'
            }
        },
        'loggers': {
            'config': {
            },
            'stream_notifier': {
                'level': config.log_level,
                'handlers': ['stream_notifier_file']
            },
            'stream_printer': {
                'level': config.log_level,
                'handlers': ['stream_printer_file']
            },
            'stream_websocket_server': {
                'level': config.log_level,
                'handlers': ['stream_websocket_server_file']
            },
            'twitch_poller': {
                'level': config.log_level,
                'handlers': ['twitch_poller_file']
            }
        },
        'root': {
            'level': config.log_level,
            'handlers': ['console', 'file']
        }
    })

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
