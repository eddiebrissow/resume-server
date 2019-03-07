from django.conf import settings
from django.db import models



def user_directory_path(instance, filename):
    print(instance)
    return '{0}/{1}'.format(instance.user, filename)





class Resume(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    user = models.CharField(max_length=255, null=True)
    page_count = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True) # timezone.now
    updated = models.DateTimeField(null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')
    class Meta:
        permissions = (
            ('add_user', 'Add User'),
        )




