from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete= models.CASCADE)
    name = models.CharField(max_length=200)  # Storing the name of the place - 200 length max
    visited = models.BooleanField(default=False) # Set the default to False to indicate if the place has been visited
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)

        super().save(*args, **kwargs)

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)
        
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)
        
        super().save(*args, **kwargs)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'  # Use the photo url if exists otherwise return no photo
        notes_str = self.notes[100:] if self.notes else 'no notes' # checking if notes and show the 100 characters otherwise says no photo
        return f'{self.name}, visited? {self.visited} on {self.date_visited}. Notes: {notes_str}. Photo {photo_str}'  # final string with all the information
    