var fieldNumber = Ext.getCmp('{{ component.field__number.client_id }}'),
    fieldDateIssue = Ext.getCmp('{{ component.field__date_issue.client_id }}'),
    fieldIssuedBy = Ext.getCmp('{{ component.field__issued_by.client_id }}'),
    delegateTypeFld = Ext.getCmp('{{ component.field__type.client_id }}'),
    lexDelegateType = parseInt("{{ component.LEX_TYPE }}"),
    fieldsArray = [fieldNumber, fieldDateIssue, fieldIssuedBy];

delegateTypeFld.on('change', checkFieldsAllowBlank);

function checkFieldsAllowBlank(cmp, value) {
    var allowBlank = !(parseInt(value) === lexDelegateType);

    fieldsArray.forEach(function (field) {
        if (field) {
            field.allowBlank = allowBlank;
            field.validate();
        }
    });
}

checkFieldsAllowBlank(delegateTypeFld, delegateTypeFld.getValue());
