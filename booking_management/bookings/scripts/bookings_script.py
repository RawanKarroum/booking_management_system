from bookings.models import Booking

def run():
    booking = Booking()
    booking.room_id = 2
    booking.check_in_date = "2024-12-12"
    booking.check_out_date = "2024-12-24"

    booking.save()