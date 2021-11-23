# Copyright (c) 2021, Rutwik Hiwalkar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from qmail.qmail.doctype.qmail.qmail import send
from datetime import date
import calendar
from jinja2 import Template
import jinja2schema


class QMailScheduleRule(Document):
	pass


@frappe.whitelist()
def check_intervals():
	# Daily filter
	daily = {"interval": "Daily", "enabled": 1}
	rules = get_rules(daily)
	check_target_doctype_and_send(rules)

	# Weekly filter
	today = date.today()
	weekly = {
		"interval": "Weekly",
		"weekday": calendar.day_name[today.weekday()],
		"enabled": 1,
	}
	rules = get_rules(weekly)

	# Monthly filter
	monthly = {"interval": "Monthly", "day_of_month": today.strftime("%d"), "enabled": 1}
	rules = get_rules(monthly)

	return


def get_rules(filters):
	rules = frappe.get_all(
		"QMail Schedule Rule",
		fields=[
			"interval",
			"repeat",
			"day_of_month",
			"doc",
			"docfield",
			"value",
			"sender",
			"subject",
			"recipient",
			"message",
			"attach_pdf",
		],
		filters=filters,
	)

	return rules


def check_target_doctype_and_send(rules):
	for rule in rules:
		fields = list(jinja2schema.infer(rule.message).keys())
		fields.append("name")

		docs = frappe.get_all(
			rule.doc, fields=fields, filters={rule.docfield.lower(): [rule.operator, rule.value]}
		)

		if docs:
			message = get_email_from_template(rule.message, docs[0])
			recipient = frappe.get_value(rule.doc, docs[0]["name"], rule.recipient)

			# create new qmail object
			qmail = frappe.get_doc(
				{
					"doctype": "QMail",
					"sender": rule.sender,
					"recipient": [{"recipient": recipient}],
					"subject": rule.subject,
					"message": message,
				}
			).insert()

			send(qmail.name)
			# attach pdf if 1


def get_email_from_template(jinja, args):
	message = Template(jinja).render(args)

	return message


@frappe.whitelist()
def get_fields(doctype):
	doc = frappe.get_doc("DocType", doctype)
	fields = list(filter(None, [field.label for field in doc.fields]))

	return fields
