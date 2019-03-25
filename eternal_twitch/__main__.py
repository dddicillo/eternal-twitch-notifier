from .config import Config
from .store import Store
from .twitch_poller import TwitchPoller
from .stream_printer import StreamPrinter
from .stream_notifier import StreamNotifier
from signal import signal, SIGINT, pause
from time import sleep
import logging


def main():
    '''Main module function.'''
    threads = []
    config = Config()

    # Configure Logging
    logging.basicConfig(
        filename=config.log_file,
        filemode='w',
        format='%(asctime)s [%(levelname)s] - %(name)s: %(message)s',
        level=config.log_level)

    # Initialize Store
    store = Store(config)

    logging.info('Initializing...')
    print('Initializing...')
    twitch_poller = TwitchPoller(config, store)
    stream_printer = StreamPrinter(config, store)
    stream_notifier = StreamNotifier(config, store)

    # Signal Handler
    def handle_signal(sig, frame):
        stream_notifier.stop()
        stream_printer.stop()
        twitch_poller.stop()
        exit(0)
    signal(SIGINT, handle_signal)

    # Run Twitch Poller
    twitch_poller.run()

    # Run Stream Printer
    stream_printer.run()

    # Run Stream Notifier
    stream_notifier.run()

    store.stream_changes.subscribe(
        lambda next: logging.info(next)
    )

    # Block Main Thread
    pause()


main()
