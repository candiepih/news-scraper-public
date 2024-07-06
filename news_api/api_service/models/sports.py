from .base_model import BaseModel


class Sports(BaseModel):
    class Meta:
        db_table = 'sports'
        verbose_name = 'Sports'
        verbose_name_plural = 'Sports'
