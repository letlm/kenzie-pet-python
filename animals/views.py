from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status

from .models import Animal
from .serializers import AnimalSerializer


class AnimalsView(APIView):

    def get(self, request: Request) -> Response:
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)
       
        return Response(serializer.data)


    def post(self, request: Request) -> Response:

        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnimalDetailsView(APIView):
    def patch(self, request: Request, animal_id: int) -> Response:
        
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)

        serializer.save()
       
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
