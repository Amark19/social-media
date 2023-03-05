def time_diff(curr_time,time_posted):
    time_diff = curr_time - time_posted
    if time_diff.total_seconds()/60 < 60:
        return f'{int(time_diff.total_seconds()/60)} mins ago'
    elif time_diff.total_seconds()/3600 < 24:
        return f'{int(time_diff.total_seconds()/3600)} hours ago'
    else:
        return f'{int(time_diff.total_seconds()/86400)} days ago'