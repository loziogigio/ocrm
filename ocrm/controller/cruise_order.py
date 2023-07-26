import frappe
from ocrm.repository.AddressReposiotory import AddressRepository
from ocrm.repository.AreaReposiotory import AreaRepository
from ocrm.repository.CompanyRepository import CompanyRepository
from ocrm.repository.OrderReposiotory import OrderRepository
from ocrm.repository.PortRepository import PortRepository
from ocrm.repository.ShipRepository import ShipRepository
from ocrm.repository.CruiseGroupRepository import CruiseGroupRepository
from ocrm.repository.CruiseRepository import CruiseRepository

from frappe.utils.password import update_password
from ocrm.model.Company import Company
from mymb_ecommerce.mymb_ecommerce.order import _create_address
from ocrm.services.cruise_service import add_cruise_categories, add_cruise_participants, add_cruise_closing_details, add_cruise_histories, add_cruise_flats, add_cruise_options, add_cruise_prices


@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_order(uuid, limit=20, time_laps=None):
    
    print(f"UUID:", {uuid})
    try:
        # Assuming 'uuid' is the unique ID of the cruise order
        cruise_order = frappe.get_doc("Cruise Order", {"uuid": uuid})

        # Commit the changes
        frappe.db.commit()
        return {
            "data": cruise_order
        }
    except frappe.DoesNotExistError:
        return None


        

