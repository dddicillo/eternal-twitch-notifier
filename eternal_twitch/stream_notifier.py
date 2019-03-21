from rx.core import Observer
from rx.operators import filter, pluck
from pushbullet import PushBullet
from re import search, I
from logging import getLogger

logger = getLogger('stream-notifier')


class StreamNotifier(Observer):
    '''Sends notifications when a new stream matching key_words begins.'''

    def __init__(self, config, store):
        self.key_words = config.key_words
        self.pushbullet = PushBullet(config.pushbullet_token)
        self.updated_streams = store.stream_changes.pipe(
            filter(lambda change: change['type'] == 'add' or (
                change['type'] == 'change' and 'name' in change['changed_fields'])),
            pluck('stream')
        )

    def on_next(self, updated_stream):
        '''Responds to updates to the updated_streams observable.'''
        logger.info('change')
        for key_word in self.key_words:
            logger.info('checking for %s in %s', key_word, updated_stream.name)
            if search(key_word, updated_stream.name, flags=I):
                self.notify(updated_stream)
                break

    def notify(self, stream):
        '''Sends a notification.'''
        logger.info('Sending notification for stream \'%s\' by \'%s\'',
                    stream.name, stream.streamer)
        self.pushbullet.push_link('%s | %s' % (
            stream.streamer, stream.name), stream.url)

    def run(self):
        '''Subscribes the notifier to changes to the store.'''
        self.updated_streams.subscribe(self)
