from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Puppy, Toy
from .forms import FeedingForm

# Define the home view
def home(request):
  return render (request, 'home.html')

def about(request):
  return render(request, 'about.html')

def puppy_index(request):
  puppies = Puppy.objects.all()
  return render(request, 'puppies/index.html', { 'puppies': puppies })

def puppy_detail(request, puppy_id):
  puppy = Puppy.objects.get(id=puppy_id)
  return render(request, 'puppies/detail.html', { 'puppy': puppy })

class PuppyCreate(CreateView):
  model = Puppy
  fields = '__all__'
  success_url = '/puppies'

class PuppyUpdate(UpdateView):
  model = Puppy
  # Let's disallow the renaming of a puppy by excluding the name field!
  fields = ['breed', 'description', 'age']

class PuppyDelete(DeleteView):
  model = Puppy
  success_url = '/puppies/'

def puppy_detail(request, puppy_id):
  puppy = Puppy.objects.get(id=puppy_id)
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  return render(request, 'puppies/detail.html', {
    'puppy': puppy, 'feeding_form': feeding_form
  })

def add_feeding(request, puppy_id):
  # create a ModelForm instance using the data in request.POST
  # request.POST = req.body
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the puppy_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.puppy_id = puppy_id
    new_feeding.save()
  return redirect('puppy-detail', puppy_id=puppy_id)


class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'