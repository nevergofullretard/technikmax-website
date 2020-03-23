from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'), #PostListView.as_view()

    # path('user/<str:username>', views.UserPostListView.as_view(), name='user-posts'),    #mit dem html-tags kann man auf Variablen zugreifen
    # path('blog/', views.PostListView.as_view(), name='blog'),
    path('post/<int:pk>/<str:name>/', views.PostDetailView.as_view(), name='post-detail'),    #<pk> heist primäry key = Primärschlüssel des Posts
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),


    path('art/<str:name>/', views.type_detail, name='types'),
    path('bereich/<str:name>/', views.section_detail, name='sections'),

    path('kategorien/', views.CategoriesListView.as_view(), name='categories'),
    path('kategorie/<str:name>/', views.category_detail, name='category-detail'),

    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('image/add/', views.upload_image, name='upload-image'),

    path('about/', views.about, name='about'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('impressum/', views.impressum, name='impressum'),

]
