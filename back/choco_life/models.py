from django.db import models
from django.db.models import Max, Sum, Min
from main.models import MainUser


class EventCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Company(models.Model):
    title = models.CharField(max_length=50)
    info = models.TextField(blank=True, null=True)
    sale_points = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=50)
    img = models.URLField(blank=True, null=True)
    alert_info = models.TextField()
    expiration_date = models.DateTimeField(null=False)
    use_until_date = models.DateTimeField(null=False)
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    @property
    def min_price(self):
        return Certificate.objects.filter(event=self).aggregate(price=Min('final_price'))['price']

    @property
    def discount(self):
        return Certificate.objects.filter(event=self).aggregate(discount=Max('discount'))['discount']

    @property
    def total_bought_amount(self):
        return Certificate.objects.filter(event=self).aggregate(sum=Sum('bought_amount'))['sum']


class Certificate(models.Model):
    title = models.CharField(max_length=50)
    discount = models.IntegerField(default=0)
    bought_amount = models.IntegerField(default=0)
    initial_price = models.IntegerField(default=0)
    event = models.ForeignKey(
        Event,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    @property
    def final_price(self):
        return (100 - self.discount) / 100 * self.initial_price

    def __str__(self):
        return self.title


class UserCertificate(models.Model):
    user = models.ForeignKey(
        MainUser,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    amount = models.IntegerField(default=0)
