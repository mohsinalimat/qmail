// Copyright (c) 2021, Rutwik Hiwalkar and contributors
// For license information, please see license.txt

frappe.ui.form.on("QMail Settings", {
  refresh: function (frm) {
    [
      [__("Novice"), "build", true],
      [__("Ameateur"), "deploy_to_staging", true],
      [__("Pro"), "promote_to_production", true],
    ].forEach(([label, method, show]) => {
      if (show)
        frm.add_custom_button(
          label,
          () => {
            console.log(method);
          },
          __("Change Plan")
        );
    });
  },
});
