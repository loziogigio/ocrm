import phpserialize
import frappe
from ocrm.repository.AddressReposiotory import AddressRepository
from ocrm.repository.AreaReposiotory import AreaRepository
from ocrm.repository.CompanyRepository import CompanyRepository
from ocrm.repository.OrderReposiotory import OrderRepository
from ocrm.repository.PortRepository import PortRepository
from ocrm.repository.ShipRepository import ShipRepository
from ocrm.repository.CruiseGroupRepository import CruiseGroupRepository
from ocrm.repository.CruiseRepository import CruiseRepository
from datetime import datetime


from frappe.utils.password import update_password
from ocrm.model.Company import Company
from mymb_ecommerce.mymb_ecommerce.order import _create_address


@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_cruises_from_external_db(limit=20, time_laps=None):
    # Initialize the CruiseRepository with the external DB connection string
    cruise_repo = CruiseRepository()

    # Fetch all the cruises from the external database
    external_cruises = cruise_repo.get_all_cruises(limit=limit, time_laps=time_laps, to_dict=True)

    # Commit the changes
    frappe.db.commit()
    return {
        "data":external_cruises
    }

@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_companies_from_external_db(limit=20 , time_laps=None):

    # Initialize the UserRepository with the external DB connection string
    company_repo = CompanyRepository()

    # Fetch all the users from the external database
    external_users = company_repo.get_all_companies(limit=limit , time_laps=time_laps , to_dict=True)
    
    # Commit the changes
    frappe.db.commit()
    return {
        "data":external_users
    }

@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_ships_from_external_db(limit=20 , time_laps=None):

    # Initialize the ShipRepository with the external DB connection string
    ship_repo = ShipRepository()

    # Fetch all the ships from the external database
    external_ships = ship_repo.get_all_ships(limit=limit , time_laps=time_laps , to_dict=True)
    
    # Commit the changes
    frappe.db.commit()
    return {
        "data":external_ships
    }

@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_cruise_groups_from_external_db(limit=20 , time_laps=None):

    # Initialize the CruiseGroupRepository with the external DB connection string
    cruise_group_repo = CruiseGroupRepository()

    # Fetch all the cruise groups from the external database
    external_cruise_groups = cruise_group_repo.get_all_cruise_groups(limit=limit , time_laps=time_laps , to_dict=True)
    
    # Commit the changes
    frappe.db.commit()
    return {
        "data":external_cruise_groups
    }

@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_areas_from_external_db(limit=20 , time_laps=None):

    # Initialize the AreaRepository with the external DB connection string
    area_repo = AreaRepository()

    # Fetch all the area from the external database
    external_areas = area_repo.get_all_areas(limit=limit , time_laps=time_laps , to_dict=True)
    
    # Commit the changes
    frappe.db.commit()
    return {
        "data":external_areas
    }

@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_ports_from_external_db(limit=20 , time_laps=None):

    # Initialize the PortRepository with the external DB connection string
    port_repo = PortRepository()

    # Fetch all the cruise groups from the external database
    external_ports = port_repo.get_all_ports(limit=limit , time_laps=time_laps , to_dict=True)
    
    # Commit the changes
    frappe.db.commit()
    return {
        "data":external_ports
    }



@frappe.whitelist(allow_guest=True, methods=['GET'])
def get_orders_from_external_db(limit=20 , time_laps=None):

    # Initialize the OrderRepository with the external DB connection string
    port_repo = OrderRepository()

    # Fetch all the cruise groups from the external database
    external_ports = port_repo.get_all_orders(limit=limit , time_laps=time_laps , to_dict=True)
    
    # Commit the changes
    frappe.db.commit()
    return {
        "data":external_ports
    }



@frappe.whitelist(allow_guest=True, methods=['GET'])
def import_companies_from_external_db(limit=None , time_laps=None):
    try:
        # Initialize the CompanyRepository with the external DB connection string
        company_repo = CompanyRepository()

        # Fetch all the companies from the external database
        external_companies = company_repo.get_all_companies(limit=limit , time_laps=time_laps)

        # Loop through the external companies and create Cruise Company doc in ERPNext
        for external_company in external_companies:
            create_cruise_company(external_company)
        
        # Commit the changes
        frappe.db.commit()

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while importing companies: {str(e)}", title="Import Companies Error")


