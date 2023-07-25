import phpserialize
import frappe
import json
from datetime import datetime



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
        # Check if the category already exists
        existing_category = None
        for c in order.get('cruise_categories'):
                if c.cabin_no == categories['CabinNo']:
                    existing_category = c
                    break
        
        if existing_category is not None:
            # Update the existing category
            existing_category.update({
                "cabin_no": categories['CabinNo'],   # Assuming 'name' is the correct key in your category data
                "deck_code": categories['DeckCode'],
                "deck_name": categories['DeckName'],
                "physically_challenged": True,
                "bed_arrangement": categories['BedArrangement'],
                "ship_location_description": categories['ShipLocationDesc'],
                "obview": True,
            })
        else:
            # Add a new participant
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

def add_cruise_closing_details(order, details):
    # Deserialize the details information
    details = phpserialize.loads(details.encode('utf-8'), decode_strings=True)
    print(f"Processing details: {details}")  # Print Processing details data

    try:
        # Check if the detail already exists
        existing_detail = None
        for c in order.get('cruise_closing_details'):
                if c.number_of_adults == details['num_adult']:
                    existing_detail = c
                    break
        
        # Preprocess the complex dictionary fields
        details['cruise_adults'] = json.dumps(details['cruise_adults'])
        details['cruise_childs'] = json.dumps(details['cruise_childs'])
        details['tax'] = json.dumps(details['tax'])
        details['insurance'] = json.dumps(details['insurance'])
        details['benefits'] = json.dumps(details['benefits'])

        if existing_detail is not None:
            print(f"existing_details: {existing_detail}")
            # Update the existing detail
            existing_detail.update({
                "number_of_adults": details['num_adult'],   # Assuming 'num_adult' is the correct key in your detail data
                "number_of_children": details['num_child'],
                "cruise_adults": details['cruise_adults'],
                "cruise_children": details['cruise_childs'],
                "tax": details['tax'],
                "insurance": details['insurance'],
                "total": details['total'],
                "discount": details['discount'],
                "benefits": details['benefits'],
                "grand_total": details['grand_total'],
            })
        else:
            # Add a new participant
            order.append('cruise_closing_details', {
                "number_of_adults": details['num_adult'],   # Assuming 'num_adult' is the correct key in your detail data
                "number_of_children": details['num_child'],
                "cruise_adults": details['cruise_adults'],
                "cruise_children": details['cruise_childs'],
                "tax": details['tax'],
                "insurance": details['insurance'],
                "total": details['total'],
                "discount": details['discount'],
                "benefits": details['benefits'],
                "grand_total": details['grand_total'],
            })

    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating/updating a Closing Detail: {str(e)}", title="Cruise Closing Detail Creation/Update Error")

    # Save the order with the updated details
    order.save(ignore_permissions=True)
    # Commit the transaction
    frappe.db.commit()

def add_cruise_histories(order, histories):
    # Deserialize the histories information
    histories = phpserialize.loads(histories.encode('utf-8'), decode_strings=True)
    print(f"Processing histories: {histories}")  # Print Processing details data

    # For each history in the deserialized list, update or create a Cruise History document
    for history in histories.values():
        # cruise_history_id_seq = history['msg']
        try:
            print(f"Processing history: {history}")  # Print history data

            # Check if the history already exists
            existing_history = None
            for h in order.get('cruise_histories'):
                if h.date == convert_date(history['date']) and h.message == history['msg']:
                    existing_history = h
                    break

            if existing_history is not None:
                # Update the existing history
                existing_history.update({
                    "date": convert_date(history['date']),
                    "message": history['msg'],
                })
            else:
                # Add a new history
                order.append('cruise_histories', {
                    "date": convert_date(history['date']),
                    "message": history['msg'],
                })
            print(f"Result history: {convert_date(history['date'])}")
        except Exception as e:
            # Log the error
            frappe.log_error(message=f"An error occurred while creating/updating a History: {str(e)}", title="Cruise History Creation/Update Error")

    # Save the order with the updated histories
    order.save(ignore_permissions=True)
    # Commit the transaction
    frappe.db.commit()


