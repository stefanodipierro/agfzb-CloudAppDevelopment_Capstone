from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm

# from .models import related models
from django.http import JsonResponse
from .models import Dealership, Review, CarModel, CarMake
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def static_page_view(request):
    return render(request, 'djangoapp/static_page.html')

def about_view(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
#def contact(request):
def contact_view(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'djangoapp/login.html')


# Create a `logout_request` view to handle sign out request
# 
def user_logout(request):
    logout(request)
    return redirect('djangoapp:index')
# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('djangoapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    dealerships = Dealership.objects.all()
    context["dealership_list"] = dealerships
    return render(request, 'djangoapp/index.html', context)





# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    
    context = {
        # altre variabili
        'dealer_id': dealer_id
    }
        # Aggiungi un campo emoji ai dati della recensione
    reviews = Review.objects.filter(dealership_id=dealer_id)
    for review in reviews:
        review.emoji = get_sentiment_emoji(review.review)
    context["reviews"] = reviews

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        context["dealer_id"] = dealer_id
        context["cars"] = CarModel.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        review = Review(
            name=request.user.username,
            dealership_id=dealer_id,
            review=request.POST["content"],
            purchase_date=datetime.strptime(request.POST["purchasedate"], "%Y-%m-%d").strftime("%Y-%m-%d"),

        )
        review.save()
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


def all_dealerships(request):
    dealerships = list(Dealership.objects.values())
    return JsonResponse(dealerships, safe=False)

def dealerships_by_state(request, state):
    dealerships = list(Dealership.objects.filter(st=state.upper()).values())
    return JsonResponse(dealerships, safe=False)

def reviews_for_dealership(request, dealer_id):
    reviews = list(Review.objects.filter(dealership_id=dealer_id).values())
    return JsonResponse(reviews, safe=False)

def post_review(request):
    # Assuming JSON payload in POST request
    data = request.json
    Review.objects.create(**data)
    return JsonResponse({"status": "success"})

def get_sentiment_emoji(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    
    # Scegli un emoji in base al punteggio di polarità
    if sentiment['compound'] >= 0.05:
        return '😊'  # Emoji positivo
    elif sentiment['compound'] <= -0.05:
        return '😢'  # Emoji negativo
    else:
        return '😐'  # Emoji neutro
