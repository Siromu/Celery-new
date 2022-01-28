from celery import app
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Post
from django.template.loader import render_to_string


@receiver(post_save, sender=Post)
@app.task()
def new_st(sender, instance, created, **kwargs):
    html_content = render_to_string(
        'notify.html',
        {

            'post': instance,
        }
    )
    if created:
        subject = f'Новая публикация - {instance.title}, раздел {instance.postCategory} ... {instance.dateCreation}'
    else:
        subject = f'Изменения в публикации: {instance.title}, раздел {instance.postCategory} ... {instance.dateCreation}'

    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='sth0400@mail,ru',
        to=['deathsempai@mail.ru'],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


