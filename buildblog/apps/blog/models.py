from distutils.command.upload import upload
from email.mime import image
from email.policy import default
from urllib.parse import urlparse
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from common.app_utils import unique_media_upload, icon_media_upload
from django.core.validators import FileExtensionValidator
from ckeditor_uploader.fields import RichTextUploadingField 

User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


TECHNOLOGY_TYPE_CHOICES = (
    (1, _("Programing Language")),
    (2, _("Database")),
    (3, _("Framework")),
    (4, _("Cloud Service")),
    (5, _("Web Server")),
    (6, _("Library")),
    (7, _("Git Platform")),
)


class Technology(BaseModel):
    name = models.CharField(_('Title'), max_length=250)
    platform = models.IntegerField(choices=TECHNOLOGY_TYPE_CHOICES, default=1)
    icon = models.FileField(upload_to= icon_media_upload, validators=[FileExtensionValidator(['svg'])])
    background_image = models.ImageField(upload_to = unique_media_upload, null=True, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Technology"

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.img.url
        except:
            url=''
        return url


class Blog(BaseModel):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=40)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_users")
    contents = RichTextUploadingField()
    image = models.ImageField(upload_to=unique_media_upload)
    video = models.FileField(upload_to=unique_media_upload, null=True, blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    published = PublishedManager()
    url = models.URLField(max_length=400)
    related_technology = models.ManyToManyField(Technology)
    sub_title = models.CharField(max_length=254)
    objects = models.Manager()
    published = PublishedManager()
    point = models.IntegerField(default=0)
    primary_technology = models.ForeignKey(Technology, related_name="blog_technologies", on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, blank=True, related_name='like')
    like_count = models.BigIntegerField(default='0')

    class Meta:
        ordering = ("-published_at",)

    def url_text(self):
        parsed_url = urlparse(self.url)
        return parsed_url.hostname

    def get_absolute_url(self):
        return reverse('blog_list', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title}"
    
    def total_likes(self):
        return self.likes.all().count()


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


