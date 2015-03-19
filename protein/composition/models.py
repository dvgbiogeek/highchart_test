from django.db import models
import re


class Protein(models.Model):
    name = models.CharField(max_length=160)
    sequence = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Protein, self).save(*args, **kwargs)

    def clean(self):
        if self.sequence:
            self.sequence = re.sub(r"\s+", "", self.sequence)
