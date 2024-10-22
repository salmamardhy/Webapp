from django.contrib.auth.backends import ModelBackend
from website_a7f.models import Member

class KTPNameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            member = Member.objects.get(ktpname=username)
            if member.check_password(password):  # Use check_password to validate hashed password
                return member
        except Member.DoesNotExist:
            return None