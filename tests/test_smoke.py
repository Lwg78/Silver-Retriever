import unittest
import os
import shutil
from src.engine import RobustEngine

class TestSilverRetriever(unittest.TestCase):
    def setUp(self):
        # Create a dummy environment
        self.engine = RobustEngine()
        self.test_file = "test_doc.txt"
        with open(self.test_file, "w") as f:
            f.write("This is a test document about AIAP. The deadline is tomorrow.")

    def test_ingestion(self):
        """Test if engine can read a file without crashing."""
        success = self.engine.ingest_file(self.test_file)
        self.assertTrue(success)
        self.assertIn("test_doc.txt", self.engine.get_loaded_files())

    def test_search(self):
        """Test if search returns results."""
        self.engine.ingest_file(self.test_file)
        results = self.engine.search("AIAP")
        self.assertTrue(len(results) > 0)
        self.assertIn("AIAP", results[0]['payload']['text'])

    def tearDown(self):
        # Cleanup
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.engine.nuke_library()

if __name__ == '__main__':
    unittest.main()