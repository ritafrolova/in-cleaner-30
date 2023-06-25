from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_worker = models.BooleanField(default=False)
    balance = models.IntegerField(default=15000)

    def __str__(self):
        return self.username


class Specialty(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile/images/', blank=True, null=True)
    bio = models.TextField(max_length=2000, default="")
    type = models.ForeignKey
    rating = models.FloatField(default=0.0)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)

    @property
    def get_avatar(self):
        return self.photo.url


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_orders')
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='worker_orders', blank=True,
                               null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    is_done = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, blank=True, null=True)
    report = models.OneToOneField('Report', related_name='order_report', on_delete=models.SET_NULL, null=True,
                                  blank=True)

    def __str__(self):
        return f"Order #{self.id}"


class Report(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='report_order')
    photo1 = models.ImageField(upload_to='reports/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='reports/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='reports/', blank=True, null=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Report #{self.id}"
