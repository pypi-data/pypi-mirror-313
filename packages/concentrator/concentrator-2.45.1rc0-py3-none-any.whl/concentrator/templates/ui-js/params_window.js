/**
 * Created by ira on 10/13/14.
 */

win.on('beforesubmit', beforeSubmitHandler);
function beforeSubmitHandler(submit){
    submit.timeout = 60000 * 60 * 1000;
}