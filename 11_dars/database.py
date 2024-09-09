ORM_DATABASE = {
    'default': {
        'connection': 'sqlite:///database.db',
    },
    'apps': {
        'models': ['models', 'aerich.models'],
        'default_connection': 'default',
    }
}

