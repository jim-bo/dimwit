## imports ##
import json
import logging
import requests
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
import unittest
from sklearn import datasets
import numpy as np

## class ##
class SmplRest(object):

    def __init__(self, path, port):
        """ initialises connection to API, return error if doesnt work
        :param hostname: host name of the API
        :param port: port of the API
        """

        # sanity check path and port.
        try:
            int(port)
        except ValueError:
            logging.error("bad port")
            return

        if path.count("http") > 0 or path.count(":") > 0:
            logging.error("bad path")
            return

        # save them.
        self.path = path
        self.port = port
        self.auth = False

        logging.getLogger("requests").setLevel(logging.WARNING)

        # make GET request on root. DISABLED BECAUSE DON"T KNOW HOW TO SENT EMPTY CREDENTIALS
        #status, resp = self.get_resource("/", auth=("", ""))

        # sanity check status.
        #if status != 200:
        #    logging.error("server not responding")
        #    logging.error(resp)
        #    return

    def register_token(self, token):
        """ set default authorization
        :param token: token based authentication
        """
        self.auth = (token,'')

    #######################
    ## Requests
    #######################

    def get_item(self, resource, obj_id, params={}, auth=False):
        """ get on item level
        :param resource: string of resource
        :param where: clause for search
        :param params: extra parameters
        :param auth: authorization
        :return: :(status, resp): code and json response
        """

        # check authorization.
        auth = self._check_authorization(auth)
        if not auth:
            return False, False

        # create header.
        headers = self._create_headers()

        # build the url.
        url = self._build_url(resource, item=obj_id)

        # perform the request
        resp = requests.get(url, headers=headers, params=params, auth=auth)

        # log the response.
        self._log_response(resp)

        # create the return.
        status, resp = self._create_return(resp)

        # return code and json data.
        return status, resp


    def patch_item(self, resource, obj_id, data, etag=None, params={}, auth=False):
        """
        :param resource:
        :param obj_id:
        :param data:
        :param etag:
        :param params:
        :param auth:
        :return:
        """

        # check authorization.
        auth = self._check_authorization(auth)
        if not auth:
            return False, False

        headers = self._create_headers()

        # get required etag if not passed in.
        if etag is None:
            if '_etag' in data:
                etag = data['_etag']

            if etag is None:
                status, resp = self.get_item(resource, obj_id, {}, auth)
                self.assert_code(status, resp, 200)
                assert '_etag' in resp, 'The required _etag was not found.'
                etag = resp['_etag']

        headers['If-Match'] = etag

        # strip ancillary.
        to_remove = []
        for key in data:
            if key[0] == '_':
                to_remove.append(key)
        for key in to_remove:
            del data[key]

        # sanitize where statements.
        data = self._stringify_json(data)

        # build the url.
        url = self._build_url(resource, item=obj_id)

        # perform the request
        resp = requests.patch(url, headers=headers, data=data, params=params, auth=auth)

        # log the response.
        self._log_response(resp)

        # create the return.
        status, resp = self._create_return(resp)

        # return code and json data.
        return status, resp


    def get_resource(self, resource, where={}, params={}, auth=False):
        """ get on resource level
        :param resource: string of resource
        :param where: clause for search
        :param params: extra parameters
        :param auth: authorization
        :return: :(status, resp): code and json response
        """

        # check authorization.
        auth = self._check_authorization(auth)
        if not auth:
            return False, False

        # create header.
        headers = self._create_headers()

        # sanitize where statements.
        where = self._stringify_json(where)
        params['where'] = where

        # build the url.
        url = self._build_url(resource)

        # perform the request
        resp = requests.get(url, headers=headers, params=params, auth=auth)

        # log the response.
        self._log_response(resp)

        # create the return.
        status, resp = self._create_return(resp)


        # return code and json data.
        return status, resp


    def post_resource(self, resource, data, params={}, auth=False):
        """ get on resource level
        :param resource: string of resource
        :param payload: json to post
        :param params: extra parameters
        :param auth: authorization
        :return: :(status, resp): code and json response
        """

        # check authorization.
        auth = self._check_authorization(auth)
        if not auth:
            return False, False

        # create header.
        headers = self._create_headers()

        # sanitize where statements.
        data = self._stringify_json(data)

        # build the url.
        url = self._build_url(resource)

        # perform the request
        resp = requests.post(url, data=data, headers=headers, params=params, auth=auth)

        # log the response.
        self._log_response(resp)

        # create the return.
        status, resp = self._create_return(resp)

        # return code and json data.
        return status, resp


    def put_file_s3(self, action, fields, file_path):
        """ PUT file to s3 given pre-signed URL
        :param action: URL
        :param fields: list({"name":str,"value":str})
        :param file_path: file path on local system
        :return: :(status, resp): code and json response
        """

        # perform the request
        with open(file_path, 'rb') as fin:

            # create ordered payload.
            payload = list()
            for entry in fields:
                payload.append((entry['name'],  entry['value']))
            payload.append(("file", fin))

            # post it, multipart is forced when using files=xyz
            resp = requests.post(action, files=payload)

        # log the response.
        self._log_response(resp)

        # create the return.
        status = resp.status_code

        # return code and json data.
        return status, resp

    def put_file_gcs(self, action, file_path):
        """ PUT file to Google Cloud Storage given pre-signed URL
        :param action: URL
        :param file_path: file path on local system
        :return: :(status, resp): code and json response
        """
        with open(file_path, 'rb') as fin:
            # post it
            resp = requests.put(action, data=fin)

        # log the response
        self._log_response(resp)

        # create the return
        status = resp.status_code

        # return code and json data
        return status, resp

    ######################
    ## utility
    ######################

    def _check_authorization(self, auth):
        """ ensure we have provided authorization
        :param auth: authorization token (token,) or (user,pw)
        :return: :rtype:
        """
        if auth == False:
            if self.auth == False:
                logging.error("no authorization provided")
                return False
            auth = self.auth
        return auth


    def _create_headers(self, params={}):
        """ create headers payload
        :param extra: extra params for header
        :return: :dict: authentication encoded
        """

        # parse authorization scheme

        # build header.
        #params['Authorization'] = 'Basic ' + base64.b64encode(auth)
        params['content-type'] = 'application/json'
        return params


    def _stringify_json(self, payload):
        """ ensures payload is in json
        :param payload: dictionary
        :return: :dict: json formatted dictionary
        """
        if type( payload ) is dict:
            return json.dumps( payload )
        else:
            return payload

    def _build_url(self, resource, item=None):
        """ builds URL for item or resource.
        :param resource: string
        :param item: string
        :return: :string: url
        """

        # the basic url.
        entry='http://%s:%i' % (self.path, self.port)

        # add item or resource.
        if item:
            return "%s/%s/%s" % ( entry, resource.strip('/'), item.strip('/') )
        else:
            return "%s/%s" % ( entry, resource.strip('/') )

    def _log_response(self, response):
        """ prints response info to logger
        :param response: json/text response
        """

        return

        logging.debug(response.headers)
        try:
            logging.debug(response.json())
        except:
            logging.debug(response.text)

    def async_wait(self, resource, obj_id, time_step, time_out, auth=False):
        """ wait for asynchronous job to finish using ref_count
        :param resource: string of resource
        :param obj_id: object id with running job
        :param time_step: how many seconds in each step
        :param time_out: how many steps
        :param auth: authorization
        """

        # check status.
        check_status = True
        count = 0
        while (check_status):

            # wait a little bit
            time.sleep(time_step)

            # query resource.
            status, resp = self.get_item(resource, obj_id, auth=auth)
            self.assert_code(status, resp, 200)

            # check if the job has finished.
            if resp['job_done'] is True:
                check_status = False

            # die after a certain amount of time.
            if count == time_out:
                logging.warning('%s resource did not finish within expected time.' % (resource))
                return None

            count += 1

        # return the result.
        return resp

    @staticmethod
    def _pretty(input):
        return json.dumps(input, sort_keys=True, indent=4, separators=(',', ': '))

    @staticmethod
    def _create_return(response):
        try:
            txt = response.json()
        except ValueError as e:
            print e
            print response.text
            assert False
        return response.status_code, txt

    ######################
    ## assertions
    ######################
    def assert_code(self, status, resp, code):
        assert status == code, self._pretty(resp)

    def assert_not_empty(self, resp):
        assert '_items' in resp and len(resp['_items']) > 0

    def assert_good_insert(self, status, resp):
        assert status != 422, self._pretty(resp)
        assert resp['_status'] != 'ERR', self._pretty(resp)

    def assert_bad_insert(self, status, resp):
        assert status >= 400, self._pretty(resp)
        assert resp['_status'] == 'ERR', self._pretty(resp)

    def assert_err_code(self, resp, code):
        assert resp['_status'] == 'ERR', self._pretty(resp)
        msg = resp['_error']['message']
        assert msg.split(': ', 1)[0] == code.name, 'Expected {0}, got {1}'.format(code.name, msg)


