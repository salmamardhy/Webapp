# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.core.validators import RegexValidator
import string
import random

def generate_member_id(ktpname):
    while True:
        prefix = ktpname[:3].upper()
        rand_num = ''.join(random.choices(string.digits, k=9))
        parity = ''.join(random.choices(string.ascii_uppercase, k=3))
        member_id = f"{prefix}{rand_num[:3]}{parity[0]}{rand_num[3:6]}{parity[1]}{rand_num[6:]}{parity[2]}" 
        if not Member.objects.filter(memberid=member_id).exists():  # Check if the ID is unique
            return member_id

class Member(models.Model):
    memberid = models.CharField(primary_key=True, max_length=15)
    password = models.CharField(max_length=30)

    letter_validator = RegexValidator(regex=r'^[a-zA-Z\s]+$', message='Only letters and spaces are allowed')

    ktpname = models.CharField(max_length=100, validators=[letter_validator])
    firstname = models.CharField(max_length=50, validators=[letter_validator])
    middlename = models.CharField(max_length=20, blank=True, null=True, validators=[letter_validator])
    lastname = models.CharField(max_length=50, validators=[letter_validator])
    memberstatus = models.IntegerField()

    def save(self, *args, **kwargs):
        self.ktpname = self.ktpname.lower()
        self.firstname = self.firstname.lower()
        self.middlename = self.middlename.lower() if self.middlename else self.middlename
        self.lastname = self.lastname.lower()

        if not self.memberid:
            self.memberid = generate_member_id(self.ktpname)

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'member'

