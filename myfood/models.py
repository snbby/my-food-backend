import io
import time
import urllib
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils.functional import classproperty
from openai import OpenAI

from myfood.storages import S3Storage
from myfood.ai.openAI import custom_open_ai_client




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

class SiteStatus(models.Model):
    url = models.CharField(max_length=128, null=False, blank=False)
    status_code = models.IntegerField(null=True, blank=True)
    loading_ms = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Site Status'


class ModelChat(models.Model):
    class OpenAIModels(models.TextChoices):
        gpt_4o_mini = 'gpt-4o-mini', 'gpt-4o-mini'
        gpt_4o = 'gpt-4o', 'gpt-4o'

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model = models.CharField(max_length=50, default=OpenAIModels.gpt_4o_mini, choices=OpenAIModels.choices)
    system_message = models.TextField(max_length=2048, default='You are a helpful assistant.')
    user_input = models.TextField(max_length=8192, null=False, blank=False)
    model_answer = models.TextField(max_length=8192, null=False)
    usage_prompt_tokens = models.PositiveIntegerField(null=False)
    usage_completion_tokens = models.PositiveIntegerField(null=False)
    usage_total_tokens = models.PositiveIntegerField(null=False)
    response_time = models.PositiveIntegerField(null=False)
    
    def build_messages(self):
        messages = [
            {'role': 'system', 'content': self.system_message},
            {'role': 'user', 'content': self.user_input}
        ]
        return messages
    
    def run(self):
        start = time.time()
        
        client = OpenAI(api_key=settings.ME_OPEN_AI_API_KEY, organization=settings.ME_OPEN_AI_ORGANIZATION)
        
        completion = client.chat.completions.create(
            model=self.model,
            messages=self.build_messages()
        )
        self.model_answer = completion.choices[0].message.content
        self.usage_prompt_tokens = completion.usage.prompt_tokens
        self.usage_completion_tokens = completion.usage.completion_tokens
        self.usage_total_tokens = completion.usage.total_tokens
        
        self.response_time = int((time.time() - start) * 1000)
        return completion
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.run()
        super().save(force_insert, force_update, using, update_fields)
    
    

class ModelOpenAIImageGeneration(models.Model):
    class OpenAIImageResolution(models.TextChoices):
        s256x256 = '256x256', '256x256'
        s512x512 = '512x512', '512x512'
        s1024x1024 = '1024x1024', '1024x1024'
        s1792x1024 = '1792x1024', '1792x1024'
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prompt = models.CharField(max_length=4096, null=False, blank=False, default='What to generate?')
    image_number = models.PositiveIntegerField(null=False, default=1)
    image_resolution = models.CharField(
        max_length=32, null=False, blank=False, default=OpenAIImageResolution.s256x256, 
        choices=OpenAIImageResolution.choices, 
        help_text='If Dalle3-E model is used the resolution can be only 1024x1024'
        )
    use_dalle3 = models.BooleanField(default=False)
    request_seconds = models.FloatField(null=True, blank=True)
    image_size = models.IntegerField(null=True, blank=True)
    openai_temp_image_link = models.CharField(max_length=512, null=True, blank=True)
    s3_generated_image = models.FileField(storage=S3Storage, null=True, blank=True)

    def __str__(self):
        return f'{self.id}.{self.prompt:15}'
    
    def generate_image(self):
        start = time.time()
        self.image_resolution = self.image_resolution if self.use_dalle3 is False else self.OpenAIImageResolution.s1024x1024
        data = {
            'prompt': self.prompt,
            'n': self.image_number,
            'size': self.image_resolution
        }
        
        # Generate image
        r = custom_open_ai_client.image_generation(data, use_dalle3=self.use_dalle3)
        response_json = r.json()
        self.request_seconds = round(time.time() - start, 2)
        self.openai_temp_image_link = response_json['data'][0]['url']
        
        # Download image
        r = custom_open_ai_client.get_media(self.openai_temp_image_link)
        self.image_size = round(int(r.headers.get('content-length')) / 1024, 0)
        dalli_text = 'dalle3' if self.use_dalle3 else 'basic'
        self.s3_generated_image.save(f'openai/imageGen/image_gen_{dalli_text}_{uuid4().hex}', io.BytesIO(r.content), save=False)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.generate_image()
        super().save(force_insert, force_update, using, update_fields)

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

class ModelLink(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, null=False, blank=False)
    link = models.CharField(max_length=2048, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Links'

class ModelImageUpload(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(null=True, blank=True)
    s3_file = models.FileField(storage=S3Storage)

class ModelLumaGenerate(models.Model):
    class LumaStatus(models.TextChoices):
        initial = 'initial', 'initial'
        generated_presign_url = 'generated_presign_url', 'generated_presign_url'
        uploaded_image = 'uploaded_image', 'uploaded_image'
        is_generating = 'is_generating', 'is_generating'
        finished = 'finished', 'finished'
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(null=False, blank=False)
    s3_file = models.FileField(storage=S3Storage, null=False, blank=False)
    access_token = models.CharField(max_length=1024, null=False, blank=False)
    luma_id = models.CharField(max_length=1024, null=True, blank=True)
    luma_presigned_url = models.CharField(max_length=2048, null=True, blank=True)
    luma_image_public_url = models.CharField(max_length=2048, null=True, blank=True)
    luma_video_public_url = models.CharField(max_length=2048, null=True, blank=True)
    result_video = models.FileField(storage=S3Storage, null=True, blank=True)
    status = models.CharField(default=LumaStatus.initial, choices=LumaStatus.choices, blank=True)
    last_result_check = models.DateField(null=True, blank=True)
    authenticated = models.BooleanField(default=False)
    
    
    def generate_luma_video(self):
        from me.luma import luma_client
        
        luma_client.generate(self)
    
    def check_generations(self) -> dict:
        from me.luma import luma_client
        
        generations = luma_client.get_generations(self)
        self.last_result_check = models.functions.Now()
        for generation in generations:
            if self.luma_id == generation['id'] and generation['state'] == 'completed':
                self.status = self.LumaStatus.finished
                self.luma_video_public_url = generation['video']['url']
                video_bytes = luma_client.get_video(self.luma_video_public_url)
                video_name = f'luma_{self.id}_{urllib.parse.quote_plus(self.text)}.mp4'
                self.result_video.save(video_name, video_bytes)
        self.save()
        return generations
