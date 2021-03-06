from rx import timer
from twitch import TwitchClient
from .model.stream import Stream
from logging import getLogger

logger = getLogger('twitch_poller')
STREAMS_KEY = '/streams'


class TwitchPoller():
    '''Regularly updates the store with information retrieved from Twitch.'''

    def __init__(self, config, store):
        self.client = TwitchClient(client_id=config.twitch_client_id)
        self.store = store
        self.polling_interval = config.polling_interval
        self.deletion_count = dict()
        self.deletion_grace_count = config.deletion_grace_count

    def get_streams(self):
        '''Fetch stream information from Twitch API.'''
        streams = [Stream.from_twitch_data(stream) for stream in self.client.streams.get_live_streams(
            game='eternal')]
        logger.debug('Retrieved %d streams from Twitch' % (len(streams)))
        sorted(streams, key=lambda stream: stream.viewers, reverse=True)
        return streams

    def merge_streams(self, new_streams):
        '''Adds new streams to store. Updates existing streams with new data. Removes completed streams.'''
        ended_streams = self.get_ended_streams(new_streams)
        if len(ended_streams) > 0:
            logger.debug('Removing %d ended streams...' % (len(ended_streams)))
        for stream in ended_streams:
            if self.should_delete(stream):
                self.store.delete_stream(stream)
                del self.deletion_count[stream.id]

        if len(new_streams) > 0:
            logger.debug('Adding or updating %d streams...' %
                         (len(new_streams)))
        for stream in new_streams:
            self.store.write_or_update_stream(stream)
            self.deletion_count[stream.id] = 0

    def get_ended_streams(self, new_streams):
        '''Returns a list of streams that are in the store but not in the new_streams list.'''
        old_streams = self.store.read_streams()

        new_stream_ids = set(map(lambda stream: stream.id, new_streams))
        old_stream_ids = set(map(lambda stream: stream.id, old_streams))
        ended_stream_ids = old_stream_ids.difference(new_stream_ids)

        return list(filter(lambda stream: stream.id in ended_stream_ids, old_streams))

    def should_delete(self, stream):
        '''Returns true when a stream has met or exceeded the deletion_grace_count.'''
        self.deletion_count[stream.id] = self.deletion_count.get(
            stream.id, 0) + 1
        return (self.deletion_count[stream.id] >= self.deletion_grace_count)

    def run(self):
        '''Polls the Twitch API periodically.'''
        logger.info('Starting Twitch poller...')
        logger.info('polling_interval: %d' % (self.polling_interval))

        def poll(it):
            streams = self.get_streams()
            self.merge_streams(streams)

        self.disposer = timer(0, self.polling_interval).subscribe(on_next=poll)

    def stop(self):
        '''Stops polling the Twitch API periodically.'''
        if hasattr(self, 'disposer'):
            logger.info('Stopping Twitch poller...')
            self.disposer.dispose()
