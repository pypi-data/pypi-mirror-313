{% block content_extension %}

/*
вспомогательная функция вызова окна
 */

var cntxParams = win.actionContextJson,
    сhangesOpenURL = '{{ component.changes_tab.changes_open_url }}',
    сhangesPrintURL = '{{ component.changes_tab.changes_print_url }}',
    permPrivGridURL = '{{ component.changes_tab.perm_priv_grid_url }}',
    сhangesGrid = Ext.getCmp('{{ component.changes_tab.grid.client_id }}'),
    declarationEditWin = Ext.getCmp('{{ component.client_id }}');

function openWindow(url, params){
    Ext.applyIf(params, cntxParams);
    Ext.Ajax.request({
        url: url,
        method: 'POST',
        params: params,
        success: function (res, opt) {
            var win = smart_eval(res.responseText);
            if (win){
                win.show();
                win.on('close', function (p) {
                    сhangesGrid.store.reload();
                });
            }
        },
        failure: Ext.emptyFn
    });
}
/**
 * применяем изменения в полям формы,
 * для комбобоксов должно придти значения вида:
 * {"children.health_need_id": 16}
 * без setSize, размер схлопывается до 0, причину не удалось выяснить
 * если комбобокс с Ext.data.HttpProxy, то стор принудительно загружаем
 */
declarationEditWin.on('refresh_fields', function(data){
    if (data) {
        this.getForm().items.each(function (f) {
            if (!f.disabled) {
                var name = f.getName();
                //Признак что это combobox
                if (f['clearFilterOnReset'] && name in data) {
                    var store = f.getStore();
                    if (!store.url) return true;
                    store.on('load', function(st, records, options ){
                        f.setValue(data[name]);
                        f.setSize(f.lastSize.width - 1);
                    })
                    store.load();
                }
            }
        })
        this.getForm().setValues(data);
        privGrid.getStore().reload();
        declarationEditWin.on('beforeclose', function(a,b,c){
            /**
             * При подтверждении данных, пришедших с ЕПГУ, данные заявки могут измениться
             * (например: статус, льгота), поэтому достаем и обновляем вручную стор грида реестра.
             */
            var currWin = win;
            while ((currWin.parentWindow !== null) && (currWin.parentWindow !== undefined))
                currWin = currWin.parentWindow;
            if (currWin.refreshGridStore !== undefined)
                currWin.refreshGridStore();
        });
        // Для вкладки "Желаемые организации/Льготы" смотрим, есть ли права на редактирование льготы
        unitTab.on('activate', onPrivilegeGrid);
        /**
         * При подтверждении данных, пришедших с ЕПГУ, данные заявки могут измениться
         * (например: добавлена льгота), поэтому делаем активными данные privGrid в зависимости от прав.
         */
        function onPrivilegeGrid(tab){
        Ext.Ajax.request({
              url: permPrivGridURL,
              method: 'POST',
              params: { 'declaration_id': declarationEditWin.actionContextJson['declaration_id'] },
              success: function (res, opt) {
                  smart_eval(res.responseText);
                  var result = Ext.decode(res.responseText);
                  if (result && result.perm) {
                      privGrid.getTopToolbar().enable();
                      privGrid.getBottomToolbar().enable();
                  }
              },
              failure: function (res, opt) {
                  uiAjaxFailMessage();
              }
          });
        }
        unitGrid.getStore().reload();
        docGrid.getStore().reload();
        delegateGrid.getStore().reload();
        statusGrid.getStore().reload();
    }
});

function openChanges(){
    if (checkSelection("Просмотр")) {
        var selectedRow = сhangesGrid.getSelectionModel().getSelected();

        openWindow(сhangesOpenURL, {'id': selectedRow.id});
    }
}

function printChanges(){
    openWindow(сhangesPrintURL, {'blank': true});
}

function checkSelection(title) {
    title = typeof title == "undefined" ? "Редактирование" : title;
    if (!сhangesGrid.getSelectionModel().hasSelection()) {
        Ext.Msg.show({
            title: title,
            msg: "Элемент не выбран",
            buttons: Ext.Msg.OK,
            icon: Ext.MessageBox.INFO
        });
        return false;
    }
    return true;
}

{% endblock %}