def add_cruise_flats(order, flats):
    # Deserialize the flats information
    flats = phpserialize.loads(flats.encode('utf-8'), decode_strings=True)
    print(f"Processing flats: {flats}")  # Print Processing details data

    # For each history in the deserialized list, update or create a Cruise History document
    try:
        # Check if the flat already exists
        existing_flat = None
        for f in order.get('cruise_flats'):
            if f.cruise_id == flats['uuid_crociera']:
                existing_flat = f
                break

        if existing_flat is not None:
            # Update the existing flat
            existing_flat.update({
                "cruise_name": flats['nome_crociera'],
                "cruise_id": flats['uuid_crociera'],
                "status": flats['stato'],
                "departure_date": convert_date(flats['data_partenza']),
                "return_date": convert_date(flats['data_ritorno']),
                "departure_port": flats['porto_partenza'],
                "arrival_port": flats['porto_arrivo'],
                "issue_date": convert_date(flats['emissione']),
                "requestor": flats['richiedente'],
                "phone": flats['telefono'],
                "email": flats['email'],
                "quote_code": flats['cod_preventivo'],
                "booking_code": flats['cod_prenotazione'],
                "consultant": flats['consulente'],
                "cruise_company": flats['compagnia'],
                "ship_name": flats['nave'],
                "cabin_booking": flats['prenotazione_cabina'],
                "cabin_type": flats['tipo_cabina'],
                "pricing_list": flats['listino'],
                "pricing_includes": flats['listino_comprende'],
                "pricing_does_not_include": flats['listino_non_comprende'],
                "participants": json.dumps(flats['partecipanti']),
                "prices": json.dumps(flats['prezzi']),
                "deposits": json.dumps(flats['acconti']),
                "cabin_number": flats['cabinNumber'],
                "booking_number": flats['bookingNumber'],
            })
        else:
            # Add a new flat
            order.append('cruise_flats', {
                "cruise_name": flats['nome_crociera'],
                "cruise_id": flats['uuid_crociera'],
                "status": flats['stato'],
                "departure_date": convert_date(flats['data_partenza']),
                "return_date": convert_date(flats['data_ritorno']),
                "departure_port": flats['porto_partenza'],
                "arrival_port": flats['porto_arrivo'],
                "issue_date": convert_date(flats['emissione']),
                "requestor": flats['richiedente'],
                "phone": flats['telefono'],
                "email": flats['email'],
                "quote_code": flats['cod_preventivo'],
                "booking_code": flats['cod_prenotazione'],
                "consultant": flats['consulente'],
                "cruise_company": flats['compagnia'],
                "ship_name": flats['nave'],
                "cabin_booking": flats['prenotazione_cabina'],
                "cabin_type": flats['tipo_cabina'],
                "pricing_list": flats['listino'],
                "pricing_includes": flats['listino_comprende'],
                "pricing_does_not_include": flats['listino_non_comprende'],
                "participants": json.dumps(flats['partecipanti']),
                "prices": json.dumps(flats['prezzi']),
                "deposits": json.dumps(flats['acconti']),
                "cabin_number": flats['cabinNumber'],
                "booking_number": flats['bookingNumber'],
            })
    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating/updating a flat: {str(e)}", title="Cruise flat Creation/Update Error")

    # Save the order with the updated flats
    order.save(ignore_permissions=True)
    # Commit the transaction
    frappe.db.commit()

def add_cruise_options(order, options):
    # Deserialize the options information
    options = phpserialize.loads(options.encode('utf-8'), decode_strings=True)
    print(f"Processing options: {options}")  # Print Processing details data

    # For each history in the deserialized list, update or create a Cruise History document
    try:
        # Check if the option already exists
        existing_option = None
        for o in order.get('cruise_options'):
            if o.session_id == options['SessionInfo']['SessionID']:
                existing_option = o
                break

        if existing_option is not None:
            # Update the existing option
            existing_option.update({
                "session_id": options['SessionInfo']['SessionID'],
                "session_info": json.dumps(options['SessionInfo']),
                "booking_context": json.dumps(options['BookingContext']),
                "advisory_info": json.dumps(options['AdvisoryInfo']),
                "booking_info": json.dumps(options['BookingInfo']),
            })
        else:
            # Add a new option
            order.append('cruise_options', {
                "session_id": options['SessionInfo']['SessionID'],
                "session_info": json.dumps(options['SessionInfo']),
                "booking_context": json.dumps(options['BookingContext']),
                "advisory_info": json.dumps(options['AdvisoryInfo']),
                "booking_info": json.dumps(options['BookingInfo']),
            })
    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating/updating a option: {str(e)}", title="Cruise option Creation/Update Error")

    # Save the order with the updated options
    order.save(ignore_permissions=True)
    # Commit the transaction
    frappe.db.commit()

def add_cruise_prices(order, prices):
    # Deserialize the prices information
    prices = phpserialize.loads(prices.encode('utf-8'), decode_strings=True)
    print(f"Processing prices: {prices}")  # Print Processing details data

    # For each history in the deserialized list, update or create a Cruise History document
    try:
        # Check if the price already exists
        existing_price = None
        for o in order.get('cruise_prices'):
            if o.promotion_code == prices['promotionCode']:
                existing_price = o
                break

        if existing_price is not None:
            # Update the existing price
            existing_price.update({
                "promotion_code": prices['promotionCode'],
                "cabin_details": json.dumps(prices['cabin']),
                "flight_details": json.dumps(prices['flight']),
            })
        else:
            # Add a new price
            order.append('cruise_prices', {
                "promotion_code": prices['promotionCode'],
                "cabin_details": json.dumps(prices['cabin']),
                "flight_details": json.dumps(prices['flight']),
            })
    except Exception as e:
        # Log the error
        frappe.log_error(message=f"An error occurred while creating/updating a option: {str(e)}", title="Cruise option Creation/Update Error")

    # Save the order with the updated options
    order.save(ignore_permissions=True)
    # Commit the transaction
    frappe.db.commit()

def convert_date(date):
    return datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')

