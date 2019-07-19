import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import create_app


app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my-secret')
        self.assertFalse(current_app is None)
        self.assertTrue(
          app.config['SQLALCHEMY_DATABASE_URI'] ==
          os.environ.get('DATABASE_URL'))
        self.assertTrue(
          app.config['MAIL_SERVER'] == os.environ.get('MAIL_SERVER'))
        self.assertTrue(
          app.config['MAIL_PORT'] == int(os.environ.get('MAIL_PORT')))
        self.assertTrue(app.config['MAIL_USE_TLS'])
        self.assertTrue(
          app.config['MAIL_USERNAME'] == os.environ.get('MAIL_USERNAME'))
        self.assertTrue(
          app.config['MAIL_PASSWORD'] == os.environ.get('MAIL_PASSWORD'))


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my-secret')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
          app.config['SQLALCHEMY_DATABASE_URI'] ==
          os.environ.get('DATABASE_TEST_URL')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my-secret')
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(
          app.config['MAIL_SERVER'] == os.environ.get('MAIL_SERVER'))
        self.assertTrue(
          app.config['MAIL_PORT'] == int(os.environ.get('MAIL_PORT')))
        self.assertTrue(app.config['MAIL_USE_TLS'])
        self.assertTrue(
          app.config['MAIL_USERNAME'] == os.environ.get('MAIL_USERNAME'))
        self.assertTrue(
          app.config['MAIL_PASSWORD'] == os.environ.get('MAIL_PASSWORD'))


if __name__ == '__main__':
    unittest.main()
