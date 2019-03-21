from etcd import Client, EtcdKeyNotFound, EtcdAlreadyExist
from rx.subjects import ReplaySubject
from os import path
from json import dumps, loads
from .model.stream import Stream
from logging import getLogger

logger = getLogger('store')
STREAMS_KEY = '/streams'


class Store:
    '''Handles persistence of streams information in backend.'''

    def __init__(self, config):
        self.etcd = Client(host=config.etcd_hosts, allow_reconnect=True)
        self.stream_changes = ReplaySubject()
        self.initialize_store()

    def initialize_store(self):
        '''Clears leftover store data at the beginning of execution.'''
        logger.info('Initializing store...')
        try:
            self.etcd.delete(STREAMS_KEY, recursive=True)
        except EtcdKeyNotFound:
            return

    def write_or_update_stream(self, stream):
        '''Adds a new stream to the store or updates the existing stream.'''
        key = path.join(STREAMS_KEY, str(stream.id))
        value = dumps(stream.data, default=str)
        try:
            self.etcd.write(key, value, prevExist=False)
            logger.info('Key \'%s\' did not exist. Added new entry.' % (key))
            self.stream_changes.on_next(dict(
                type='add',
                target=stream.id,
                changed_fields=stream.data.keys(),
                stream=stream
            ))
        except EtcdAlreadyExist:
            prevStream = self.read_stream(stream.id)
            if stream != prevStream:
                self.etcd.write(key, value, prevExist=True)
                logger.info('Key \'%s\' updated.' % (key))
                self.stream_changes.on_next(dict(
                    type='change',
                    target=stream.id,
                    changed_fields=prevStream.changed_fields(stream),
                    stream=stream
                ))

    def read_stream(self, stream_id):
        '''Reads a stream by ID from the store.'''
        data = loads(self.etcd.read(path.join(STREAMS_KEY, str(stream_id))).value)
        return Stream(data)

    def read_streams(self):
        '''Reads a list of all streams from the store.'''
        try:
            return [Stream(loads(stream.value)) for stream in self.etcd.read(STREAMS_KEY).children]
        except EtcdKeyNotFound:
            return []

    def delete_stream(self, stream):
        '''Deletes a stream from the store.'''
        try:
            self.etcd.delete(path.join(STREAMS_KEY, str(stream.id)))
            logger.info('Key \'%s\' deleted.')
            self.stream_changes.on_next(dict(
                type='delete',
                target=stream.id,
                changed_fields=stream.data.keys(),
                stream=stream
            ))
        except EtcdKeyNotFound:
            return
