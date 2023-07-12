# ocrm/repository/ShipRepository.py

from ocrm.model.Ship import Ship
from ocrm.settings.configurations import Configurations
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from datetime import datetime, timedelta

class ShipRepository:

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

    def get_all_ships(self, limit=None, time_laps=None, to_dict=False):
        # Create a query for the Ship table
        query = self.session.query(Ship)
        
        # Conditionally add a time filter if time_laps is provided
        if time_laps is not None:
            time_laps = int(time_laps)  # Convert time_laps to integer
            time_threshold = datetime.now() - timedelta(minutes=time_laps)
            query = query.filter(Ship.created_at >= time_threshold)
        
        # Apply the limit
        if limit is not None:
            query = query.limit(limit)
        
        # Execute the query
        results = query.all()
        
        # Optionally convert the results to dictionaries
        if to_dict:
            return [ship.to_dict() for ship in results]
        else:
            return results
