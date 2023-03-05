from user.models import userData

#get userdata from username
def get_user_data(username):
    global user_data
    user_data = userData.objects.values(
        'name', 'user_desc', 'user_email', 'user_phone', 'user_birthday', 'user_pic').filter(user_name=username)
    return user_data
