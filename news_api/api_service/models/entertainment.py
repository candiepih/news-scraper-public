from .base_model import BaseModel


class Entertainment(BaseModel):
    class Meta:
        db_table = 'entertainment'
        verbose_name = 'Entertainment'
        verbose_name_plural = 'Entertainment'
