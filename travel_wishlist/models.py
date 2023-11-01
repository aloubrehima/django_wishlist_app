from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=200)  # Storing the name of the place - 200 length max
    visited = models.BooleanField(default=False) # Set the default to False to indicate if the place has been visited

    def __str__(self):
        return f'{self.name} visited? {self.visited}'