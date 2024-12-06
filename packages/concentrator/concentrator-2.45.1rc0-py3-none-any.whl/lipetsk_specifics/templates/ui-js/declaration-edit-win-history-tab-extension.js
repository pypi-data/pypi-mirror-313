
{% extends 'ui-js/declaration-edit-win-history-tab.js' %}

{% block content_extension %}

{% load import_objects %}

{# Показывает окно настройки печати отказа в изменении данных #}
function printRefuseToChangeData(){

    Ext.Ajax.request({
        url: '{% action_url "lipetsk_specifics.actions.DeclLipetskPrintNotificationPack" "refuse_to_change_data_window_action" %}',
        params: objGrid.actionContextJson,
        success: function (response, options) {
            smart_eval(response.responseText);
        },
        failure: function (response, options) {
            uiAjaxFailMessage(response, options);
        }
    })
}


{% endblock %}
