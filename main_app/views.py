from django.shortcuts import render

# Add the following import
from django.http import HttpResponse

# Add the Cat class & list and view function below the imports
class Puppy:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, breed, description, age):
    self.name = name
    self.breed = breed
    self.description = description
    self.age = age

puppies = [
  Puppy('Lolo', 'pom', 'Kinda rude.', 3),
  Puppy('Sachi', 'dachshund', 'Looks like a turtle.', 0),
  Puppy('Fancy', 'corgi', 'Happy fluff ball.', 4),
  Puppy('Bonk', 'westie', 'Bark loudly.', 6)
]

# Define the home view
def home(request):
  return HttpResponse('<h1>Hello puppies[⽝]🐕</h1>')

def about(request):
  return render(request, 'about.html')

# Add new view
def puppy_index(request):
  return render(request, 'puppies/index.html', { 'puppies': puppies })