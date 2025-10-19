from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    platform = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Початкова (стара) ціна для відображення знижки
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    cover = models.ImageField(upload_to='images/', blank=True, null=True)
    screenshot = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def discount_percent(self):
        try:
            if self.original_price and self.original_price > 0 and self.price is not None and self.original_price > self.price:
                return int(round(100 - (float(self.price) / float(self.original_price) * 100)))
        except Exception:
            return None
        return None

    class Meta:
        unique_together = (('title', 'platform'),)
        indexes = []
