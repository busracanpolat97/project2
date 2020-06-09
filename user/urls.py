from django.urls import path

from . import views

urlpatterns = (
    # ex: /home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('notes/', views.notes, name="notes"),
    path('addnote/', views.addnote, name='addnote'),
    path('noteedit/<int:id>', views.noteedit, name='noteedit'),
    path('notedelete/<int:id>', views.notedelete, name='notedelete'),
    path('noteaddimage/<int:id>', views.noteaddimage, name='noteaddimage'),

    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),

)
