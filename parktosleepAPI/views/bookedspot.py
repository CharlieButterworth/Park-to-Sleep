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
from parktosleepAPI.models import RentalPost, Rentee, BookedSpot


class BookSpotView(ViewSet):

    #   This will create the booked spot
    def create(self, request, pk=None):

        pts_user = Rentee.objects.get(pts_user=request.auth.user)
        rentalpost = RentalPost.objects.get(pk=pk)

        bookedspot = BookedSpot()
        bookedspot.renter = pts_user
        bookedspot.rental_spot = rentalpost

        bookedspot.date = request.data['date']

        try:
            bookedspot.save()
            serializer = BookedSpotSerializer(
                bookedspot, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single booking
        Returns:
            Response -- JSON serialized post instance
        """

        # pts_user = pts_token.objects.get(user=request.auth.user)


# This is where the if/else is for which post renders when

        try:
            bookedspot = BookedSpot.objects.get(pk=pk)

            serializer = BookedSpotSerializer(
                bookedspot, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """

        # ORM MEthod that get all Booked Spots objects from the DB

        bookedspot = BookedSpot.objects.all()

        sort_parameter = self.request.query_params.get('sortby', None)

        if sort_parameter is not None and sort_parameter == 'user':
            current_pts_user = Rentee.objects.get(
                pts_user=request.auth.user)
            user_bookings = BookedSpot.objects.filter(
                renter=current_pts_user)

            serializer = BookedSpotSerializer(
                user_bookings, many=True, context={'request': request})

            return Response(serializer.data)

        if sort_parameter is not None and sort_parameter == 'rentee':
            current_pts_user = Rentee.objects.get(
                pts_user=request.auth.user)
            user_bookings = BookedSpot.objects.filter(
                renter=current_pts_user)

            serializer = BookedSpotSerializer(
                user_bookings, many=True, context={'request': request})

            return Response(serializer.data)

        # Run the  RentalPost objects throught the serializer to parse wanted properties and to return JS readble code.

        serializer = BookedSpotSerializer(bookedspot,
                                          many=True, context={'request': request})

        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
        depth = 2


class RenteeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rentee
        fields = ('pts_user', )


class BookedSpotSerializer(serializers.ModelSerializer):

    renter = RenteeSerializer(many=False)

    class Meta:
        model = BookedSpot
        fields = ('renter', 'date', 'rental_spot',)
        depth = 3
