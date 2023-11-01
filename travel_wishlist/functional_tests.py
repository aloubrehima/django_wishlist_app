from selenium.webdriver.chrome.webdriver import WebDriver

from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):  # Test class to check the title 

    @classmethod
    def setUpClass(cls):
        super().setUpClass() 
        cls.selenium = WebDriver() # Initialize a selenium webdriver instance
        cls.selenium.implicitly_wait(10)   # set a wait time for the selenium actions

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()  # quit the selenium webdriver instance
        super().tearDownClass()


    def test_title_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)  # Assert to check if the titel contains travel wishlist

    
class AddPlacesTest(LiveServerTestCase):  # test a new place

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_add_new_place(self):

        self.selenium.get(self.live_server_url) # Load home page
        input_name = self.selenium.find_element_by_id('id_name') # Using the ID to find the input field for the place 
        input_name.send_keys('Denver') # put a place name 

        add_button = self.selenium.find_element_by_id('add-new-place') # Finding the add button 
        add_button.click()  # Clicl the add button 

        denver = self.selenium.find_element_by_id('place-name-5') # Find the new element that represent the added place 
        self.assertEqual('Denver', denver.text) # Check to see if the place name is Denver 

        self.assertIn('Denver', self.selenium.page_source)  # Assert that Denver is present in the page source
        self.assertIn('New York', self.selenium.page_source) # Assert that if New York is present too
        self.assertIn('Tokyo', self.selenium.page_source)   # This one too

