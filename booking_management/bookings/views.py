from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from .serializers import BookingSerializer
import logging

logger = logging.getLogger('django')

class BookingAPIView(APIView):
    def post(self, request):
        # Extract booking details
        room_id = request.data.get("room_id")
        check_in_date = request.data.get("check_in_date")
        check_out_date = request.data.get("check_out_date")

        if not room_id or not check_in_date or not check_out_date:
            return Response({"error": "Room ID, Check-in date, and Check-out date are required"}, status=400)

        # Fetch room details from the Hotel Service API
        hotel_service_url = f'http://localhost:8000/api/rooms/{room_id}/'
        response = requests.get(hotel_service_url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch room details from Hotel Service"}, status=400)

        room_data = response.json()
        if not room_data.get("available"):
            return Response({"error": "Room is not available"}, status=400)

        # Create and save the booking
        booking = Booking.objects.create(
            room_id=room_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
        )

        # Include room details in the response
        response_data = {
            "id": booking.id,
            "room_id": booking.room_id,
            "hotel_name": room_data["hotel"],  
            "room_price": room_data["price"],  
            "check_in_date": booking.check_in_date,
            "check_out_date": booking.check_out_date,
        }

        return Response(response_data, status=201)