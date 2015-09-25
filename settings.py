DOMAIN = {'people': {}}

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'dimwit'

XML = False

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

two_d = {
    'type': 'list',
    'schema': {
        'type': 'list',
        'schema': {
            'type': 'float'
        }
    }
}

entry = {
    'schema': {
        'data': two_d,
        'pca': two_d,
        'tsne': two_d,
        'ica': two_d
    }
}

DOMAIN = {
    'entry': entry,
}