from configparser import ConfigParser
from os import environ
from traceback import format_exc
from sys import exit
from logging import getLogger

logger = getLogger('config')

CONFIG_FILE = 'conf/eternal_twitch.cfg'


class Config(ConfigParser):
    '''Represents configuration details.'''

    def __init__(self, file=CONFIG_FILE):
        super(Config, self).__init__()
        super(Config, self).read(file)

    def log(self):
        logger.info('twitch_client_id=%s' % (self.twitch_client_id))
        logger.info('pushbullet_token=%s' % (self.pushbullet_token))
        logger.info('etcd_hosts=%s' % (str(self.etcd_hosts)))
        logger.info('printer_enabled=%s' % (str(self.printer_enabled)))
        logger.info('notifier_enabled=%s' % (str(self.notifier_enabled)))
        logger.info('polling_interval=%s' % (str(self.polling_interval)))
        logger.info('key_words=%s' % (str(self.key_words)))
        logger.info('deletion_grace_count=%s' %
                    (str(self.deletion_grace_count)))
        logger.info('log_stdout=%s' % (str(self.log_stdout)))
        logger.info('log_file=%s' % (self.log_file))
        logger.info('log_level=%s' % (self.log_level))

    @property
    def twitch_client_id(self):
        if 'TWITCH_CLIENT_ID' in environ:
            return environ['TWITCH_CLIENT_ID']
        return self.get('twitch', 'client_id')

    @twitch_client_id.setter
    def twitch_client_id(self, twitch_client_id):
        self['twitch']['client_id'] = twitch_client_id

    @property
    def pushbullet_token(self):
        if 'PUSHBULLET_TOKEN' in environ:
            return environ['PUSHBULLET_TOKEN']
        return self.get('pushbullet', 'token')

    @pushbullet_token.setter
    def pushbullet_token(self, pushbullet_token):
        self['pushbullet']['token'] = pushbullet_token

    @property
    def etcd_hosts(self):
        if 'ETCD_HOSTS' in environ:
            host_ports = environ['ETCD_HOSTS'].split(',')
        else:
            host_ports = self.get(
                'etcd', 'hosts', fallback='localhost:12379,localhost:22379,localhost:32379').split(',')

        return tuple(map(lambda x: (x.split(':')[0], int(x.split(':')[1])), host_ports))

    @etcd_hosts.setter
    def etcd_hosts(self, etcd_hosts):
        host_ports = map(lambda x: ':'.join(x), etcd_hosts)
        self['etcd']['hosts'] = ','.join(host_ports)

    @property
    def printer_enabled(self):
        if 'STREAM_PRINTER_ENABLED' in environ:
            return environ['STREAM_PRINTER_ENABLED'].lower() == 'true'
        return self.getboolean('general', 'stream_printer_enabled', fallback=False)

    @printer_enabled.setter
    def printer_enabled(self, printer_enabled):
        self['general']['stream_printer_enabled'] = bool(printer_enabled)

    @property
    def notifier_enabled(self):
        if 'STREAM_NOTIFIER_ENABLED' in environ:
            return environ['STREAM_NOTIFIER_ENABLED'].lower() == 'true'
        return self.getboolean('general', 'stream_notifier_enabled', fallback=False)

    @notifier_enabled.setter
    def notifier_enabled(self, notifier_enabled):
        self['general']['stream_notifier_enabled'] = bool(notifier_enabled)

    @property
    def polling_interval(self):
        if 'POLLING_INTERVAL' in environ:
            return int(environ['POLLING_INTERVAL'])
        return self.getint('general', 'polling_interval', fallback=2)

    @polling_interval.setter
    def polling_interval(self, polling_interval):
        self['general']['polling_interval'] = int(polling_interval)

    @property
    def key_words(self):
        if 'KEY_WORDS' in environ:
            return environ['KEY_WORDS'].split(',')
        return self.get('general', 'key_words',
                        fallback='campaign,drop,diamond,gold,silver,bronze').split(',')

    @key_words.setter
    def key_words(self, key_words):
        self['general']['key_words'] = ','.join(key_words)

    @property
    def deletion_grace_count(self):
        if 'DELETION_GRACE_COUNT' in environ:
            return environ['DELETION_GRACE_COUNT']
        return self.getint('general', 'deletion_grace_count', fallback=5)

    @deletion_grace_count.setter
    def deletion_grace_count(self, deletion_grace_count):
        self['general']['deletion_grace_count'] = deletion_grace_count

    @property
    def log_stdout(self):
        if 'LOG_STDOUT' in environ:
            return environ['LOG_STDOUT'].lower() == 'true'
        return self.getboolean('logging', 'stdout', fallback=False)

    @log_stdout.setter
    def log_stdout(self, log_stdout):
        self['logging']['stdout'] = bool(log_stdout)

    @property
    def log_file(self):
        if 'LOG_FILE' in environ:
            return environ['LOG_FILE']
        return self.get('logging', 'file', fallback='eternal_twitch.log')

    @log_file.setter
    def log_file(self, log_file):
        self['logging']['file'] = log_file

    @property
    def log_level(self):
        if 'LOG_LEVEL' in environ:
            return environ['LOG_LEVEL']
        return self.get('logging', 'level', fallback='INFO')

    @log_level.setter
    def log_level(self, log_level):
        self['logging']['level'] = log_level
