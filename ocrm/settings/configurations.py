import frappe
from frappe import _
from mymb_ecommerce.utils.Database import Database
from frappe.utils.password import get_decrypted_password


class Configurations:
    def __init__(self):
        self.doc = frappe.get_doc('Mymb b2c Settings')
        self.image_uri = self.doc.get('image_uri')

    def get_image_uri_instance(self):
        """Get the Solr image instance from the Mymb b2c Settings DocType"""

        return self.image_uri
    
    def get_mymb_b2c_payment_success_page(self):
        """Get Success payment page from the Mymb b2c Settings DocType"""

        return self.mymb_b2c_payment_success_page
    

    def get_mysql_connection(self):
        """Get the MySQL connection from the Mymb b2c Settings DocType"""
        if not hasattr(self, 'mysql_connection'):
            username = self.doc.get('db_username')
            encrypted_db_password = self.doc.get('db_password')
            db_password = get_decrypted_password("Mymb b2c Settings", self.doc.name, 'db_password')  # Decrypt the password
            db_host = self.doc.get('db_host')
            db_port = self.doc.get('db_port')
            db_item_data = self.doc.get('db_item_data')


            db_config = {
                'drivername': 'mysql',
                'username': username,
                'password': db_password,
                'host': db_host,
                'port': db_port,
                'database': db_item_data
            }
            self.mysql_connection = Database(db_config)

        return self.mysql_connection
