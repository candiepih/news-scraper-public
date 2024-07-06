from .base_model import BaseModel


class VideoGames(BaseModel):
    class Meta:
        db_table = 'video_games'
        verbose_name = 'Video Games'
        verbose_name_plural = 'Video Games'
