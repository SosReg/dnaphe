from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import requests, json
from bs4 import BeautifulSoup as bs
from .models import Post, Topic, Lang_tag, Comment
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .forms import CommentForm, LinkPostForm, TextPostForm, PostUpdateForm
from django.core.paginator import Paginator
import requests
from django.contrib import messages




# Create your views here.


def index(request):
    template = 'home/home.html'
    # context = [i for i in Post.objects.order_by('-date_posted', '-upvote') if (i.topic == 'news' and i.upvote != 0) or (i.topic != 'news')]
    context=[]
    for i in Post.objects.order_by('-date_posted', '-upvote'):
        if str(i.topic) != 'news':
            context.append(i)
        elif str(i.topic) == "news" and i.upvote != 0:
            context.append(i)
        else:
            pass

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 20)
    context = paginator.page(page)
    context = {'posts': context}
    return render(request, template, context)

def jpt(request):
	return render(request, 'home/verifyforzoho.html')

def popular(request):

    p = Post.objects.all()
    # q = p.order_by('-upvote','-date_posted')
    # r = [i for i in q if i.was_published_recently() and i.upvote>0]
    q = {i:i.comments.count() for i in p if i.upvote>0 or i.comments.count()>0}
    #print(q.values()) ### remove this
    max_comments_count = max(q.values(), default=0)
    if max_comments_count != 0:
        for i in q.keys():
            q[i] = q[i]/max_comments_count * 10

    max_upvote=max([i.upvote for i in q], default=0)
    if max_upvote != 0:
        for i in q.keys():
            q[i] = (q[i]+i.upvote/max_upvote * 10)/2

    qd = p.order_by('-date_posted')
    n = len(qd)
    q_d = {}
    for i in qd:
        q_d[i]=n
        n=n-1
    max_d = max(q_d.values())
    q_d = {i:(10* q_d[i]/max_d) for i in q_d}
    q_d = {i:((q[i]+q_d[i])/2) for i in q.keys()}

    qd_a = [[q_d[i], i] for i in q_d]

    qd_a.sort(reverse=True)

    context = [i[1] for i in qd_a]


    template = 'home/home.html'


    page = request.GET.get('page', 1)

    paginator = Paginator(context, 20)
    context = paginator.page(page)
    context = {'posts': context}

    return render(request, template, context)

def news(request):
    t = Topic.objects.filter(topic_text__icontains='news')
    p = Post.objects.filter(topic__in=t)
    q = p.order_by('-date_posted')
    context = [i for i in q if i.was_published_recently()]

    template = 'home/home.html'

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 20)
    context = paginator.page(page)
    context = {'posts': context}

    return render(request, template, context)

def botpage(request):
    template = 'home/bot_page.html'
    return render(request, template)

def onlineKhabarBot(request):
    page = requests.get('https://www.onlinekhabar.com/content/news')
    soup = bs(page.text, 'lxml')
    body = soup.body
    title = []
    content = []
    urls = []
    img_urls =[]
    for div in body.findAll('div', class_='item'):
        try:
            if div.a.text != '':
                title.append(div.a.text)
            for a in div.findAll('a'):
                if a.get('href') != '':
                    urls.append(a.get('href'))
            for p in div.findAll('p'):
                if p.text != '':
                    content.append(p.text)
            for img in div.findAll('img'):
                img_urls.append(img.get('src'))
        except:
            pass
    unique_urls = []
    for i in urls:
        if i not in unique_urls:
            unique_urls.append(i)

    post = []
    for i in range(len(title)):
        try:
            post.append([title[i], content[i], unique_urls[i], img_urls[i]])
        except:
            pass

    page.close()

    context = {'posts': post}

    return render(request, 'home/bot_content.html', context)