def create_cruise_company(external_company):
    # Assuming that the external_company object has fields: id (unique company id), name, short_name, order, uuid, created_at, updated_at
    company_id = external_company.id
    name = external_company.name
    short_name = external_company.short_name
    order = external_company.order
    UUID = external_company.UUID

    try:
        # Check if the company already exists
        company = frappe.db.exists("Cruise Company", {"uuid": UUID})
        if company:
            # Fetch the company document for updating
            company = frappe.get_doc("Cruise Company", company)
            company.company_id = company_id
            company.name = name
            company.short_name = short_name
            company.order = order
            company.uuid = UUID
            company.save(ignore_permissions=True)
            frappe.log_error(message=f"Successfully updated company with uuid: {UUID}", title="Company Update")
        else:
            # Create a new company document
            company = frappe.get_doc({
                "doctype": "Cruise Company",
                "company_id": company_id,
                "company_name": name,
                "short_name": short_name,
                "order": order,
                "uuid": UUID
            })
            company.insert(ignore_permissions=True)
            frappe.log_error(message=f"Successfully created company with uuid: {UUID}", title="Company Creation")

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating or updating company with uuid {UUID}: {str(e)}", title="Company Creation/Update Error")


@frappe.whitelist(allow_guest=True, methods=['POST'])
def import_cruises_groups_from_external_db(limit=None , time_laps=None , filters=None):
    try:
        # Initialize the CruiseGroupRepository with the external DB connection string
        cruise_groups_repo = CruiseGroupRepository()

        # Fetch all the cruise groups from the external database
        external_cruise_groups = cruise_groups_repo.get_all_cruise_groups(limit=limit , time_laps=time_laps , filters=filters)

        # Loop through the external companies and create Cruise Company doc in ERPNext
        for external_cruise_group in external_cruise_groups:
            create_cruise_group(external_cruise_group)
        
        # Commit the changes
        frappe.db.commit()

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while importing companies: {str(e)}", title="Import Cruise Group Error")


def create_cruise_group(external_group):
    # Assuming that the external_group object has fields: id, code, coords, static, static_small, area_id, custom_area_id, created_at, updated_at
    cruise_group_id = external_group.id
    code = external_group.code
    coords = external_group.coords
    static = external_group.static
    static_small = external_group.static_small
    area_id = external_group.area_id
    custom_area_id = external_group.custom_area_id
    
    try:
        # Check if the group already exists
        group = frappe.db.exists("Cruise Group", {"code": code})
        if group:
            # Fetch the group document for updating
            group = frappe.get_doc("Cruise Group", group)
        else:
            # Create a new group document
            group = frappe.get_doc({
                "doctype": "Cruise Group",
                "cruise_group_id": cruise_group_id,
                "code": code,
                "coords": coords,
                "static": static,
                "static_small": static_small,
                "area_id": area_id,
                "custom_area_id": custom_area_id
            })
            group.insert(ignore_permissions=True)
            
        # Update group information
        group.cruise_group_id = cruise_group_id
        group.code = code
        group.coords = coords
        group.static = static
        group.static_small = static_small
        group.area_id = area_id
        group.custom_area_id = custom_area_id
        group.save(ignore_permissions=True)

        # Log the successful creation or update
        frappe.log_error(message=f"Successfully created or updated group with id: {cruise_group_id}", title="Group Creation/Update")

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating or updating group with id {cruise_group_id}: {str(e)}", title="Group Creation/Update Error")


@frappe.whitelist(allow_guest=True, methods=['GET'])
def import_ships_from_external_db(limit=None , time_laps=None):
    try:
        # Initialize the ShipRepository with the external DB connection string
        ships_repo = ShipRepository()

        # Fetch all the ships from the external database
        external_ships = ships_repo.get_all_ships(limit=limit , time_laps=time_laps)

        # Loop through the external ships and create Ship doc in ERPNext
        for external_ship in external_ships:
            create_ship(external_ship)
        
        # Commit the changes
        frappe.db.commit()

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while importing ships: {str(e)}", title="Import Ship Error")


