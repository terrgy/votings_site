let full_time_changer
let are_days_hidden_full, are_hours_hidden_full, are_minutes_hidden_full, are_seconds_hidden_full

function declination(value, one_word, two_word, five_word) {
  let dec = value % 100
  if ((dec > 10) && (dec < 20)) {
    return five_word
  }
  let unit = dec % 10
  if ((unit > 1) && (unit < 5)) {
    return two_word
  }
  if (unit === 1) {
    return one_word
  }
  return five_word
}

function change_full_time_fields_visibility() {
  let seconds_block_value = $('#left_time_seconds .left_time-value')
  if (seconds_block_value.html() === '0') {
    seconds_block_value.parent().hide()
    are_seconds_hidden_full = true
  } else {
    seconds_block_value.parent().show()
    are_seconds_hidden_full = false
  }
  let minutes_block_value = $('#left_time_minutes .left_time-value')
  if (minutes_block_value.html() === '0') {
    minutes_block_value.parent().hide()
    are_minutes_hidden_full = true
  } else {
    minutes_block_value.parent().show()
    are_minutes_hidden_full = false
  }
  let hours_block_value = $('#left_time_hours .left_time-value')
  if (hours_block_value.html() === '0') {
    hours_block_value.parent().hide()
    are_hours_hidden_full = true
  } else {
    hours_block_value.parent().show()
    are_hours_hidden_full = false
  }
  let days_block_value = $('#left_time_days .left_time-value')
  if (days_block_value.html() === '0') {
    days_block_value.parent().hide()
    are_days_hidden_full = true
  } else {
    days_block_value.parent().show()
    are_days_hidden_full = false
  }
}

function start_full_time() {
  change_full_time_fields_visibility()
  if (are_seconds_hidden_full && are_minutes_hidden_full && are_hours_hidden_full && are_days_hidden_full) {
    $('#is_ended_block').show()
    $('#left_time_block').hide()
  } else {
    $('#is_ended_block').hide()
    $('#left_time_block').show()
    full_time_changer = setInterval(change_full_time, 1000)
  }
}

function end_full_time() {
  clearInterval(full_time_changer)
  $('#is_ended_block').show()
  $('#left_time_block').hide()
}

function change_full_time() {
  let seconds_block_value = $('#left_time_seconds .left_time-value')
  let seconds = Number(seconds_block_value.html()) - 1
  if (seconds < 0) {
    seconds = 59
    let minutes_block_value = $('#left_time_minutes .left_time-value')
    let minutes = Number(minutes_block_value.html()) - 1
    if (minutes < 0) {
      minutes = 59
      let hours_block_value = $('#left_time_hours .left_time-value')
      let hours = Number(hours_block_value.html()) - 1
      if (hours < 0) {
        hours = 23
        let days_block_value = $('#left_time_days .left_time-value')
        let days = Number(days_block_value.html()) - 1
        if (days < 0) {
          end_full_time()
          return
        } else if (days === 0) {
          days_block_value.parent().hide()
          are_days_hidden_full = true
        }
        days_block_value.html(days)
        $('#left_time_days .left_time-word').html(declination(days, 'день', 'дня', 'дней'))
        hours_block_value.parent().show()
        are_hours_hidden_full = false
      } else if (hours === 0) {
        hours_block_value.parent().hide()
        are_hours_hidden_full = true
      }
      hours_block_value.html(hours)
      $('#left_time_hours .left_time-word').html(declination(hours, 'час', 'часа', 'часов'))
      minutes_block_value.parent().show()
      are_minutes_hidden_full = false
    } else if (minutes === 0) {
      minutes_block_value.parent().hide()
      are_minutes_hidden_full = true
    }
    minutes_block_value.html(minutes)
    $('#left_time_minutes .left_time-word').html(declination(minutes, 'минута', 'минуты', 'минут'))
    seconds_block_value.parent().show()
    are_seconds_hidden_full = false
  } else if (seconds === 0) {
    if (!are_minutes_hidden_full || !are_hours_hidden_full || !are_days_hidden_full) {
      seconds_block_value.parent().hide()
      are_seconds_hidden_full = true
    }
  }
  seconds_block_value.html(seconds)
  $('#left_time_seconds .left_time-word').html(declination(seconds, 'секунда', 'секунды', 'секунд'))
}
