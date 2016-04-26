from django.db import models


class BaseCar(models.Model):
    colour = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)


class HondaCar(BaseCar):
    cupholders = models.IntegerField()

    def __unicode__(self):
        return "%s %s Honda Car" % (self.colour, self.model)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'car'
        # verbose_name = 'spaceship'


class FordCar(BaseCar):
    horsepowers = models.IntegerField()
