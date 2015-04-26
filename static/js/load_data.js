
function ajaxSelect(id) {
    var element = document.getElementById(id);

    var onLoaded = function(data) {
        var i=0;
        for (var key in data) {
            var label = data[key];
            element.options[i++] = new Option(label, key)
        }
        element.options[0].defaultSelected = true;
        element.selectedIndex = 0;
    };

    var onLoadError = function(error) {
        var msg = "Ошибка "+error.errcode
        if (error.message) msg = msg + ' :'+error.message;
        alert(msg)
    };

    var showLoading = function(on) {
        element.disabled = on
    };

    var onSuccess = function(data) {
        if (!data.errcode) {
            onLoaded(data);
            showLoading(false)
        } else {
            showLoading(false);
            onLoadError(data)
        }
    };


    var onAjaxError = function(xhr, status){
        showLoading(false);
        var errinfo = { errcode: status };
        if (xhr.status != 200) {
            // может быть статус 200, а ошибка
            // из-за некорректного JSON
            errinfo.message = xhr.statusText
        } else {
            errinfo.message = 'Некорректные данные с сервера'
        }
        onLoadError(errinfo)
    };


    return {
        load: function(url) {
            showLoading(true);

            while (element.firstChild) {
                element.removeChild(element.firstChild)
            }

            $.ajax({ // для краткости - jQuery
                url: url,
                dataType: "json",
                success: onSuccess,
                error: onAjaxError,
                cache: false
            })
        }
    }
}


$(document).ready(function() {
    $("#id_specialization").change(function() {
        select = ajaxSelect('id_doctor');
        select.load('/main/get_doctors/json/' + $(this).val());
    });
    if ($("#id_specialization").val()){
        select = ajaxSelect('id_doctor');
        select.load('/main/get_doctors/json/' + $("#id_specialization").val());
    }
});