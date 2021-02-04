$(function () {
  start_full_time()
})

function success_favourite(json_obj, target) {
  target.html(json_obj['html'])
}

function success_cancel_vote(json_obj) {
  $('#variants_block').html(json_obj['variants_block-html'])
}

function success_vote(json_obj) {
  $('#variants_block').html(json_obj['variants_block-html'])
}

$(document).on('click', '.favourite_button_block .favourite_button', function (event) {
  event.preventDefault()
  let favourite_button = $(this)
  action_button_ajax_request(success_favourite, favourite_button.attr('href'), favourite_button.parent())
})

$(document).on('click', '#cancel_vote_btn', function (event) {
  event.preventDefault()
  let cancel_button = $(this)
  action_button_ajax_request(success_cancel_vote, cancel_button.attr('href'))
})

$(document).on('submit', '#vote_form', function (event) {
  event.preventDefault()
  form_ajax_request(success_vote, $(this))
})

$(document).on('click', '.vote_single_button', function (event) {
  event.preventDefault()
  let button = $(this)
  let extra_data = button.attr('name') + '=' + button.attr('value')
  form_ajax_request(success_vote, $('#vote_form'), null, extra_data)
})
