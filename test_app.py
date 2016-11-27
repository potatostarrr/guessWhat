
import unittest
import os
from flask import json

from tracking import app

class test( unittest.TestCase):
    def test_200(self):
        test = app.test_client(self)
        response = test.get("/", content_type = "html/txt")
        self.assertEqual(response.status_code, 200)