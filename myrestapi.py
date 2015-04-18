import json
import falcon
from wsgiref import simple_server


class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSONTranslator(object):

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])


class ContainerManager:

    def list_containers():
        print('Listing containers')

    def create_container(data):
        print ('Creating container using the following data: %s' % data)

    def delete_container(name):
        print('Killing container %s.' % name)


class ContainerResource(object):

    def __init__(self):
        self.manager = ContainerManager

    def on_get(self, req, resp):
        self.manager.list_containers()
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        try:
            data = req.context['doc']
        except KeyError:
            raise falcon.HTTPBadRequest('No data received')

        self.manager.create_container(data)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, name):
        self.manager.delete_container(name)
        resp.status = falcon.HTTP_200


api = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])

containers = ContainerResource()
api.add_route('/containers/', containers)
api.add_route('/containers/{name}', containers)

# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8080, api)
    httpd.serve_forever()
