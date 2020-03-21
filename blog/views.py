from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django import forms

from .models import Post, Images, Project, Category, Type, Section
from .forms import UploadImageForm, PostForm

deutsch = ['Haus', 'Weihnachten', 'Wollen', 'möchten', 'sprechen', 'besuchen']
italienisch = ['Casa', 'Natale', 'volere', 'prendere', 'parlare', 'visitare']



def remove_spaces(title):
    title_tag = ''
    for i in range(len(title)):
        letter = title[i]
        if letter == ' ' or letter == '.' or letter == '/' or letter == '_' or letter == '-':
            try:
                last = title[i-1]
                next = title[i + 1]
                if next == ' ' or next == '.' or next == '/' or next == '_' or next == '-' \
                       or last == ' ' or last == '.' or last == '/' or last == '_' or last == '-':
                    pass

                else:
                    title_tag += '-'
            except IndexError:
                pass
        else:
            title_tag += letter

    return title_tag

class PostListView(ListView):
    model = Post
    template_name = 'blog/blog_home.html' # <app>/<model>_<viewtype>.html in diesem fall blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-date'] # das heißt vom neuesten zum ältesten
    paginate_by = 5 #das heißt, dass nach dem 2. Post eine neue Seite kommt


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Blog"
        context['des'] = "Blog über Technik-Themen, Programmieren und Engineering"
        context['keywords'] = "Blog, Programmieren"
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date') # das filtert die Posts, sodass nur diejenigen
                                                                        # aufscheinen, die der User geschrieben hat



class PostDetailView(DetailView):
    model = Post


    def get_context_data(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()
        obj = super().get_object(queryset=queryset)

        context = super().get_context_data(**kwargs)
        context['title'] = obj.title
        context['des'] = obj.description
        keywords = ""
        for cat in obj.categories.all():
            keywords += str(cat) + ", "
        context['keywords'] = keywords

        suggestions = []
        cat_ids = [x.id for x in obj.categories.all()]
        next_id = None

        if obj.next:
            suggestions.append([obj.next])
            next_id = obj.next.id
        else:
            suggestions.append([])

        best_sugg = {}
        for post in Post.objects.filter(type=obj.type ,categories__id__in=cat_ids).exclude(id=next_id).exclude(id=obj.id):
            same = 0
            post_cat_ids = [x.id for x in post.categories.all()]
            for cat in post_cat_ids:
                if cat in cat_ids:
                    same += 1

            best_sugg[post] = same


        suggestions.append([k for k, v in sorted(best_sugg.items(), key=lambda item: item[1])][::-1])

        context['suggestions'] = suggestions
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'title', 'description', 'date', 'type', 'categories', 'background_image', 'next']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        title = form.instance.title


        form.instance.title_tag = remove_spaces(title)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images_query'] = Images.objects.all()[::-1]
        return context





class PostUpdateView(UpdateView, LoginRequiredMixin):
    model = Post
    fields = ['content', 'title', 'description', 'date', 'type', 'categories', 'background_image', 'next']
    template_name = 'blog/post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        title = form.instance.title

        form.instance.title_tag = remove_spaces(title)

        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images_query'] = Images.objects.all()[::-1]
        return context


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    success_url = '/'

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


def compare_date_list(list1, list2): # for comaparing DATES!
    final_list = []
    if not list1:
        for i in list2:
            final_list.append({'project': i})
        return final_list

    if not list2:
        for i in list1:
            final_list.append({'blog': i})
        return final_list

    else:

        for blog, project in zip(list1, list2):
            if blog.date > project.date:
                final_list.extend([{'blog': blog}, {'project': project}])
            else:
                final_list.extend([{'project': project}, {'blog': blog}])

        return final_list


def home(request):
    posts = Post.objects.all().order_by('-date')

    newest = posts


    title = "Tech-Blog und Projekte"
    des = "Interessantes bis hin zu Must-Know über Prorammieren von Hardware sowie Software, Sicherheit im Netz und generell Technik-Themen"
    keywords = "Technik, Programming, Programmieren, Projekte, Blog"
    topics = []

    for post in posts:
        for cat in post.categories.all():
            if cat not in topics and len(topics) < 4:
                topics.append(cat)
    return render(request, 'blog/home.html', {'newest': newest, 'title': title, 'des': des, 'keywords': keywords, 'topics': topics, 'types': Type.objects.all()})

def about(request):
    return render(request, 'blog/about.html', {'title': 'Über mich'})

def kontakt(request):
    return render(request, 'blog/contact.html', {'title': 'Kontakt'})

def impressum(request):
    return render(request, 'blog/impressum.html', {'title': 'Impressum & Datenschutz'})
''' Projects ab hier'''

