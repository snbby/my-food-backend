from django.contrib import admin
from django.utils.html import format_html

from myfood.models import ModelLink, ModelServerHealth, SiteStatus, ModelOpenAIImageGeneration, \
    ModelImageUpload, ModelLumaGenerate, ModelChat, FoodProduct
from myfood.utils import attributed
from myfood.mixins import MyFoodModelAdmin
from myfood.ai.luma import NotAuthenticatedException


@admin.register(FoodProduct)
class AdminFoodProduct(MyFoodModelAdmin):
    list_display = FoodProduct().admin_fields
    search_fields = ('brands', 'product_name')


# @admin.register(ModelChat)
class AdminChat(MyFoodModelAdmin):
    list_filter = ('model', 'system_message', 'created_at')
    readonly_fields = ('model_answer', 'usage_prompt_tokens', 'usage_completion_tokens', 'usage_total_tokens', 'response_time', 'updated_at', 'created_at')
    list_display = ('model', 'system_message', 'user_input', 'model_answer', 'usage_prompt_tokens', 'usage_completion_tokens', 'usage_total_tokens', 'response_time', 'created_at')
    fields = ('model', 'system_message', 'user_input', 'model_answer', 'usage_prompt_tokens', 'usage_completion_tokens', 'usage_total_tokens', 'response_time', 'updated_at', 'created_at')

# @admin.register(SiteStatus)
class AdminSiteStatus(MyFoodModelAdmin):
    readonly_fields = ('id', 'url', 'status_code', 'loading_ms', 'created_at')
    list_display = ('id', 'url', 'status_code', 'loading_ms', 'created_at')
    fields = ('id', 'status_code', 'loading_ms', 'created_at')
    list_filter = ('status_code', 'created_at', 'url')

    def has_add_permission(self, request):
        return False


@admin.register(ModelOpenAIImageGeneration)
class AdminImageGeneration(MyFoodModelAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at', 'request_seconds', 'size_kb', 'image_preview', 's3_generated_image', 'openai_temp_image_link')
    list_display = ('id', 'created_at', 'use_dalle3', 'image_resolution', 'size_kb', 'request_seconds', 'prompt', 'image_preview')
    fields = ('created_at', 'updated_at', 'prompt', 'use_dalle3', 'image_resolution', 'size_kb', 's3_generated_image', 'image_preview')
    list_filter = ('image_resolution', 'use_dalle3')

    @admin.display(description='Image link')
    def image_link_clickable(self, obj: ModelOpenAIImageGeneration):
        return format_html("<a href='{url}' target='_blank'>image_link</a>", url=obj.s3_generated_image.url)

    @admin.display(description='size kb')
    def size_kb(self, obj: ModelOpenAIImageGeneration):
        if obj.image_size:
            response = f'{obj.image_size} KB'
        else:
            response = '-'

        return response

    @admin.display(description='Image preview')
    def image_preview(self, obj: ModelOpenAIImageGeneration):
        if obj.s3_generated_image:
            response = format_html("<img src = '{url}' width='256' height='256'/>", url=obj.s3_generated_image.url)
        else:
            response = '-'

        return response
    


@admin.register(ModelServerHealth)
class AdminServerHealth(MyFoodModelAdmin):
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


@admin.register(ModelLink)
class AdminLink(MyFoodModelAdmin):
    readonly_fields = ('id', 'clk_link')
    list_display = ('id', 'clk_link', 'created_at')
    fields = ('link', 'name')

    @attributed(short_description='Link')
    def clk_link(self, obj):
        return format_html("<a href='{url}' target='_blank'>{name}</a>", url=obj.link, name=obj.name)

# @admin.register(ModelImageUpload)
class AdminUploadFile(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'text', 's3_file')
    fields = ('s3_file', 'text')
    
# @admin.register(ModelLumaGenerate)
class AdminLumaGenerate(MyFoodModelAdmin):
    readonly_fields = (
        'created_at', 'updated_at', 'status', 
        'luma_id', 'luma_image_public_url', 'luma_presigned_url', 'luma_video_preview', 'result_video'
        )
    list_display = ('id', 'status', 'created_at', 'updated_at', 'text', 's3_file', 'luma_id', 'luma_video_preview')
    fields = (
        'created_at', 'updated_at', 'status', 'text', 's3_file', 'access_token', 
        'luma_id', 'luma_image_public_url', 'luma_presigned_url', 'luma_video_preview', 'result_video'
        )
    
    @admin.display(description='Luma video')
    def luma_video_preview(self, obj: ModelLumaGenerate):
        if obj.luma_video_public_url:
            response = format_html(f"<video controls><source src='{obj.luma_video_public_url}'></video>")
        else:
            response = '-'

        return response

    
    def save_model(self, request, obj: ModelLumaGenerate, form, change):
        super().save_model(request, obj, form, change)

        # Send to generation if not on generation
        if obj.status == ModelLumaGenerate.LumaStatus.initial:
            try:
                obj.generate_luma_video()
            except NotAuthenticatedException as err:
                self.message_user(request=request, message=str(err), level='error')
                return
            
            if obj.status == ModelLumaGenerate.LumaStatus.is_generating:
                self.message_user(request=request, message=f'Luma generation started successfully', level='info')
            elif obj.status in (ModelLumaGenerate.LumaStatus.generated_presign_url, ModelLumaGenerate.LumaStatus.uploaded_image):
                self.message_user(request=request, message=f'Something went wrong with status, check console', level='warning')
            else:
                self.message_user(request=request, message=f'Unrecognized result', level='warning')
                
        elif obj.status == ModelLumaGenerate.LumaStatus.is_generating:
            try:
                obj.check_generations()
            except NotAuthenticatedException as err:
                self.message_user(request=request, message=str(err), level='error')
                return
            
            if obj.status == ModelLumaGenerate.LumaStatus.finished:
                self.message_user(request=request, message=f'Luma generation finished', level='info')
            else:
                self.message_user(request=request, message=f'Generation is still in progress', level='warning')