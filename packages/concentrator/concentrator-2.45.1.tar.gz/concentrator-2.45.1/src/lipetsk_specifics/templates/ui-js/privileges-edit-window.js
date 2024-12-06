{% block content %}
{% comment %}
/**
 * Шаблон частично зависит от шаблона (необходим для корректной работы окна)
 * kinder/plugins/privilege_attributes/templates/ui-js/
 * privileges-edit-window-privilege-attributes.js.
 */
{% endcomment %}

var privilegeConfirmationURL = '{{ component.privilege_confirmation_url }}',
    privilegeConfirmationFlag = false,
    privilegeField = Ext.getCmp(
        '{{ component.field__privilege_id.client_id }}'),
    ownerField = Ext.getCmp(
        '{{ component.privilege_owner.client_id }}'),
    confirmPrivilegeButton = Ext.getCmp(
        '{{ component.confirm_privilege_button.client_id }}'),
    privilegeReportTypeFields = Ext.util.JSON.decode(
        '{{ component.privilege_report_type_fields|safe }}'),
    dismissalDate = Ext.getCmp(
        '{{ component.field__dismissal_date.client_id }}'),
    report_type = parseInt('{{ component.privilege_report_type }}');

win.actionContextJson.privilege_confirmation = false;

dismissalDate.on('show', function (cmp) {
   // {# Хак отображения кнопки выбора текущей даты, после показа компонента #}
   cmp.setWidth(cmp.getWidth() - 18);
});

//{# Отправление запроса, открытие окна с определенными параметрами #}
function openWindow(url, params, close){
    Ext.applyIf(params, win.actionContextJson);

    Ext.Ajax.request({
        url: url,
        method: 'POST',
        params: params,
        success: function (res, opt) {
            smart_eval(res.responseText);
            if (close) {
                win.close();
            }
        },
        failure: function (res, opt) {
            uiAjaxFailMessage();
        }
    });
}

//{# Показ определенных полей в зависимости от типа отчета для льготы #}
function showControlsByReportType(report_type) {
    for (var i in privilegeReportTypeFields) {
        Ext.each(privilegeReportTypeFields[i], function (item) {
            Ext.getCmp(item).hide();
        })
    }

    if (report_type) {
        Ext.each(privilegeReportTypeFields[report_type], function (item) {
            Ext.getCmp(item).show();
        });
    }
}

showControlsByReportType(report_type);
//{# При изменении льготы включается показ определенных полей #}
privilegeField.on('change', function (cmp, value) {
    if (value) {
        Ext.Ajax.request({
            params: {'privilege_id': value},
            url: '{{ component.get_report_type_url }}',
            success: function (res, opt) {
                var obj = Ext.util.JSON.decode(res.responseText);
                showControlsByReportType(obj.report_type);
            },
            failure: uiAjaxFailMessage
        });
    } else {
        showControlsByReportType();
    }
});

//{# Обработчик сохранения льготы, иногда открывает доп.окно #}
function afterSubmitForm(win, form, action){
    closeWindow = ! privilegeConfirmationFlag;

    if (privilegeConfirmationFlag) {
        privilegeConfirmationFlag = false;
        openWindow(
            privilegeConfirmationURL,
            {'parent_window_id': win.id},
            false
        );
    }

    return closeWindow;
}

//{# Обработчик нажатия на кнопку подтверждения льготы #}
function privilegeConfirmation(){
    form = win.getForm()

    if (form.isDirty()) {
        Ext.Msg.show({
            title: 'Внимание',
            msg: String.format('Для подтверждения льготы необходимо сохранить ' +
                               'внесенные данные.<br/> Cделать это сейчас?'),
            icon: Ext.Msg.QUESTION,
            buttons: {
                yes : 'Сохранить и продолжить',
                no : 'Отменить и продолжить редактирование льготы'
            },
            modal: true,
            fn: function(btn, text, opt){
                if (btn === 'yes') {
                    privilegeConfirmationPreSave();
                }
            }
        });
    } else {
        privilegeConfirmationPreSave();
    }
}

//{# Сохранение подтверждения льготы  #}
function privilegeConfirmationPreSave(btn, text, opt){
    privilegeConfirmationFlag = true;
    win.actionContextJson.privilege_confirmation = true;

    win.submitForm();
}

//{# Включение/выключение доступа к кнопке подтверждения льготы #}
function enableConfirmPrivilegeButton(){
    if (ownerField.getValue() && is_created_child()) {
        confirmPrivilegeButton.enable();
    } else {
        confirmPrivilegeButton.disable();
    }
}

enableConfirmPrivilegeButton();
ownerField.on('select', enableConfirmPrivilegeButton);
win.on('aftersubmit', afterSubmitForm);

{% endblock %}
