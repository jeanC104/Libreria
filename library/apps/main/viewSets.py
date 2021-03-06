from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Book, Favourite, Comment
from .serializers import BookSerializer, FavouriteSerializer, CommentSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	paginate_by = 10


class FavouriteViewSet(viewsets.ModelViewSet):

	queryset = Favourite.objects.all()
	permission_classes = [IsAuthenticated]
	serializer_class = FavouriteSerializer

	def get_queryset(self):
		return self.queryset.filter(user = self.request.user)

	def create(self, request):
		if Favourite.objects.filter(user = request.user, book__id = request.DATA['book']).exists():
			Favourite.objects.get(user = request.user, book__id = request.DATA['book']).delete()
		else:
			Favourite.objects.create(user = request.user, 
						book = get_object_or_404(Book, pk = request.DATA['book']))
		return Response(status = status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def get_queryset(self):
		return self.queryset.filter(book__pk = self.kwargs["book_pk"])