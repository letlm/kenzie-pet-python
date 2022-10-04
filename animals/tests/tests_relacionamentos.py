from animals.models import Animal
from django.test import TestCase
from groups.models import Group
from traits.models import Trait

# One to Many
# Group (1) e Animal (N)

class AnimalGroupTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.animal_one_data = {
            "name":"Shake de Milkshake",
            "age":5,
            "weight": 5,
            "sex":"Macho"
        }

        cls.animal_two_data = {
            "name":"Pudim",
            "age":5,
            "weight": 3
        }

        cls.animal_three_data = {
            "name":"Estopinha",
            "age": 5,
            "weight": 3,
            "sex": "Femea"
        }

        cls.group_data = {
            "name":"dog",
            "scientific_name": "canis familiaris"
        }

        
        cls.group = Group.objects.create(**cls.group_data)

      

        cls.animal_one = Animal.objects.create(**cls.animal_one_data)
        cls.animal_two = Animal.objects.create(**cls.animal_two_data)
        cls.animal_three = Animal.objects.create(**cls.animal_three_data)

        cls.animals = Animal.objects.all()

    def test_group_may_contain_multiple_animals(self):
        for animal in self.animals:
            animal.group = self.group
            animal.save()

        self.assertEquals(
            len(self.animals),
            self.group.animals.count()
        )

        for animal in self.animals:
            self.assertIs(animal.group, self.group)

    def test_animal_cannot_belong_to_more_than_one_group(self):
        for animal in self.animals:
            animal.group = self.group
            animal.save()

        group_two_data = {
            "name":"cat",
            "scientific_name": "cats familiaris"
        }

        group_two = Group.objects.create(**group_two_data)

        for animal in self.animals:
            animal.group = group_two
            animal.save()
        
        for animal in self.animals:
            self.assertNotIn(animal, self.group.animals.all())
            self.assertIn(animal, group_two.animals.all())


## Many To Many
# Traist #Animals
class AnimalAndTraitsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.animal_one_data = {
            "name":"Shake de Milkshake",
            "age":5,
            "weight": 5,
            "sex":"Macho"
        }

        cls.animal_two_data = {
            "name":"Pudim",
            "age":5,
            "weight": 3
        }

        cls.animal_three_data = {
            "name":"Estopinha",
            "age": 5,
            "weight": 3,
            "sex": "Femea"
        }

        cls.animal_one = Animal.objects.create(**cls.animal_one_data)
        cls.animal_two = Animal.objects.create(**cls.animal_two_data)
        cls.animal_three = Animal.objects.create(**cls.animal_three_data)

        cls.animals = Animal.objects.all()

        cls.traits_data = {
            "name":"fofinho"
        }

        cls.traits = Trait.objects.create(**cls.traits_data)

    def test_trait_with_more_than_one_animal(self):
        for animal in self.animals:
            self.traits.animals.add(animal)

        self.assertEquals(len(self.animals), self.traits.animals.count())

        for animal in self.animals:
            self.assertIn(self.traits, animal.traits.all())


    def test_animal_with_more_than_one_trait(self):
        traits_two_data = {
            "name": "pelo curto"
        }

        traits_two = Trait.objects.create(**traits_two_data)

        for animal in self.animals:
            animal.traits.add(self.traits)
            animal.save()
            animal.traits.add(traits_two)
            animal.save()

            self.assertIn(animal, self.traits.animals.all())
        