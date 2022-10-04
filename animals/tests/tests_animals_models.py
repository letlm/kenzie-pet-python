from animals.models import Animal
from django.core.exceptions import ValidationError
from django.test import TestCase


class AnimalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.sex_default = "Não informado"

        cls.animal_one_data = {
            "name":"Shake de Milkshake",
            "age":5,
            "weight":6,
            "sex":"Macho"
        }

        cls.animal_two_data = {
            "name":"Pudim",
            "age":5,
            "weight":6
        }

        cls.animal_three_data = {
            "name":"Estopinha",
            "age": 5,
            "weight":4,
            "sex": "Escolha inválida"
        }

        cls.animal_four_data = {
            "name":"Estopinha",
            "age": "None",
            "weight": "None",
            "sex": "Femea"
        }


        cls.animal_one = Animal.objects.create(**cls.animal_one_data)

        cls.animal_two = Animal.objects.create(
            **cls.animal_two_data
        )

        cls.animal_three = Animal(**cls.animal_three_data)

        cls.animal_four = Animal(**cls.animal_four_data)

    def test_animals_fields(self):
        self.assertEqual(self.animal_one.name, self.animal_one_data["name"])
        self.assertEqual(self.animal_one.age, self.animal_one_data["age"])
        self.assertEqual(self.animal_one.weight, self.animal_one_data["weight"])
        self.assertEqual(self.animal_one.sex, self.animal_one_data["sex"])

    def test_name_max_length(self):
        animal = Animal.objects.get(id=1)
        max_length = animal._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_sex_default_choice(self):
        animal = Animal.objects.get(id=2)
        sex_default_animal = animal.sex
        self.assertEqual(sex_default_animal, self.sex_default)

    def test_sex_wrong_choice(self):
        with self.assertRaises(ValidationError):
            self.animal_three.full_clean()
    
    def test_age_and_weight_incorrect_fields(self):
        with self.assertRaises(ValidationError):
            self.animal_four.full_clean()
       
