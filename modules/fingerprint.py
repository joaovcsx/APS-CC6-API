#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy
import cv2
import urllib2
import numpy as np
import jwt

from urlparse import urlparse
from image_processing import ImageProcessing
from base_handler import BaseHandler
from firebase_module import FirebaseFingerprints

# quadrantes = [
#     {
#         'height_min': 0, 'height_max': img_height / 2, 
#         'width_min': 0, 'width_max': img_width / 2
#     },
#     {
#         'height_min': 0, 'height_max': img_height / 2, 
#         'width_min': (img_width / 2) + 1, 'width_max': img_width
#     },
#     {
#         'height_min': (img_height / 2) + 1, 'height_max': img_height, 
#         'width_min': 0, 'width_max': img_width / 2
#     },
#     {
#         'height_min': (img_height / 2) + 1, 'height_max': img_height, 
#         'width_min': (img_width / 2) + 1, 'width_max': img_width
#     }
# ]

class FingerprintHandler(BaseHandler):

    def get(self):
        try:
            print('\nGET')
            fingerprints = FirebaseFingerprints.get()
            self.response_send(fingerprints)

        except Exception as error:
            self.response_error(error)


    def post(self):
        try:
            print('\nPOST')
            request_dict = self.request.POST
            image_processing = ImageProcessing()
            image_processing.format_image(request_dict)
            quadrants, count = image_processing.get_pixels()

            quadrants_encode = jwt.encode(quadrants, 'secretX', algorithm='HS256')
            # jwt.decode(encoded_jwt, 'secretX', algorithms=['HS256'])
            params_create = {
                u"count": count,
                u"quadrants": quadrants_encode,
                u"name": request_dict.get('name') or u"",
                u"level": int(request_dict.get('level') or 0),
                u"photo_url": request_dict.get('photo_url') or u"",
            }
            FirebaseFingerprints.create(params_create)
            self.response_send({'status': 'created'})

        except Exception as error:
            self.response_send({'status': 'error', 'error': str(error)})
