from django.db import models


class Glossary(models.Model):
    term = models.CharField(max_length=160)
    definition = models.TextField()
    reference = models.CharField(max_length=160)

    def __str__(self):
        return self.term
