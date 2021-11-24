frappe.listview_settings['QMail'] = {
		get_indicator(doc) {
        if (doc.status == 'draft') {
            return [__('draft'), 'grey']
        } else if (doc.status == 'delivered') {
            return [__('delivered'), 'green']
        } else if (doc.status == 'failed') {
            return [__('failed'), 'red']
				} else if (doc.status == 'pending') {
						return [__('pending'), 'orange']
				}
    }
}