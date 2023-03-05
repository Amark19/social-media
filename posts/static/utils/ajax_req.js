function make_req(type, url, data, callback) {
    $.ajax({
        type: type,
        url: url,
        data: {
            data: data,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: callback,
    });
}
