#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy
import cv2
import urllib2
import jwt
import numpy as np

from urlparse import urlparse

QUADRANTS_NAME = ['quadrant_1', 'quadrant_2', 'quadrant_3', 'quadrant_4']

class ImageProcessing():

    def __init__(self):
        """ Init class """
        self._image = None

    @property
    def image(self):
        """Lease status"""
        return self._image

    @image.setter
    def image(self, image):
        self._image = image

    def format_image(self, post_params):
        """
        Format image
        :params dict post_params: {
            uploadFile: File
        }
        """
        try:
            image = post_params.get('uploadFile').value
            validate_url = urlparse(image)
            if validate_url.scheme and validate_url.netloc:
                file_image = urllib2.urlopen(image)
                image = base64.encodestring(file_image.read())

            nparr = np.fromstring(image, np.uint8)
            img_np = cv2.imdecode(nparr, flags=1)

            img_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
            img_gray = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            # cv2.imwrite('teste3.png', img_gray)
            self.image = img_gray
        except Exception as error:
            raise Exception(error, 400)

    def get_pixels(self):
        """
        Get black Pixels from image
        :return dict quadrants: Dict with list of pixels
        """
        try:
            img_height, img_width = self.image.shape
            image_formatted = self.image
            quadrants_params = self._get_quadrants(img_height, img_width)
            quadrants = {}
            count_black_pixels = 0

            for idx, quadrant in enumerate(quadrants_params):
                black_pixels = []
                for height in range(quadrant['height_min'], quadrant['height_max']):
                    for width in range(quadrant['width_min'], quadrant['width_max']):
                        if image_formatted[height].item(width) == 0:
                            black_pixels.append({'x': width, 'y': height})

                name = 'quadrant_{}'.format(idx + 1)
                count_black_pixels += len(black_pixels)
                quadrants['{}'.format(name)] = black_pixels

            return quadrants, count_black_pixels
        except Exception as error:
            print error
            raise Exception(error, 400)

    def check_if_fingerprint_exists(self, fingerprints):
        """
        Check if fingerprint exists
        :params list fingerprints: list of dict Fingerprints
        :return dict fingerprint: Return Fingerprint document if exists
        """
        for fingerprint in fingerprints:
            if self.compare_fingerprints(fingerprint['quadrants'], fingerprint['count']):
                return fingerprint
        return False

    def compare_fingerprints(self, quadrants_jwt, count_pixels):
        """
        Compare fingerprints
        :params str quadrants: Quadrants incode JWT
        :return bool: Return true if if fingerprint exists
        """

        def validate_pixels(height, width, im_bw):
            """Validate pixels"""
            try:
                if im_bw[height].item(width) == 0:
                    return True
                return False
            except Exception as error:
                return False

        count = 0
        quadrants = jwt.decode(quadrants_jwt, 'secretX', algorithms=['HS256'])

        for quadrant in QUADRANTS_NAME:
            for pixels in quadrants[quadrant]:
                if validate_pixels(pixels['y'], pixels['x'], self.image):
                    count += 1

        return count_pixels * 0.92 <= count


    @classmethod
    def _get_quadrants(cls, img_height, img_width):
        """
        :param int img_height: Image height
        :param int img_width: Image width
        :return list dict: List with min and max of pixels per quadrant
        """
        return [
            {
                'height_min': 0, 'height_max': int(img_height / 2),
                'width_min': 0, 'width_max': int(img_width / 2)
            },
            {
                'height_min': 0, 'height_max': int(img_height / 2),
                'width_min': int(img_width / 2) + 1, 'width_max': img_width
            },
            {
                'height_min': int(img_height / 2) + 1, 'height_max': img_height,
                'width_min': 0, 'width_max': int(img_width / 2)
            },
            {
                'height_min': int(img_height / 2) + 1, 'height_max': img_height,
                'width_min': int(img_width / 2) + 1, 'width_max': img_width
            }
        ]