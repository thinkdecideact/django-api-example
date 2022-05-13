from django.db import models
from django.utils import timezone


class Store(models.Model):
    name = models.CharField('name', max_length=255, blank=True, null=True)
    address = models.CharField('address', max_length=255, blank=True, null=True)
    priority = models.PositiveIntegerField('order', default=100)
    ctime = models.DateTimeField('create time', blank=True, null=True, default=timezone.now)
    mtime = models.DateTimeField('update time', blank=True, null=True, default=timezone.now)
    comment = models.CharField('comment', max_length=255, blank=True, null=True)
    is_active = models.IntegerField('active status', choices=[(1, 'Yes'), (0, 'No')], default=1)
    is_del = models.IntegerField('delete status', choices=[(1, 'Yes'), (0, 'No')], default=0)

    class Meta:
        managed = False
        db_table = 'tdar_store'
        verbose_name = 'Store'
        verbose_name_plural = verbose_name
        ordering = ('-mtime', '-pk', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.ctime = timezone.now()
        self.mtime = timezone.now()
        return super().save(*args, **kwargs)
