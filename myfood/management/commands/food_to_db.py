import csv
import sys
import gzip
import shutil
import os

from django.core.management import BaseCommand
from django.db.utils import DataError
from django.conf import settings
import requests

from myfood.models import FoodProduct
from myfood.utils import init_kwargs
from myfood import logger

csv.field_size_limit(sys.maxsize)

class Command(BaseCommand):
    eng_food_link = settings.MYFOOD_CSV_LINK
    eng_food_link_gz = f'{eng_food_link}.gz'
    local_folder = 'artifacts/myfood'
    local_path = f'{local_folder}/eng_products.csv'
    local_path_gz = f'{local_path}.gz'
    not_none_fields = ('product_name', 'brands', 'energy_kcal_100g', 'carbohydrates_100g', 'fat_100g', 'proteins_100g')
    
    exceptions = 0
    
    def download_file(self, url: str):
        with requests.get(url, stream=True, timeout=15) as r:
            r.raise_for_status()
            with open(self.local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk: 
                    f.write(chunk)

    def handle(self, *args, **options):
        logger.info('Create folder if not exist')
        os.makedirs(self.local_folder, exist_ok=True)

        # Headers 206
        logger.info('Started to download product file')
        self.download_file(self.eng_food_link)

        logger.info('Started to extract gz file')
        with gzip.open(self.local_path_gz, 'rb') as f_in:
            with open(self.local_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


        with open(self.local_path, newline='') as f:
            products = csv.DictReader(f, delimiter='\t')
            self.bulk_write_raw(products)
            # self.update_data(products)

        # logger.info(f'Deleting local files')
        os.remove(self.local_path)
        os.remove(self.local_path_gz)

        logger.info(f'Finished.')
        
    def bulk_write_raw(self, products: list):
        logger.info('Deleting all objects in FoodProduct')
        FoodProduct.objects.all().delete()

        logger.info('Started to write food products to db. Will notify each 100.000 rows')
        bulk_to_write = []
        for num_row, product in enumerate(products):
            if num_row % 100000 == 0 and num_row != 0:
                logger.info(f'Started to write bulk: {num_row}')
                FoodProduct.objects.bulk_create(bulk_to_write)
                logger.info(f'Ended writing bulk: {num_row}')
                bulk_to_write = []
            
            product = {key.replace('-', '_'): value for key, value in product.items() if key is not None}  # Necessary changes before
            product_only_existing_fields = init_kwargs(FoodProduct, product)  # Pick the appropriate fields
            product = FoodProduct(**product_only_existing_fields)
            if any([product.product_name == '', product.product_name is None, product.brands == '', product.brands is None, product.energy_kcal_100g == '']):
                continue
            if all([product.fat_100g == '', product.proteins_100g == '', product.carbohydrates_100g == '']):
                continue
            product.energy_kcal_100g = int(float(product.energy_kcal_100g)) if all([product.energy_kcal_100g != '', self.check_number(product.energy_kcal_100g, minimal_number=1000)]) else 0
            product.fiber_100g = product.fiber_100g if all([product.fiber_100g != '', self.check_number(product.fiber_100g)]) else 0
            product.saturated_fat_100g = product.saturated_fat_100g if all([product.saturated_fat_100g != '', self.check_number(product.saturated_fat_100g)]) else 0
            product.salt_100g = product.salt_100g if all([product.salt_100g != '', self.check_number(product.salt_100g)]) else 0
            product.sugars_100g = product.sugars_100g if all([product.sugars_100g != '', self.check_number(product.sugars_100g)]) else 0
            product.fat_100g = product.fat_100g if all([product.fat_100g != '', self.check_number(product.fat_100g)]) else 0
            product.proteins_100g = product.proteins_100g if all([product.proteins_100g != '', self.check_number(product.proteins_100g)]) else 0
            product.carbohydrates_100g = product.carbohydrates_100g if all([product.carbohydrates_100g != '', self.check_number(product.carbohydrates_100g)]) else 0
            product.brands = product.brands.capitalize()
            product.product_name = product.product_name.capitalize()
            bulk_to_write.append(product)
            # try:
                # product.save()
            # except:
                # print(product_only_existing_fields)
            

        if len(bulk_to_write) > 0:
            logger.info(f'Started to write last bulk')
            FoodProduct.objects.bulk_create(bulk_to_write)
            logger.info(f'Ended writing last bulk')
            bulk_to_write = []

    def update_data(self, products: list):
        logger.info('Started to write food products to db. Will notify each 100.000 rows')
        for num_row, product in enumerate(products):
            if num_row % 100000 == 0 and num_row != 0:
                logger.info(f'Writing row: {num_row}')
                
            product = {key.replace('-', '_'): value for key, value in product.items() if key is not None}  # Necessary changes before
            product_only_existing_fields = init_kwargs(FoodProduct, product)  # Pick the appropriate fields

            product = FoodProduct.objects.filter(code=product_only_existing_fields['code']).first()
            if not product:
                product = FoodProduct(**product_only_existing_fields)
                if any([product.product_name == '', product.energy_kcal_100g == '']):
                    continue
                if all([product.fat_100g == '', product.proteins_100g == '', product.carbohydrates_100g == '']):
                    continue
            
            product.energy_kcal_100g = int(float(product.energy_kcal_100g)) if all([product.energy_kcal_100g != '', self.check_number(product.energy_kcal_100g)]) else 0
            product.fiber_100g = product.fiber_100g if product.fiber_100g != '' else 0
            product.saturated_fat_100g = product.saturated_fat_100g if product.saturated_fat_100g != '' else 0
            product.salt_100g = product.salt_100g if product.salt_100g != '' else 0
            product.sugars_100g = product.sugars_100g if product.sugars_100g != '' else 0
            product.fat_100g = product.fat_100g if product.fat_100g != '' else 0
            product.proteins_100g = product.proteins_100g if product.proteins_100g != '' else 0
            product.carbohydrates_100g = product.carbohydrates_100g if product.carbohydrates_100g != '' else 0
            product.brands = product.brands.capitalize()
            product.product_name = product.product_name.capitalize()
                                    
            try:
                product.save()
            except DataError:
                self.exceptions += 1
                continue
    
    def check_number(self, potential_number: str, minimal_number: int = 100) -> bool: 
        try:
            if float(potential_number) < minimal_number or float(potential_number) == 0:
                return True
        except (ValueError, TypeError):
            return False

