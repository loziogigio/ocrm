# Copyright (c) 2023, Crowdechain S.r.o and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import os
import json


import requests  # To make HTTP requests

class CarbinPricelist(Document):


	DATA_FILE = "data_file.json"

	@staticmethod
	def get_current_data() -> dict[str, dict]:
		"""Read data from disk"""
		if not os.path.exists(CarbinPricelist.DATA_FILE):
				return {}

		with open(CarbinPricelist.DATA_FILE) as f:
				return json.load(f)

	@staticmethod
	def update_data(data: dict[str, dict]) -> None:
		"""Flush updated data to disk"""
		with open(CarbinPricelist.DATA_FILE, "w+") as data_file:
				json.dump(data, data_file)

	def get_price(self, customer, cruise_name):
		# Construct the payload
		data = {
			"customer": customer,
			"cruise_name": cruise_name
		}
		
		# Assuming you have an external service to get the cabin price list
		response = requests.post('https://external-service-url.com/get-price', json=data)

		# Error handling for the request
		response.raise_for_status()

		# Get the price list data
		
		price_list_data = response.json()
 
 
		return price_list_data
	
	def db_insert(self, *args, **kwargs):
		pass

	def load_from_db(self):
		pass

	def db_update(self):
		pass

	@staticmethod
	def get_list(args):
		pass

	@staticmethod
	def get_count(args):
		pass

	@staticmethod
	def get_stats(args):
		pass