class RestMocker(object):

    # no tests here.
    __test__ = False

    # connection parameters.
    client = None

    # initialized users.
    admin_auth = ('', '')

    ####################
    # class methods

    def prepare_rest(self, host=False, port=False):

        # make rest connection.
        h = 'localhost'
        if host is not False:
            h = host

        p = 5000
        if port is not False:
            p = port

        self.client = SmplRest(h, p)

class DBMocker(RestMocker):

    # no tests here.
    __test__ = False

    # connection parameters.
    db = None
    mongo_client = None

    ####################
    # class methods
    def prepare_db(self, no_drop=False):
        """
        make REST connection and mongo connection.
        """
        # creatsmplapi.apitasks.diffexpresse mongo connection.
        self.mongo_client = MongoClient('localhost:27017')

        # set the database.
        self.db = self.mongo_client['dimwit']
        # clean the database.
        if not no_drop:
            self.db_drop_collections()

    def clean_db(self):

        # clean the database.
        self.db_drop_collections()

        # close it.
        self.mongo_client.close()

    ####################
    # utility methods

    def db_drop_collections(self):
        """ drops all colelctions
        """

        # get all collections.
        collections = self.db.collection_names(include_system_collections=False)

        # drop them.
        for collection in collections:
            self.db.drop_collection(collection)

