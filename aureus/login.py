import os

from prompt_toolkit import prompt

_MMC_USER_ENV = 'MMC_USERNAME'
_MMC_PW_ENV = 'MMC_PASSWORD'

_RESOURCE_USER_ENV = 'MAVEN_RESOURCE_USERNAME'
_RESOURCE_PW_ENV = 'MAVEN_RESOURCE_PASSWORD'


def mmc_credentials_factory():
    return MMCCredentials()


def resource_credentials_factory():
    return ResourceCredentials()


class BasicCredentials(object):
    _USERNAME_PROMPT = 'Username: '

    def __init__(self, user_var, pw_var):
        self.user_var = user_var
        self.pw_var = pw_var

        if not self._logged_in():
            self._login()

    def _logged_in(self):
        return bool(self.username) and bool(self.password)

    @classmethod
    def _set_property(cls, prop, value):
        os.environ[prop] = value

    @classmethod
    def _get_property(cls, prop):
        return os.environ.get(prop, None)

    def _login(self):
        self.username = prompt(self._USERNAME_PROMPT)
        self.password = prompt('Password: ', is_password=True)

    def __getitem__(self, item):
        return [self.username, self.password][item]

    @property
    def password(self):
        return self._get_property(self.pw_var)

    @password.setter
    def password(self, value):
        self._set_property(self.pw_var, value)

    @property
    def username(self):
        return self._get_property(self.user_var)

    @username.setter
    def username(self, value):
        self._set_property(self.user_var, value)


class MMCCredentials(BasicCredentials):
    _USERNAME_PROMPT = 'MMC Username: '

    def __init__(self):
        super().__init__(_MMC_USER_ENV, _MMC_PW_ENV)


class ResourceCredentials(BasicCredentials):
    _USERNAME_PROMPT = 'Nexus Username: '

    def __init__(self):
        super().__init__(_RESOURCE_USER_ENV, _MMC_PW_ENV)
