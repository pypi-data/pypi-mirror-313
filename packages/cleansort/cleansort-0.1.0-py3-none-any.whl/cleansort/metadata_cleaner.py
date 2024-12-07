from bs4 import BeautifulSoup
import pandas as pd

class MetadataCleaner:
    def __init__(self):
        self.desired_fields = [
            'title', 'author', 'isbn', 'source_site',
            'journal', 'article', 'chapter'
        ]

    def clean_metadata(self, metadata_str):
        """
        Clean metadata by extracting only desired fields
        Args:
            metadata_str (str): Raw metadata in HTML or text format
        Returns:
            dict: Cleaned metadata with only desired fields
        """
        # Parse HTML if the metadata is in HTML format
        try:
            soup = BeautifulSoup(metadata_str, 'html.parser')
            meta_tags = soup.find_all('meta')
            if meta_tags:  # Only process as HTML if meta tags are found
                metadata = {}
                for tag in meta_tags:
                    name = tag.get('name', '').lower()
                    content = tag.get('content', '')
                    
                    if name in self.desired_fields:
                        metadata[name] = content
                return metadata
        except:
            pass
            
        # If not HTML or no meta tags found, parse as text
        return self._parse_text_metadata(metadata_str)

    def _parse_text_metadata(self, metadata_str):
        """Parse non-HTML metadata"""
        cleaned_data = {}
        lines = [line.strip() for line in metadata_str.split('\n') if line.strip()]
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                if key in self.desired_fields:
                    cleaned_data[key] = value.strip()
                    
        return cleaned_data