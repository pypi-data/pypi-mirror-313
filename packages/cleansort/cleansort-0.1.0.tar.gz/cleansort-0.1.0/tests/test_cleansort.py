import unittest
import os
from cleansort import CleanSort

class TestCleanSort(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.cleansort = CleanSort('sqlite:///:memory:')
        
    def test_html_metadata_processing(self):
        # Sample metadata in HTML format
        sample_metadata = """
        <meta name="title" content="Sample Book">
        <meta name="author" content="John Doe">
        <meta name="isbn" content="123-456-789">
        <meta name="source_site" content="example.com">
        <meta name="irrelevant" content="should be removed">
        """
        
        result = self.cleansort.process_metadata(sample_metadata)
        
        # Check if cleaning worked
        self.assertIn('titles', result)
        self.assertIn('authors', result)
        self.assertIn('identifiers', result)
        self.assertIn('sources', result)
        
        # Check if sorting worked
        self.assertEqual(result['authors']['author'], 'John Doe')
        self.assertEqual(result['identifiers']['isbn'], '123-456-789')
        
    def test_text_metadata_processing(self):
        # Sample metadata in text format
        sample_metadata = """
        title: Another Book
        author: Jane Smith
        isbn: 987-654-321
        source_site: library.com
        irrelevant: should be removed
        """
        
        result = self.cleansort.process_metadata(sample_metadata)
        
        # Check if cleaning worked
        self.assertIn('titles', result)
        self.assertIn('authors', result)
        self.assertIn('identifiers', result)
        self.assertIn('sources', result)
        
        # Check if sorting worked
        self.assertEqual(result['authors']['author'], 'Jane Smith')
        self.assertEqual(result['identifiers']['isbn'], '987-654-321')
        
    def test_database_storage_and_retrieval(self):
        sample_metadata = """
        <meta name="title" content="Test Book">
        <meta name="author" content="Test Author">
        <meta name="isbn" content="test-isbn">
        <meta name="source_site" content="test.com">
        """
        
        # Process and store metadata
        self.cleansort.process_metadata(sample_metadata)
        
        # Retrieve all stored metadata
        stored_data = self.cleansort.get_stored_metadata()
        
        # Check if data was stored correctly
        self.assertIn('authors', stored_data)
        self.assertIn('identifiers', stored_data)
        self.assertEqual(stored_data['authors']['author'], 'Test Author')
        
        # Test category-specific retrieval
        authors_data = self.cleansort.get_stored_metadata('authors')
        self.assertEqual(authors_data['authors']['author'], 'Test Author')

if __name__ == '__main__':
    unittest.main()