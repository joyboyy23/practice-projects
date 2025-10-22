from django.shortcuts import render
from django.http import Http404

    # sample data (will come from database later)
POSTS = [
    {
        'id': 1,
        'title': 'First Blog Post',
        'content': '''This is my first blog post. Django is awesome! 
        I'm learning how to build web applications with Python and Django.
        The MVT pattern makes everything so organized and easy to understand.''',
        'author': 'Joyboy',
        'date': 'Oct 18, 2025'
    },
    {
        'id': 2,
        'title': 'Learning Django',
        'content': '''Today I learned about Django templates and views. 
        Templates allow me to create dynamic HTML pages, and views handle the logic.
        It's making web development so much easier and more enjoyable!''',
        'author': 'Joyboy',
        'date': 'Oct 17, 2025'
    },
    {
        'id': 3,
        'title': 'Python Web Development',
        'content': '''Python is an excellent language for web development. 
        Django makes it even better with its batteries-included approach.
        The admin interface, ORM, and security features are incredible.''',
        'author': 'Joyboy',
        'date': 'Oct 16, 2025'
    }
]

def home(request):
    #home page with all posts
    context = {
        'posts': POSTS,
        'blog_title': 'My Awesome Blog'
    }
    return render(request, 'blog/home.html', context)

def post_detail(request, post_id):
    #individual post detail page
    #find post by id
    post = None
    for p in POSTS:
        if p['id'] == post_id:
            post = p
            break

    #if post not found, raise 404
    if not post:
        raise Http404("Post not found")
    
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)

def about(request):
    #about page
    context = {
        'title': 'About',
    }
    return render(request, 'blog/about.html', context)


