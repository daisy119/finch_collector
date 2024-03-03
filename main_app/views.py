from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Puppy, Toy
from .forms import FeedingForm

# Define the home view
class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def puppy_index(request):
  puppies = Puppy.objects.filter(user=request.user)
    # You could also retrieve the logged in user's cats like this
  # cats = request.user.cat_set.all()
  return render(request, 'puppies/index.html', { 'puppies': puppies })


class PuppyCreate(LoginRequiredMixin, CreateView):
  model = Puppy
  fields = ['name', 'breed', 'description', 'age']
  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)
  

class PuppyUpdate(LoginRequiredMixin, UpdateView):
  model = Puppy
  # Let's disallow the renaming of a puppy by excluding the name field!
  fields = ['breed', 'description', 'age']

class PuppyDelete(LoginRequiredMixin, DeleteView):
  model = Puppy
  success_url = '/puppies/'

@login_required
def puppy_detail(request, puppy_id):
  puppy = Puppy.objects.get(id=puppy_id)
  # id_in look up id
  toys_puppy_doesnt_have = Toy.objects.exclude(id__in = puppy.toys.all().values_list('id'))
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  return render(request, 'puppies/detail.html', {
    'puppy': puppy, 'feeding_form': feeding_form, 'toys': toys_puppy_doesnt_have
  })

@login_required
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


class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, puppy_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Puppy.objects.get(id=puppy_id).toys.add(toy_id)
  return redirect('puppy-detail', puppy_id=puppy_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('puppy-index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
  # Same as: return render(request, 'signup.html', {'form': form, 'error_message': error_message})