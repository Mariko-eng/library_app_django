from django import forms
from .models import Category,Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),required=False)
    image = forms.ImageField(required=False)
    file = forms.FileField(required=False)
    link = forms.URLField(required=False)

    class Meta:
        model = Product
        fields = [
            "product_type",
            "category",
            "title",
            "description",
            "image",
            "file",
            "link",
        ]