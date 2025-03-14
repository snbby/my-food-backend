from django.db import models
from django.utils.functional import classproperty


class FoodProduct(models.Model):
    def __str__(self):
        return f'{self.product_name}|{self.brands}'

    @classproperty
    def admin_fields(self):
        return ['id', 'product_name', 'brands', 'countries', 'fat_100g', 'carbohydrates_100g', 'proteins_100g']
    
    @classproperty
    def api_fields(self):
        return ['product_name', 'brands', 'countries', 'energy_kcal_100g', 'fat_100g', 'carbohydrates_100g', 'proteins_100g', 'fiber_100g', 'sugars_100g', 'salt_100g', 'saturated_fat_100g']

    class Meta:
        indexes = [
            models.Index(fields=['product_name', 'brands']),
            models.Index(fields=['product_name', 'brands', 'countries']),
            models.Index(fields=['code']),
            models.Index(fields=['product_name']),
            models.Index(fields=['brands'])
        ]    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    product_name = models.CharField(null=True, blank=True)
    brands = models.CharField(null=True, blank=True)
    countries = models.CharField(null=True, blank=True)

    energy_kcal_100g = models.IntegerField(null=True, blank=True)
    carbohydrates_100g = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    proteins_100g = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    fat_100g = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)

    fiber_100g = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    sugars_100g = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    salt_100g = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    saturated_fat_100g = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    
    code = models.CharField(null=True, blank=True)
    
    # cholesterol = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5)
    # categories = models.CharField(null=True, blank=True)
    # completeness = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    # created_datetime = models.DateTimeField(null=True, blank=True)
    # creator = models.CharField(null=True, blank=True)
    # image_ingredients_small_url = models.CharField(null=True, blank=True)
    # image_ingredients_url = models.CharField(null=True, blank=True)
    # image_nutrition_small_url = models.CharField(null=True, blank=True)
    # image_nutrition_url = models.CharField(null=True, blank=True)
    # image_small_url = models.CharField(null=True, blank=True)
    # image_url = models.CharField(null=True, blank=True)
    # last_modified_by = models.CharField(null=True, blank=True)
    # last_modified_datetime = models.DateTimeField(null=True, blank=True)
    # last_updated_datetime = models.DateTimeField(null=True, blank=True)
    # main_category = models.CharField(null=True, blank=True)
    # nutriscore_score = models.IntegerField(null=True, blank=True)
    # iron_100g = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=5)
    # vitamin_c_100g = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5)
    # vitamin_a_100g = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=5)
    # serving_size = models.CharField(null=True, blank=True)
    # serving_quantity = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    # quantity = models.CharField(null=True, blank=True)    
    # url = models.CharField(null=True, blank=True)
    # ingredients_analysis_tags = models.CharField(null=True, blank=True)
    # ingredients_tags = models.CharField(null=True, blank=True)    
    # nutrition_levels_tags = models.CharField(null=True, blank=True)
    # nutriscore_grade = models.CharField(null=True, blank=True)
    # energy_100g = models.IntegerField(null=True, blank=True)
    # pnns_groups_1 = models.CharField(null=True, blank=True)
    # pnns_groups_2 = models.CharField(null=True, blank=True)
    # popularity_tags = models.CharField(null=True, blank=True)

        
class ModelServerHealth(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    disk_total = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    disk_free = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    min_5_avg_cpu_load_perc = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    min_10_avg_cpu_load_perc = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    min_15_avg_cpu_load_perc = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    memory_total = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    memory_free = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Server Health'

