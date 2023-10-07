from django import forms
from .models import Category, Post

class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="All Categories", required=False)

    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class' : 'form-control form-control-lg'}) 
        self.fields['category'].label = str()


class PostTypeFilterForm(forms.Form):
    post_type = forms.ChoiceField(choices=Post.POST_TYPE_CHOICES, required=False)
    
    def __init__(self, *args, **kwargs):
        super(PostTypeFilterForm, self).__init__(*args, **kwargs)
        self.fields['post_type'].widget.attrs.update({'class' : 'form-control form-control-lg'}) 
        self.fields['post_type'].label = str()

class AgeGroupFilterForm(forms.Form):
    age_group = forms.ChoiceField(choices=Post.AGE_CHOICES, required=False)
    def __init__(self, *args, **kwargs):
        super(AgeGroupFilterForm, self).__init__(*args, **kwargs)
        self.fields['age_group'].widget.attrs.update({'class' : 'form-control form-control-lg'}) 
        self.fields['age_group'].label = str()
