
var requestField = Ext.getCmp('{{ component.field__request.client_id }}');

requestField.fileInput.dom.disabled = true;
requestField.buttonFile.setDisabled(true);
requestField.buttonClear.setDisabled(true);
requestField.buttonFile.hide();
requestField.buttonClear.hide();
