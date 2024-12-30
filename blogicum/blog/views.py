from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .constants import PAGINATOR
from .forms import CommentForm, FormPost
from .mixins import OnlyAuthorMixin
from .models import Category, Comment, Post
from .utils import paginate_queryset


def get_base_post_queryset():
    """
    Получить базовый QuerySet для постов с фильтром публикации.
    """
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True,
    ).select_related("category", "author", "location")


def index(request):
    """
    Главная страница блога, отображает список постов.
    """
    posts = get_base_post_queryset().filter(is_published=True)
    page_obj = paginate_queryset(posts, request, PAGINATOR)
    return render(request, "blog/index.html", {"page_obj": page_obj})


def category_posts(request, category_slug):
    """
    Страница, отображающая посты конкретной категории.
    """
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    posts = get_base_post_queryset().filter(category=category, is_published=True)
    page_obj = paginate_queryset(posts, request, PAGINATOR)
    return render(
        request, "blog/category.html", {"category": category, "page_obj": page_obj}
    )


def profile_view(request, username):
    """
    Страница профиля пользователя с его постами.
    """
    user = get_object_or_404(User, username=username)
    if request.user == user:
        posts = Post.objects.filter(author=user)
    else:
        posts = Post.objects.filter(author=user, is_published=True, pub_date__lte=now())
    page_obj = paginate_queryset(posts, request, PAGINATOR)
    context = {
        "profile": user,
        "page_obj": page_obj,
        "is_owner": request.user == user,
    }
    return render(request, "blog/profile.html", context)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Обновление профиля пользователя.
    """

    model = User
    template_name = "blog/user.html"
    fields = ["username", "first_name", "last_name", "email"]

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Создание нового поста.
    """

    model = Post
    form_class = FormPost
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user.username})


class PostUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    """
    Редактирование существующего поста.
    """

    model = Post
    template_name = "blog/create.html"
    form_class = FormPost

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        return super().form_valid(form)


class PostDetailView(DetailView):
    """
    Просмотр деталей поста.
    """

    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(
                is_published=True, pub_date__lte=now(), category__is_published=True
            )
        else:
            queryset = queryset.filter(
                Q(
                    is_published=True,
                    pub_date__lte=now(),
                    category__is_published=True,
                )
                | Q(author=self.request.user)
            )

        obj = get_object_or_404(queryset, pk=self.kwargs.get("pk"))
        if obj.pub_date > now() and obj.author != self.request.user:
            return get_object_or_404(Post, pk=None)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.all()
        return context


class PostDeleteView(OnlyAuthorMixin, LoginRequiredMixin, DeleteView):
    """
    Удаление поста.
    """

    model = Post
    template_name = "blog/create.html"
    success_url = reverse_lazy("create_post")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = {"instance": self.get_object()}
        return context

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


@login_required
def add_comment(request, pk):
    """
    Добавление комментария к посту.
    """
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("blog:post_detail", pk=pk)
    else:
        form = CommentForm()
    return render(request, "blog/comment.html", {"form": form, "post": post})


@login_required
def edit_comment(request, pk, comment_id):
    """
    Редактирование комментария.
    """
    post = get_object_or_404(Post, id=pk)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if comment.author != request.user:
        return redirect("blog:post_detail", pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/comment.html", {"form": form, "comment": comment})


@login_required
def delete_comment(request, pk, comment_id):
    """
    Удаление комментария.
    """
    post = get_object_or_404(Post, id=pk)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if comment.author != request.user:
        return redirect("blog:post_detail", pk=pk)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", pk=pk)
    return render(request, "blog/comment.html", {"comment": comment})
