import unittest
import logging
from inoopa_utils.inoopa_logging import create_logger

class TestInoopaLogging(unittest.TestCase):
    def test_create_logger(self):
        logger = create_logger("test_logger", "DEBUG")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertEqual(logger.name, "test_logger")

if __name__ == '__main__':
    unittest.main()