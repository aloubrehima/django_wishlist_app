from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.
@login_required
def place_list(request):

    if request.method == 'POST':
        # creeate new place
        form = NewPlaceForm(request.POST)  # creating a form from data in the request
        place = form.save(commit=False)  # creating a model object from form
        place.user = request.user
        if form.is_valid():  # validation against DB constraints
            place.save()   # save place to db
            return redirect('place_list')  # reloads home page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True # mark the place as visisted if the user is the owner
            place.save()
        else:
            return HttpResponseForbidden() # return this message is the user is not the owner
        
    # return redirect ('places_visited')  # redirect to places visited 
    return redirect('place_list')  # redirect to wishlist places

@login_required
def about(request):
    author = 'Alou'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk) # Use the primary key to get the place object or return a 404 message

    # Does this place belong to the current user?

    if place.user != request.user:
        return HttpResponseForbidden
    
    # is this a GET request (show data + form), or a POST request (update Place object)?

    # if POST request, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # tempo
        
        return redirect('place_details', place_pk= place_pk)
    
    else:
        # if GET request, show place info and optiona form
        # If place is visited, show form; if place is not visited, no form

        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})
    
    return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete() # after checking if the user is the owner, delete the place
        return redirect('place_list') # and redirect it to the place_list view
    else:
        return HttpResponseForbidden