def create_ship(external_ship):
    # Assuming that the external_ship object has fields: id, name, code, featured, order, active, UUID, company_id
    ship_id = external_ship.id
    ship_name = external_ship.name
    code = external_ship.code
    featured = external_ship.featured
    order = external_ship.order
    active = external_ship.active
    UUID = external_ship.UUID
    company_id = external_ship.company_id
    
    try:
        # Check if the ship already exists
        ship = frappe.db.exists("Ship", {"uuid": UUID})
        if ship:
            # Fetch the ship document for updating
            ship = frappe.get_doc("Ship", ship)
        else:
            # Create a new ship document
            ship = frappe.get_doc({
                "doctype": "Ship",
                "ship_id": ship_id,
                "ship_name": ship_name,
                "code": code,
                "featured": featured,
                "order": order,
                "active": active,
                "uuid": UUID,
                "company_id": company_id,
            })
            ship.insert(ignore_permissions=True)
            
        # Update ship information
        ship.ship_id = ship_id
        ship.ship_name = ship_name
        ship.code = code
        ship.featured = featured
        ship.order = order
        ship.active = active
        ship.uuid = UUID
        ship.company_id = company_id
        ship.save(ignore_permissions=True)

        # Log the successful creation or update
        frappe.log_error(message=f"Successfully created or updated ship with id: {ship_id}", title="Ship Creation/Update")

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating or updating ship with id {ship_id}: {str(e)}", title="Ship Creation/Update Error")


@frappe.whitelist(allow_guest=True, methods=['POST'])
def import_cruises_from_external_db(limit=None, time_laps=None, filters=None):
    try:
        # Initialize the CruiseRepository with the external DB connection string
        cruises_repo = CruiseRepository()

        # Fetch all the cruises from the external database
        external_cruises = cruises_repo.get_all_cruises(limit=limit, time_laps=time_laps, filters=filters)

        # Loop through the external cruises and create Cruise doc in ERPNext
        for external_cruise in external_cruises:
            create_cruise(external_cruise)
        
        # Commit the changes
        frappe.db.commit()

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while importing cruises: {str(e)}", title="Import Cruise Error")


def create_cruise(external_cruise):
    # Assuming that the external_cruise object has necessary fields
    cruise_id = external_cruise.id
    display_name = external_cruise.display_name
    name = external_cruise.name
    company_id = external_cruise.company_id
    ship_id = external_cruise.ship_id
    cruise_group_id = external_cruise.cruise_group_id
    adv = external_cruise.adv
    date_start = external_cruise.date_start
    date_end = external_cruise.date_end
    cruise_code = external_cruise.code
    original_code = external_cruise.original_code
    area_code = external_cruise.area_code
    duration = external_cruise.duration
    featured = external_cruise.featured
    active = external_cruise.active
    immediate_confirm = external_cruise.immediate_confirm
    UUID = external_cruise.UUID
    flights = external_cruise.flights
    flight_type = external_cruise.flight_type
    
    try:
        # Check if the cruise already exists
        cruise = frappe.db.exists("Cruise", {"uuid": UUID})
        if cruise:
            # Fetch the cruise document for updating
            cruise = frappe.get_doc("Cruise", cruise)
        else:
            # Create a new cruise document
            cruise = frappe.get_doc({
                "doctype": "Cruise",
                "cruise_id": cruise_id,
                "display_name": display_name,
                "cruise_name": name,
                "company_id": company_id,
                "ship_id": ship_id,
                "cruise_group_id": cruise_group_id,
                "adv": adv,
                "date_start": date_start,
                "date_end": date_end,
                "cruise_code": cruise_code,
                "original_code": original_code,
                "area_code": area_code,
                "duration": duration,
                "featured": featured,
                "active": active,
                "immediate_confirm": immediate_confirm,
                "uuid": UUID,
                "flights": flights,
                "flight_type": flight_type,
            })
            cruise.insert(ignore_permissions=True)
            
        # Update cruise information
        cruise.cruise_id = cruise_id
        cruise.display_name = display_name
        cruise.cruise_name = name
        cruise.company_id = company_id
        cruise.ship_id = ship_id
        cruise.cruise_group_id = cruise_group_id
        cruise.adv = adv
        cruise.date_start = date_start
        cruise.date_end = date_end
        cruise.cruise_code = cruise_code
        cruise.original_code = original_code
        cruise.area_code = area_code
        cruise.duration = duration
        cruise.featured = featured
        cruise.active = active
        cruise.immediate_confirm = immediate_confirm
        cruise.uuid = UUID
        cruise.flights = flights
        cruise.flight_type = flight_type
        cruise.save(ignore_permissions=True)

        # Log the successful creation or update
        frappe.log_error(message=f"Successfully created or updated cruise with id: {cruise_id}", title="Cruise Creation/Update")

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating or updating cruise with id {cruise_id}: {str(e)}", title="Cruise Creation/Update Error")



