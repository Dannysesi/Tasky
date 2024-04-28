from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', default='default.png', folder='profile_pic', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_team_lead = models.BooleanField(default=False)
    is_team_member = models.BooleanField(default=False)
    # first_name = models.CharField(max_length=50, blank=True, null=True)
    # last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()


