from django.test import TestCase
from groups.models import Group


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.group_one_data = {
            "name":"dog",
            "scientific_name": "canis familiaris"
        }


        cls.group_one = Group.objects.create(**cls.group_one_data)


    def test_groups_fields(self):
        self.assertEqual(self.group_one.name, self.group_one_data["name"])
        self.assertEqual(self.group_one.scientific_name, self.group_one_data["scientific_name"])


    def test_name_max_length(self):
        group = Group.objects.get(id=1)
        max_length = group._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

    def test_scientific_name_max_length(self):
        group = Group.objects.get(id=1)
        max_length = group._meta.get_field('scientific_name').max_length
        self.assertEqual(max_length, 50)

