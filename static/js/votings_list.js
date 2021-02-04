function table_row_click(url) {
  document.location.href = url
}

$(document).on('click', '.favourite_button_block .favourite_button', function (event) {
  event.preventDefault()
  let favourite_button = $(this)
  action_button_ajax_request(success_favourite, favourite_button.attr('href'), favourite_button.parent())
})

function success_favourite(json_obj, target) {
  target.html(json_obj['html'])
}

$(function () {
  start_strict_time()
})
