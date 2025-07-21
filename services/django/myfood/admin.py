from django.contrib import admin
from myfood.models import FoodProduct, ModelServerHealth
from myfood.utils import attributed


@admin.register(FoodProduct)
class AdminFoodProduct(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'brands', 'countries', 'fat_100g', 'carbohydrates_100g', 'proteins_100g')
    search_fields = ('brands', 'product_name')


@admin.register(ModelServerHealth)
class AdminServerHealth(admin.ModelAdmin):
    readonly_fields = (
        'id', 'dsk_total', 'dsk_free', 'min_5_load', 'min_10_load', 'min_15_load', 'ttl_memory',
        'fre_memory', 'created_at'
    )
    list_display = (
        'id', 'dsk_total', 'dsk_free', 'min_5_load', 'min_10_load', 'min_15_load', 'ttl_memory',
        'fre_memory', 'created_at'
    )

    def has_add_permission(self, request):
        return False

    @attributed(short_description='disk total')
    def dsk_total(self, obj):
        return f'{obj.disk_total} GB'

    @attributed(short_description='disk free')
    def dsk_free(self, obj):
        return f'{obj.disk_free} GB'

    @attributed(short_description='CPU 5 min load')
    def min_5_load(self, obj):
        return f'{obj.min_5_avg_cpu_load_perc} %'

    @attributed(short_description='CPU 10 min load')
    def min_10_load(self, obj):
        return f'{obj.min_10_avg_cpu_load_perc} %'

    @attributed(short_description='CPU 15 min load')
    def min_15_load(self, obj):
        return f'{obj.min_15_avg_cpu_load_perc} %'

    @attributed(short_description='memory total')
    def ttl_memory(self, obj):
        return f'{obj.memory_total} GB'

    @attributed(short_description='memory free')
    def fre_memory(self, obj):
        return f'{obj.memory_free} GB'
