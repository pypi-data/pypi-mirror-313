import unittest
from inoopa_utils.rabbitmq_helpers import get_messages_from_queue, push_to_queue, empty_queue

class TestRabbitMQHelpers(unittest.TestCase):
    def test_push_and_get_message(self):
        push_to_queue("test_queue", ["test_message"])
        messages = get_messages_from_queue("test_queue", 1)
        self.assertIn("test_message", messages)

    def test_empty_queue(self):
        push_to_queue("test_queue", ["test_message"])
        empty_queue("test_queue")
        messages = get_messages_from_queue("test_queue", 1)
        self.assertEqual(messages, [])

if __name__ == '__main__':
    unittest.main()