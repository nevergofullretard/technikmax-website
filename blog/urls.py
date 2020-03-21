from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='blog-home'), #PostListView.as_view()

    # path('user/<str:username>', views.UserPostListView.as_view(), name='user-posts'),    #mit dem html-tags kann man auf Variablen zugreifen
    # path('blog/', views.PostListView.as_view(), name='blog'),
    path('post/<int:pk>/<str:name>/', views.PostDetailView.as_view(), name='post-detail'),    #<pk> heist primäry key = Primärschlüssel des Posts
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),


    path('art/<str:name>/', views.type_detail, name='types'),
    path('bereich/<str:name>/', views.section_detail, name='sections'),

    path('kategorien/', views.CategoriesListView.as_view(), name='categories'),
    path('kategorie/<str:name>/', views.category_detail, name='category-detail'),

    # path('projects/', views.ProjectsListView.as_view(), name='project'),
    # path('project/<int:pk>/<str:name>/', views.ProjectDetailView.as_view(), name='project-detail'),
    # # <pk> heist primäry key = Primärschlüssel des Posts
    # path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    # path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    # path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),

    path('image/add/', views.upload_image, name='upload-image'),
    # path('blogpost/add/', views.PostCreateView.as_view(), name='upload-blogpost'),


    path('about/', views.about, name='about'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('impressum/', views.impressum, name='impressum'),

]
