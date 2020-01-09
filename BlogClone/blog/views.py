from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (TemplateView, ListView, DetailView,
                                    CreateView, UpdateView, DeleteView)

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

#for the DeleteView
from django.urls import reverse_lazy

#this import is explained in the 'CreatePostView'
#its the class based equivalent to the 'login_required' import for function based views
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required




class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    #defining how to grab the List
    #get_queryset is like a sql query on my own model
    def get_queryset(self):
        #grab the 'post' model and 'filter' out all the 'objects' based on the following conditions (check documentation for query/field lookups)
        # __lte = less then or equal to; __exact; ... all is basically translating sql code in python
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    #Because we dont want anyone to be able to access the CreatePostView
    #With function based views we used 'login_required' for this
    #in class based views we use 'mixins'
    #these are basically classes that we 'mix in' to the class we are inheriting from
    #these mixins need a few more attributes to be defined

    #where to send the user if he is not logged in?
    login_url = '/login/'
    #redirect logged in user to the detail view
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    #all attributes are the same for creation and update
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    #success url when deleting is done
    success_url = reverse_lazy('post_list')

#before i publish a post i want it to be in draft (Entwurf)

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    #Now its very similar to the PostListView just this time making sure that there is NO publication date on the post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')

########################################################
#now we do the views needed for the commment function###

@login_required
def add_comment_to_post(request,pk):
    # either get post object with corresponding pk or show 404 page
    post = get_object_or_404(Post,pk=pk)
    #if someone filled out the form and hit the submit button (method == 'POST')
    if request.method == 'POST':
        #pass the request to the Comment form and make it form
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # post object is in the comment form as a foreign key from Post model
            # So here we say because the form is valid make the comment.post equal to the post itself
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        #if not hit submit yet show the CommentForm (connected in the comment_form.html)
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    #approve method in comment model, which sets approved to true
    comment.approve()
    #again post is defined in Comment model as a foreign key
    #means we are sending the user back to the actual post
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    #when we delete the comment we dont habe comment.post.pk anymore to redirect to
    #thats why before deleting it we reassign it to a new variable 'post_pk'
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)


@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
