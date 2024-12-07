from .metadata_cleaner import MetadataCleaner
from .metadata_sorter import MetadataSorter
from .database_handler import DatabaseHandler

class CleanSort:
    def __init__(self, db_path='sqlite:///metadata.db'):
        self.cleaner = MetadataCleaner()
        self.sorter = MetadataSorter()
        self.db_handler = DatabaseHandler(db_path)

    def process_metadata(self, metadata_str):
        """
        Process metadata: clean, sort, and store
        Args:
            metadata_str (str): Raw metadata
        Returns:
            dict: Processed and sorted metadata
        """
        # Clean the metadata
        cleaned_data = self.cleaner.clean_metadata(metadata_str)
        
        # Sort the cleaned data
        sorted_data = self.sorter.sort_metadata(cleaned_data)
        
        # Store in database
        self.db_handler.store_metadata(sorted_data)
        
        return sorted_data

    def get_stored_metadata(self, category=None):
        """
        Retrieve stored metadata
        Args:
            category (str, optional): Specific category to retrieve
        Returns:
            dict: Retrieved metadata
        """
        return self.db_handler.retrieve_metadata(category)