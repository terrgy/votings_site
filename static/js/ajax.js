function action_button_ajax_request(success_func, href, target = null) {
  $.ajax({
    url: href,
    type: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    dataType: 'json',
    success: function (json_obj) {
      if ('messages' in json_obj) {
        add_messages(json_obj['messages'])
      }
      if (target) {
        success_func(json_obj, target)
      } else {
        success_func(json_obj)
      }
    },
    error: function () {
      add_messages(create_message('error', 'Ошибка получения данных с сервера'))
    }
  })
}

function form_ajax_request(success_func, form, target = null, extra_data = '') {
  let data = form.serialize()
  if (extra_data !== '') {
    data += '&' + extra_data
  }
  $.ajax({
    url: form.attr('action'),
    type: 'POST',
    data: data,
    dataType: 'json',
    success: function (json_obj) {
      if ('messages' in json_obj) {
        add_messages(json_obj['messages'])
      }
      if (target) {
        success_func(json_obj, target)
      } else {
        success_func(json_obj)
      }
    },
    error: function () {
      add_messages(create_message('error', 'Ошибка получения данных с сервера'))
    }
  })
}


function image_upload_ajax_request(success_func, form, target = null) {
  let image_input = form.find('input[type=file]')
  if (typeof image_input[0].files[0] === undefined) {
    return
  }
  let data = new FormData(form[0])
  $.ajax({
    url: form.attr('action'),
    type: 'POST',
    data: data,
    cache: false,
    dataType: 'json',
    processData: false,
    contentType: false,
    success: function (json_obj) {
      if ('messages' in json_obj) {
        add_messages(json_obj['messages'])
      }
      if (target) {
        success_func(json_obj, target)
      } else {
        success_func(json_obj)
      }
    },
    error: function () {
      add_messages(create_message('error', 'Ошибка получения данных с сервера'))
    }
  })
}
