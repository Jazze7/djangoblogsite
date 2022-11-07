import csv
import uuid
import wget
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from posts.models import Author, Category, Post
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Deleting existing data")

        Category.objects.all().delete()
        Post.objects.all().delete()
        Author.objects.all().delete()

        file = open(settings.BASE_DIR / "new_posts.csv")
        csv_reader = csv.reader(file)

        next(csv_reader)

        for row in csv_reader:
            author_name = row[1].split(",")[0]
            content = row[2]
            date = row[3]
            tags = row[5]
            title = row[6]
            image = "https://picsum.photos/1500/1000"
            file_name = f'{uuid.uuid4()}.jpg'
            file_path = f'{settings.BASE_DIR}/media/posts/{file_name}'
            image_filename = wget.download(image, file_path)

            uploaded_file_url = f'posts/{file_name}'

            if Author.objects.filter(name=author_name).exists():
                author = Author.objects.filter(name=author_name)[0]
            else:
                user = User.objects.create_user(
                    username=uuid.uuid4(),
                    password="password",
                    first_name=author_name,
                )
                author = Author.objects.create(name=author_name, user=user)
            post = Post.objects.create(
                title=title,
                description=content,
                short_description=content[:50],
                time_to_read="6 mins",
                featured_image=uploaded_file_url,
                author=author,
                published_date=date
            )
            tags_list = tags.split(',')
            for tag in tags_list:
                if not tag.strip() == "":
                    item, created = Category.objects.get_or_create(title=tag)
                    post.categories.add(item)
        print("Process Completed")