def botPost(request):
    page = requests.get('https://www.onlinekhabar.com/content/news')
    soup = bs(page.text, 'lxml')
    body = soup.body
    title = []
    content = []
    urls = []
    img_urls = []
    for div in body.findAll('div', class_='item'):
        try:
            if div.a.text != '':
                title.append(div.a.text)
            for a in div.findAll('a'):
                if a.get('href') != '':
                    urls.append(a.get('href'))
            for p in div.findAll('p'):
                if p.text != '':
                    content.append(p.text)
            for img in div.findAll('img'):
                img_urls.append(img.get('src'))
        except:
            pass
    unique_urls = []
    for i in urls:
        if i not in unique_urls:
            unique_urls.append(i)

    for i in range(len(title)):
        if title[i] not in [i.title for i in Post.objects.all()]:
            try:
                q = Post(
                    topic = Topic.objects.get(topic_text='news'),
                    language = Lang_tag.objects.get(lang_tag_text='nepali'),
                    title = title[i],
                    content = content[i],
                    date_posted = timezone.now(),
                    author = User.objects.get(username='dnapheBot'),
                    url = unique_urls[i],
                    img_url = img_urls[i],
                )
                q.save()
            except:
                pass

    page.close()

    return HttpResponseRedirect('/')

@login_required
def upvote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.upvote += 1
    post.save()
    returnid = '#paceholder_' + str(post.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + returnid)  ## '/%s' %returnid)

@login_required
def downvote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.downvote += 1
    post.save()
    returnid = '#paceholder_' + str(post.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + returnid)

class PostTextCreateView(LoginRequiredMixin, CreateView):
    # model = Post
    # fields = ['topic', 'language', 'title', 'content']
    model = Post
    form_class = TextPostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        clientkey = self.request.POST['g-recaptcha-response']
        secretkey = '6Lfz0vgZAAAAAM1H1w4l_d9Elr1-ft8jBmGwtpWW'
        captchaData = {
        'secret': secretkey,
        'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']

        if verify:
            return super().form_valid(form)
        else:
            messages.warning(self.request, f'Please validate the CAPTCHA!!!')
            form = TextPostForm(self.request.POST) 
        return render(self.request, 'home/post_form.html', {'form': form})

       
       


        #if len(str(form.instance.content)) > 50 and not str(form.instance.content).isspace():
        #    form.instance.content = form.instance.content[:45] + ' ' + form.instance.content[45:90] +'..'
 

# class PostLinkCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['topic', 'language', 'title', 'url']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

