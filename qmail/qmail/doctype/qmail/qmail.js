// Copyright (c) 2021, Rutwik Hiwalkar and contributors
// For license information, please see license.txt

frappe.ui.form.on('QMail', {
	refresh: function(frm) {
		console.log(frm.doc)
		if (frm.doc.status === 'draft' || frm.doc.status === 'failure') {
			frm.add_custom_button(__('Send'), () => {
				frappe.call({
					method: 'qmail.qmail.doctype.qmail.qmail.send_mail',
					args: {
						docname: frm.doc.name
					},
					callback: () => {
						frm.refresh()
					}
				})
			})
		}
	}
});
