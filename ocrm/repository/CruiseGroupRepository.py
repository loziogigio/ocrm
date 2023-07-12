# ocrm/repository/CruiseGroupRepository.py
import phpserialize
from ocrm.model.CruiseGroup import CruiseGroup
from ocrm.settings.configurations import Configurations
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from datetime import datetime, timedelta

class CruiseGroupRepository:

    def __init__(self, external_db_connection_string=None):
        # Get the Configurations instance
        config = Configurations()

        # If an external DB connection string is provided, use it. Otherwise, use the default connection
        if external_db_connection_string:
            engine = create_engine(external_db_connection_string)
        else:
            db = config.get_mysql_connection()
            engine = db.engine

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def get_all_cruise_groups(self, limit=None, time_laps=None, to_dict=False ,  filters=None):
        # Create a query for the CruiseGroup table
        query = self.session.query(CruiseGroup)
        
        # Conditionally add a time filter if time_laps is provided
        if time_laps is not None:
            time_laps = int(time_laps)  # Convert time_laps to integer
            time_threshold = datetime.now() - timedelta(minutes=time_laps)
            query = query.filter(CruiseGroup.created_at >= time_threshold)

        # Apply the filters
        if filters is not None:
            for key, value in filters.items():
                # Make sure the attribute exists in the Cruise model
                if hasattr(CruiseGroup, key):
                    query = query.filter(getattr(CruiseGroup, key) == value)
        
        # Apply the limit
        if limit is not None:
            query = query.limit(limit)
        
        # Execute the query
        results = query.all()
        
        # Optionally convert the results to dictionaries
        if to_dict:
            results = [self._convert_to_dict(result) for result in results]
        
        return results  # Return the results regardless of the value of to_dict

        
    def _convert_to_dict(self, cruise_group: CruiseGroup):
        data = cruise_group.to_dict()
        if data['coords']:
            data['coords'] = phpserialize.loads(data['coords'].encode('utf-8'), decode_strings=True)
        return data