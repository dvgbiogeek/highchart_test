from django.db import models
import re


class Protein(models.Model):
    name = models.CharField(max_length=160)
    sequence = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overwrite django's save function to customize cleaning of the data
        using my custom clean() function.
        """
        self.full_clean()
        super(Protein, self).save(*args, **kwargs)

    def clean(self):
        """
        Cleans the data by removing whitespace and converting the sequence to
        all uppercase.
        """
        if self.sequence:
            self.sequence = re.sub(r"\s+", "", self.sequence)
            self.sequence = self.sequence.upper()
