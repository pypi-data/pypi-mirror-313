from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()

class MetadataEntry(Base):
    __tablename__ = 'metadata'
    
    id = Column(Integer, primary_key=True)
    category = Column(String)
    data = Column(String)  # Store as JSON string

class DatabaseHandler:
    def __init__(self, db_path='sqlite:///metadata.db'):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def store_metadata(self, sorted_metadata):
        """
        Store sorted metadata in the database
        Args:
            sorted_metadata (dict): Sorted metadata by category
        """
        for category, data in sorted_metadata.items():
            entry = MetadataEntry(
                category=category,
                data=json.dumps(data)
            )
            self.session.add(entry)
        self.session.commit()

    def retrieve_metadata(self, category=None):
        """
        Retrieve metadata from the database
        Args:
            category (str, optional): Category to retrieve
        Returns:
            dict: Retrieved metadata
        """
        if category:
            entries = self.session.query(MetadataEntry).filter_by(category=category).all()
        else:
            entries = self.session.query(MetadataEntry).all()
            
        return {entry.category: json.loads(entry.data) for entry in entries}