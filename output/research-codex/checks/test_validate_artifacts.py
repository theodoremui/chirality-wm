"""Regression tests for optional external source verification."""
import hashlib
from pathlib import Path
import tempfile
import unittest

from validate_artifacts import check_sources


class SourceVerificationTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {'sources': [{'relative_path': 'nested/source.pdf',
                                     'sha256': hashlib.sha256(b'original').hexdigest()}]}

    def test_unavailable_sources_are_not_reported_as_verified(self):
        self.assertEqual(check_sources(self.manifest, None), ('not_checked', []))

    def test_missing_changed_and_matching_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            status, errors = check_sources(self.manifest, root)
            self.assertEqual(status, 'failed')
            self.assertIn('Source missing', errors[0])
            source = root / 'nested/source.pdf'
            source.parent.mkdir()
            source.write_bytes(b'changed')
            status, errors = check_sources(self.manifest, root)
            self.assertEqual(status, 'failed')
            self.assertIn('Source changed', errors[0])
            source.write_bytes(b'original')
            self.assertEqual(check_sources(self.manifest, root), ('passed', []))


if __name__ == '__main__':
    unittest.main()
