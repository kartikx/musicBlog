from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegistrationForm, LoginForm, CreatePostForm
from .models import Post

def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username= form.cleaned_data['username'],
                                     password= form.cleaned_data['password'])
            messages.add_message(request, messages.SUCCESS, "You may now log in")
            return redirect('login')
    else :
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, 'show_valid': True})    

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username= username, password= password)

            if user is not None:
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, "Welcome back!")
                return redirect('feed')
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'show_valid': False})

def feed(request):
    posts = Post.objects.all().order_by('-date_posted')

    # read up on what exactly request.POST is
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            song     =  form.cleaned_data['song']
            artist   = form.cleaned_data['artist']
            content  = form.cleaned_data['content']
            filename = download_image(song, artist)
            post     = Post(title= song, artist = artist, content= content,
                            author= User.objects.get(username= request.user.username),
                            albumart= filename)
            post.save()

    form = CreatePostForm()
    return render(request, 'feed.html', {'posts': posts, 'form': form})

def download_image(song, artist):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options= options)

    # Not resolving for space removal between words, Google handles that for you.
    searchurl = f"https://www.google.com/search?q={song}+{artist}+album+cover&client=ubuntu&hs=USc&channel=fs&sxsrf=ALeKk01Y5nCWBeQ_Z7aJebp81Qz7Lpz0hg:1595422846626&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjbpKig9eDqAhXq6XMBHfoqC_0Q_AUoAXoECA8QAw&biw=1297&bih=645"

    driver.get(searchurl)

    first_image_url = driver.find_element_by_xpath('//div//div//div//div//div//div//div//div//div//div[1]//a[1]//div[1]//img[1]')
    first_image_url.click()

    time.sleep(3)

    popup_image = driver.find_elements_by_class_name("n3VNCb")
    popup_image_url = popup_image[0].get_attribute("src")

    album_image = requests.get(popup_image_url)

    song = ''.join(song.split(' '))
    artist = ''.join(artist.split(' '))

    filename = song + artist + '.' + popup_image_url[-3:]

    if not os.path.exists('/home/kartik/musicBlog2.0/mBlogApp/static/AlbumArt'):
        os.makedirs('/home/kartik/musicBlog2.0/mBlogApp/static/AlbumArt')

    # optimize
    image_path = os.path.join('/home/kartik/musicBlog2.0/mBlogApp/static/AlbumArt', filename)

    if album_image.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(album_image.content) 

    return filename
