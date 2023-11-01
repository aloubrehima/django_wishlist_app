from django.test import TestCase
from django.urls import reverse

from .models import Place  

class TestHomePage(TestCase):  # Test class for the home page

    # Test method to check if the home page shows a message for an empty database
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list') # Obtain the URL for the home page using the place_list reverse
        response = self.client.get(home_page_url) # Make a Get request
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # Make sure that the correct template is used
        self.assertContains(response, 'You have no places in your wishlist')  # Specific message for an empty list

class TestWishList(TestCase):   # Test class for the wishlist

    fixtures = ['test_places']  # Loading fixtures for test data

    def test_wishlist_contains_not_visited_places(self): # Test method to check if the wishlist contains not-visited places
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo') # Make sure to check that these places are in the response
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco') # Make sure to check that these places are not in the response
        self.assertNotContains(response, 'Moab')

class TestVisistedPage(TestCase):  # Test class for the visited page

    def test_visited_page_shows_empty_list_message_for_empty_database(self):  # Check if the visisted page shows a message for an empty database
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')

class TestVisitedList(TestCase):

    fixtures = ['test_places']

    def test_visited_list_shows_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')        
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'New York')
        self.assertNotContains(response, 'Tokyo')

class TestAddNewPlace(TestCase):  # Test class for adding a new place

    def test_add_new_unvisited_place_to_wishlist(self):   # Test method to check if a new unvisited place can be added to the wishlist

        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False }  # Data w

        response = self.client.post(add_place_url, new_place_data, follow=True)
        
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # Check if the template was used correctly

        response_places = response.context['places']  
        self.assertEqual(1, len(response_places))  # Only one place should be present in the response
        tokyo_from_response = response_places[0]  # get the added place from the response

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)

        self.assertEqual(tokyo_from_database, tokyo_from_response) # Check to see if the added place is th same like the one in the db

class TestVisitPlace(TestCase):  # Test class for visiting a place

    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
    
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)  
        self.assertTrue(new_york.visited)   # Is the visited field true in the db?

    def test_visit_non_existent_place(self): # Test method to check handling of visiting a non-existent place
        visit_nonexistent_place_url = reverse('place_was_visited', args=(123456, ))
        response = self.client.post(visit_nonexistent_place_url, follow=True)
        self.assertEqual(404, response.status_code) # # Asserting that the response status code is 404 (Not Found)