# class ProjectsListView(ListView):
#     model = Project
#     template_name = 'blog/project_home.html' # <app>/<model>_<viewtype>.html in diesem fall blog/post_list.html
#     context_object_name = 'posts'
#     ordering = ['-date'] # das heißt vom neuesten zum ältesten
#     paginate_by = 5 #das heißt, dass nach dem 2. Post eine neue Seite kommt
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Projekte"
#         context['des'] = "Projekte über Programmieren mit High-Level und Low-Level Languages sowie Technik-Themen"
#         context['keywords'] = "Projekte, Programmieren"
#         return context
#
#
# class ProjectDetailView(DetailView):
#     model = Project
#
#     def get_context_data(self, queryset=None, **kwargs):
#         if queryset is None:
#             queryset = self.get_queryset()
#         obj = super().get_object(queryset=queryset)
#
#         context = super().get_context_data(**kwargs)
#         context['title'] = obj.title
#         context['des'] = obj.description
#         keywords = ""
#         for cat in obj.categories.all():
#             keywords += str(cat) + ", "
#         context['keywords'] = keywords
#         return context
#
# class ProjectCreateView(LoginRequiredMixin, CreateView):
#     model = Project
#     fields = ['content', 'title', 'description', 'date', 'categories', 'font_color', 'background_color', 'background_image', 'github']
#     template_name = 'blog/project_form.html'
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#
#         title = form.instance.title
#
#
#         form.instance.title_tag = remove_spaces(title)
#
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(context)
#         context['images_query'] = Images.objects.all()[::-1]
#         return context
#
#
#
#
# class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
#     model = Project
#     fields = ['content', 'title', 'description', 'date', 'categories', 'font_color', 'background_color',
#               'background_image', 'github']
#     template_name = 'blog/project_form.html'
#
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#
#         title = form.instance.title
#
#
#         form.instance.title_tag = remove_spaces(title)
#
#         return super().form_valid(form)
#
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['images_query'] = Images.objects.all()
#         return context
#
#
# class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Project
#     success_url = '/'
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False


'''Categories ab hier !'''



def section_detail(request, name):
    sec = get_object_or_404(Section.objects.all(), name=name)
    cats = Category.objects.filter(section=sec)

    posts = []
    for cat in cats:
        post = Post.objects.filter(categories__id__in=[cat.id]).order_by('-date')
        posts.extend(post)

    newest = posts

    pre = 'Beiträge über '
    title = str(sec.name)
    des = sec.description
    keywords = "Technik, Programming, Programmieren, Projekte, Blog, " + str(sec.name)
    color = sec.color
    return render(request, 'blog/category_detail.html', {'cat': sec, 'newest': newest, 'title': title, 'des': des, 'keywords': keywords, 'color': color, 'pre': pre})

def type_detail(request, name):
    cat = get_object_or_404(Type.objects.all(), name=name)

    posts = Post.objects.filter(type__id__in=[cat.id]).order_by('-date')
    newest = posts

    title = "Alle " + str(cat.name)
    des = cat.description
    keywords = str(cat.name)

    return render(request, 'blog/category_detail.html', {'cat': cat, 'newest': newest, 'title': title, 'des': des, 'keywords': keywords})


class CategoriesListView(ListView):
    model = Category
    template_name = 'blog/categories_home.html' # <app>/<model>_<viewtype>.html in diesem fall blog/post_list.html
    context_object_name = 'categories'
    ordering = ['name']
    paginate_by = 50 #das heißt, dass nach dem 2. Post eine neue Seite kommt

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Kategorien"
        context['des'] = "Kategorien zu Blogs und Projekte über Programmieren mit High-Level und Low-Level Languages sowie Technik-Themen"
        context['keywords'] = "Blog, Programmieren"
        cats = {}

        for sect in Section.objects.all():
            cats[sect] = Category.objects.filter(section=sect)

        context['cats'] = cats
        return context

def category_detail(request, name):
    cat = get_object_or_404(Category.objects.all(), name=name)

    posts = Post.objects.filter(categories__id__in=[cat.id]).order_by('-date')
    newest = posts
    pre = 'Beiträge über '
    title =  str(cat.name)
    des = cat.description
    keywords = "Technik, Programming, Programmieren, Projekte, Blog, " + str(cat.name)
    color = cat.section.color
    return render(request, 'blog/category_detail.html', {'cat': cat, 'newest': newest, 'title': title, 'des': des, 'keywords': keywords, 'color': color, 'pre':pre})


''' FIXING ORIENTATION BUG LATER;
First help site:
 https://medium.com/@giovanni_cortes/rotate-image-in-django-when-saved-in-a-model-8fd98aac8f2a
 https://www.google.com/search?hl=de&q=why%20django%20rotates%20images
 '''
@login_required
def upload_image(request):
    if request.method == 'POST':

        form = UploadImageForm(request.POST or None, request.FILES or None)
        name = request.POST.get('name')
        type = request.FILES['image'].content_type.split('/')[1]
        new_name = str(name) + "." + str(type)

        request.FILES['image'].name = new_name

        if form.is_valid():

            form.save()
            messages.success(request, 'Das Bild wurde hochgeladen')
        # else:
        #     print(form.errors)
    else:
        form = UploadImageForm()

    return render(request, 'blog/image.html', {'form': form})

# @login_required
# def upload_blogpost(request):
#     class LinkImageForm(forms.Form):
#         images = []
#         for image in Images.objects.all():
#             images.append((image.image.url, image.name))
#
#         bild = forms.ChoiceField(choices=images)
#
#
#     if request.method == 'POST':
#         content_form = PostForm(request.POST)
#         if content_form.is_valid():
#             title = request.POST.get('title')
#             content = content_form.cleaned_data.get('content')




        # return HttpResponseRedirect(reverse("post-detail", args=[post.id]))

    # else:
    #     content_form = PostForm()
    #     image = LinkImageForm()
    # return render(request, 'blog/new_post.html', {'form': content_form, 'image': image})