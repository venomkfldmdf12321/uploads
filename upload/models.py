from django.db import models


class User_Profile(models.Model):
    display_picture = models.FileField()

    def __str__(self):
        return self.fname