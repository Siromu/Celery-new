from django.urls import path, include

from .views import NewsPost, NewsID, PostPage, NewsCreateView, NewsDeleteView, NewsUpdateView, SubscribersView, Success_sub


urlpatterns = [
    path('', NewsPost.as_view()),
    path('search/', PostPage.as_view()),
    path('<int:pk>', NewsID.as_view()),
    path('add/', NewsCreateView.as_view(), name='News_create'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='News_delete'),
    path('<int:pk>/edit/',  NewsUpdateView.as_view(), name='News_update'),
    path('subscribe/', SubscribersView.as_view(), name='sub_notification'),
    path('success_sub/', Success_sub.as_view(), name='Success_sub'),

]





