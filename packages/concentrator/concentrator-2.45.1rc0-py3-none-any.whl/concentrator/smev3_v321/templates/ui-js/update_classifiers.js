var actionType = Ext.getCmp('{{ component.action_type.client_id }}'),
    classifier= Ext.getCmp('{{ component.classifier.client_id }}');


function setTasks() {
    /**
     * Отправляет выбранные справочники в ЕСНСИ, если форма прошла валидацию
     */
    var form = win.getForm();
    var invalidFields = [];
    form.items.each(function(f){
        if (!f.validate()){
            invalidFields.push('<br>- ' + f.fieldLabel);
        }
    });

    if (invalidFields.length){
        Ext.Msg.show({
            title: 'Проверка формы',
            msg: 'На форме имеются некорректно заполненные поля:' + invalidFields.toString() + '.',
            buttons: Ext.Msg.OK,
            icon: Ext.Msg.WARNING
        });
        return;
    }
    params = {action_type: actionType.getValue(), classifier: classifier.getValue()};
    var mask = new Ext.LoadMask(win.getEl());
    mask.show();
    Ext.Ajax.request({
        url: "{{ component.set_task_url }}",
        params: params,
        success: function(response) {
            Ext.Msg.show({
                title: 'Внимание',
                msg: 'Отправка справочников ЕСНСИ началась в фоновом режиме',
                buttons: Ext.Msg.OK,
                icon: Ext.Msg.WARNING,
                fn: function(){
                    mask.hide();
                    win.close(true);
                }
            });
        },
        failure: function(response, opts) {
            mask.hide();
            uiAjaxFailMessage();
        }
    });
}