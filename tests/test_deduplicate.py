import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from deduplicate import canonical_name, deduplicate


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
            self.assertTrue((tmp_path / "a.txt").exists())
            self.assertFalse((tmp_path / "b.txt").exists())
            self.assertTrue((sub / "c.txt").exists())


    def test_deletes_uuid_prefixed_duplicates(self) -> None:
        """Files with the same name after stripping a UUID prefix are duplicates."""
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            base = "report.pdf"
            (tmp_path / f"4d391215-6e1f-43c7-aad9-80fa67349ab1_{base}").write_text("v1")
            (tmp_path / f"33411634-12cd-47b2-bb2f-32c8064ef03f_{base}").write_text("v2")
            (tmp_path / f"ddb64d4b-a890-4ac1-b379-da4216ac66cb_{base}").write_text("v3")

            deleted = deduplicate(tmp_path)

            self.assertEqual(deleted, 2)
            remaining = list(tmp_path.iterdir())
            self.assertEqual(len(remaining), 1)

    def test_uuid_prefix_does_not_affect_truly_different_files(self) -> None:
        """Files with different canonical names are not treated as duplicates."""
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "4d391215-6e1f-43c7-aad9-80fa67349ab1_report_A.txt").write_text("a")
            (tmp_path / "33411634-12cd-47b2-bb2f-32c8064ef03f_report_B.txt").write_text("b")

            deleted = deduplicate(tmp_path)

            self.assertEqual(deleted, 0)
            self.assertEqual(len(list(tmp_path.iterdir())), 2)

    def test_canonical_name_strips_uuid_prefix(self) -> None:
        self.assertEqual(
            canonical_name("4d391215-6e1f-43c7-aad9-80fa67349ab1_MyDoc.pdf"),
            "MyDoc.pdf",
        )

    def test_canonical_name_leaves_non_uuid_name_unchanged(self) -> None:
        self.assertEqual(canonical_name("report.pdf"), "report.pdf")
        self.assertEqual(canonical_name("not-a-uuid_file.txt"), "not-a-uuid_file.txt")


if __name__ == "__main__":
    unittest.main()
