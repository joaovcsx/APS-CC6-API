
#!/usr/bin/python
# -*- coding: utf-8 -*-
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("aps-cc6-firebase-adminsdk-6vond-313cc0ea8c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class FirebaseModule(object):

    def __init__(self):
        """ Init class """

class FirebaseFingerprints():

    # def __init__(self, params=None):
    #     """ Init class """
    #     self.quadrants_with_pixels = None

    # @property
    # def quadrants_with_pixels(self):
    #     """Lease status"""
    #     return self._quadrants_with_pixels

    # @quadrants_with_pixels.setter
    # def quadrants_with_pixels(self, quadrants_with_pixels):
    #     self._quadrants_with_pixels = quadrants_with_pixels

    @classmethod
    def create(cls, params):
        """Create document Figerprint"""
        query_ref = db.collection(u'fingerprints').document()
        return query_ref.set(params)

    @classmethod
    def get(cls):
        """Get documents Figerprints"""
        fingerprints = db.collection(u'fingerprints').get()
        fingerprints_result = []
        for fingerprint in fingerprints:
            fingerprints_result.append(fingerprint.to_dict())

        return fingerprints_result