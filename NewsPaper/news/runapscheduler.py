from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Category(models.Model):
    name = models.CharField(max_length=200)
    subscribers = models.ManyToManyField(User)

class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

@receiver(post_save, sender=Article)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        for user in instance.category.subscribers.all():
            send_mail(
                'New article in your subscribed category',
                f'{instance.summary} Read more at: <http://website.com/{instance.id}>',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to our news application',
            'We are glad to see you here!',
            'from@example.com',
            [instance.email],
            fail_silently=False,
        )