def PostDetailView(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts = [i for i in Post.objects.filter(pk=post.id)]
    # comment = [i for i in Comment.objects.filter(post=post)]
    comment = Comment.objects.filter(post=post)
    comments = [i for i in comment.order_by('date_posted')]
    context = {
        'posts': posts,
        'comments': comments
    }

    return render(request, 'home/post_detail.html', context)

@login_required
def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            form.instance.author = request.user
            comment.save()
            return redirect('post-detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'home/comment_form.html', {'form': form})

@login_required
def c_upvote(request, c_id):
    comment = get_object_or_404(Comment, pk=c_id)
    comment.comment_upvote += 1
    comment.save()
    returnid = '#paceholder_' + str(comment.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')+returnid)       ## '/%s' %returnid)
    # return HttpResponseRedirect(request,)

@login_required
def c_downvote(request, c_id):
    comment = get_object_or_404(Comment, pk=c_id)
    comment.comment_downvote += 1
    comment.save()
    returnid = '#paceholder_' + str(comment.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')+returnid)

def kantipurDailyBot(request):
    page = requests.get('https://www.kantipurdaily.com/news')
    soup = bs(page.text, 'lxml')
    body = soup.body
    title = []
    content = []
    urls = []
    img_urls =[]
    for article in body.findAll('article'):
        try:
            title.append(article.a.text)
            content.append(article.p.text)
            urls.append(article.a.get('href'))
            for j in article.findAll('div', class_='image'):
                img_urls.append(j.a.img.get('data-src'))
        except:
            pass

    clean_urls=[]

    for i in urls:
        clean_url = 'https://www.kantipurdaily.com'+i
        clean_urls.append(clean_url)

    clean_image_urls = []

    for i in img_urls:
        j = i.replace('usaa','usab')
        j = j.replace('lowquality/','')
        j = j.replace('-300x0-lowquality.jpg', '-1000x0.jpg')
        clean_image_urls.append(j)

    post = []
    for i in range(len(title)):
        try:
            post.append([title[i], content[i], clean_urls[i], clean_image_urls[i]])
        except:
            pass

    context = {'posts': post}

    page.close()

    return render(request, 'home/bot_content.html', context)

def kantipurbotPost(request):
    page = requests.get('https://www.kantipurdaily.com/news')
    soup = bs(page.text, 'lxml')
    body = soup.body
    title = []
    content = []
    urls = []
    img_urls =[]
    for article in body.findAll('article'):
        try:
            title.append(article.a.text)
            content.append(article.p.text)
            urls.append(article.a.get('href'))
            for j in article.findAll('div', class_='image'):
                img_urls.append(j.a.img.get('data-src'))
        except:
            pass

    clean_urls=[]

    for i in urls:
        clean_url = 'https://www.kantipurdaily.com'+i
        clean_urls.append(clean_url)

    clean_image_urls = []

    for i in img_urls:
        j = i.replace('usaa','usab')
        j = j.replace('lowquality/','')
        j = j.replace('-300x0-lowquality.jpg', '-1000x0.jpg')
        clean_image_urls.append(j)

    for i in range(len(title)):
        if title[i] not in [i.title for i in Post.objects.all()]:
            try:
                q = Post(
                    topic = Topic.objects.get(topic_text='news'),
                    language = Lang_tag.objects.get(lang_tag_text='nepali'),
                    title = title[i],
                    content = content[i],
                    date_posted = timezone.now(),
                    author = User.objects.get(username='dnapheBot'),
                    url = clean_urls[i],
                    img_url = clean_image_urls[i],
                )
                q.save()
            except:
                pass

    page.close()

    return HttpResponseRedirect('/')

def ratopatibot(request):
    page = requests.get('http://ratopati.com/category/news')
    soup = bs(page.text, 'lxml')
    body = soup.body
    title = []
    content = []
    urls = []
    img_urls = []
    for i in body.findAll('div', class_='item'):
        try:
            for j in i.findAll('div', class_='item-header'):
                img_urls.append(j.a.img.get('src'))
            for k in i.findAll('div', class_='item-content'):
                title.append(k.a.text)
                content.append(k.p.text)
                urls.append('http://ratopati.com' + k.a.get('href'))
        except:
            pass

    post = []
    for i in range(len(title)):
        try:
            post.append([title[i], content[i], urls[i], img_urls[i]])
        except:
            pass

    context = {'posts': post}

    page.close()

    return render(request, 'home/bot_content.html', context)

def ratopatibotPost(request):
    page = requests.get('http://ratopati.com/category/news')
    soup = bs(page.text, 'lxml')
    body = soup.body
    title = []
    content = []
    urls = []
    img_urls = []
    for i in body.findAll('div', class_='item'):
        try:
            for j in i.findAll('div', class_='item-header'):
                img_urls.append(j.a.img.get('src'))
            for k in i.findAll('div', class_='item-content'):
                title.append(k.a.text)
                content.append(k.p.text)
                urls.append('http://ratopati.com' + k.a.get('href'))
        except:
            pass

    for i in range(len(title)):
        if title[i] not in [i.title for i in Post.objects.all()]:
            try:
                q = Post(
                    topic = Topic.objects.get(topic_text='ratopati-News'),
                    language = Lang_tag.objects.get(lang_tag_text='nepali'),
                    title = title[i],
                    content = content[i],
                    date_posted = timezone.now(),
                    author = User.objects.get(pk=7),
                    url = urls[i],
                    img_url = img_urls[i],
                )
                q.save()
            except:
                pass
    page.close()
    return HttpResponseRedirect('/')

def canadanepalbot(request):
    page=requests.get('http://www.canadanepal.net/')
    soup = bs(page.text,'lxml')

    title=[]
    content=[]
    urls=[]
    img_urls=[]
    video_urls=[]

    body=soup.body

    for i in body.findAll('div',class_='mid_p'):
        title.append(i.p.text)
        urls.append(i.a.get('href'))

    for i in urls:
        page2 = requests.get(i)
        soup2 = bs(page2.text, 'lxml')
        link = soup2.findAll('iframe')
        a = ''
        for j in link:
            a = j.get('src')
        a = a.split('?')
        for k in a:
            if k.find('embed') > 0:
                a = k
        video_urls.append(a)
        page2.close()

    post = []
    for i in range(len(title)):
        try:
            post.append([title[i], urls[i], urls[i], video_urls[i]])
        except:
            pass

    context = {'posts': post}
    # page.close()

    return render(request, 'home/canada_nepal_bot_content.html', context)

def canadanepalbotPost(request):
    page=requests.get('http://www.canadanepal.net/')
    soup = bs(page.text,'lxml')

    title=[]
    content=[]
    urls=[]
    img_urls=[]
    video_urls=[]

    body=soup.body

    for i in body.findAll('div',class_='mid_p'):
        title.append(i.p.text)
        urls.append(i.a.get('href'))

    for i in urls:
        page2 = requests.get(i)
        soup2 = bs(page2.text, 'lxml')
        link = soup2.findAll('iframe')
        a = ''
        for j in link:
            a = j.get('src')
        a = a.split('?')
        for k in a:
            if k.find('embed') > 0:
                a = k
        video_urls.append(a)
        page2.close()

    for i in range(len(title)):
        if title[i] not in [i.title for i in Post.objects.all()]:
            try:
                q = Post(
                    topic = Topic.objects.get(topic_text='canadanepal'),
                    language = Lang_tag.objects.get(lang_tag_text='nepali'),
                    title = title[i],
                    content = urls[i],
                    date_posted = timezone.now(),
                    # author = User.objects.get(pk=8),
                    author = User.objects.get(username='dnapheBot'),
                    url = urls[i],
                    video_url = video_urls[i],
                )
                q.save()
            except:
                pass
    page.close()

    return HttpResponseRedirect('/')

def topicsHomeView(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    post = Post.objects.filter(topic=topic)

    posts = [i for i in post.order_by('-date_posted', '-upvote')]
    topics = [topic]

    context = {
        'topic': topics,
        'posts': posts,
    }

    return render(request, 'home/topics_home.html', context)

def userPostListView(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    posts = posts.order_by('-date_posted')
    comments = Comment.objects.filter(author=user)
    comments = comments.order_by('-date_posted')

    context = {
        'posts': posts,
        'user': [user],
        'comments': comments,
    }

    template = 'home/user_profile.html'

    return render(request, template, context)

@login_required
def LinkPostCreateView(request):
    # post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6Lfz0vgZAAAAAM1H1w4l_d9Elr1-ft8jBmGwtpWW'
        captchaData = {
        'secret': secretkey,
        'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']
        
        form = LinkPostForm(request.POST)
        if form.is_valid() and verify:
            post = form.save(commit=False)
            form.instance.author = request.user

            page = requests.get(post.url)
            soup = bs(page.content, 'html5lib')
            # soup = bs(page.text, 'lxml')

            for i in soup.select('meta'):
                if i.get('property') == 'og:title':
                    post.content = i.get('content')
                if i.get('property') == 'og:image':
                    post.img_url = i.get('content')
                if i.get('property') == 'og:site_name':
                    if i.get('content') == 'YouTube':
                        for j in soup.select('meta'):
                            if j.get('property') == 'og:video:secure_url':
                                a = j.get('content')
                                if a.find('embed') > 0:
                                    post.video_url=j.get('content')

            if post.content=='':
                if len(str(post.url))>30:
                    post.content=post.url[:30]+'...'
                else:
                    post.content=str(post.url)

            if len(str(post.content)) > 50 and str(post.content).find(' ')<0:
                post.content = post.content[:30]+' '+post.content[30:]

            VALID_IMAGE_EXTENSIONS = [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
            ]

            if post.img_url and any([post.img_url.endswith(e) for e in VALID_IMAGE_EXTENSIONS]):
                try:
                    requests.get(post.img_url)
                except:
                    try:
                        a = requests.get(post.url+post.img_url)
                        if a.status_code==200:
                            post.img_url=post.url+post.img_url
                        else:
                            post.img_url = '/static/home/default-link-img.png'
                    except:
                        post.img_url='/static/home/default-link-img.png'
            else:
                post.img_url='/static/home/default-link-img.png'

            post.save()
            page.close()
            return redirect('post-detail', post_id=post.id)
        if not verify:
            messages.warning(request, f'Please validate the CAPTCHA!!!')        

    else:
        form = LinkPostForm()
    return render(request, 'home/post_form.html', {'form': form})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # model = Post
    # fields = ['topic','language','title', 'content', 'url']

    model = Post
    form_class = PostUpdateForm

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_staff:
            return True

        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_staff:
            return True

        return False

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment_text']

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author or self.request.user.is_staff:
            return True

        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment


    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author or self.request.user.is_staff:
            return True

        return False

    def get_success_url(self):
        comment = self.get_object()
        success_url = '/post/%s' %comment.post.id
        if success_url:
            return success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

def searchView(request):
    if request.method=='GET':
        search_string = request.GET.get('search_input')
        t = Topic.objects.filter(topic_text__icontains=search_string)
        p = Post.objects.filter(title__icontains=search_string)
        p_c = Post.objects.filter(content__icontains=search_string)
        q = p.order_by('-date_posted')
        q_c = p_c.order_by('-date_posted')
        context = {
            'posts': q,
            'topics': t,
            'post_c': q_c
        }
        return render(request, 'home/search_results.html', context)





def gpbotPost(request):
    page = requests.get('https://gorkhapatraonline.com/mainnews')
    soup = bs(page.text, 'html5lib')
    body = soup.body
    title = []
    content = []
    urls = []
    img_urls = []
    # for div in body.findAll('div', class_='item'):
    #     try:
            # if div.a.text != '':
            #     title.append(div.a.text)
            # for a in div.findAll('a'):
            #     if a.get('href') != '':
            #         urls.append(a.get('href'))
            # for p in div.findAll('p'):
            #     if p.text != '':
            #         content.append(p.text)
            # for img in div.findAll('img'):
            #     img_urls.append(img.get('src'))


    for div in body.findAll('div',class_='business'):
        try:
        	urls.append(div.a.get('href'))
        	img_urls.append(div.find('div',class_='trending1').img.get('src'))
        	title.append(div.find('div',class_='trending2').find('p',class_='trand middle-font').text.strip())
        	content.append(div.find('div',class_='trending2').find('p',class_='description').text.strip())

        except:
            pass
    unique_urls = []
    for i in urls:
        if i not in unique_urls:
            unique_urls.append(i)

    for i in range(len(title)):
        if title[i] not in [i.title for i in Post.objects.all()]:
            try:
                q = Post(
                    topic = Topic.objects.get(topic_text='news'),
                    language = Lang_tag.objects.get(lang_tag_text='nepali'),
                    title = title[i],
                    content = content[i],
                    date_posted = timezone.now(),
                    author = User.objects.get(username='dnapheBot'),
                    url = unique_urls[i],
                    img_url = img_urls[i],
                )
                q.save()
            except:
                pass

    page.close()

    return HttpResponseRedirect('/news')


def ytbotPost(request):

    api_key = "AIzaSyCuaUvnhxfNpcxcfHsl1l09scXwfNvGL8Q"
    maxResults=25
    part = "snippet,contentDetails,statistics"
    chart = "mostPopular"
    url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&chart={chart}&maxResults={maxResults}&regionCode=NP&key={api_key}"

    page = requests.get(url)

    page_json = page.json()

    page.close()

    title = []
    video_urls=[]
    content = []

    for i in page_json['items']:
        video_urls.append("https://youtube.com/embed/"+i['id'])
        title.append(i['snippet']['title'])
        content.append(i['snippet']['title'])

    for i in range(len(title)):
        if title[i] not in [i.title for i in Post.objects.all()]:
            try:
                q = Post(
                    topic = Topic.objects.get(topic_text='youtube-nepali'),
                    language = Lang_tag.objects.get(lang_tag_text='nepali'),
                    title = title[i],
                    content = content[i],
                    date_posted = timezone.now(),
                    author = User.objects.get(username='dnapheBot'),
                    video_url = video_urls[i],
                    # url = unique_urls[i],
                    # img_url = img_urls[i],
                )
                q.save()
            except:
                pass

    # page.close()

    return HttpResponseRedirect('/')
