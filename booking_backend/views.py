from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Booking, Room, Slot, Login
from .sdu_api import *

#results: integer returning status of SDU response
#0: login and password is found, role is correct
#1: login or password is not correct
#2: role is not correct
@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("login")
        password = request.POST.get("password")
        role = request.POST.get("role")
        result = TEST_API().RequestPassword((username,password,role)) #this abominocity must be fixed later, TODO: remove magic numbers and mayyyybe use ENUMs here
        response = Login.objects.create(result = result[0], login = username, role = role, name = result[1])
        return JsonResponse(response.toJSON())
    return JsonResponse({"error": "incorrect method, login awaits POST request"}, status = 404)

def rooms(request):
    bookableRooms = Room.objects.filter(bookable = True)
    data = []
    
    for room in bookableRooms:
        data.append(room.toJSON())
        
    return JsonResponse(data, safe = False)

def roomDetail(request, room_id):
    room = Room.objects.filter(id = room_id, bookable = True).first()
    
    if room == None:
        return JsonResponse({"error": "Room not found"}, status = 404)
    
    return JsonResponse(room.toJSON())
    
def roomSlots(request, room_id):
    if Room.objects.filter(id = room_id, bookable = True).exists() != True:
        return JsonResponse({"error": "Room not found"}, status = 404)
    
    slots = Slot.objects.filter(room_id = room_id)
    
    response = []
    for s in slots:
        response.append(s.toJSON())
    
    return JsonResponse(response, safe = False)


def bookings(request):
    if request.method == "GET":
        qs = Booking.objects.select_related("room", "slot")
        
        response = []
        for booking in qs:
            response.append(booking.toJSON())
            
        return JsonResponse(response, safe = False)