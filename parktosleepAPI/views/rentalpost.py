"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from datetime import timezone
import datetime
import pytz
from datetime import date
from rest_framework.decorators import action
from parktosleepAPI.models import RentalPost, Rentee, BookedSpot


class RentalPostsView(ViewSet):
    """Rental Posts"""

    @action(methods=['post', ], detail=True)
    def book(self, request, pk=None):
        """Managing users booking rental spots"""

        # A user wants to book a spot
        if request.method == "POST":
            # The pk would be `id` if the URL above was requested
            rental_spot = RentalPost.objects.get(pk=pk)

            # Django uses the `Authorization` header to determine
            # which user is making the request to sign up
            renter = Rentee.objects.get(pts_user=request.auth.user)

            # try:
            # Determine if the spot is already booked
            # replace this string with whatever method or function collects your data
            date_in = request.data["date"]

            date_processing = date_in.replace(
                'T', ' ')
            date_processing += ":00"

            date_is_processing = date_in.replace(
                'T', '-').replace(':', '-').split('-')
            date_is_processing = [int(v) for v in date_is_processing]
            datebooked = datetime.datetime(*date_is_processing)
            awareTimezone = pytz.utc.localize(datebooked)
            try:
                books = BookedSpot.objects.all()

                alreadybooked = BookedSpot.objects.get(
                    rental_spot=rental_spot
                )
                book = BookedSpot.objects.get(
                    date=date_processing)
                # except RuntimeWarning:

                # print(alreadybooked.rental_spot.start_time,
                #       alreadybooked.rental_spot.end_time)

            except BookedSpot.DoesNotExist:

                # The spot is not booked.
                book = BookedSpot()
                book.rental_spot = rental_spot
                book.renter = renter
                book.date = request.data["date"]

                if awareTimezone > rental_spot.end_time or awareTimezone < rental_spot.start_time:
                    return Response(
                        {'message': 'Date is outside of booking range.'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )
                book.save()
                return Response({}, status=status.HTTP_201_CREATED)

            except BookedSpot.MultipleObjectsReturned:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        sort_parameter = self.request.query_params.get('sortby', None)

        if sort_parameter is not None and sort_parameter == 'user':
            current_pts_user = Rentee.objects.get(pts_user=request.auth.user)
            user_posts = RentalPost.objects.filter(
                rentee=current_pts_user)

            serializer = RentalPostSerializer(
                user_posts, many=True, context={'request': request})

            return Response(serializer.data)
        # Run the  RentalPost objects throught the serializer to parse wanted properties and to return JS readble code.

        post = self.request.query_params.get('rentalpost_id', None)
        if post is not None:
            rentalposts = rentalposts.filter(rentalposts_id=post)
        try:
            for rp in rentalposts:
                if rp.rentee == request.auth.user:
                    rp.is_current_user = True
                else:
                    rp.is_current_user = False

            serializer = RentalPostSerializer(rentalposts,
                                              many=True, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        rentalpost = RentalPost.objects.get(pk=pk)

        pts_user = Rentee.objects.get(pts_user=request.auth.user)

        rentalpost.rentee = pts_user
        rentalpost.max_length = request.data["max_length"]
        rentalpost.description = request.data["description"]
        rentalpost.city = request.data["city"]
        rentalpost.state = request.data["state"]
        rentalpost.address = request.data["address"]
        rentalpost.start_time = request.data["start_time"]
        rentalpost.end_time = request.data["end_time"]

        rentalpost.save(force_update=True)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

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
        fields = ('id', 'first_name', 'last_name',)


class RenteeSerializer(serializers.ModelSerializer):

    pts_user = UserSerializer(many=False)

    class Meta:

        model = Rentee
        fields = ["pts_user", 'phone']
        depth = 2


class RentalPostSerializer(serializers.ModelSerializer):
    """JSON serializer for Rental Postd

    Arguments:
        serializer type
    """
    rentee = RenteeSerializer(many=False)

    class Meta:
        model = RentalPost
        fields = ('id', 'rentee', 'max_length', 'description',
                  'city', 'state', 'address', 'start_time', 'end_time',)
        depth = 2
