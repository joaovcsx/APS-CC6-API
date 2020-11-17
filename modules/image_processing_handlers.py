#!/usr/bin/python
# -*- coding: utf-8 -*-

from base_handler import BaseHandler
from image_processing import ImageProcessing
from firebase_module import FirebaseFingerprints

class ImageProcessingHandler(BaseHandler):

    def post(self):
        try:
            print('\nPOST ImageProcessingHandler')
            request_dict = self.request.POST
            image_processing = ImageProcessing()
            image_processing.format_image(request_dict)

            # quadrants, count = image_processing.get_pixels()
            fingerprints = FirebaseFingerprints.get()
            result = image_processing.check_if_fingerprint_exists(fingerprints)

            if result:
                result['valid'] = True
                self.response_send(result)
            else:
                self.response_send({'valid': False})

        except Exception as error:
            print error
            self.response_error(error)
