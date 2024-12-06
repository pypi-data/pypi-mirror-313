import cv2 as cv
import datetime
import imagesize
import numpy

from datetime import date

from django.core.files import File
from django.core.files.storage import storages
from django.core.validators import get_available_image_extensions
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from crimsonslate_portfolio.validators import validate_media_file_extension


class MediaCategory(models.Model):
    name = models.CharField(max_length=64)
    cover = models.ImageField(
        verbose_name="cover image",
        storage=storages["bucket"],
        upload_to="category/",
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Media(models.Model):
    title = models.CharField(
        max_length=64,
        unique=True,
    )
    source = models.FileField(
        upload_to="source/",
        storage=storages["bucket"],
        validators=[validate_media_file_extension],
    )
    thumb = models.ImageField(
        verbose_name="thumbnail",
        storage=storages["bucket"],
        upload_to="thumb/",
        null=True,
        blank=True,
        default=None,
    )
    subtitle = models.CharField(max_length=128, blank=True, null=True, default=None)
    desc = models.TextField(
        verbose_name="description", max_length=2048, blank=True, null=True, default=None
    )
    slug = models.SlugField(
        max_length=64, unique=True, blank=True, null=True, default=None
    )
    is_hidden = models.BooleanField(default=False)
    is_image = models.BooleanField(default=None, blank=True, null=True)
    categories = models.ManyToManyField("MediaCategory", default=None, blank=True)

    date_created = models.DateField(default=date.today)
    datetime_published = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["date_created"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "slug"],
                name="%(app_label)s_%(class)s_unique_title_and_slug",
            )
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, **kwargs) -> None:
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)

        if self.file_extension in get_available_image_extensions():
            self.is_image = True
        else:
            self.is_image = False
            self.set_thumbnail(file=None)
        return super().save(**kwargs)

    def get_absolute_url(self) -> str:
        return reverse("media detail", kwargs={"slug": self.slug})

    def set_thumbnail(self, file: File | None = None) -> None:
        self.thumb = file if file else self.generate_thumbnail()

    def generate_thumbnail(self, loc: int = 0) -> File:
        timestamp: str = f"{datetime.datetime.now():%y_%m_%d_%f}"
        filename: str = f"default_thumbnail_{timestamp}.jpg"
        frame: numpy.ndarray = self._capture_frame(loc)

        cv.imwrite(filename, frame)
        return File(open(filename, "rb"))

    def _capture_frame(self, loc: int = 0) -> numpy.ndarray:
        if self.is_image:
            raise ValueError("Cannot capture frame from image")

        capture = cv.VideoCapture(self.source.path)
        if loc > 0:
            capture.set(cv.CAP_PROP_POS_FRAMES, loc)

        try:
            ret, frame = capture.read()
            if not ret:
                raise ValueError(f"Failed to read frame {loc} in '{self.source.path}'")
            if frame.dtype != numpy.uint8:
                frame = numpy.clip(frame * 255, 0, 255).astype(numpy.uint8)
            return frame

        finally:
            capture.release()

    @property
    def dimensions(self) -> tuple[int, int]:
        if not self.is_image and not self.thumb:
            self.set_thumbnail(file=None)
            self.refresh_from_db()

        image = self.source.path if self.is_image else self.thumb.path
        width, height = imagesize.get(image)
        return int(width), int(height)

    @property
    def file_extension(self) -> str:
        return self.source.file.name.split(".")[-1]

    @property
    def url(self) -> str:
        return self.source.url
