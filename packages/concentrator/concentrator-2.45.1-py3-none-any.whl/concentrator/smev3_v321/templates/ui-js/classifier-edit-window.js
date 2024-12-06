var codeField = Ext.getCmp('{{ component.field__code.client_id }}'),
    uidField = Ext.getCmp('{{ component.field__uid.client_id }}');

codeField.validationEvent = 'change';
uidField.validationEvent = 'change';

function checkFields(){
    if (!uidField.getValue() && !codeField.getValue()){
        codeField.markInvalid();
        uidField.markInvalid();
    } else {
        codeField.clearInvalid();
        uidField.clearInvalid();
    }
}

checkFields();
codeField.on('change', checkFields);
uidField.on('change', checkFields);
codeField.on('blur', checkFields);
uidField.on('blur', checkFields);

function beforeSubmit(submit){
    let invalidNames = [codeField.fieldLabel, uidField.fieldLabel];
    if (!uidField.getValue() && !codeField.getValue()){
        Ext.Msg.show({
            title: 'Проверка формы',
            msg: 'На форме имеются некорректно заполненные поля:<br>- ' +
                invalidNames.join(',<br>- ') + '.',
            buttons: Ext.Msg.OK,
            icon: Ext.Msg.WARNING
        });
        checkFields();
        return false;
    }
}
