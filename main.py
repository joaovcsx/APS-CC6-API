import webapp2
import sys

sys.path.append('modules')
from paste import httpserver
from base_handler import BaseHandler
from firebase_module import FirebaseFingerprints
from fingerprint import FingerprintHandler
from image_processing_handlers import ImageProcessingHandler

class Index(BaseHandler):
    """Index"""

    def get(self):
        """Get App Index"""
        FirebaseFingerprints.get()
        self.response_send({"API": "APS - Processamento de Imagem"})

    def post(self):
        self.log_request_post()


app = webapp2.WSGIApplication([
    webapp2.Route('/v1', handler=Index, name='home'),
    webapp2.Route(
        '/v1/fingerprint/exists',
        handler=ImageProcessingHandler,
        name='home'),
    webapp2.Route(
        '/v1/fingerprints',
        handler=FingerprintHandler,
        name='fingerprint')
], debug=True)

def main():
    httpserver.serve(app, host='0.0.0.0', port='8050')
    # httpserver.serve(app, host='127.0.0.1', port='8050')

if __name__ == '__main__':
    main()
