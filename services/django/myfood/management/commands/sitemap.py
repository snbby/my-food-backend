from datetime import datetime

from django.core.management import BaseCommand
from myfood.models import FoodProduct


class Command(BaseCommand):
    base_url = 'https://my-food.com'
    local_path = 'artifacts/myfood/sitemap.xml'
    skip_product_names = ['And', 'Aux', '100%', 'With', 'Mix', 'Free', 'Atlantic', 'M&m\'s']

    def generate(self, links: list):
        # links = ['https://my-food.com', 'https://about.com']
        today = datetime.today().strftime('%Y-%m-%d')
        
        with open(self.local_path, 'w') as f:
            f.writelines(['<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'])
            for link in links:
                f.writelines(
                        [
                            '    <url>\n',
                            f'       <loc>{link}</loc>\n', 
                            f'       <lastmod>{today}</lastmod>\n',
                            '        <changefreq>daily</changefreq>\n',
                            '        <priority>0.8</priority>\n',
                            '    </url>\n'
                        ]
                    )
            
            f.writelines('</urlset>')

    
    def handle(self, *args, **options):
        # print(self.get_product_occurances())
        # print(self.get_brand_occurances())
        sitemap_urls = []
        for row, (product, num) in enumerate(self.get_product_occurances().items()):
            if num < 100:
                break
            print(row, product, num)
            sitemap_urls.append(f'{self.base_url}/?search={product}')
        self.generate(sitemap_urls)
        
    def get_product_occurances(self):
        product_occurances = {}
        products = FoodProduct.objects.all()
        
        for product in products:
            product_name = product.product_name.split(' ')
            for name in product_name:
                name = name.capitalize().replace(',', '')
                
                if len(name) > 2 and name not in self.skip_product_names:
                    if name not in product_occurances:
                        product_occurances[name] = 1
                    else:
                        product_occurances[name] += 1
        sorted_product_occurances = {k: v for k, v in sorted(product_occurances.items(), key=lambda item: item[1], reverse=True)}
        return sorted_product_occurances
    
    def get_brand_occurances(self):
        brand_occurances = {}
        products = FoodProduct.objects.all()
        
        for product in products:
            product_brands = product.brands.split(',')
            for brand in product_brands:
                brand = brand.capitalize()
                
                if len(brand) > 2 and brand not in self.skip_product_names:
                    if brand not in brand_occurances:
                        brand_occurances[brand] = 1
                    else:
                        brand_occurances[brand] += 1
        sorted_brand_occurances = {k: v for k, v in sorted(brand_occurances.items(), key=lambda item: item[1], reverse=True)}
        return sorted_brand_occurances