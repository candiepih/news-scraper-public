from .base_model import BaseModel


class GlobalNews(BaseModel):
    class Meta:
        db_table = 'global_news'
        verbose_name = 'Global News'
        verbose_name_plural = 'Global News'
