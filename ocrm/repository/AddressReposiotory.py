from sqlalchemy.orm import sessionmaker
from ocrm.settings.configurations import Configurations
from ocrm.model.Address import Address

class AddressRepository:

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

    def get_addresses_for_user(self, user_id):
        """
        Get all addresses for a specific user from the external database.
        """
        query = self.session.query(Address).filter(Address.user_id == user_id)
        return query.all()
