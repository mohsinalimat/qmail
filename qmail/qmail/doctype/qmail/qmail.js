// Copyright (c) 2021, Rutwik Hiwalkar and contributors
// For license information, please see license.txt

frappe.ui.form.on('QMail', {
	refresh: function(frm) {
		if (frm.doc.status === 'draft' || frm.doc.status === 'failure') {
			frm.add_custom_button(__('Send'), () => {
				frappe.call({
					method: 'qmail.qmail.doctype.qmail.qmail.send',
					args: {
						docname: frm.doc.name
					},
					callback: () => {
						frm.refresh()
					}
				})
			})
		}
		frm.refresh()
	}
});
