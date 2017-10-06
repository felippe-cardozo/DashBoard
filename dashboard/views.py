from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import DocumentForm, TaskForm
from .models import Document, Task
from .search import index_to_es


@login_required
def log_out(request):
    logout(request)
    return redirect('dashboard')


@login_required
def dashboard(request):
    task_list = Task.objects.all().filter(status='processada')
    paginator = Paginator(task_list, 20)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    return render(request, 'dashboard/dashboard.html', {'tasks': tasks})


@login_required
def new(request):
    task_form = TaskForm
    document_form = DocumentForm()
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES)
        if task_form.is_valid() and document_form.is_valid():
            task = task_form.save(commit=False)
            task.author = request.user
            task.save()
            files = request.FILES.getlist('upload')
            for f in files:
                Document.objects.create(upload=f, task=task)
            task.status = 'processada'
            task.save()
            return redirect('detail', task_id=task.id)
    return render(request, 'dashboard/new.html', {'d_form': document_form,
                                                  't_form': task_form})


@login_required
def update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task_form = TaskForm(instance=task)
    document_form = DocumentForm()
    documents = task.document_set.all()
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)
        document_form = DocumentForm(request.POST, request.FILES)
        if task_form.is_valid() and document_form.is_valid():
            task_form.save()
            files = request.FILES.getlist('upload')
            for f in files:
                Document.objects.create(upload=f, task=task)
            marked_to_del = request.POST.getlist('documents')
            if marked_to_del:
                for f in marked_to_del:
                    Document(pk=f).upload.delete()
                    Document(pk=f).delete()
            return redirect('detail', task_id=task.id)
    return render(request, 'dashboard/update.html', {
        't_form': task_form, 'd_form': document_form, 'docs': documents,
        'task_id': task_id
        })


@login_required
def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    docs = task.document_set.all()
    return render(request, 'dashboard/detail.html', {'task': task,
                                                     'docs': docs})


@login_required
def destroy(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.document_set.all():
        [d.upload.delete() for d in task.document_set.all()]
    task.delete()
    return redirect('dashboard')


@login_required
def mark_as_done(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id)
        task.status = 'done'
        task.done_user = request.user
        task.save()
        index_to_es(task)
        return redirect('dashboard')
    return redirect('dashboard')
