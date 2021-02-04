$(document).on('submit', '.image_edit_form', function (event) {
  event.preventDefault()
  let form_obj = $(this)
  image_upload_ajax_request(success_image_upload_form, form_obj)
})

function success_image_upload_form(json_obj) {
  $('#image_upload_form').html(json_obj['image_upload_form-html'])
  console.log(json_obj)
}
