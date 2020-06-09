from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from home.models import UserProfile, Setting
from note.models import Category, Comment, Note, NoteForm, NoteImageForm, Images
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(pk=current_user.id)
    context= {'category': category,
              'profile': profile}
    return render(request, 'user_profile.html',context)

def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form= ProfileUpdateForm(request.POST,request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profilin Güncellendi')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

def change_password(request):
    if request.method=='POST':
        form =PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla değiştirilmiştir.')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Lütfen aşağıdaki hatayı düzeltin!<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form =PasswordChangeForm(request.user)
        return render(request,'change_password.html', {
            'form': form, 'category': category
        })

@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments= Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comment.html', context)

@login_required(login_url='/login')
def deletecomment(request, id):
    current_user =request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Yorumunuz silindi..')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')  # Check login
def notes(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    note = Note.objects.filter(user_id=current_user.id, status='True')
    context = {
        'category': category,
        'note': note,
        'setting': setting,
    }
    return render(request, 'user_notes.html', context)


@login_required(login_url='/login')  # Check login
def addnote(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Note()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.category = form.cleaned_data['category']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.status = 'False'
            data.save()  # veritabanına kaydet
            messages.success(request, 'Your Content Insterted Successfuly')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.success(request, 'Note Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/addnote')
    else:
        category = Category.objects.all()
        form = NoteForm()
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_addnote.html', context)


@login_required(login_url='/login')  # Check login
def noteedit(request, id):
    setting = Setting.objects.get(pk=1)
    note = Note.objects.get(id=id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Product Updated Successfuly')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.success(request, 'Product Form Error: ' + str(form.errors))
            return HttpResponseRedirect('/user/addnote/' + str(id))
    else:
        category = Category.objects.all()
        form = NoteForm(instance=note)
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_addnote.html', context)


@login_required(login_url='/login')  # Check login
def notedelete(request, id):
    current_user = request.user
    Note.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Note deleted...')
    return HttpResponseRedirect('/user/notes')


def noteaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = NoteImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.note_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfuly uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error: ' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        note = Note.objects.get(id=id)
        images = Images.objects.filter(note_id=id)
        form = NoteImageForm()
        context = {
            'note': note,
            'images': images,
            'form': form,
        }
        return render(request, 'note_gallery.html', context)