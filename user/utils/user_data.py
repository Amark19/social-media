from user.models import userData

def get_user_data(r):
    global user_data
    user_data = userData.objects.values(
        'name', 'user_desc', 'user_email', 'user_phone', 'user_birthday', 'user_pic').filter(user_name=r.user.username)
    return user_data
