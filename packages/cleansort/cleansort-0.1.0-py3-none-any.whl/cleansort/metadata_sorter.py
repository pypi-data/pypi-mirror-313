import pandas as pd

class MetadataSorter:
    def __init__(self):
        self.categories = {
            'authors': ['author'],
            'identifiers': ['isbn'],
            'titles': ['title', 'article', 'journal', 'chapter'],
            'sources': ['source_site']
        }

    def sort_metadata(self, cleaned_metadata):
        """
        Sort cleaned metadata into categories
        Args:
            cleaned_metadata (dict): Cleaned metadata
        Returns:
            dict: Sorted metadata by category
        """
        sorted_data = {}
        
        for category, fields in self.categories.items():
            category_data = {}
            for field in fields:
                if field in cleaned_metadata:
                    category_data[field] = cleaned_metadata[field]
            if category_data:
                sorted_data[category] = category_data
                    
        return sorted_data