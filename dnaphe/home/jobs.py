
import requests, sys, time
from bs4 import BeautifulSoup as bs
from django.shortcuts import render

from .models import Post, Topic, Lang_tag, T_Jobs
from django.utils import timezone
from django.contrib.auth.models import User


## time declarations
minute = 60
hour = 60 * minute
half_day = 12 * hour
full_day = 24 * hour
week = 7 * full_day
month = 30 * full_day
year = 12 * month

## job = gorkhapatra_news
def gp_news():
    try:
        job = T_Jobs.objects.get(job_name="gorkhapatra_news")
        if job.trigger == 1:
            try:
                page = requests.get('https://gorkhapatraonline.com/mainnews')
                soup = bs(page.text, 'html5lib')
                body = soup.body
                title = []
                content = []
                urls = []
                img_urls = []

                for div in body.findAll('div', class_='business'):
                    try:
                        urls.append(div.a.get('href'))
                        img_urls.append(div.find('div', class_='trending1').img.get('src'))
                        title.append(div.find('div', class_='trending2').find('p', class_='trand middle-font').text.strip())
                        content.append(div.find('div', class_='trending2').find('p', class_='description').text.strip())

                    except:
                        job.job_msg = str(timezone.now()) + ": could not access elements in the gorkhapatra page. \n" + sys.exc_info()[0]
                        job.save()
                unique_urls = []
                for i in urls:
                    if i not in unique_urls:
                        unique_urls.append(i)

                for i in range(len(title)):
                    if title[i] not in [i.title for i in Post.objects.all()]:
                        try:
                            q = Post(
                                topic=Topic.objects.get(topic_text='news'),
                                language=Lang_tag.objects.get(lang_tag_text='nepali'),
                                title=title[i],
                                content=content[i],
                                date_posted=timezone.now(),
                                author=User.objects.get(username='dnapheBot'),
                                url=unique_urls[i],
                                img_url=img_urls[i],
                            )
                            q.save()
                            job.job_msg = str(timezone.now()) + " job ran successfully."
                            job.save()
                            page.close()

                        except:
                            job.job_msg = str(timezone.now()) + ": could not post to the model. \n" + sys.exc_info()[0]
                            job.save()

            except:
                job.job_msg = str(timezone.now()) + ": could not access the gorkhapatra page. \n" + sys.exc_info()[0]
                job.save()


    except:
        job = T_Jobs.objects.get(job_name="gorkhapatra_news")
        job.job_msg = str(timezone.now()) + ": could not get the job table from model. \n" + sys.exc_info()[0]
        job.save()

## job = kantipur_news
def kantipur_news():
    try:
        job = T_Jobs.objects.get(job_name="kantipur_news")
        if job.trigger:
            try:
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
                        job.job_msg = str(timezone.now()) + ": couldn't get the content from the page. \n Error: \n" + sys.exc_info()[0]
                        job.trigger = 0
                        job.save()

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
                            job.job_msg = str(timezone.now()) + ": couldn't create posts. \n Error: \n" + sys.exc_info()[0]
                            job.trigger = 0
                            job.save()

                page.close()
                job.job_msg = str(timezone.now()) + ": Job ran successfully."
                job.dte_last_update = timezone.now()
                job.save()
            except:
                # job = T_Jobs.objects.get(job_name="kanitpur_news")
                job.job_msg = str(timezone.now()) + ": couldn't get the content from url. \n Error: \n" + sys.exc_info()[0]
                job.trigger = 0
                job.save()
    except:
        job = T_Jobs.objects.get(job_name="kanitpur_news")
        job.job_msg = str(timezone.now()) + ": couldn't fetch the job from the database. \n Error: \n" + sys.exc_info()[0]
        job.trigger = 0
        job.save()

## job = ok_news
def ok_news():
    try:
        job = T_Jobs.objects.get(job_name="ok_news")
        if job.trigger:
            try:
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
                        job.job_msg = str(timezone.now()) + ": couldn't get the contents from the page. \n Error: \n" + sys.exc_info()[0]
                        job.trigger = 0
                        job.save()
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
                            job.job_msg = str(timezone.now()) + ": couldn't get the url requested. \n Error: \n" + sys.exc_info()[0]
                            job.trigger = 0
                            job.save()
                page.close()
                job.job_msg = str(timezone.now()) + ": Job ran succesfully."
                job.dte_last_update = timezone.now()
                job.save()

            except:
                job.job_msg = str(timezone.now()) + ": couldn't get the url requested. \n Error: \n" + sys.exc_info()[0]
                job.trigger = 0
                job.save()
    except:
        job = T_Jobs.objects.get(job_name="kanitpur_news")
        job.job_msg = str(timezone.now()) + ": couldn't fetch the job from the database. \n Error: \n" + sys.exc_info()[0]
        job.trigger = 0
        job.save()

## job = yt_most_popular_nepal
def yt_most_popular_nepal():
    try:
        job = T_Jobs.objects.get(job_name="yt_most_popular_nepal")
        if job.trigger:
            try:
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
                            job.job_msg = str(timezone.now()) + ": couldn't post to the Posts in database. \n Error: \n" + sys.exc_info()[0]
                            job.trigger = 0
                            job.save()

                job.job_msg = str(timezone.now()) + ": Job ran successfully."
                job.dte_last_update = timezone.now()
                job.save()

            except:
                job.job_msg = str(timezone.now()) + ": something went wrong connecting to api. \n Error: \n" + sys.exc_info()[0]
                job.trigger = 0
                job.save()
    except:
        job = T_Jobs.objects.get(job_name="yt_most_popular_nepal")
        job.job_msg = str(timezone.now()) + ": couldn't get the job from the database. \n Error: \n" + sys.exc_info()[0]
        job.trigger = 0
        job.save()


def coz_func(request):
    while T_Jobs.objects.get(job_name="master_job").trigger:
        gp_news()
        kantipur_news()
        ok_news()
        yt_most_popular_nepal()
        time.sleep(half_day)

    return HttpResponseRedirect('/')

def jobs_page(request):
    template = "home/jobs_page.html"
    #jobs = [i for i in T_Jobs.objects.all()]
    jobs = T_Jobs.objects.all()
    context = {'jobs': jobs}
    return render(request, template, context)
