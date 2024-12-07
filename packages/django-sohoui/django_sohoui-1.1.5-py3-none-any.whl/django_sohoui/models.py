from django.db import models

class AdminMenus(models.Model):
    
    name = models.CharField(max_length=100, verbose_name='菜单名称' )
    url = models.URLField(verbose_name='菜单链接')
    icon = models.CharField(max_length=100, verbose_name='菜单图标icon')
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父级菜单')
    sort = models.IntegerField(verbose_name='排序')
    is_show = models.BooleanField(verbose_name='是否显示')
    
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'System菜单设置'
        verbose_name_plural = 'System菜单设置'
        ordering = ['sort']
