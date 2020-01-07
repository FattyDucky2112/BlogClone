from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        #Im Folgenden wird die Form zum styling mit CSS verknüpft
        widgets = {
            'title':forms.TextInput(attrs = {'class':'textinputclass'}),
            'text':forms.Textarea(attrs = {'class':'editable medium-editor-textarea postcontent'}) #editable und medium-editor-textarea sind importierte Klassen; textinputclass und postcontent sind eigene Klassen die wir selbst in CSS definiert haben
            }



class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs = {'class':'textinputclass'}),
            'text':forms.Textarea(attrs = {'class':'editable medium-editor-textarea'})
            }
