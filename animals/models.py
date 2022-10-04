from django.db import models


class SexOptions(models.TextChoices):
    MALE = 'Macho'
    FEMALE = 'Femea'
    UNINFORMED = 'Não informado'


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15, 
        choices=SexOptions.choices, 
        default=SexOptions.UNINFORMED
    )

    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="animals", null=True, blank=True)
    traits = models.ManyToManyField("traits.Trait", related_name="animals")


   