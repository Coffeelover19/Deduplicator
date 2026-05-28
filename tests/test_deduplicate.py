import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from deduplicate import deduplicate


class DeduplicateTests(unittest.TestCase):
    def test_deletes_only_duplicate_files(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "a.txt").write_text("same")
            (tmp_path / "b.txt").write_text("same")
            (tmp_path / "c.txt").write_text("different")

            deleted = deduplicate(tmp_path)

            self.assertEqual(deleted, 1)
            self.assertTrue((tmp_path / "a.txt").exists())
            self.assertFalse((tmp_path / "b.txt").exists())
            self.assertTrue((tmp_path / "c.txt").exists())

    def test_ignores_subdirectories(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "a.txt").write_text("same")
            (tmp_path / "b.txt").write_text("same")
            sub = tmp_path / "sub"
            sub.mkdir()
            (sub / "c.txt").write_text("same")

            deleted = deduplicate(tmp_path)

            self.assertEqual(deleted, 1)
            self.assertTrue((sub / "c.txt").exists())


if __name__ == "__main__":
    unittest.main()
