from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import EditForm, CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class Edit(UpdateView):
    form_class = EditForm
    template_name = 'users/change_user.html'
    success_url = reverse_lazy('posts:index')

    def get_object(self):
        return self.request.user
