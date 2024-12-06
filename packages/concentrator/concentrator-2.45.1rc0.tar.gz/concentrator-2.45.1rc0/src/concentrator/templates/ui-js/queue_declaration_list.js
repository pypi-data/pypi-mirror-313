{% block content_extension %}
var styleSheetId = 'declaration-list-highlight';
Ext.util.CSS.createStyleSheet(
    '.changes-highlighted-row {color: blue;}', styleSheetId);
// Добавление подсветки синим при наличии изменений ЕПГУ (ставим в начало)
declarationRowHighlightHandlers.textColor.unshift(
    ifRecordParamTrueThenReturnResult.bind(
        null, 'changes_await', 'changes-highlighted-row'),
)

// {# Обработка чекбокса отображения только заявок на подтверждение #}
var needConfirmationOnly = Ext.getCmp('{{ component.need_confirmation_only.client_id}}');
needConfirmationOnly.on('check', showNeedConfirmationOnly);

function showNeedConfirmationOnly(){
    store.baseParams['need_confirmation_only']=needConfirmationOnly.getValue() ? 1 : 0;
    win.grid.refreshStore();
}

{% endblock %}
