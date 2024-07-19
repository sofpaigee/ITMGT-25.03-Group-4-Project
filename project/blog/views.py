from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, UpdateView
from django.http import HttpResponse
import os
from blog.models import Resource
from users.forms import ResourceUpload, ResourceUpdateForm
from django.contrib.auth.decorators import login_required

def home(request):
    context = {
        'resource': Resource.objects.all(),
    }
    return render(request, 'blog/home.html', context)

@login_required
def resource_list(request):
    search_query = request.GET.get('q')
    subject_filter = request.GET.get('subject')

    resources = Resource.objects.all()

    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if subject_filter:
        resources = resources.filter(subject=subject_filter)

    resources = resources.order_by('-date_uploaded')

    subjects = [
        ('MATH 31.1', 'MATH 31.1'),
        ('LAS 21', 'LAS 21'),
        ('MATH 31.2', 'MATH 31.2'),
        ('DECSC 22', 'DECSC 22'),
        ('ITMGT 25.03', 'ITMGT 25.03'),
        ('MATH 31.3', 'MATH 31.3'),
        ('ACCT 115', 'ACCT 115'),
        ('LLAW 113', 'LLAW 113'),
        ('MATH 70.1', 'MATH 70.1'),
        ('ECON 110', 'ECON 110'),
        ('ACCT 125', 'ACCT 125'),
        ('LLAW 115', 'LLAW 115'),
        ('MATH 61.2', 'MATH 61.2'),
        ('DECSC 25', 'DECSC 25'),
        ('ECON 121', 'ECON 121'),
        ('FINN 115', 'FINN 115'),
        ('QUANT 121', 'QUANT 121'),
        ('QUANT 162', 'QUANT 162'),
        ('LAS 111', 'LAS 111'),
        ('MKTG 111', 'MKTG 111'),
        ('QUANT 163', 'QUANT 163'),
        ('LAS 123', 'LAS 123'),
        ('QUANT 192', 'QUANT 192'),
        ('LAS 120', 'LAS 120'),
        ('LAS 140', 'LAS 140'),
        ('OPMAN 125', 'OPMAN 125'),
        ('QUANT 164', 'QUANT 164'),
        ('QUANT 199', 'QUANT 199'),
        ('LAS 197.10', 'LAS 197.10'),
    ]

    context = {
        'resources': resources,
        'subjects': subjects,
        'selected_subject': subject_filter,
    }
    return render(request, 'blog/resource_list.html', context)

def upload_resource(request):
    if request.method == 'POST':
        form = ResourceUpload(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = request.user
            resource.subject = form.cleaned_data.get('subjects')
            resource.save()
            print("Resource uploaded:", resource)
            return redirect('resource_list')
    else:
        form = ResourceUpload()
    return render(request, 'blog/resource_upload.html', {'form': form})

class ResourceListView(ListView): 
    model = Resource
    template_name = 'blog/resource_list.html'
    context_object_name = 'resources'
    ordering = ['-date_uploaded']
    paginate_by = 1

class UserResourceListView(ListView):  
    model = Resource
    template_name = 'blog/user_resource_list.html'
    context_object_name = 'resources'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Resource.objects.filter(author=user).order_by('-date_uploaded')

class ResourceDetailView(DetailView):
    model = Resource

class ResourceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resource
    form_class = ResourceUpdateForm
    template_name = 'blog/update_resource.html' 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial_file'] = self.object.file
        return kwargs

    def form_valid(self, form):
        if 'file' in self.request.FILES:
            form.instance.file = self.request.FILES['file']
        return super().form_valid(form)

    def test_func(self):
        resource = self.get_object()
        return self.request.user == resource.author

    def get_success_url(self):
        return reverse('resource-detail', kwargs={'pk': self.object.pk})

class ResourceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resource
    template_name = 'blog/resource_confirm_delete.html'
    success_url = reverse_lazy('resource_list')

    def test_func(self):
        resource = self.get_object()
        return self.request.user == resource.author

@login_required
def download_file(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    file_path = resource.file.path

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        return HttpResponse("File not found.")

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
