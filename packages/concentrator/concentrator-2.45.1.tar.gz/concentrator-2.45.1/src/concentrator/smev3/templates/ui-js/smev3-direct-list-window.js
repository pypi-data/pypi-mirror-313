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
