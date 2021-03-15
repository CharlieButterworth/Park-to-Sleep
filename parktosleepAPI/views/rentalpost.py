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

        # pts_user = Rentee.objects.get(user=request.auth.user)

        rentalpost = RentalPost()
        # rentalpost.rentee = pts_user
        rentalpost.maxLength = request.data["max_length"]
        rentalpost.description = request.data["description"]
        rentalpost.city = request.data["city"]
        rentalpost.approved = True
        rentalpost.state = request.data["state"]
        rentalpost.address = request.data["address"]
        rentalpost.startTime = request.data["start_time"]
        rentalpost.endTime = request.data["end_time"]

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


class RentalPostSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = RentalPost
        fields = ('id', 'rentee', 'max_length', 'description',
                  'city', 'state', 'address', 'start_time', 'end_time')
        depth = 1
