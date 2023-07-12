import frappe
from ocrm.repository.AddressReposiotory import AddressRepository
from ocrm.repository.UserRepository import UserRepository
from frappe.utils.password import update_password
from ocrm.model.User import User
from mymb_ecommerce.mymb_ecommerce.order import _create_address



@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_users_from_external_db(limit=20 , time_laps=None):

    # Initialize the UserRepository with the external DB connection string
    user_repo = UserRepository()

    # Fetch all the users from the external database
    external_users = user_repo.get_all_users(limit=limit , time_laps=time_laps , to_dict=True)
    
    # Commit the changes
    frappe.db.commit()
    return {
        "data":external_users
    }




@frappe.whitelist(allow_guest=True, methods=['POST'])
def import_users_from_external_db(limit=None , time_laps=None , filters=None):
    try:
        # Initialize the UserRepository with the external DB connection string
        user_repo = UserRepository()

        # Fetch all the users from the external database
        external_users = user_repo.get_all_users(limit=limit, time_laps=time_laps, filters=filters)

        # Loop through the external users and create customer and user accounts in ERPNext
        for external_user in external_users:

            create_customer_and_user(external_user)
        
        # Commit the changes
        frappe.db.commit()

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while importing users: {str(e)}", title="Import Users Error")




def create_customer_and_user(external_user: User):
    email = external_user.email
    first_name = external_user.first_name
    last_name = external_user.last_name
    external_user_id = external_user.id
    password = "123#Abc"
    
    try:
        # Check if the user already exists
        user = frappe.db.exists("User", {"email": email})
        if user:
            # Fetch the user document for updating
            user = frappe.get_doc("User", user)
        else:
            # Create a new user document
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "send_welcome_email": False,
                "roles": [{"role": "Customer"}]
            })
            user.insert(ignore_permissions=True)
            # Reset the password
            update_password(email, password)

        # Update user information
        user.first_name = first_name
        user.last_name = last_name
        user.save(ignore_permissions=True)

        # Check if the customer already exists
        customer = frappe.db.exists("Customer", {"email_id": email})
        if customer:
            # Fetch the customer document for updating
            customer = frappe.get_doc("Customer", customer)
        else:
            # Create a new customer document
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": f"{first_name} {last_name}",
                "customer_group": "B2C",
                "territory": "Italy",
                "customer_type": "Individual",
                "email_id": email,
                "mobile_no": external_user.phone if external_user.phone else "",
                "cruise_user_id": external_user.id
            })
            customer.insert(ignore_permissions=True)

        # Update customer information
        customer.customer_name = f"{first_name} {last_name}"
        customer.customer_group = "B2C"
        customer.territory = "Italy"
        customer.customer_type = "Individual"
        customer.email_id = email
        if external_user.phone:
            customer.mobile_no = external_user.phone
        customer.user = user.name
        customer.cruise_user_id = external_user.id
        customer.save(ignore_permissions=True)

        # Log the successful creation or update
        frappe.log_error(message=f"Successfully created or updated user and customer for email: {email}", title="User and Customer Creation/Update")

         # Create an instance of AddressRepository to retrieve addresses
        address_repo = AddressRepository()
        user_addresses = address_repo.get_addresses_for_user(external_user_id)

        # Loop through addresses and create them in ERPNext
        for user_address in user_addresses:
            # Check if 'phone' attribute exists in 'user_address'
            phone = user_address.phone if hasattr(user_address, 'phone') else ""

            contact_info = {
                "email_id": email,
                "phone": phone,
                "billing_address": {
                    "address_line1": user_address.address,
                    "city": user_address.city,
                    "state": user_address.province,
                    "pincode": user_address.cap,
                    "country": 'Italy'
                }
            }
            # Call the _create_address method
            _create_address(customer, contact_info, address_type='Billing', full_name=f"{first_name} {last_name}")


        # Log the successful creation or update
        frappe.log_error(message=f"Successfully created or updated user and customer for email: {email}", title="User and Customer Creation/Update")

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating or updating user and customer for email {email}: {str(e)}", title="User and Customer Creation/Update Error")
