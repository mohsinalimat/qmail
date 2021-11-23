// Copyright (c) 2021, Rutwik Hiwalkar and contributors
// For license information, please see license.txt

frappe.ui.form.on('QMail Schedule Rule', {
	refresh: function(frm) {
		frappe.call({
			method: 'qmail.qmail.doctype.qmail_schedule_rule.qmail_schedule_rule.check_intervals'
		})
		if (frm.doc.doc) {
			get_fields(frm)
		}
	},
	doc: function(frm) {
		get_fields(frm)
	},

});

function get_fields(frm) {
	frappe.call({
		method: 'qmail.qmail.doctype.qmail_schedule_rule.qmail_schedule_rule.get_fields',
		args: {
			doctype: frm.doc.doc
		},
		callback: (resp) => {
			frappe.meta.get_docfield('QMail Schedule Rule', 'docfield', frm.doc.name).options = resp.message;
			frm.refresh_field('docfield')
		}
	})
}

