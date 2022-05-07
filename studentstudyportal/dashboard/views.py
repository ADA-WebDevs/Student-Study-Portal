from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.views import generic

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request, 'The notes "{}" was added successfully'.format(notes.title))
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    data = {'notes':notes, 'form':form}
    return render(request, 'dashboard/notes.html', data)

def delete_notes(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes

def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homework.save()
            messages.success(request, 'The homework "{}" was added successfully'.format(homework.title))
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    data = {'homeworks':homework, 'homework_done':homework_done, 'form':form}
    return render(request, 'dashboard/homework.html', data)

def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def youtube(request):
    form = SearchForm()
    data = {'form':form}
    return render(request, 'dashboard/youtube.html', data)