@frappe.whitelist(allow_guest=True, methods=['POST'])
def import_areas_from_external_db(limit=None, time_laps=None):
    try:
        # Initialize the AreaRepository with the external DB connection string
        area_repo = AreaRepository()

        # Fetch all the areas from the external database
        external_areas = area_repo.get_all_areas(limit=limit, time_laps=time_laps)

        # Loop through the external areas and create Area doc in ERPNext
        for external_area in external_areas:
            create_area(external_area)
        
        # Commit the changes
        frappe.db.commit()

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while importing areas: {str(e)}", title="Import Area Error")

def create_area(external_area):
    # Assuming that the external_area object has necessary fields
    area_id = external_area.id
    parent_id = external_area.parent_id
    lft = external_area.lft
    rgt = external_area.rgt
    depth = external_area.depth
    name = external_area.name
    featured = external_area.featured
    UUID = external_area.UUID

    try:
        # Check if the area already exists
        area = frappe.db.exists("Area", {"uuid": UUID})
        if area:
            # Fetch the area document for updating
            area = frappe.get_doc("Area", area)
        else:
            # Create a new area document
            area = frappe.get_doc({
                "doctype": "Area",
                "area_id": area_id,
                "parent_id": parent_id,
                "lft": lft,
                "rgt": rgt,
                "depth": depth,
                "area_name": name,
                "featured": featured,
                "uuid": UUID,
            })
            area.insert(ignore_permissions=True)
            
        # Update area information
        area.area_id = area_id
        area.parent_id = parent_id
        area.lft = lft
        area.rgt = rgt
        area.depth = depth
        area.area_name = name
        area.featured = featured
        area.uuid = UUID
        area.save(ignore_permissions=True)

        # Log the successful creation or update
        frappe.log_error(message=f"Successfully created or updated area with id: {area_id}", title="Area Creation/Update")

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating or updating area with id {area_id}: {str(e)}", title="Area Creation/Update Error")



@frappe.whitelist(allow_guest=True, methods=['POST'])
def import_ports_from_external_db(limit=None, time_laps=None):
    try:
        # Initialize the PortRepository with the external DB connection string
        port_repo = PortRepository()

        # Fetch all the ports from the external database
        external_ports = port_repo.get_all_ports(limit=limit, time_laps=time_laps)

        # Loop through the external ports and create Port doc in ERPNext
        for external_port in external_ports:
            create_port(external_port)
        
        # Commit the changes
        frappe.db.commit()

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while importing ports: {str(e)}", title="Import Port Error")

