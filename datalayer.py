## imports ##
from contextlib import contextmanager
from pymongo import MongoClient

## mongo ##
# make connection to mongo here for proper connection pooling.
client = MongoClient('localhost')

# grab database.
db = client['dimwit']

@contextmanager
def mongoctx():
    """
    create a mongo db context which can be used to access db
    :return: :rtype: db pointer
    """

    # yield the db
    yield db