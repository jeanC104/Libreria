from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import Book, Favourite
from .serializers import BookSerializer, FavouriteSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	paginate_by = 10


class FavouriteViewSet(viewsets.ViewSet):

	queryset = Favourite.objects.all()
	permission_classes = [IsAuthenticated]

	def list(self, request):
		favourite_books = Favourite.objects.filter(user = request.user)
		favourite_ser = FavouriteSerializer(favourite_books, many=True, context={'request': request})
		return Response(favourite_ser.data)

	def retrieve(self, request, pk):
		favourite_book = Favourite.objects.get(user = request.user, pk = pk)
		favourite_ser = FavouriteSerializer(favourite_book)
		return Response(favourite_ser.data)

	def create(self, request):
		if Favourite.objects.filter(user = request.user, book__id = request.POST['book']).exists():
			Favourite.objects.get(user = request.user, book__id = request.POST['book']).delete()
		else:
			Favourite.objects.create(user = request.user, 
						book = get_object_or_404(Book, pk = request.POST['book']))
		return Response(status=status.HTTP_201_CREATED)