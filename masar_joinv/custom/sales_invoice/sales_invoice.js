frappe.ui.form.on("Sales Invoice",  {
   on_submit: function(frm){

        frappe.call({
                method:"masar_joinv.api.general_si",
                args:{
                        name :frm.doc.name,
                        is_return : frm.doc.is_return , 
                        posting_date :frm.doc.posting_date , 
                        is_pos :frm.doc.is_pos
                },
                callback: function(r){
                        frappe.msgprint(r.message); 
                }
        });
   }
});
      