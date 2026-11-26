"""核验清册及源记录没有丢失。"""

from pathlib import Path
import tempfile
import unittest

from source_reader import read_inventory, read_observations


class SourceTests(unittest.TestCase):
    root = Path(__file__).resolve().parents[1] / "records"

    def test_inventory(self):
        self.assertEqual(sorted(read_inventory(self.root)), ['audience', 'services', 'supports'])

    def test_two_independent_traces(self):
        first = list(read_observations(self.root / "shift.jsonl"))
        second = list(read_observations(self.root / "comparison.jsonl"))
        self.assertEqual((len(first), len(second)), (15, 6))
        self.assertNotEqual(first, second)

    def test_reports_clock_regression(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "unexpected.jsonl"
            path.write_text('{"at":4,"kind":"read"}\n{"at":3,"kind":"write"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unexpected.jsonl:2"):
                list(read_observations(path))
