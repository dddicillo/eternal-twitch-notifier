from rx.core import Observer
from os import system
from texttable import Texttable
from re import sub, I
from colorama import Fore
from logging import getLogger

logger = getLogger('stream-printer')


class StreamPrinter(Observer):
    '''Prints stream information to stdout.'''

    def __init__(self, config, store):
        self.key_words = config.key_words
        self.store = store

    def on_next(self, stream_change):
        '''Responds to updates to the stream_changes observable.'''
        system('clear')
        print(self.get_formated_stream_details())

    def get_formated_stream_details(self):
        '''Returns a formatted table of stream details.'''
        streams = self.store.read_streams()
        streams = sorted(
            streams, key=lambda stream: stream.viewers, reverse=True)

        out = StreamPrinter.create_table(streams)
        return self.colorize(out)

    def colorize(self, out):
        '''Highlights key_words in the output.'''
        for key_word in self.key_words:
            out = sub(r"(%s\w*)" % (key_word), Fore.GREEN +
                      r'\1' + Fore.RESET, out, flags=I)
        return out

    def run(self):
        '''Subscribes the printer to changes to the store.'''
        logger.info('Starting stream printer...')
        self.disposer = self.store.stream_changes.subscribe(self)

    def stop(self):
        '''Stops printing changes to the store.'''
        logger.info('Stopping stream printer...')
        if self.disposer:
            self.disposer.dispose()

    @staticmethod
    def create_table(streams):
        '''Creates a terminal-friendly table from streams.'''
        table = Texttable()
        table.set_deco(Texttable.HEADER | Texttable.VLINES)
        table.set_header_align(['l', 'l', 'l'])
        table.set_max_width(0)
        data = [['Streamer', 'Title', 'Viewers']]
        data.extend(list(map(lambda stream: [
            stream.streamer,
            stream.name,
            stream.viewers
        ], streams)))
        table.add_rows(data)
        return table.draw()
