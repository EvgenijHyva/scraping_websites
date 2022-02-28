from django.db import models

class Restaurants(models.Model):
    class Meta:
        verbose_name = "Ravintola"
        verbose_name_plural = "Ravintolat"
        ordering = ("name",)

    name = models.CharField(max_length=128, unique=True, verbose_name="Ravintolan nimi")
    is_active = models.BooleanField(default=True, blank=False, verbose_name="Actiivinen")
    url = models.URLField(unique=True, verbose_name="Menu url")
    map_url = models.URLField(blank=True, null=True, default=None, verbose_name="Sijainti kartaalla")
    address = models.CharField(max_length=256, blank=True, null=True, default=None, verbose_name="Osoite")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Luotu")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Päivitetty")

    def __str__(self):
        return self.name

    @property
    def to_dict(self):
        return {
            "name": self.name,
            "is_active": self.is_active,
            "url": self.url,
            "Created_at": self.created_at,
            "map_url": self.map_url,
            "address": self.address
        }

class RestaurantMenu(models.Model):
    class Meta:
        verbose_name = "Lounaslista"
        verbose_name_plural = "Lounaslistat"
        ordering = ("-id", "-added_at")

    id = models.AutoField(primary_key=True, verbose_name='id')
    restaurant = models.ForeignKey("Restaurants", related_name="restaurants", unique=False,
                           on_delete=models.CASCADE, verbose_name="Lounaspaikka")
    day = models.CharField(max_length=64, verbose_name="Päivä")
    menu_catalogs = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name="Valikon osiot")
    dishes = models.TextField(blank=True, null=True, verbose_name="Ruoka")
    dishes_description = models.TextField(blank=True, verbose_name="Kuvaus")
    price = models.CharField(max_length=64, verbose_name="Hinta",
                                null=True, blank=True, default=None)
    additional_price = models.CharField(max_length=64, verbose_name="Hinta valikoima", blank=True, null=True, default=None)
    info = models.TextField(blank=True, verbose_name="Info")
    additional_info = models.TextField(blank=True, verbose_name="Lisää info")
    date = models.DateField(blank=False, verbose_name="Päivämäärä")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Luotu')

    def __str__(self):
        return f" {self.restaurant.name} | {self.day} | {self.date}"

    @property
    def dishes_as_list(self):
        if self.dishes:
            return list(self.dishes.split("\n"))

    @property
    def additional_info_as_list(self):
        if self.additional_info:
            return list(self.additional_info.split("\n"))

    @property
    def to_dict(self):
        return {
            "restaurant": self.restaurant.name,
            "day": self.day,
            "menu_catalogs": self.menu_catalogs,
            "dishes": self.dishes,
            "dishes_description": self.dishes_description,
            "price": self.price,
            "additional_price": self.additional_price,
            "info": self.info,
            "additional_info": self.additional_info,
            "date": self.date
        }


class Errors(models.Model):
    class Meta:
        verbose_name = "Error "
        verbose_name_plural = "Errors"
        ordering = ("-target",)

    id = models.AutoField(primary_key=True)
    target = models.ForeignKey("Restaurants", on_delete=models.CASCADE, verbose_name="Virheen kohde")
    resolved = models.BooleanField(default=False, verbose_name="Korjattu")
    error_text = models.TextField(blank=False, verbose_name="Virheen kuvaus")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Päivä ja aika")

    def __str__(self):
        return f"{self.target.name} | {self.created_at}"
