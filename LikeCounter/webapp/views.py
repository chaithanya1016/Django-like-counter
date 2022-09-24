from django.shortcuts import render, redirect
from .models import Post, Like

# Create your views here.

def post_view(request):
    posts = Post.objects.all()
    user = request.user
    context = {
        'posts' : posts,
        'user' : user,
    }
    return render(request, 'webapp/home.html', context)


def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user,post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()    
    return redirect('posts:post-list')