from user.models import userData
from django.core.files.storage import default_storage
from PIL import Image,ImageOps
from io import BytesIO


def get_user_data(username):
    global user_data
    user_data = userData.objects.values(
        'name', 'user_name', 'user_desc', 'user_email', 'user_phone', 'user_birthday', 'user_pic').filter(user_name=username)
    return user_data

def getUserModelInstance(username):
    return userData.objects.get(user_name=username)

def compress_and_save_image(image):
    img = Image.open(image)
    img = img.resize((1080, 1080))  
    im = ImageOps.exif_transpose(img)
    img_io = BytesIO()
    im = im.convert('RGB')
    im.save(img_io, format='JPEG', quality=50) 
    img_io.seek(0)
    return img_io
