from django.test import TestCase
from traits.models import Trait


class TraitsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.trait_one_data = {
            "name":"fofinho",
        }

        cls.trait_one = Trait.objects.create(**cls.trait_one_data)


    def test_trait_fields(self):
        self.assertEqual(self.trait_one.name, self.trait_one_data["name"])
      

    def test_name_max_length(self):
        trait = Trait.objects.get(id=1)
        max_length = trait._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

