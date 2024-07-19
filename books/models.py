from django.db import models
from django.utils.text import slugify

from publishers.models import Publisher
from authors.models import Author
import uuid

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.conf import settings


class BookTitle(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Book Position {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Book(models.Model):
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=24, blank=True)
    # QR code
    qr_code = models.ImageField(upload_to="qr_codes", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.book_id:
            # make the self.book.id 24 characters

            self.book_id = uuid.uuid4().hex[:24].lower()

            #  self.book_id = str(uuid.uuid4().hex[:24].lower())

            # self.book_id = str(uuid.uuid4().('-', '')[:24].lower())

            # generate QR code
            qrcode_img = qrcode.make(self.book_id)
            canvas = Image.new('RGB', (290, 290), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.title}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()

        return super().save(*args, **kwargs)
