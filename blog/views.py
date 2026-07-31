from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.utils.text import slugify
from .models import Post, Category, Tag, Comment, Like
from .forms import PostForm



# Homepage - shows all published posts
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-created_at')

# Post Detail Page
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Only show draft posts to the author or admin
        if obj.status == 'draft' and obj.author != self.request.user and not self.request.user.is_superuser:
            raise Http404("This post is not available.")
        
        # Increment view count
        session_key = f'viewed_post_{obj.pk}'
        if not self.request.session.get(session_key, False):
            obj.view_count += 1
            obj.save(update_fields=['view_count'])
            self.request.session[session_key] = True
        return obj

# Category Filter
class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Post.objects.filter(category__slug=slug, status='published').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

# Tag Filter
class TagView(ListView):
    model = Post
    template_name = 'blog/tag.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Post.objects.filter(tags__slug=slug, status='published').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return context

# Search
class SearchView(ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                status='published'
            ).order_by('-created_at')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

# Author Profile
class AuthorProfileView(ListView):
    model = Post
    template_name = 'blog/author_profile.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(author_id=user_id, status='published').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from accounts.models import CustomUser
        context['author_user'] = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        return context

# Dashboard - Author only
class DashboardView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/dashboard.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')


# ===== AUTHOR ONLY VIEWS (Create, Edit, Delete) =====
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.text import slugify
from .forms import PostForm

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_author

    def handle_no_permission(self):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You must be an author to access this page.")

class PostCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:dashboard')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:dashboard')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


# ===== COMMENT VIEWS =====

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, author=request.user, text=text)
        return redirect('blog:post_detail', slug=slug)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        return user.is_superuser or user == comment.author or user == comment.post.author


# ===== LIKE VIEW =====

class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        return redirect('blog:post_detail', slug=slug)