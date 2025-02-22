# --------------- forms.py -------------------------
from django import forms

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)
    is_published = forms.BooleanField(required=False)

# --------------- views.py -------------------------
# from django.shortcuts import render
# from .forms import AddPostForm

# здесь продолжайте программу

def post_new(request):
    form = AddPostForm()
    return render(request, 'women/addpage.html', {'form': form})