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
    print(f"Processing details: {details}")  # Print participant data

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
