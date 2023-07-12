from ocrm.model.Port import Port
from ocrm.settings.configurations import Configurations
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from datetime import datetime, timedelta

class PortRepository:

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

    def get_all_ports(self, limit=None, time_laps=None, to_dict=False):
        query = self.session.query(Port)
        if time_laps is not None:
            time_laps = int(time_laps)
            time_threshold = datetime.now() - timedelta(minutes=time_laps)
            query = query.filter(Port.created_at >= time_threshold)
        if limit is not None:
            query = query.limit(limit)
        results = query.all()
        if to_dict:
            return [port.to_dict() for port in results]
        else:
            return results
