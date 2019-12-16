from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm


#class PostListView(ListView):
#    queryset = Post.published.all()
#    context_object_name = 'posts'
#    paginate_by = 3
#    template_name = 'blog/post/list.html'

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 post on the even page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not integer - return first
        posts = paginator.page(1)
    except EmptyPage:
        # if number page bigger last number - return last page
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,'blog/post/detail.html',{'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of active comment for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # user sent post
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment, but not save it
            new_comment = comment_form.save(commit=False)
            # bind comment to the current post
            new_comment.post = post
            # save comment in db
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form})