def create_port(external_port):
    # Assuming that the external_port object has necessary fields
    port_id = external_port.id
    locode = external_port.locode
    name = external_port.name
    valid = external_port.valid
    enable = external_port.enable
    country_id = external_port.country_id
    featured = external_port.featured
    order = external_port.order
    UUID = external_port.UUID

    try:
        # Check if the port already exists
        port = frappe.db.exists("Port", {"uuid": UUID})
        if port:
            # Fetch the port document for updating
            port = frappe.get_doc("Port", port)
        else:
            # Create a new port document
            port = frappe.get_doc({
                "doctype": "Port",
                "port_id": port_id,
                "locode": locode,
                "port_name": name,
                "valid": valid,
                "enable": enable,
                "country_id": country_id,
                "featured": featured,
                "order": order,
                "uuid": UUID,
            })
            port.insert(ignore_permissions=True)
            
        # Update port information
        port.port_id = port_id
        port.locode = locode
        port.port_name = name
        port.valid = valid
        port.enable = enable
        port.country_id = country_id
        port.featured = featured
        port.order = order
        port.uuid = UUID
        port.save(ignore_permissions=True)

        # Log the successful creation or update
        frappe.log_error(message=f"Successfully created or updated port with id: {port_id}", title="Port Creation/Update")

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating or updating port with id {port_id}: {str(e)}", title="Port Creation/Update Error")


@frappe.whitelist(allow_guest=True, methods=['POST'])
def import_orders_from_external_db(limit=None, time_laps=None, filters=None):
    try:
        # Initialize the CruiseRepository with the external DB connection string
        orders_repo = OrderRepository()

        # Fetch all the orders from the external database
        external_orders = orders_repo.get_all_orders(limit=limit, time_laps=time_laps, filters=filters)

        # Loop through the external orders and create Cruise doc in ERPNext
        for external_order in external_orders:
            create_order(external_order)
        
        # Commit the changes
        frappe.db.commit()

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while importing orders: {str(e)}", title="Import Cruise Error")



def create_order(external_order):
    # Assuming that the external_order object has necessary fields
    order_id = external_order.id
    pratica = external_order.pratica
    participants = external_order.participants
    prices = external_order.prices
    category = external_order.category
    flight = external_order.flight
    flight_detail = external_order.flight_detail
    offline = external_order.offline
    is_cc = external_order.is_cc
    closing_details = external_order.closing_details
    cabin = external_order.cabin
    option = external_order.option
    history = external_order.history
    flat = external_order.flat
    admin_id = external_order.admin_id
    cruise_id = external_order.cruise_id
    cabin_type_id = external_order.cabin_type_id
    price_type_id = external_order.price_type_id
    payment_rule_id = external_order.payment_rule_id
    membership_id = external_order.membership_id
    pax_type_id = external_order.pax_type_id
    quote_id = external_order.quote_id
    last_price_update = external_order.last_price_update
    UUID = external_order.UUID
    status = external_order.status
    cruise_user_id =  external_order.user_id


    # Get the Customer's email from Customer.cruise_user_id=cruise_user_id 
    customer_email_id = frappe.db.get_value("Customer", {"cruise_user_id": cruise_user_id} ,'email_id')
    
    if not customer_email_id:
        # Log the error and return
        frappe.log_error(message=f"Customer with cruise_user_id {cruise_user_id} does not exist", title="Customer Not Found")
        return

    user = frappe.get_doc("User", {"email": customer_email_id})

    if not user:
        # Log the error and return
        frappe.log_error(message=f"User with email {customer_email_id} does not exist", title="User Not Found")
        return
    
    cruise = frappe.get_doc("Cruise", {"cruise_id": cruise_id})

    if not cruise:
        # Log the error and return
        frappe.log_error(message=f"Cruise with id {cruise_id} does not exist", title="Cruise Not Found")
        return
    
    try:
        # Check if the order already exists
        order = frappe.db.exists("Cruise Order", {"order_id": order_id})
        if order:
            # Fetch the order document for updating
            order = frappe.get_doc("Cruise Order", order)
        else:
            # Create a new order document
            order = frappe.get_doc({
                "doctype": "Cruise Order",
                "order_id": order_id,
                "pratica": pratica,
                "participants": participants,
                "prices": prices,
                "category": category,
                "flight": flight,
                "flight_detail": flight_detail,
                "offline": offline,
                "is_cc": is_cc,
                "closing_details": closing_details,
                "cabin": cabin,
                "option": option,
                "history": history,
                "flat": flat,
                "user": user,
                "cruise": cruise,
                "cabin_type_id": cabin_type_id,
                "price_type_id": price_type_id,
                "payment_rule_id": payment_rule_id,
                "membership_id": membership_id,
                "pax_type_id": pax_type_id,
                "quote_id": quote_id,
                "last_price_update": last_price_update,
                "uuid": UUID,
                "order_status": status
            })
            order.insert(ignore_permissions=True)
            
        # Update order information
        order.order_id = order_id
        order.pratica = pratica
        order.participants = participants
        order.prices = prices
        order.category = category
        order.flight = flight
        order.flight_detail = flight_detail
        order.offline = offline
        order.is_cc = is_cc
        order.closing_details = closing_details
        order.cabin = cabin
        order.option = option
        order.history = history
        order.flat = flat
        order.user = user
        order.cruise = cruise
        order.cabin_type_id = cabin_type_id
        order.price_type_id = price_type_id
        order.payment_rule_id = payment_rule_id
        order.membership_id = membership_id
        order.pax_type_id = pax_type_id
        order.quote_id = quote_id
        order.last_price_update = last_price_update
        order.uuid = UUID
        order.order_status = status
        order.save(ignore_permissions=True)

        #add participants
        add_cruise_participants(order, participants)

        add_cruise_categories(order, category)

        # Log the successful creation or update
        frappe.log_error(message=f"Successfully created or updated order with id: {order_id}", title="Cruise Order Creation/Update")

        

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating or updating order with id {order_id}: {str(e)}", title="Cruise Order  Creation/Update Error")

