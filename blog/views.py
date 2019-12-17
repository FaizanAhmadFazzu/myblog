from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Post, FollowUser, Comment, Like, Profile
from django.db.models import Q 
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponseRedirect

@method_decorator(login_required, name="dispatch")    
class HomeView(TemplateView):
    template_name = "blog/home.html"
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        followedList = FollowUser.objects.filter(followed_by = self.request.user.profile)
        followedList2 = []
        for e in followedList:
            followedList2.append(e.profile)
        postList = Post.objects.filter(author__in = followedList2).order_by("-id")
        
        for p1 in postList:
            p1.liked = False
            ob = Like.objects.filter(post = p1,liked_by=self.request.user.profile)
            if ob:
                p1.liked = True        
            obList = Like.objects.filter(post = p1)
            p1.likedno = obList.count()
        context["post_list"] = postList
        return context;

def follow(req, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by = req.user.profile)
    return HttpResponseRedirect(redirect_to="/blog/profile")

def unfollow(req, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by = req.user.profile).delete()
    return HttpResponseRedirect(redirect_to="/blog/profile")

def like(req, pk):
    post = Post.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by = req.user.profile)
    return HttpResponseRedirect(redirect_to="/blog/home")

def unlike(req, pk):
    post = Post.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by = req.user.profile).delete()
    return HttpResponseRedirect(redirect_to="/blog/home")

@method_decorator(login_required, name="dispatch")    
class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ["name", "age", "address", "status", "gender", "phone_no", "description", "image"]


@method_decorator(login_required, name="dispatch")    
class ProfileDetailView(DetailView):
    model = Profile



def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-date_posted'
    )
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/blog_category.html", context)
    


class PostDetailView(DetailView):
    model = Post
     
@method_decorator(login_required, name="dispatch")    
class PostListView(ListView):
    model = Post
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        return Post.objects.filter(Q(author = self.request.user.profile)).filter(Q(title__icontains = si) | Q(content__icontains = si)).order_by("-id");   
    
@method_decorator(login_required, name="dispatch")    
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'categories', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)
    

@method_decorator(login_required, name="dispatch")    
class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'categories' 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@method_decorator(login_required, name="dispatch")    
class ProfileListView(ListView):
    model = Profile
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        profList = Profile.objects.filter(Q(name__icontains = si) | Q(address__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si)).order_by("-id");
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile = p1,followed_by=self.request.user.profile)
            if ob:
                p1.followed = True
        return profList

@method_decorator(login_required, name="dispatch")    
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def contact(request):
    return render(request, 'blog/contact.html', {'title': 'Contact'})

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})