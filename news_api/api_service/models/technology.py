from .base_model import BaseModel


class Technology(BaseModel):
    class Meta:
        db_table = 'technology'
        verbose_name = 'Technology'
        verbose_name_plural = 'Technology'
