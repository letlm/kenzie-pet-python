from math import log as ln

from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException
from traits.models import Trait
from traits.serializers import TraitsSerializer

from .models import Animal, SexOptions


class FieldsException(APIException):
    status_code = 422

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexOptions.choices, 
        default=SexOptions.UNINFORMED)

    age_in_human_years = serializers.SerializerMethodField(read_only=True)
    
    group = GroupSerializer()
    traits = TraitsSerializer(many=True)
    
    def get_age_in_human_years(self, obj):
        human_age = 16 * ln(obj.age) + 31
        return round(human_age, 2)


    def create(self, validated_data: dict) -> Animal:
        group_animal = validated_data.pop('group')
        traits_animal = validated_data.pop('traits')

        group_save = Group.objects.get_or_create(**group_animal)[0]

        animal = Animal.objects.create(**validated_data, group=group_save)

        for trait in traits_animal:
            traits_save = Trait.objects.get_or_create(**trait)[0]
            animal.traits.add(traits_save)

        return animal


    def update(self, instance: Animal, validated_data: dict) -> Animal:
        keys_not_editable = ('sex', 'group', 'traits')
        key_errors = {}

        for key, value in validated_data.items():
            if key in keys_not_editable:
                key_errors.update({f'{key}': f'You can not update {key} property'})
                continue

            setattr(instance, key, value)

        if key_errors:
            raise FieldsException(key_errors)

        instance.save()
        return instance



