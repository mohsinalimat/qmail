// Copyright (c) 2021, Rutwik Hiwalkar and contributors
// For license information, please see license.txt

frappe.ui.form.on("QMail Settings", {
  refresh: function (frm) {
    console.log(frm.doc.team);
    [
      [__("Mail5"), true],
      [__("Free100"), true],
      [__("Novice"), true],
      [__("Amateur"), true],
      [__("Pro"), true],
    ].forEach(([label, show]) => {
      if (show)
        frm.add_custom_button(
          label,
          () => {
            frappe
              .call({
                method: "qmail.qmail.doctype.qmail_settings.qmail_settings.change_plan",
                args: {
                  team: frm.doc.team,
                  site: frm.doc.site,
                  plan: label
                },
              })
              .then((r) => {
                if (r.message) {
                  frappe.msgprint("Plan changed successfully.");
                  // update the plan fields
                }

                frm.refresh();
              });
          },
          __("Change Plan")
        );
    });
  },
});
