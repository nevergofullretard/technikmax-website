from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


from .models import Post, Images, Category, Type, Section, Texte
from .forms import UploadImageForm

deutsch = ['Haus', 'Weihnachten', 'Wollen', 'möchten', 'sprechen', 'besuchen']
italienisch = ['Casa', 'Natale', 'volere', 'prendere', 'parlare', 'visitare']



def remove_spaces(title):
    title_tag = ''
    for i in range(len(title)):
        letter = title[i].lower()
        if letter == ' ' or letter == '.' or letter == '/' or letter == '_' or letter == '-' or letter == '?' or letter == '!' or letter =='&' or letter == ':':
            try:
                last = title[i-1]
                next = title[i + 1]
                if next == ' ' or next == '.' or next == '/' or next == '_' or next == '-' \
                       or last == ' ' or last == '.' or last == '/' or last == '_' or last == '-' or letter == '?' or letter == '!' or letter =='&' or letter == ':':
                    pass

                else:
                    title_tag += '-'
            except IndexError:
                pass

        elif letter == 'ö':
            title_tag += 'oe'
        elif letter == 'ä':
            title_tag += 'ae'
        elif letter == 'ü':
            title_tag += 'ue'


        else:
            title_tag += letter

    return title_tag



class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(published=True)
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html in diesem fall blog/post_list.html
    context_object_name = 'newest'
    ordering = ['-date'] # das heißt vom neuesten zum ältesten
    paginate_by = 7 #das heißt, dass nach dem 2. Post eine neue Seite kommt


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Technik Blog und Projekte"
        context['des'] = "Interessantes bis hin zu Must-Know über  Hardware sowie Software, Sicherheit im Netz und generell Technik-Themen"
        context['meta_des'] = "Interessantes bis hin zu Must-Know über Prorammieren von Hardware sowie Software, Sicherheit im Netz und generell Technik-Themen"
        context['keywords'] = "Technik, Programming, Programmieren, Projekte, Blog, Software, Hardware, Internet"
        topics = []
        context['unpublished'] = Post.objects.filter(published=False)
        posts = Post.objects.all().order_by('-date')
        for post in posts:
            for cat in post.categories.all():
                if cat not in topics and len(topics) < 4:
                    topics.append(cat)
        context['topics'] = topics
        context['types'] = Type.objects.all()

        return context


class PostDetailView(UserPassesTestMixin, DetailView):
    model = Post

    def test_func(self):
        queryset = self.get_queryset()
        obj = super().get_object(queryset=queryset)
        if obj.published == False:
            raise Http404
        else:
            return obj





    def get_context_data(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()
        obj = super().get_object(queryset=queryset)

        context = super().get_context_data(**kwargs)
        context['title'] = obj.title
        context['des'] = obj.description
        context['meta_des'] = obj.meta_description
        if obj.background_image:
            context['img'] = str(obj.background_image.image.url)
        keywords = ""
        for cat in obj.categories.all():
            keywords += str(cat) + ", "
        context['keywords'] = keywords


        cat_ids = [x.id for x in obj.categories.all()]
        next_id = None



        best_sugg = {}
        if obj.next:
            sim_posts = Post.objects.filter(categories__id__in=cat_ids).exclude(id=obj.next.id).exclude(id=obj.id)
        else:
            sim_posts = Post.objects.filter(categories__id__in=cat_ids).exclude(id=obj.id)

        for post in sim_posts:
            same = 0
            post_cat_ids = [x.id for x in post.categories.all()]
            for cat in post_cat_ids:
                if cat in cat_ids:
                    same += 1

            best_sugg[post] = same

        suggestions = [k for k, v in sorted(best_sugg.items(), key=lambda item: item[1])][::-1]


        paginator = Paginator(suggestions, 5)
        page = self.request.GET.get('page')
        suggestions = paginator.get_page(page)

        context['newest'] = suggestions
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'title', 'description', 'meta_description', 'date', 'type', 'categories', 'background_image', 'next', 'published']
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
    fields = ['content', 'title', 'description', 'meta_description', 'date', 'type', 'categories', 'background_image', 'next', 'published']
    template_name = 'blog/post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        title = form.instance.title
        form.instance.last_mod = timezone.now()
        print(form.instance.last_mod)

        form.instance.title_tag = remove_spaces(title)

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images_query'] = Images.objects.all()[::-1]
        return context


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    success_url = '/'


def about(request):

    return render(request, 'blog/about.html', {'title': 'Über mich','meta_des': 'Über Technikmax, die Person dahinter und Intentionen', 'content': Texte.objects.get(title="about")})

def kontakt(request):
    return render(request, 'blog/contact.html', {'title': 'Kontakt', 'meta_des': 'Technikmax Kontaktmöglichkeiten'})

def impressum(request):
    return render(request, 'blog/impressum.html', {'title': 'Impressum & Datenschutz', 'meta_des': 'Technikmax Impressum & Datenschutz'})
''' Projects ab hier'''




def section_detail(request, name):
    sec = get_object_or_404(Section.objects.all(), tag_name=name)
    cats = Category.objects.filter(section=sec)

    posts = []
    for cat in cats:
        post = Post.objects.filter(categories__id__in=[cat.id]).order_by('-date')
        posts.extend(post)

    paginator = Paginator(posts, 7)
    page = request.GET.get('page')
    newest = paginator.get_page(page)
    meta_des = sec.meta_description

    pre = 'Beiträge über '
    title = str(sec.name)
    des = sec.description
    keywords = "Technik, Programming, Programmieren, Projekte, Blog, " + str(sec.name)
    return render(request, 'blog/category_detail.html', {'meta_des': meta_des, 'cat': sec, 'newest': newest, 'title': title, 'des': des, 'keywords': keywords, 'color': sec.color, 'pre': pre})

def type_detail(request, name):
    cat = get_object_or_404(Type.objects.all(), tag_name=name)

    posts = Post.objects.filter(type__id__in=[cat.id]).order_by('-date')
    paginator = Paginator(posts, 7)
    page = request.GET.get('page')
    newest = paginator.get_page(page)


    title = "Alle " + str(cat.name)
    des = cat.description
    keywords = str(cat.name)
    meta_des = cat.meta_description

    return render(request, 'blog/category_detail.html', {'meta_des': meta_des, 'cat': cat, 'newest': newest, 'title': title, 'des': des, 'keywords': keywords})


class CategoriesListView(ListView):
    model = Category
    template_name = 'blog/categories_home.html' # <app>/<model>_<viewtype>.html in diesem fall blog/post_list.html
    context_object_name = 'categories'
    ordering = ['name']
    # paginate_by = 50 #das heißt, dass nach dem 2. Post eine neue Seite kommt

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
    cat = get_object_or_404(Category.objects.all(), tag_name=name)

    posts = Post.objects.filter(categories__id__in=[cat.id]).order_by('-date')

    paginator = Paginator(posts, 7)
    page = request.GET.get('page')
    newest = paginator.get_page(page)

    pre = 'Beiträge über '
    title =  str(cat.name)
    des = cat.description
    keywords = "Technik, Programming, Programmieren, Projekte, Blog, " + str(cat.name)
    color = cat.section.color
    meta_des = cat.meta_description
    return render(request, 'blog/category_detail.html', {'meta_des': meta_des, 'newest': newest, 'cat': cat, 'title': title, 'des': des, 'keywords': keywords, 'color': color, 'pre':pre})



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
        print(type)
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

