var grid = Ext.getCmp('{{component.grid.client_id}}'),
    store = grid.getStore();
var styleSheetId = 'direct-list-highlight';
Ext.util.CSS.createStyleSheet('.highlighted-row-blue {color: blue;}', styleSheetId);

// Удаление стилей при закрытии окна
win.on("beforeclose", function () {
    Ext.util.CSS.removeStyleSheet(styleSheetId)
});

// Подсветка строк направлений
function highlightRow(record, index, params) {
    if (record.json['applicant_answer_highlight']) {
        return 'highlighted-row-blue';
    }
}

var needConfirmationOnly = Ext.getCmp('{{ component.need_confirmation_only.client_id}}');
// Обработка изменения значения чекбокса "На подтверждение"
function showNeedConfirmationOnly() {
    store.baseParams['need_confirmation_only'] = needConfirmationOnly.getValue() ? 1 : 0;
    store.load();
}
needConfirmationOnly.on('check', showNeedConfirmationOnly);