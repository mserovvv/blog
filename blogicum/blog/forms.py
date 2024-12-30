from django import forms

from .models import Comment, Post


class FormPost(forms.ModelForm):
    """
    Форма для создания и редактирования постов.
    """
    class Meta:
        model = Post
        fields = ["title", "text", "image", "category", "location", "pub_date"]
        widgets = {
            "pub_date": forms.DateTimeInput(
                attrs={
                    "type": "date-local",
                    "class": "form-control",
                }, format="%d-%m-%Y"
            ),
        }


class CommentForm(forms.ModelForm):
    """
    Форма для добавления комментариев.
    """
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }
        labels = {"text": "Ваш комментарий"}
