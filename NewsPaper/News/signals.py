from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
from django.template.loader import render_to_string


@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    # получаем наш html

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
