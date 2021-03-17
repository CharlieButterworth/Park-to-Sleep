"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date
from parktosleepAPI.models import RentalPost, Rentee


class RentalPostsView(ViewSet):
    """Rental Posts"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """

        pts_user = Rentee.objects.get(pts_user=request.auth.user)

        rentalpost = RentalPost()
        rentalpost.rentee = pts_user
        rentalpost.max_length = request.data["maxLength"]
        rentalpost.description = request.data["description"]
        rentalpost.city = request.data["city"]
        rentalpost.state = request.data["state"]
        rentalpost.address = request.data["address"]
        rentalpost.start_time = request.data["start_time"]
        rentalpost.end_time = request.data["end_time"]

        try:
            rentalpost.save()
            serializer = RentalPostSerializer(
                rentalpost, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post
        Returns:
            Response -- JSON serialized post instance
        """

        # pts_user = pts_token.objects.get(user=request.auth.user)


# This is where the if/else is for which post renders when

        try:
            rentalpost = RentalPost.objects.get(pk=pk)

            serializer = RentalPostSerializer(
                rentalpost, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """

        # ORM MEthod that get all Rental Posts objects from the DB

        rentalposts = RentalPost.objects.all()

        # Run the  RentalPost objects throught the serializer to parse wanted properties and to return JS readble code.

        serializer = RentalPostSerializer(
            rentalposts, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single rental post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            rentalpost = RentalPost.objects.get(pk=pk)
            rentalpost.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RentalPost.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class RenteeSerializer(serializers.ModelSerializer):

    pts_user = UserSerializer(many=False)

    class Meta:

        model = Rentee
        fields = ["pts_user", ]


class RentalPostSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    rentee = RenteeSerializer(many=False)

    class Meta:
        model = RentalPost
        fields = ('id', 'rentee', 'max_length', 'description',
                  'city', 'state', 'address', 'start_time', 'end_time',)
        depth = 2
