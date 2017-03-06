from datetime import timedelta
from celery.schedules import crontab
from kombu import Exchange, Queue
import os




class Config(object):
    # PLACEHOLDER
    PLACEHOLDER = os.environ['PLACEHOLDER']

    # Hosted graphite statsd prefix
    STATSD_PREFIX = os.getenv('STATSD_PREFIX')

    NOTIFICATION_QUEUE_PREFIX = os.getenv('NOTIFICATION_QUEUE_PREFIX')

    # Logging
    DEBUG = False
    LOGGING_STDOUT_JSON = os.getenv('LOGGING_STDOUT_JSON') == '1'

    ###########################
    # Default config values ###
    ###########################

    NOTIFY_APP_NAME = 'api'
    NOTIFY_ENVIRONMENT = 'development'
    AWS_REGION = 'eu-west-1'
    NOTIFY_LOG_PATH = '/var/log/notify/application.log'

    BROKER_URL = 'sqs://'
    BROKER_TRANSPORT_OPTIONS = {
        'region': AWS_REGION,
        'polling_interval': 1,
        'visibility_timeout': 30,
        'queue_name_prefix': NOTIFICATION_QUEUE_PREFIX
    }
    CELERY_ENABLE_UTC = True,
    CELERY_TIMEZONE = 'Europe/London'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_IMPORTS = ('app.celery.tasks', )
    CELERYBEAT_SCHEDULE = {
        'run-scheduled-jobs': {
            'task': 'test',
            'schedule': crontab(minute=1),
            'options': {'queue': 'process-ftp'}
        },
    }
    CELERY_QUEUES = [
        Queue('process-ftp', Exchange('default'), routing_key='process-ftp')
    ]

    STATSD_ENABLED = False
    STATSD_HOST = "statsd.hostedgraphite.com"
    STATSD_PORT = 8125



######################
# Config overrides ###
######################

class Development(Config):
    CSV_UPLOAD_BUCKET_NAME = 'development-notifications-csv-upload'
    NOTIFY_ENVIRONMENT = 'development'
    NOTIFICATION_QUEUE_PREFIX = 'development'
    DEBUG = True


class Test(Config):
    NOTIFY_ENVIRONMENT = 'test'
    CSV_UPLOAD_BUCKET_NAME = 'test-notifications-csv-upload'
    DEBUG = True
    STATSD_ENABLED = True
    STATSD_HOST = "localhost"
    STATSD_PORT = 1000


class Preview(Config):
    NOTIFY_ENVIRONMENT = 'preview'
    CSV_UPLOAD_BUCKET_NAME = 'preview-notifications-csv-upload'


class Staging(Config):
    NOTIFY_ENVIRONMENT = 'staging'
    CSV_UPLOAD_BUCKET_NAME = 'staging-notify-csv-upload'
    STATSD_ENABLED = True


class Live(Config):
    NOTIFY_ENVIRONMENT = 'live'
    CSV_UPLOAD_BUCKET_NAME = 'live-notifications-csv-upload'
    STATSD_ENABLED = True


configs = {
    'development': Development,
    'test': Test,
    'live': Live,
    'staging': Staging,
    'preview': Preview
}
