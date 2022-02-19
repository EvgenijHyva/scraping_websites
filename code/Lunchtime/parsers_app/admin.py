from django.contrib import admin
from .models import Restaurants, RestaurantMenu, Errors


@admin.register(Restaurants)
class AdminRestaurants(admin.ModelAdmin):
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("name",)
    list_display = ("name", "is_active", "address", "created_at", "updated_at", "id")

@admin.register(RestaurantMenu)
class AdminRestaurantMenu(admin.ModelAdmin):
    ordering = ("-added_at", "-id")
    readonly_fields = ("added_at", )
    list_display = ("restaurant", "price", "additional_price","date", "day", "info", "id")

@admin.register(Errors)
class AdminErrors(admin.ModelAdmin):
    ordering = ("created_at",)
    readonly_fields = ("created_at", )
    search_fields = ("created_at", )
    list_display = ("id", "target", "resolved", "error_text", "created_at")