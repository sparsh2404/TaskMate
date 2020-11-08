from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import tasklist
from .form import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required()
def todolist(request):
    if request.method == "POST":
        form = Taskform(request.POST or None )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,("New Task Added"))
        return redirect('todolist')
    else:

        all_task = tasklist.objects.filter(manage = request.user)
        paginator = Paginator(all_task,2)
        page = request.GET.get('pg')
        all_task = paginator.get_page(page)
        return render(request,'todolist.html',{'all_task':all_task})

@login_required()
def delete_task(request,task_id):
    task = tasklist.objects.get(pk = task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request, ("Acess Restricted, you are not allowed to acess!"))

    return redirect('todolist')


@login_required()
def edit_task(request,task_id):
    if request.method == "POST":
        task = tasklist.objects.get(pk=task_id)
        form = Taskform(request.POST or None ,instance=task)
        if form.is_valid():
            form.save()

        messages.success(request, ("Task UpDated"))
        return redirect('todolist')
    else:

        task__odj = tasklist.objects.get(pk = task_id)
        return render(request, 'edit.html', {'task_obj': task__odj})


@login_required()
def complete_task(request,task_id):
    task = tasklist.objects.get(pk = task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request,("Acess Restricted, you are not allowed to acess!"))
    return redirect('todolist')


@login_required()
def pending_task(request,task_id):
    task = tasklist.objects.get(pk = task_id)
    task.done = False
    task.save()

    return redirect('todolist')


def index(request):
    context = {
        'welcome_index': " sparsh welcome to index page"
    }
    return render(request,'index.html',context)



def contact(request):
    context = {
        'welcome_contact': " sparsh welcome to contact page"
    }
    return render(request,'contact.html',context)


def about(request):
    context = {
        'welcome_about': " sparsh welcome to about page"
    }
    return render(request,'about.html',context)
