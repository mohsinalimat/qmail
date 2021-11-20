# Copyright (c) 2021, Rutwik Hiwalkar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.desk.form.load import get_attachments
import requests
import json


class QMail(Document):
	pass


@frappe.whitelist(allow_guest=True)
def send(docname):
	"""
	send data
	"""
	doc = frappe.get_doc("QMail", docname)

	data = {}

	team = frappe.db.get_single_value("QMail Settings", "team")
	data["team"] = team
	data["site"] = frappe.local.site
	data["sender"] = doc.sender
	data["recipient"] = [r.recipient for r in doc.recipient]
	data["cc"] = [c.recipient for c in doc.cc]
	data["bcc"] = [b.recipient for b in doc.bcc]
	data["subject"] = doc.subject
	data["html"] = doc.html
	data["content"] = doc.html_message if doc.html else doc.message
	files = attachments(docname)

	resp = requests.post(
		"https://staging.frappe.cloud/api/method/press.api.email.send_mail",
		data={"data": json.dumps(data)},
		files=files,
	)

	if json.loads(resp.text)["message"] == "Error":
		frappe.throw("Plan not available or expired.")

	doc.status = "pending"
	doc.save()
	frappe.db.commit()

def attachments(docname):
	"""
	prepare attachments
	"""
	files = get_attachments("QMail", docname.name)
	attachments = []

	for file in files:
		perm_level = 'private' if file['is_private'] == 1 else 'public'
		attachments.append((file["file_name"], read_file(perm_level, file["file_name"])))

	return attachments

def read_file(perm_level, file_name):
	file_path = frappe.get_site_path(perm_level, "files", file_name)
	with open(file_path, "rb") as f:
		content = f.read()

	return content


@frappe.whitelist(allow_guest=True)
def change_message_status(**data):
	doc = frappe.get_doc("QMail", data["message_id"])
	doc.status = data["status"]
	doc.save()
	frappe.db.commit()

	return "Success"