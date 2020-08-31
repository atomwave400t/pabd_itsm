# -*- coding: utf-8 -*-


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class Asset_type(models.Model):
    name = models.CharField(primary_key=True, max_length=30, unique=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(primary_key=True, max_length=1, unique=True)

    def __str__(self):
        return self.name


class User_type(models.Model):
    name = models.CharField(primary_key=True, max_length=20, unique=True)

    def __str__(self):
        return self.name


class Field_type(models.Model):
    name = models.CharField(primary_key=True, max_length=20, unique=True)

    def __str__(self):
        return self.name


class Name(models.Model):
    name = models.CharField(primary_key=True, max_length=30, unique=True)

    def __str__(self):
        return self.name


class Priority(models.Model):
    value = models.IntegerField(primary_key=True, unique=True)
    time_hours = models.IntegerField()

    def __str__(self):
        return str(self.value)


class Business_unit(models.Model):
    name = models.CharField(primary_key=True, max_length=12, unique=True)
    address = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(primary_key=True, max_length=20, unique=True)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class AssetStatus(models.Model):
    name = models.CharField(primary_key=True, max_length=20, unique=True)

    def __str__(self):
        return self.name


class Classification(models.Model):
    name = models.CharField(primary_key=True, max_length=20, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name + ", [" + self.description + "]"


class Sr_pattern(models.Model):
    name = models.CharField(primary_key=True, max_length=128, unique=True)
    description = models.CharField(max_length=255)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT)

    def __str__(self):
        return self.name + ", " + self.description + ", " + self.classification


class Pattern_row(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    pattern = models.ForeignKey(Sr_pattern, on_delete=models.PROTECT)
    is_required = models.BooleanField()
    type = models.ForeignKey(Field_type, on_delete=models.PROTECT)

    def __str__(self):
        return self.name + ", " + self.description + ", " + self.pattern + ", " + self.is_required + ", " + self.type


class ITSM_UserManager(BaseUserManager):
    def create_user(self, login, name, surname, password=None):
        if not login:
            raise ValueError("Login is required")

        name_instance = Name.objects.get(name=name)
        user = self.model(login=login, name=name_instance.name, surname=surname, address=address,
                            email_address=email_address, gender=gender, user_type=user_type,
                            business_unit=business_unit, job_title=job_title)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, name, surname, password):
        name_instance = Name.objects.get(name=name)
        user = self.model(login=login, name=name_instance, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_operator = True
        user.save(using=self._db)
        return user


class ITSM_User(AbstractBaseUser):
    login = models.CharField(max_length=61, primary_key=True, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    name = models.ForeignKey(Name, on_delete=models.PROTECT, null=True, blank=True)
    surname = models.CharField(max_length=30)
    address = models.CharField(max_length=60, null=True, blank=True)
    email_address = models.EmailField(max_length=30, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_change_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    user_type = models.ForeignKey(User_type, on_delete=models.PROTECT, null=True, blank=True)
    business_unit = models.ForeignKey(Business_unit, on_delete=models.PROTECT, null=True, blank=True)
    job_title = models.CharField(max_length=40, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_operator = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = ITSM_UserManager()

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



# class Pattern_record(models.Model):
#     id = models.AutoField(primary_key=True)


# class Person(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.ForeignKey(Name, on_delete=models.PROTECT)
#     surname = models.CharField(max_length=30)
#     address = models.CharField(max_length=60)
#     email_address = models.EmailField(max_length=30)
#     gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
#     login = models.CharField(max_length=61, unique=True)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     last_change_date = models.DateTimeField(auto_now=True)
#     user_type = models.ForeignKey(User_type, on_delete=models.PROTECT)
#     business_unit = models.ForeignKey(Business_unit, on_delete=models.PROTECT)
#     job_title = models.CharField(max_length=40)
#
#     def __str__(self):
#         return self.login

    # class Meta:
    #     unique_together = (("id","login"),)

# insert into itsm_person(surname, address, email_address, login, job_title, creation_date, last_change_date, business_unit_id, gender_id, name_id, user_type_id)
# values ("Kunysz", "Wymyslona 150", "mail@mail.pl", "krzysztof.kunysz", "Admin", "2020-05-05 12:00:00", "2020-05-05 12:00:00", "EXO_TEC_CRO", "M", "Krzysztof", "ADMIN");

class Asset(models.Model):
    id = models.AutoField(primary_key=True)
    person_id = models.ForeignKey(ITSM_User, on_delete=models.PROTECT, null=True, blank=True, related_name='asset_person_id')
    business_unit = models.ForeignKey(Business_unit, on_delete=models.PROTECT, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    code_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.ForeignKey(AssetStatus, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change_date = models.DateTimeField(auto_now=True)
    last_change_author_id = models.ForeignKey(ITSM_User, on_delete=models.PROTECT, related_name='asset_last_change_author_id')
    asset_type = models.ForeignKey(Asset_type, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.code_name


class Service_request(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=1024)
    status_id = models.ForeignKey(Status, on_delete=models.PROTECT)
    author_id = models.ForeignKey(ITSM_User, on_delete=models.PROTECT, related_name='sr_author_id')
    owner_id = models.ForeignKey(ITSM_User, on_delete=models.PROTECT, null=True, blank=True, related_name='sr_owner_id')
    creation_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    resume_date = models.DateTimeField(null=True, blank=True)
    last_change_date = models.DateTimeField(auto_now=True)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT, null=True, blank=True)
    business_unit = models.ForeignKey(Business_unit, on_delete=models.PROTECT)
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, null=True, blank=True)
    pattern = models.ForeignKey(Sr_pattern, on_delete=models.PROTECT, null=True, blank=True)
    asset_id = models.ForeignKey(Asset, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title + ", " + str(self.status_id) + ", " + str(self.owner_id) + ", " + str(self.creation_date)


class Work_journal(models.Model):
    id = models.AutoField(primary_key=True)
    record_title = models.CharField(max_length=60)
    record_description = models.CharField(max_length=1024)
    service_request_id = models.ForeignKey(Service_request, on_delete=models.PROTECT)
    is_internal = models.BooleanField()
    author_id = models.ForeignKey(ITSM_User, on_delete=models.PROTECT, related_name='work_author_id')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record_title + ", " + str(self.author_id)


class Communication_journal(models.Model):
    id = models.AutoField(primary_key=True)
    record_title = models.CharField(max_length=255)
    record_description = models.CharField(max_length=1024, null=True, blank=True)
    service_request_id = models.ForeignKey(Service_request, on_delete=models.PROTECT)
    is_internal = models.BooleanField()
    author_id = models.ForeignKey(ITSM_User, on_delete=models.PROTECT, related_name='communication_author_id')
    receiver_id = models.ForeignKey(ITSM_User, on_delete=models.PROTECT, related_name='communication_receiver_id')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record_title + ", " + self.author_id + ", " + self.receiver_id
