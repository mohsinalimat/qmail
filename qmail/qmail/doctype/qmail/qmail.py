# Copyright (c) 2021, Rutwik Hiwalkar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.desk.form.load import get_attachments
import requests
import json


class QMail(Document):
	def on_submit(self):
		"""
		send data
		"""
		data = {}

		team = frappe.db.get_single_value("QMail Settings", "team")
		data["team"] = team
		data["site"] = frappe.local.site
		data["sender"] = self.sender
		data["recipient"] = [r.recipient for r in self.recipient]
		data["subject"] = self.subject
		data["html"] = self.html
		data["content"] = self.html_message if self.html else self.message
		files = self.attachments()

		resp = requests.post(
			"https://staging.frappe.cloud/api/method/press.api.email.send_mail",
			data={"data": json.dumps(data)},
			files=files,
		)

		if json.loads(resp.text)["message"] == "Error":
			frappe.throw("Plan not available or expired.")

	def attachments(self):
		"""
		prepare attachments
		"""
		files = get_attachments("QMail", self.name)
		attachments = []

		for file in files:
			attachments.append((file["file_name"], self.read_file(file["file_name"])))

		return attachments

	def read_file(self, file_name):
		file_path = frappe.get_site_path("public", "files", file_name)
		with open(file_path, "rb") as f:
			content = f.read()

		return content
