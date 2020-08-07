import requests
import os
import random
import string
import tempfile

def download_image(post, album_image_url):
    if not album_image_url:
        return;

    r = requests.get(album_image_url)

    tf = tempfile.NamedTemporaryFile()
    tf.write(r.content)
    filename = get_random_alphanumeric_string(8) + '.jpg'

    post.albumart.save(filename, tf)

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_string = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_string
