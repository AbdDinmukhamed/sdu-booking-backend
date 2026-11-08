from django.test import TestCase
from .models import Booking, Room, Slot, Login


class BookingApiTests(TestCase):

    def setUp(self):
        self.room = Room.objects.create(name = "J102", building = "Main Building", floor = 1, capacity = 143, equipment = ["Projector"], description = "Standard classroom.", bookable = True)


        
    #success
    def testRoomsListReturnsBookableRoom(self):
        response = self.client.get("/api/rooms")
        
        print("\n\n\n")
        
        print("Test 1:\n")
        
        self.assertEqual(response.status_code, 200)
        print(f"response status code: {response.status_code} and supposed correct status code 200")
        
        data = response.json()
        self.assertEqual(len(data), 1)
        print(f"amount of rooms in the response: {len(data)} and supposed amount 1")
        
        self.assertEqual(data[0]["name"], "J102")
        print(f"name of the room: {data[0]["name"]} and supposed name J102")
        
        self.assertEqual(data[0]["floor"], 1)
        print(f"floor of the room: {data[0]["floor"]} and supposed floor 1")
        
        self.assertEqual(data[0]["capacity"], 143)
        print(f"capacity of the room: {data[0]["capacity"]} and supposed capacity 143")
        
        self.assertEqual(data[0]["equipment"], ["Projector"])
        print(f"equipment of the room: {data[0]["equipment"]} and supposed equipment: ", str(["Projector"]))
        
        

    #failure unkown room
    def testUnknownRoomReturns404(self):
        print("\n\n\n")
        print("Test 2:\n")
        
        response = self.client.get("/api/rooms/9999")
        self.assertEqual(response.status_code, 404)
        print(f"response status code: {response.status_code} and supposed correct status code 404")
        
        self.assertEqual(response.json(), {"error": "Room not found"})
        print(f"response: {response.json()} and supposed response: ", str({"error": "Room not found"}))

    #success
    def testLogin(self):
        print("\n\n\n")
        print("Test 3:\n")
        response = self.client.post("/api/login", {"login": "240107002", "password": "student123","role": "student"})
        data = response.json()
        self.assertEqual(data["result"], 0)
        print("Result is equal to 0 meaning the password and role is correct in a given login")
        self.assertEqual(data["name"],"Student 240107002")
        print("Name is equal to what is expected for given POST request")
    
    #failure for login (username or password)
    def testLoginFailureUsername(self):
        print("\n\n\n")
        print("Test 4:\n")
        response = self.client.post("/api/login", {"login": "240161002", "password": "student123","role": "student"})
        data = response.json()
        self.assertEqual(data["result"], 1)
        print("Result for incorrect username gives 1 meaning it is correctly returning wrong password or username error code")
    
    #failure for login (role)
    def testLoginFailureRole(self):
        print("\n\n\n")
        print("Test 5:\n")
        response = self.client.post("/api/login", {"login": "240107002", "password": "student123","role": "staff"})
        data = response.json()
        self.assertEqual(data["result"], 2)
        print("Result for incorrect role gives 2 meaning it is correctly returning wrong role error code")
