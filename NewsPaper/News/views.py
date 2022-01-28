import requests
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category
from .forms import SubscribeForm
from .filternews import PostFilter
from .NewsForm import PostCreateForm
from django.core.mail import send_mail
from django.core.mail import mail_admins # импортируем функцию для массовой отправки писем админам
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html


class NewsPost(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'News'
    queryset = Post.objects.order_by('-dateCreation')


class NewsID(DetailView):
    model = Post
    template_name = 'flatpages/NewsId.html'
    context_object_name = 'NewsId'


class PostPage(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'News'
    ordering = ['-dateCreation']
    paginate_by = 10 #оставила 1 вместо 10 для наглядности, а то страницы пропадают, постов мало

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        author = request.POST['Author']
        title = request.POST['Title']
        category_id = request.POST['Category']
        text = request.POST['Text']

        post = Post(author=author, title=title, category_id=category_id, text=text)  # создаём новый товар и сохраняем
        post.save()
        return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.


class PostDetailView(DetailView):
    template_name = 'News_app/News_detail.html'
    queryset = Post.objects.all()


class NewsCreateView(CreateView):
    template_name = 'News_app/News_create.html'
    form_class = PostCreateForm


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'News_app/News_update.html'
    form_class = PostCreateForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'News_app/News_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'News_delete'


class Notify(DetailView):
    model = Post
    template_name = 'notify.html'
    context_object_name = 'notify'


class Success_sub(ListView):
    model = Category
    template_name = 'success_sub.html'
    context_object_name = 'success_sub'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscribersView(View):

    def get(self, request, *args, **kwargs):
        form = SubscribeForm()
        return render(request, 'sub_notification.html', {'form':form})

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=request.POST['category'])
        category.subs.add(request.user)
        category.save()

        html_content = render_to_string(
            'sub_created.html',
            {
                'user' : request.user,
                'category': category,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Подписка оформлена!',
            from_email='sth0400@mail.ru',
            to=[request.POST['email']],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return redirect('Success_sub')



