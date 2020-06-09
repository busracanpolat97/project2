import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ
from note.models import Note, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Note.objects.all()[:4]
    category = Category.objects.all()
    daynotes= Note.objects.all()[:4]
    lastnotes = Note.objects.all().order_by('-id')[:4]
    randomnotes = Note.objects.all().order_by('?')[:4]


    context = {'setting': setting,
               'category' : category,
               'page':'home',
               'sliderdata':sliderdata,
               'daynotes': daynotes,
               'lastnotes': lastnotes,
               'randomnotes': randomnotes
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'hakkimizda', 'category': category}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'referanslar', 'category': category}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):

    if request.method == 'POST':
        form=ContactFormu(request.POST)
        if form.is_valid():
            data=ContactFormMessage() #model ile bağlantı kur
            data.name=form.cleaned_data['name']  #formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save() #veritabanına kaydet
            messages.success(request,'Mesajınız başarıyla gönderilmiştir. Teşekkür ederiz...')
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form=ContactFormu()
    category = Category.objects.all()
    context={'setting':setting, 'form': form, 'category': category}
    return render(request, 'iletisim.html', context)

def category_notes(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    notes = Note.objects.filter(category_id=id)
    context = {'notes': notes,
               'category': category,
               'categorydata': categorydata}
    return render(request,'notes.html',context)

def note_detail(request,id,slug):
    category = Category.objects.all()
    note = Note.objects.get(pk=id)
    images= Images.objects.filter(note_id=id)
    comment= Comment.objects.filter(note_id=id, status='True')
    context = {'note': note,
               'category': category,
               'images': images,
               'comment': comment}
    return render(request,'note_detail.html',context)

def note_search(request):
    if request.method == 'POST':
        form= SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()

            query =form.cleaned_data['query']
            catid= form.cleaned_data['catid']
            if catid ==0:
                notes=Note.objects.filter(title__icontains=query)
            else:
                notes= Note.objects.filter(title__icontains=query, category_id=catid)

            #return HttpResponse(notes)
            context = {'notes': notes,
                       'category': category,
                       }
            return render(request, 'notes_search.html',context)
    return HttpResponseRedirect('/')

def note_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    notes = Note.objects.filter(title__icontains=q)
    results = []
    for rs in notes:
      note_json = {}
      note_json = rs.title
      results.append(note_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı yada şifre yanlış ")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request,'login.html',context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            current_user= request.user
            data= UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user"
            data.save()
            messages.success(request,"Hoşgeldiniz... Sitemize başarılı bir şekilde üye oldunuz.")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
                'form': form,
               }

    return render(request, 'signup.html', context)


def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('notenumber')
    context = {'category': category,
               'faq': faq,
               'setting': setting,
               }
    return render(request, 'faq.html', context)