from django.db import models
from .managers import SavanaUserOauth2Manager

# Create your models here.
class SavanaDiscordUsers(models.Model):
    objects = SavanaUserOauth2Manager()
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=200)
    public_flags = models.IntegerField()
    flags = models.IntegerField(null=True)
    locale = models.CharField()
    discord_tag = models.TextField(null=True)
    avatar = models.CharField(null=True)
    mfa_enabled = models.CharField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    has_module_perms = models.BooleanField(default=True)
    has_module_permission = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)

    def is_authenticated(self, request):
        return True


