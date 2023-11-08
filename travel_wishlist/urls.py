from django.urls import path
from . import views

urlpatterns = [ # URL pattern for the app
    path('', views.place_list, name='place_list'),  # Mapping the root URL to the 'place_list' view function
    path('visited', views.places_visited, name='places_visited'),  # Mapping the '/visited' URL to the 'places_visited' view function
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    path('about', views.about, name='about'),
    path('place/<int:place_pk>', views.place_details, name='place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place')
]