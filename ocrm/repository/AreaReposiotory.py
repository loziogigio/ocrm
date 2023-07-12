from ocrm.model.Area import Area
from ocrm.settings.configurations import Configurations
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from datetime import datetime, timedelta

class AreaRepository:

    def __init__(self, external_db_connection_string=None):
        config = Configurations()
        if external_db_connection_string:
            engine = create_engine(external_db_connection_string)
        else:
            db = config.get_mysql_connection()
            engine = db.engine
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def get_all_areas(self, limit=None, time_laps=None, to_dict=False):
        query = self.session.query(Area)
        if time_laps is not None:
            time_laps = int(time_laps)
            time_threshold = datetime.now() - timedelta(minutes=time_laps)
            query = query.filter(Area.created_at >= time_threshold)
        if limit is not None:
            query = query.limit(limit)
        results = query.all()
        if to_dict:
            return [area.to_dict() for area in results]
        else:
            return results
