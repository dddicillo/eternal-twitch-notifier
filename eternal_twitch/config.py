from configparser import ConfigParser
from traceback import format_exc
from sys import exit

CONFIG_FILE = 'conf/eternal_twitch.cfg'


class Config(ConfigParser):
    '''Represents configuration details.'''

    def __init__(self, file=CONFIG_FILE):
        super(Config, self).__init__()
        super(Config, self).read(file)

    @property
    def twitch_client_id(self):
        return self.get('twitch', 'client_id')

    @twitch_client_id.setter
    def twitch_client_id(self, twitch_client_id):
        self['twitch']['client_id'] = twitch_client_id

    @property
    def pushbullet_token(self):
        return self.get('pushbullet', 'token')

    @pushbullet_token.setter
    def pushbullet_token(self, pushbullet_token):
        self['pushbullet']['token'] = pushbullet_token

    @property
    def etcd_hosts(self):
        host_ports = self.get(
            'etcd', 'hosts', fallback='localhost:12379,localhost:22379,localhost:32379').split(',')

        return tuple(map(lambda x: (x.split(':')[0], int(x.split(':')[1])), host_ports))

    @etcd_hosts.setter
    def etcd_hosts(self, etcd_hosts):
        host_ports = map(lambda x: ':'.join(x), etcd_hosts)
        self['etcd']['hosts'] = ','.join(host_ports)

    @property
    def polling_interval(self):
        return self.getint('general', 'polling_interval', fallback=2)

    @polling_interval.setter
    def polling_interval(self, polling_interval):
        self['general']['polling_interval'] = int(polling_interval)

    @property
    def key_words(self):
        return self.get('general', 'key_words',
                        fallback='campaign,drop,diamond,gold,silver,bronze').split(',')

    @key_words.setter
    def key_words(self, key_words):
        self['general']['key_words'] = ','.join(key_words)

    @property
    def deletion_grace_count(self):
        return self.getint('general', 'deletion_grace_count', fallback=5)

    @deletion_grace_count.setter
    def deletion_grace_count(self, deletion_grace_count):
        self['general']['deletion_grace_count'] = deletion_grace_count

    @property
    def log_file(self):
        return self.get('logging', 'file', fallback='eternal_twitch.log')

    @log_file.setter
    def log_file(self, log_file):
        self['logging']['file'] = log_file

    @property
    def log_level(self):
        return self.get('logging', 'level', fallback='INFO')

    @log_level.setter
    def log_level(self, log_level):
        self['logging']['level'] = log_level
