from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
import os
from django.conf import settings
from posts.models import Post
import random
from unidecode import unidecode
class Command(BaseCommand):
    help = 'Download images from RichTextField content'

    def handle(self, *args, **kwargs):
        queryset = Post.objects.all()  # Adjust this query as per your needs

        for post in queryset:
            soup = BeautifulSoup(post.content, 'html.parser')
            img_tags = soup.find_all('img')

            for img_tag in img_tags:
                img_url = img_tag.get('src')

                # Download image
                if img_url:
                    response = requests.get(img_url)
                    if response.status_code == 200:
                        post_name = unidecode(post.title).replace(' ', '_').replace('"', '')
                        random_number = random.randint(1, 10000)
                        image_name = post_name + '_' + str(random_number) + '.jpg'
                        save_path = os.path.join(settings.MEDIA_ROOT, 'library', image_name )
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)

                        with open(save_path, 'wb') as f:
                            f.write(response.content)

                        self.stdout.write(self.style.SUCCESS(f'Successfully downloaded {image_name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Failed to download {img_url}'))
