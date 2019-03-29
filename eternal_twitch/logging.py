import logging
import logging.config


def configure_logging(config):
    '''Configure logging.'''
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s [%(levelname)s] - %(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'eternal_twitch.log',
                'mode': 'w'
            },
            'stream_notifier_file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'stream_notifier.log',
                'mode': 'w'
            },
            'stream_printer_file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'stream_printer.log',
                'mode': 'w'
            },
            'stream_websocket_server_file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'stream_websocket_server.log',
                'mode': 'w'
            },
            'twitch_poller_file': {
                'class': 'logging.FileHandler',
                'level': config.log_level,
                'formatter': 'simple',
                'filename': 'twitch_poller.log',
                'mode': 'w'
            }
        },
        'loggers': {
            'config': {
            },
            'stream_notifier': {
                'level': config.log_level,
                'handlers': ['stream_notifier_file']
            },
            'stream_printer': {
                'level': config.log_level,
                'handlers': ['stream_printer_file']
            },
            'stream_websocket_server': {
                'level': config.log_level,
                'handlers': ['stream_websocket_server_file']
            },
            'twitch_poller': {
                'level': config.log_level,
                'handlers': ['twitch_poller_file']
            }
        },
        'root': {
            'level': config.log_level,
            'handlers': ['console', 'file']
        }
    })
