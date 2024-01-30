import fake_data_generator_setup
from django.contrib.auth.models import User, Permission, ContentType
from post.models import Category, Post
from album.models import Album, Image
from search.models import Search, Option
from random import randrange, choice, choices
from django.utils import timezone
from unidecode import unidecode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from PIL import Image as PillowImage
import urllib
import faker

fake = faker.Faker('pt_BR')


def fill_out_image_field(image_field, required=False):
    try:
        image = PillowImage.open(urllib.request.urlretrieve(fake.image_url(width=randrange(400, 800),
                                                                           height=randrange(400, 800)))[0])
        img_name = fake.words(nb=1)[0] + str(randrange(11111, 99999)) + '.jpg'

        buffer = BytesIO()
        image = image.convert('RGB')
        image.save(fp=buffer, format='JPEG')
        pillow_image = ContentFile(buffer.getvalue())

        image_field.save(img_name, InMemoryUploadedFile(
            pillow_image,
            None,
            img_name,
            'image/jpeg',
            pillow_image.tell,
            None)
        )
    except urllib.error.HTTPError:
        if required:
            fill_out_image_field(image_field, required=True)


def admin_generator():
    User.objects.create_superuser(
        username='admin',
        email='admin@email.com',
        password='blognews123admin',
        first_name='admin',
        last_name='admin'
    )


def user_generator():
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = unidecode(first_name.replace(' ', '_')) + str(randrange(10000, 99999))
    email = username + '@email.com.br'
    password = username
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    return user


def content_creator_generator():
    user = user_generator()
    for model in [Post, Search, Option, Album, Image]:
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        [user.user_permissions.add(permission) for permission in permissions]

    return user


def category_generator():
    title = ' '.join(fake.words(nb=randrange(1, 5)))

    category = Category.objects.create(
        title=title
    )

    return category


def post_generator(user, category):
    title = fake.text(max_nb_chars=50)
    excerpt = fake.text(max_nb_chars=300)
    description = fake.text(max_nb_chars=5000)
    published = choices([True, False], weights=(90, 10))[0]

    post = Post.objects.create(
        title=title,
        excerpt=excerpt,
        description=description,
        published=published,
        category=category,
        user=user
    )
    image_field = post.image
    fill_out_image_field(image_field)

    return post


def album_generator(user):
    title = fake.text(max_nb_chars=50)
    published = choices([True, False], weights=(90, 10))[0]

    return Album.objects.create(
        title=title,
        published=published,
        user=user
    )


def image_generator(album):
    title = fake.text(max_nb_chars=50)

    image = Image.objects.create(
        title=title,
        album=album
    )

    image_field = image.image
    fill_out_image_field(image_field, required=True)


def research_generator(user):
    description = fake.text(max_nb_chars=300)
    days = randrange(0, 10)
    publication_date = timezone.now() + timezone.timedelta(days=days)
    finish_date = timezone.now() + timezone.timedelta(days=(days + randrange(10, 100)))

    return Search.objects.create(
        description=description,
        publication_date=publication_date,
        finish_date=finish_date,
        user=user)


def option_generator(research):
    response = fake.text(max_nb_chars=300)

    Option.objects.create(
        response=response,
        search=research
    )


if __name__ == '__main__':
    admin_generator()

    content_creators = [content_creator_generator() for _ in range(10)]

    categories = [category_generator() for _ in range(5)]

    [[post_generator(user, choice(categories)) for _ in range(randrange(1, 10))] for user in content_creators]

    albums = [album_generator(user) for _ in range(randrange(1, 5)) for user in content_creators]

    [image_generator(choices(albums)[0]) for _ in range(25)]

    researches = (research_generator(user) for _ in range(randrange(2, 5)) for user in content_creators)

    [[option_generator(research) for _ in range(randrange(2, 8))] for research in researches]

    [user_generator() for _ in range(100)]
