import psutil
from django.core.management import BaseCommand
import shutil

from myfood.models import ModelServerHealth


class Command(BaseCommand):
    def handle(self, *args, **options):
        total, _, free = shutil.disk_usage('/')
        min_5_load, min_10_load, min_15_load = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
        memory = psutil.virtual_memory()
        ModelServerHealth.objects.create(
            disk_total=total / 2 ** 30,
            disk_free=free / 2 ** 30,
            min_5_avg_cpu_load_perc=round(min_5_load, 2),
            min_10_avg_cpu_load_perc=round(min_10_load, 2),
            min_15_avg_cpu_load_perc=round(min_15_load, 2),
            memory_total=memory.total / 1024 ** 3,
            memory_free=memory.free / 1024 ** 3
        )
