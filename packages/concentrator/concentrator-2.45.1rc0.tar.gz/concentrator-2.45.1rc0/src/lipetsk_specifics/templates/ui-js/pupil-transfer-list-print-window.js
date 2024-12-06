{% extends 'pupil-transfer-list-window.js' %}

{% block ext_content %}
function print_transfer_info(){
    var grid = Ext.getCmp('{{ component.grid.client_id }}'),
        select_item = grid.getSelectionModel().getSelected();

    if (select_item){
        Ext.Ajax.request({
            url: '{{ component.print_url }}',
            params: {'transfer_id': select_item.id},
            success: function (response) {
                smart_eval(response.responseText);
            },
            failure: function () {
                uiAjaxFailMessage.apply(this, arguments);
            }
        });
    } else {
        Ext.Msg.alert('Внимание', 'Необходимо выбрать элемент из списка');
    };
}
{% endblock %}