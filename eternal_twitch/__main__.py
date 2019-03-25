from .config import Config
from .store import Store
from .twitch_poller import TwitchPoller
from .stream_printer import StreamPrinter
from .stream_notifier import StreamNotifier
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

    # Configure Twitch Poller
    twitch_poller = TwitchPoller(config, store)
    twitch_poller.run()

    # Configure Stream Printer
    stream_printer = StreamPrinter(config, store)
    stream_printer.run()

    # Configure Stream Notifier
    stream_notifier = StreamNotifier(config, store)
    stream_notifier.run()

    store.stream_changes.subscribe(
        lambda next: logging.info(next)
    )

    # Block Main Thread
    while(True):
        sleep(1)


main()
