from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.views import View
from django.core.mail import send_mail
from django.shortcuts import render, reverse, redirect
from .models import Posts
from datetime import datetime
from .filters import PostsFilter
from .forms import PostsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.utils.translation import gettext as _


class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)

class SendingMail(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'send_mail.html', {})

    def post(self, request, *args, **kwargs):

        sending = SendingMail(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],)
        sending.save()

        html_content = render_to_string(
            'send_mail.html',
            {
                'sending': sending,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{sending.client_name} {sending.date.strftime("%Y-%M-%d")}',
            body=sending.message,
            from_email='ps4123303@yandex.ru',
            to=['ps4123303@gmail.com'],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        send_mail(
            subject=f'{sending.client_name} {sending.date.strftime("%Y-%M-%d")}',
            message=sending.message,
            from_email='ps4123303@yandex.ru',
            recipient_list=[]
        )

        return redirect('sendings:make_sendings')

    def save(self):
        pass

@receiver(post_save, sender=SendingMail)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )



post_save.connect(notify_managers_appointment, sender=SendingMail)
class PostsList(ListView):
    model = Posts
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context



class PostsDetail(DetailView):
    model = Posts
    template_name = 'news.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'posts-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'posts-{self.kwargs["pk"]}', obj)

        return obj


class PostsCreate(CreateView,PermissionRequiredMixin):
    form_class=PostsForm
    model=Posts
    template_name='posts_edit.html'
    permission_required = ('news.add_posts')


class PostsUpdate(UpdateView, LoginRequiredMixin):
    form_class = PostsForm
    model = Posts
    template_name = 'posts_edit.html'
    go_to_login=login_required(login_url= 'login/')


class PostsDelete(DeleteView):
    model = Posts
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('product_list')



