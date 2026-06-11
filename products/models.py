from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_(
        'parent'), on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    title = models.CharField(_("title"), max_length=50)
    describtion = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(
        _('avatar'), upload_to='categories/', blank=True)
    is_enabled = models.BooleanField(_('is enabled'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        
    def __str__(self):
        return self.title

class Product(models.Model):
    categories = models.ManyToManyField(Category, verbose_name=_(
        'categories'), blank=True, related_name='products')
    title = models.CharField(_('title'), max_length=50)
    describtion = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='products/', blank=True)
    is_enabled = models.BooleanField(_('is enabled'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = _('product')
        verbose_name_plural = _('products')


class File(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(
        'product'), on_delete=models.CASCADE, related_name='files')
    title = models.CharField(_('title'), max_length=50)
    file = models.FileField(_('file'), upload_to='files/%Y/%m/%d/')
    is_enabled = models.BooleanField(_('is enabled'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name = _('file')
        verbose_name_plural = _('files')
