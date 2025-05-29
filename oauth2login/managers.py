from django.contrib.auth import models

class SavanaUserOauth2Manager(models.UserManager):
    def create_new_savana_user(self, user):
        print('inside savana user manager')
        discord_tag = '%s#%s' % (user['username'], user['discriminator'])

        new_user = self.create(
            id=user['id'],
            public_flags=user['public_flags'],
            flags=user['flags'],
            discord_tag=discord_tag,
            username=user['username'],
            locale=user['locale'],
            avatar=user['avatar'],
            mfa_enabled=user['mfa_enabled'],

        )
        return new_user