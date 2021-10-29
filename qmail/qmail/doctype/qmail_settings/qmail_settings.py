# Copyright (c) 2021, Rutwik Hiwalkar and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document

class QMailSettings(Document):
	def validate(self):
		"""
		Testing: if team and site is set create_subscription
		"""
		if self.team and self.site:
			data = {
				'team': self.team,
				'site': self.site,
				'passphrase': self.passphrase
			}

			response = requests.post('https://staging.frappe.cloud/api/method/press.api.email.create_subscription', data=data)

			resp_data = response.json()['message']

			frappe.db.set_value('QMail Settings', 'QMail Settings', {
				'plan_name': resp_data['plan_name'],
				'no_of_emails': resp_data['emails'],
				'price': resp_data['price']
			})

			frappe.db.commit()
