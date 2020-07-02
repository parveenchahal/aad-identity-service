import sys
from urllib.parse import urljoin, urlparse
from flask import Flask
from flask_restful import Api, Resource, request
import msal

class TokenController(Resource):

    required_args = ['client_id', 'resource']

    def __validate_request_args(self, args):
        for arg in self.required_args:
            if(arg not in args):
                raise ValueError("{0} is required argument".format(arg))
        if('secret' not in args and ('cert' not in args or 'key' not in args)):
            raise ValueError("Either secret or cert and key is required")

    def get(self, tenant="common"):
        args = request.args
        try:
            self.__validate_request_args(args)
        except ValueError as e:
            return str(e)

        aad_instance = "https://login.windows.net"
        if('aad_instance' in args):
            aad_instance = args['aad_instance']
        
        client_id = args['client_id']
        resource = args['resource']
        client_credential = None
        if('secret' in args):
            client_credential = args['secret']
        else:
            client_credential = {
                "private_key": args['key'],
                "public_certificate": args['cert']
            }
        claims = {
            "iss": client_id
        }

        path = urlparse(resource).path
        if(path.strip() in ['/', ""]):
            resource = urljoin(resource, '.default')

        app = msal.ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_credential,
            authority=urljoin(aad_instance, tenant),
            client_claims=claims)
        res = app.acquire_token_for_client([resource])
        return res

app = Flask(__name__)
api = Api(app)

api.add_resource(TokenController, '/', '/<tenant>')

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=2424)