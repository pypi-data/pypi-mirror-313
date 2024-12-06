{% block content_extension %}

var cntxParams = win.actionContextJson,
    changesApplyURL = "{{ component.changes_apply_url }}",
    changesRejectURL = "{{ component.changes_reject_url }}",
    changesPrintURL = "{{ component.changes_print_url }}",
    checkChangesApplyURL = "{{ component.check_changes_apply_url }}",
    commentaryMaxLength = "{{ component.comment_max_length }}",
    commentField = Ext.getCmp("{{ component.comment_field.client_id }}");

win.actionContextJson["grid_id"] = "{{ component.grid_id }}";

var mask = new Ext.LoadMask(win.getEl());

if (commentField) {
    commentField.getEl().dom.placeholder = 'Введите комментарий к изменениям';
}


function openWindow(url, params, close){
    Ext.applyIf(params, cntxParams);

    Ext.Ajax.request({
        url: url,
        method: "POST",
        params: params,
        success: function (res, opt) {
            mask.hide();
            smart_eval(res.responseText);
            var result = Ext.decode(res.responseText);
            if (!result.success){
                Ext.Msg.alert("Ошибка", result.message);
            }
            else {
                win.parentWindow.fireEvent("refresh_fields", result["updated_fields"]);
                win.fireEvent("closed_ok");
                win.close();
            }
        },
        failure: function (res, opt) {
            uiAjaxFailMessage();
            mask.hide();
        }
    });
}

function askComment(title, message, handler){
    Ext.Msg.show({
        title: title,
        msg: message,
        width: 400,
        buttons: Ext.MessageBox.OKCANCEL,
        multiline: 100,
        defaultTextHeight: 100,
        value: "",
        fn: function(btn, text, obj){
            if (btn === "ok") {
                if (text.length > commentaryMaxLength) {
                    var message = "Убедитесь, что комментарий содержит не более "
                        + commentaryMaxLength + " символов.";
                    Ext.Msg.alert('Ошибка', message);
                } else {
                    handler(text);
                }
            }
        },
        icon: Ext.MessageBox.QUESTION
    });
}

function applyChangesSubmit(comment){

    mask.show();

    Ext.Ajax.request({
        url: checkChangesApplyURL,
        method: "POST",
        params: cntxParams,
        success: function (res, opt) {
            smart_eval(res.responseText);
            var result = Ext.decode(res.responseText);
            if (!result.success){
                openWindow(changesApplyURL, {"comment": comment}, true);
            }
            else {
                mask.hide();
                showChangeDeclarationInfo("Внимание", result.message, {"comment": comment})
            }
        },
        failure: function (res, opt) {
            mask.hide();
            uiAjaxFailMessage();
        }
    });
}

function showChangeDeclarationInfo(title, message, params) {

    Ext.Msg.show({
        title: title,
        msg: message,
        width: 400,
        buttons: Ext.MessageBox.OKCANCEL,
        fn: function(btn, text, obj){
            if (btn === "ok") {
                openWindow(changesApplyURL, params, true);
            }
        },
        icon: Ext.MessageBox.QUESTION
    });
}

function findByField(record, id){
    return record.data.field == "Заявление: Статус";
}

function getCommentText() {
    if (commentField.getValue().length > commentaryMaxLength){
        var message = "Убедитесь, что комментарий содержит не более " + commentaryMaxLength + " символов.";
        Ext.Msg.alert("Ошибка", message);
        return null;
    }

    return commentField.getValue();
}

function applyChanges(){
    var grid = Ext.getCmp(win.actionContextJson["grid_id"]);
    var store = grid.getStore();
    var title = "Применение изменений";

    // Ужасный костыль.
    // Нужно различать применение изменений по статусу и другим полям.
    if (store.findBy(findByField) != -1){
        title = 'Внимание! После применения данного изменения заявление перейдет в статус "Архивная". Продолжить?';
    }
    comment = getCommentText()
    if (comment != null) {
        applyChangesSubmit(comment);
    }
    // askComment(title, 'Введите комментарий', applyChangesSubmit);
}

function rejectChangesSubmit(comment){
    openWindow(changesRejectURL, {"comment": comment}, true);
}

function rejectChanges(){
    comment = getCommentText()
    if (comment != null) {
        rejectChangesSubmit(comment);
    }
    // askComment('Отказ от изменений', 'Введите комментарий', rejectChangesSubmit);
}

function printChanges(){
    openWindow(changesPrintURL, {"blank": false}, false);
}

{% endblock %}
