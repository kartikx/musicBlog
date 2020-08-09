from django.contrib import messages

from requests_html import HTMLSession
import requests
import os
import random
import string
import tempfile

def download_image(request, post, album_image_url):
    if not album_image_url:
        messages.add_message(request, messages.INFO, "Couldn't find an Album Art for that song.")
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

def get_and_save_genre_desc(genre):
    session = HTMLSession()
    search_query = f"https://www.google.com/search?client=ubuntu&channel=fs&sxsrf=ALeKk00_1oJuZCQc9c9-BbFHMcyUJbxlMA%3A1596778189236&ei=zeYsX5z-DYia4-EP0KC7qAs&q=what+is+{genre.name}"

    r = session.get(search_query)
    descbox = r.html.find(".kno-rdesc")
    if descbox:
        span_items = descbox[0].find("span")
        genre.desc = span_items[0].text
    else:
        genre.desc = 'Could not find information about this genre.'
    genre.save()