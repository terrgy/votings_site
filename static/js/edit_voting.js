$(document).on('submit', '.edit-form', function (event) {
  event.preventDefault()
  let form_obj = $(this)
  form_ajax_request(success_edit_form, form_obj)
})

$(document).on('click', '#cancel_button', function (event) {
  event.preventDefault()
  action_button_ajax_request(success_edit_form, $(this).attr('href'))
})


$(document).on('submit', '.image_edit_form', function (event) {
  event.preventDefault()
  let form_obj = $(this)
  image_upload_ajax_request(success_image_upload_form, form_obj)
})

function success_image_upload_form(json_obj) {
  $('#image_upload_form').html(json_obj['image_upload_form-html'])
  console.log(json_obj)
}

function success_edit_form(json_obj) {
  if ('main_settings_form' in json_obj) {
    $('#main_settings_form').html(json_obj['main_settings_form'])
  }
  if ('vote_variant_forms' in json_obj) {
    $('#vote_variant_forms_block').html(json_obj['vote_variant_forms'])
  }
  if ('add_vote_variant_form' in json_obj) {
    $('#add_vote_variant_form_block').html(json_obj['add_vote_variant_form'])
  }
  if (json_obj['status'] === 'error') {
    $('#cancel_button').show()
  } else {
    $('#cancel_button').hide()
  }
}
