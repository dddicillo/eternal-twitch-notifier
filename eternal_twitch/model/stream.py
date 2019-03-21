class Stream:
    '''Represents a Twitch stream.'''

    def __init__(self, data):
        self.id = data['id']
        self.streamer = data['streamer']
        self.name = data['name']
        self.viewers = data['viewers']
        self.url = data['url']

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def data(self):
        return self.__dict__

    def changed_fields(self, other):
        '''Returns a list of attributes that differ between self and other.'''
        return list(filter(lambda x: self.__dict__[x] != other.__dict__[x], self.__dict__.keys()))

    @staticmethod
    def from_twitch_data(data):
        '''Creates a stream object from dictionary returned by Twitch API'''
        return Stream(dict(
            id=data['id'],
            streamer=data['channel']['name'],
            name=data['channel']['status'],
            viewers=data['viewers'],
            url=data['channel']['url']
        ))
