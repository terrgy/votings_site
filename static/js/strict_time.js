let strict_time_changer

function check_left_time_block(block) {
  let days = Number(block.find('.left_time_days').html())
  let hours = Number(block.find('.left_time_hours').html())
  let minutes = Number(block.find('.left_time_minutes').html())
  let seconds = Number(block.find('.left_time_seconds').html())
  return (days !== 0) || (hours !== 0) || (minutes !== 0) || (seconds !== 0)
}

function change_blocks_visibility() {
  $('.strict_time_block').each(function () {
    let block = $(this)
    let left_time_block = block.find('.left_time_block')
    if (check_left_time_block(left_time_block)) {
      left_time_block.show()
      block.find('.is_ended_block').hide()
    } else {
      left_time_block.hide()
      block.find('.is_ended_block').show()
    }
  })
}

function start_strict_time() {
  change_blocks_visibility()
  strict_time_changer = setInterval(change_strict_time, 1000)
}

function end_strict_time() {
  clearInterval(strict_time_changer)
  change_blocks_visibility()
}

function format_html(value) {
  if (value < 10) {
    return "0" + String(value)
  }
  return String(value)
}

function change_left_time_block_time(block) {
  let seconds_block = block.find('.left_time_seconds')
  let seconds = Number(seconds_block.html()) - 1
  if (seconds < 0) {
    let minutes_block = block.find('.left_time_minutes')
    let minutes = Number(minutes_block.html()) - 1
    if (minutes < 0) {
      let hours_block = block.find('.left_time_hours')
      let hours = Number(hours_block.html()) - 1
      if (hours < 0) {
        let days_block = block.find('.left_time_days')
        let days = Number(days_block.html()) - 1
        if (days < 0) {
          block.parent().find('.is_ended_block').show()
          block.hide()
          return
        }
        days_block.html(days)
        hours = 23
      }
      hours_block.html(format_html(hours))
      minutes = 59
    }
    minutes_block.html(format_html(minutes))
    seconds = 59
  }
  seconds_block.html(format_html(seconds))
}

function change_strict_time() {
  $('.left_time_block:visible').each(function () {
    change_left_time_block_time($(this))
  })
}
