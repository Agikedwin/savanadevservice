from django.contrib.auth.backends import BaseBackend
from .models import SavanaDiscordUsers

class SavanaUserAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user) -> SavanaDiscordUsers:
        if not user:
            return None  # Or raise a ValueError

        user_id = user['id']
        existing_user = SavanaDiscordUsers.objects.filter(id=user_id).first()

        if existing_user:
            print(f"User with ID {user_id} already exists")
            return existing_user
        else:
            print(f"User with ID {user_id} not found")
            new_user = SavanaDiscordUsers.objects.create_new_savana_user(user)
            print(f"New user created: {new_user}")
            return new_user
        print('User was found. Returning...')
        return existing_user

    def get_user(self, user_id):
        try:
            return SavanaDiscordUsers.objects.get(pk=user_id)
        except SavanaDiscordUsers.DoesNotExist:
            return None




