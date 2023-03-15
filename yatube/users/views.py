from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import EditForm, CreationForm
from posts.models import Post

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


class ChangeUser(View):
    def post(self, request, *args, **kwargs):
        print('ok')
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        

        # old_user = kwargs['old_username']    
        # if request.user.username != old_username:
        #     post_list = Post.objects.filter(author=old_username).update(author=)



        
        #return HttpResponseRedirect(reverse('author-detail', kwargs={'pk': self.object.pk}))
    
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        return HttpResponseRedirect(reverse_lazy('posts:index'))
