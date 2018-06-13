from django.forms import ModelForm, TextInput
from .models import Topic

class TopicForm(ModelForm):
	class Meta:
		model = Topic
		fields = ['name']
		widgets = {'name': TextInput(attrs={'class':'form-control', 'placeholder': 'Search for any topics', 'size': 125})}
