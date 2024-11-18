from faker import Faker
from pytest import mark

from myfood.models import ModelOpenAIImageGeneration

faker = Faker()

@mark.long
def test_openai_image_generations():
    image = ModelOpenAIImageGeneration(
        prompt=faker.sentence(nb_words=10), 
        image_resolution=ModelOpenAIImageGeneration.OpenAIImageResolution.s256x256, 
        use_dalle3=False
        )
    image.save()
    
    assert image.s3_generated_image is not None
    assert image.image_size is not None
    assert image.image_resolution is not None
    