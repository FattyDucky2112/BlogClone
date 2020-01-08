from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView,
                                    CreateView, UpdateView, DeleteView)

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

#for the DeleteView
from from django.urls import reverse_lazy

#this import is explained in the 'CreatePostView'
#its the class based equivalent to the 'login_required' import for function based views
from django.contrib.auth.mixins import LoginRequiredMixin


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
