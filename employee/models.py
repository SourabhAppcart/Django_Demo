from django.db import models

# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"


class UsersDetails(models.Model):
    address = models.TextField(null=True, blank=True)

    mobile_no = models.CharField(max_length=20)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users_details"
