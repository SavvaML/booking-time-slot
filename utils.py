import datetime
def get_time_slote():
    start_time = datetime.datetime.strptime('12:00', '%H:%M')
    end_time = datetime.datetime.strptime('17:00', '%H:%M')
    slot_time = 15
    time_slot = []
    while start_time <= end_time:
        time_slot.append(
            (start_time.strftime("%H:%M"), (start_time + datetime.timedelta(minutes=slot_time)).strftime("%H:%M")))
        start_time += datetime.timedelta(minutes=slot_time)
    return time_slot