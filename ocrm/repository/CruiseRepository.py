# ocrm/repository/CruiseRepository.py

from ocrm.model.Cruise import Cruise
from ocrm.settings.configurations import Configurations
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from datetime import datetime, timedelta


class CruiseRepository:

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

    def get_all_cruises(self, limit=None, time_laps=None, to_dict=False, filters=None):
        query = self.session.query(Cruise)
        
        if time_laps is not None:
            time_laps = int(time_laps)
            time_threshold = datetime.now() - timedelta(minutes=time_laps)
            query = query.filter(Cruise.created_at >= time_threshold)
        
        # Apply the filters
        if filters is not None:
            for key, value in filters.items():
                # Make sure the attribute exists in the Cruise model
                if hasattr(Cruise, key):
                    query = query.filter(getattr(Cruise, key) == value)
        
        if limit is not None:
            query = query.limit(limit)

        results = query.all()

        if to_dict:
            return [cruise.to_dict() for cruise in results]
        else:
            return results