import frappe
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from ocrm.settings.configurations import Configurations
from ocrm.model.Company import Company
from sqlalchemy import desc
from datetime import datetime, timedelta

class CompanyRepository:

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

    def get_all_companies(self, limit=None, time_laps=None, to_dict=False):
        # Create a query for the Company table
        query = self.session.query(Company)
        
        # Conditionally add a time filter if time_laps is provided
        if time_laps is not None:
            time_laps = int(time_laps)  # Convert time_laps to integer
            time_threshold = datetime.now() - timedelta(minutes=time_laps)
            query = query.filter(Company.created_at >= time_threshold)
        
        # Apply the limit
        if limit is not None:
            query = query.limit(limit)
        
        # Execute the query
        results = query.all()
        
        # Optionally convert the results to dictionaries
        if to_dict:
            return [user.to_dict() for user in results]
        else:
            return results

