import logging

from django.test import TransactionTestCase

from .celery import debug_task

logger = logging.getLogger(__name__)


class TestCeleryWorker(TransactionTestCase):

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_celery_works(self):
        result = debug_task.delay()
        logger.info(f"The task is: {result}")
