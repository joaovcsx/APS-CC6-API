"""Class BaseRequest"""
import json
import re

import webapp2

class BaseHandler(webapp2.RequestHandler):
    """Base request object"""

    def options(self, *args, **kwargs):
        """Header Options"""
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = self.request.headers['Origin']
        self.response.headers['Access-Control-Allow-Headers'] = ('Origin, X-Requested-With, '
                                                                 'x-http-method-override, '
                                                                 'Content-Type, Accept, ')
        self.response.headers['Access-Control-Allow-Methods'] = ('DELETE, GET, HEAD, OPTIONS, '
                                                                 'PATCH, POST, PUT')
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Access-Control-Max-Age'] = '600'
        return

    def response_send(self, response_json_obj=None, header_exposed=True, status_code=200):
        """Send response for client"""
        if header_exposed:
            self.response.headers['Access-Control-Allow-Origin'] = "*"
            self.response.content_type = 'application/json'
        if response_json_obj is not None:
            self.response.write(json.dumps(response_json_obj))
        self.response.set_status(status_code)

    def response_error(self, error_exception, header_exposed=True):
        """
        Return error to client
        :param Exception error_exception: Try Except Exception error
        :param bool header_exposed: If true add header "Access-Control-Allow-Origin": "*"
        :return None:
        """
        status_code = self.get_error_code(error_exception)
        self.response_send(
            {'message': self.get_error_message(error_exception)},
            header_exposed=header_exposed,
            status_code=status_code)
    
    def logging_request(self):
        """Logging request"""
        print(self.request)
        print('\n ___________________________________________________________ //')

    def request_json(self, key=None):
        """Get request body as json"""
        try:
            if key:
                return json.loads(self.request.body)[key]
            else:
                return json.loads(self.request.body)
        except ValueError:
            raise Exception('Invalid json parameters', 400)

    @staticmethod
    def get_error_message(error):
        """
        Get error message
        :param Exception error: Error exception
        :return int code: Error message
        """
        try:
            if error.args and len(error.args):
                return error[0]
            else:
                return str(error)
        except:
            return str(error)


    @staticmethod
    def get_error_code(error):
        """
        Get error code
        :param Exception error: Error exception
        :return int code: Error status code
        """
        try:
            if len(error.args) > 1:
                error_code = error[1]
                if isinstance(error_code, int):
                    return error[1]
        except:
            return 500
    
    def logging_error(self, error):
        print('\nerror:')
        print(error)

    def logging_response(self, response):
        try:
            print('\nresponse:')
            print(response)
            print('\ncontente:')
            print(json.loads(response.content))
        except:
            pass

    def get_content(self, response):
        try:
            return json.loads(response.content)
        except Exception as error:
            return response
    
    def log_request_post(self):
        print(self.request.POST)
