def declination(value, one_word, two_word, five_word):
    dec = value % 100
    if (dec > 0) and (dec < 20):
        return five_word
    unit = dec % 10
    if (unit > 1) and (unit < 5):
        return two_word
    if unit == 1:
        return one_word
    return five_word


def collect_full_time_block(left_time):
    hours, minutes, seconds = left_time.seconds // 3600, left_time.seconds % 3600 // 60, left_time.seconds % 60
    return {
        'left_time': {
            'days': {
                'value': left_time.days,
                'word': declination(left_time.days, 'день', 'дня', 'дней')
            },
            'hours': {
                'value': hours,
                'word': declination(hours, 'час', 'часа', 'часов')
            },
            'minutes': {
                'value': minutes,
                'word': declination(minutes, 'минута', 'минуты', 'минут')
            },
            'seconds': {
                'value': seconds,
                'word': declination(seconds, 'секунда', 'секунды', 'секунд')
            }
        }
    }


def collect_strict_time_block(left_time):
    hours, minutes, seconds = left_time.seconds // 3600, left_time.seconds % 3600 // 60, left_time.seconds % 60
    return {
        'left_time': {
            'days': left_time.days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }
    }
