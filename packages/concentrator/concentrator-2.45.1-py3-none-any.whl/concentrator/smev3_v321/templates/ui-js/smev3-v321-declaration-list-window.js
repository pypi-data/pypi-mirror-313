var isEpguSubscribedOnly = Ext.getCmp('{{ component.is_epgu_subscribed_only.client_id}}');
// Обработка изменения значения чекбокса "Только заявки, подписанные на уведомления через ЕПГУ"
function showEpguSubscribedOnly() {
    store.baseParams['is_epgu_subscribed_only'] = isEpguSubscribedOnly.getValue() ? 1 : 0;
    store.load();
}
isEpguSubscribedOnly.on('check', showEpguSubscribedOnly);