def add_cruise_participants(order, participants):
    """
    Function to deserialize and add participants to the cruise order.
    
    Args:
    order (frappe.model.document.Document): The Cruise Order document.
    participants (str): Serialized participants data.
    """
    # Deserialize the participants information
    participants = phpserialize.loads(participants.encode('utf-8'), decode_strings=True)

    # For each participant in the deserialized list, update or create a Cruise Participant document
    for participant in participants.values():
        try:
            # Convert 'birth' from 'DD/MM/YYYY' to 'YYYY-MM-DD'
            birth = datetime.strptime(participant['birth'], '%d/%m/%Y').strftime('%Y-%m-%d')
            
            print(f"Processing participant: {participant}")  # Print participant data

            # Check if the participant already exists
            existing_participant = None
            for p in order.get('cruise_participants'):
                if p.first_name == participant['name'] and p.surname == participant['surname'] and p.age == int(participant['age']):
                    existing_participant = p
                    break

            if existing_participant is not None:
                # Update the existing participant
                existing_participant.update({
                    "nationality": participant['nationality'],
                    "birth": birth,
                    "type": participant['type'],
                })
            else:
                # Add a new participant
                order.append('cruise_participants', {
                    "first_name": participant['name'],   # Assuming 'name' is the correct key in your participant data
                    "surname": participant['surname'],
                    "age": participant['age'],
                    "nationality": participant['nationality'],
                    "birth": birth,
                    "type": participant['type'],
                })

        except Exception as e:
            # Log the error
            frappe.log_error(message=f"An error occurred while creating/updating a participant: {str(e)}", title="Cruise Participant Creation/Update Error")

    # Save the order with the updated participants
    order.save(ignore_permissions=True)
    # Commit the transaction
    frappe.db.commit()


def add_cruise_categories(order, categories):
    # Deserialize the categories information
    categories = phpserialize.loads(categories.encode('utf-8'), decode_strings=True)
    try:
        print(f"Processing categories: {categories}")
        print(f"Processing categories: {categories['CabinNo']}")
        print(f"Processing categories: {categories['DeckCode']}")
        print(f"Processing categories: {categories['DeckName']}")
        order.append('cruise_categories', {
            "cabin_no": categories['CabinNo'],   # Assuming 'name' is the correct key in your category data
            "deck_code": categories['DeckCode'],
            "deck_name": categories['DeckName'],
            "physically_challenged": True,
            "bed_arrangement": categories['BedArrangement'],
            "ship_location_description": categories['ShipLocationDesc'],
            "obview": True,
        })

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating/updating a Category: {str(e)}", title="Cruise Category Creation/Update Error")

    # Save the order with the updated categories
    order.save(ignore_permissions=True)
    # Commit the transaction
    frappe.db.commit()
