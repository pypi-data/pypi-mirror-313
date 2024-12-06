{% load import_objects %}

{% block content_extension %}

{# Открывает окно для настройки создания отчета о запросе в не электронные сервисы #}
function passingSmevRequest(){
    var sm = grid.getSelectionModel();
    var mask = new Ext.LoadMask(win.getEl());

    if (!sm.hasSelection()) {
        showWarning('Элемент не выбран', 'Внимание');
        return false;
    }

    mask.show();
    Ext.Ajax.request({
        url: '{% action_url "lipetsk_specifics.actions.PassingSmevPack" "request_action" %}',
        params: {'declaration_ids': Ext.pluck(sm.getSelections(), 'id').join(',')},
        success: function (response) {
            mask.hide();
            var result = Ext.decode(response.responseText);
            if (!result.success) {
                showWarning(result.message, 'Внимание');
            } else if(result.success && result.message) {
                showMessage(result.message);
            }
        },
        failure: function (response, options) {
            mask.hide();
            uiAjaxFailMessage(response, options);
        }
    })
}

{# Открывает окно просмотра истории запросов в не электронные сервисы #}
function passingSmevHistory(){
    Ext.Ajax.request({
        url: '{% action_url "lipetsk_specifics.actions.PassingSmevPack" "list_window_action" %}',
        success: function (response, options) {
            smart_eval(response.responseText);
        },
        failure: function (response, options) {
            uiAjaxFailMessage(response, options);
        }
    })
}

{% endblock %}