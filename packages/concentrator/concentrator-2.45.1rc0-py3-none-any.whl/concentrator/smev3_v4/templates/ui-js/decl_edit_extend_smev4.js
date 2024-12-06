var adaptedProgramConsent = Ext.getCmp("{{ component.field__adapted_program_consent.client_id  }}"),
    compGroupType = parseInt("{{ component.comp_type }}");

desiredGroupTypeField.on("change", adaptedProgramConsentHandler);

/**
 * При смене значения желаемой направленности группы с "Компенсирующая" меняем значение поля
 * Согласие на обучение по адаптированной образовательной программе на false и выводим предупреждающее сообщение.
 */
function adaptedProgramConsentHandler(cmp, newValue, oldValue) {

    if (newValue !== oldValue && oldValue === compGroupType && adaptedProgramConsent.getValue() === true) {
        Ext.Msg.show({
            title: 'Внимание',
            msg: 'В заявлении Вы изменили направленность группы с "Компенсирующая" на "' + cmp.lastSelectionText + '". В связи с ' +
                'этим в заявлении будет убрана отметка "Согласие на обучение по адаптированной образовательной программе".',
            buttons: Ext.Msg.OK,
            icon: Ext.Msg.WARNING
        });
        adaptedProgramConsent.setValue(false);
    }
}