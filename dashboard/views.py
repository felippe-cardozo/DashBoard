from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


@login_required
def upload(request):
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('upload')
            for _file in files:
                Document.objects.create(upload=_file)
            return redirect('dashboard')
        form = DocumentForm()
    return render(request, 'dashboard/upload.html', {'form': form})
