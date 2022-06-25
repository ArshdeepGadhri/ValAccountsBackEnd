from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.
class MyUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_name = '{}_iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_name: username})


    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    last_modified = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    valorant_accounts = models.ManyToManyField('ValorantAccount', related_name='valorant_acounts', blank=True)

    objects = MyUserManager()

    def __str__(self):
        return self.username


class ValorantAccount(models.Model):
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, default='N/A')
    username = models.CharField(max_length=100, help_text='Valorant Account Username')
    password = models.CharField(max_length=100, help_text='Valorant Account Password')
    riot_id = models.CharField(max_length=100, help_text='Valorant In Game Name (riot ID)', null=True, blank=True)
    tagline = models.CharField(max_length=100, help_text='Valorant In Game Tag', null=True, blank=True)
    rank = models.CharField(max_length=100, help_text='Valorant In Game Rank', default='Unranked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'{self.id} | Username: {self.username}, Password: {self.password}, ID: {self.riot_id}#{self.tagline}, Rank: {self.rank}'