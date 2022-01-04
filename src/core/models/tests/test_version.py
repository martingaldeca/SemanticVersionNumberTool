from django.db import transaction
from django.test import TestCase

from core.factories import VersionFactory
from core.models import Version


class VersionTest(TestCase):

    def setUp(self):
        self.version: Version = VersionFactory(major=1, minor=1, patch=1)

    def test_formatted(self):
        self.assertEqual(self.version.formatted, f'{self.version.major}.{self.version.minor}.{self.version.patch}')

    def test_next_version(self):
        test_data_list = [
            ('major', '2.0.0'),
            ('minor', '1.2.0'),
            ('patch', '1.1.2'),
        ]
        for test_data in test_data_list:
            with self.subTest(
                test_data=test_data
            ), transaction.atomic():
                update_type, formatted = test_data
                self.assertEqual(self.version.next_version(update_type).formatted, formatted)
                transaction.set_rollback(True)

    def test_next_version_not_valid(self):
        with self.assertRaises(ValueError) as value_error:
            self.version.next_version(update_type='patata')
        self.assertEqual(str(value_error.exception), 'patata is not a valid update type')

    def test_to_json(self):
        expected_data = {
            'major': self.version.major,
            'minor': self.version.minor,
            'patch': self.version.patch,
            'formatted': self.version.formatted,
            'author': {
                'username': self.version.author.username,
                'github': self.version.author.profile.github,
            }
        }
        self.assertEqual(self.version.to_json(), expected_data)
