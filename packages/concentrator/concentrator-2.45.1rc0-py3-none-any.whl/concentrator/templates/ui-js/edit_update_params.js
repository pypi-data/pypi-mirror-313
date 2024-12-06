/**
 * User: kasimova
 * Date: 17.09.14
 * Time: 15:21
 */
var mapFields = Ext.util.JSON.decode('{{ component.model_fields|safe }}'),
    fieldModel = Ext.getCmp('{{ component.field__model_name.client_id  }}'),
    fieldParam = Ext.getCmp('{{ component.field__field_name.client_id  }}');
/**
 * При выборе модели, определяем список ее полей
 * и помещаем в стор втрого контрола
 */
fieldModel.on('select', function(combo, record, index){
    fieldParam.clearValue();
    fieldParam.getStore().removeAll();
    var model_value = record.id,
        store = [],
        arr = mapFields[model_value];
    for (var i = 0; i < arr.length; i++) {
        store[i] = [arr[i][0], arr[i][1]]
    }
    fieldParam.getStore().loadData(store);
});

fieldParam.on('beforequery', function(){
    if (!fieldModel.getValue()){
        Ext.Msg.alert('Внимание', 'Выберите "Наименование модели".');
        return false;
    }
})