## test functions ##
class EntryTest(DBMocker, unittest.TestCase):

    # this is the droid you are looking for.
    __test__ = True

    ####################
    # basic methods
    ####################

    def setUp(self):

        # prepare the DB / REST
        self.prepare_db()
        self.prepare_rest()

    def tearDown(self):
        #self.clean_db()
        pass

    ####################
    # reusable
    ####################

    ####################
    # tests
    ####################

    def basic_test(self):

        # try some query.
        status_code, resp = self.client.get_resource("entry", auth=self.admin_auth)

        # ensure we have a 200.
        self.client.assert_code(status_code, resp, 200)

    def entry_small_test(self):

        # create entry.
        entry = {
            'data': [
                [0.0, 1.0, 2.0],
                [9.4, 1.8, 0.0],
                [1.0, 1.0, 1.0]
            ]
        }

        # try the POST
        status_code, resp = self.client.post_resource("entry", entry, auth=self.admin_auth)
        self.client.assert_good_insert(status_code, resp)
        event_id = resp['_id']

        # verify it is in database.
        test = self.db['entry'].find_one({'_id': ObjectId(event_id)})
        assert test is not None, 'db returned nothing'
        assert entry['data'] == test['data']

    def entry_iris_test(self):

        # simulate data.
        iris = datasets.load_iris()
        X = iris.data

        # create entry.
        entry = {
            'data': X.tolist()
        }

        # try the POST
        status_code, resp = self.client.post_resource("entry", entry, auth=self.admin_auth)
        self.client.assert_good_insert(status_code, resp)
        event_id = resp['_id']

        time.sleep(5)

        # verify it is in database.
        test = self.db['entry'].find_one({'_id': ObjectId(event_id)})
        assert test is not None, 'db returned nothing'
        assert entry['data'] == test['data']

        # verify that reductions were run.
        assert np.array(test['pca']).shape == (X.shape[0], 3)