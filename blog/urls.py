from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('mcategory/<slug:mcat_slug>/', views.mcategory, name='mcategory'),
    path('category/<slug:cat_slug>/', views.category, name='category'),
    path('scategory/<slug:scat_slug>/', views.scategory, name='scategory'),
    path('comment/', views.comment, name='comment'),
    path('reply/', views.reply, name='reply'),
    path('comment_update/', views.comment_update, name='comment_update'),
    path('reply_update/', views.reply_update, name='reply_update'),
    path('comment_delete/', views.comment_delete, name='comment_delete'),
    path('reply_delete/', views.reply_delete, name='reply_delete'),
    path('add/', views.add_post, name='add_post'),
    path('update/<slug:slug>/', views.update_post, name='update_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
