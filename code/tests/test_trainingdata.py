import unittest

from TrainingData import TrainingData


class TrainingDataTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = TrainingData()

    def tearDown(self) -> None:
        pass

    def test_walk_step_increases_count(self):
        self.data.walk_step()
        self.assertEqual(1, self.data.number_of_steps_walked)
        self.assertEqual(1, self.data.total_steps_walked)
        self.assertEqual(1, self.data.best_steps_walked)

    def test_expressive_object_describes_in_multiple_lines(self):
        expressive = str(self.data)
        self.assertEqual(8, len(expressive.split('\n')))

    def test_score_maintains_statistics(self):
        self.data.score(200)
        self.data.score(100)
        self.assertEqual(200, self.data.best_score)
        self.assertEqual(100, self.data.last_score)

    def test_steps_reset_on_epoch(self):
        self.data.score(100)
        self.assertEqual(100, self.data.last_score)
        self.data.next_epoch()
        self.assertEqual(3, self.data.last_score)
