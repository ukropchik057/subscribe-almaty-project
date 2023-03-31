from django.db import models
from pytils.translit import slugify
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class AboutPage(models.Model):
    content = models.TextField("Описание")

    class Meta:
        verbose_name = "О проекте"
        verbose_name_plural = "О проекте"

class Category(models.Model):
    categoryName = models.CharField("Наименование категории", max_length=255)
    fontAwesomeClass = models.CharField("Font Awesome Icon", null=True, blank=True, max_length=255, default="")
    slug = models.SlugField(unique=True, blank=True, editable=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.categoryName

    def save(self, *args, **kwargs):
        self.slug = slugify(self.categoryName)
        super().save(*args, **kwargs)

class Master(models.Model):
    masterName = models.CharField("Имя мастера", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.masterName


class Service(models.Model):
    serviceName = models.CharField("Наименование услуги", max_length=255)
    price = models.FloatField("Цена")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.serviceName

class Rating(models.Model):
    rating = models.IntegerField("Рейтинг из 10")

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return f"{self.rating}"


class Business(models.Model):
    cover = models.ImageField("Изображение (500x500)", null=True, blank=True, upload_to="business/covers/", default="")
    businessName = models.CharField("Наименование компании", max_length=255)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    scheduleStart = models.TimeField("Начало работы")
    scheduleFinish = models.TimeField("Конец работы")
    phone = models.CharField("Телефон", max_length=20)
    address = models.CharField("Адрес", max_length=255)
    instagram = models.CharField("Instagram аккаунт", max_length=255, blank=True, null=True)
    yandexMapLink = models.CharField("Ссылка на карту", max_length=500)
    masters = models.ManyToManyField(Master)
    services = models.ManyToManyField(Service)
    rating = models.ForeignKey(Rating, on_delete=models.Model, verbose_name="Рейтинг", null=True, blank=True)
    postDate = models.DateTimeField("Дата публикации", default=datetime.now())

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def get_absolute_url(self):
        return reverse("businessListByCategory", args=[self.slug])

    def __str__(self):
        return self.businessName

    def save(self, *args, **kwargs):
        self.slug = slugify(self.businessName)
        super().save(*args, **kwargs)


class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False, verbose_name="Компания")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер", default="")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга", default="")
    recordDate = models.DateTimeField("Дата и время записи", default=datetime.now)
    phone = models.CharField("Телефон", max_length=20)
    postDate = models.DateTimeField("Дата публикации", default=datetime.now)
    isActive = models.BooleanField("Статус", default=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


    def __str__(self):
        return f"#{self.pk} заявка - {self.phone}"


class UserDataProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField("Аватар", null=True, blank=True, upload_to="user/avatar/")

    class Meta:
        verbose_name = "Данные пользователя"
        verbose_name_plural = "Данные пользователя"


    def __str__(self):
        return f"{self.user.username}"

