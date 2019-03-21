from .config import Config
from .store import Store
from .twitch_poller import TwitchPoller
from .stream_printer import StreamPrinter
from .stream_notifier import StreamNotifier
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

    # Start Twitch Poller
    twitch_poller = TwitchPoller(config, store)
    twitch_poller.start()
    threads.append(twitch_poller)

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
    for thread in threads:
        thread.join()


main()
