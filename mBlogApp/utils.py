def download_image(album_image_url):
    print("In download image ", album_image_url)
    r = requests.get(album_image_url)

    album_dir = os.path.join(os.path.realpath('..'), 'musicBlog2.0', 'mBlogApp', 'static', 'AlbumArt')

    filename = get_random_alphanumeric_string(8) + '.jpg'

    if not os.path.exists(album_dir):
        os.makedirs(album_dir)

    image_path = os.path.join(album_dir, filename)
    print(image_path)
    with open(image_path, 'wb') as f:
        f.write(r.content)

    return filename    

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_string = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_string
