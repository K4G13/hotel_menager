import argparse
import json

class HotelMenager:

    hotels = {}
    bookings = {}

    def __init__(self,hotels_data_file,bookings_data_file):
        try: 
            hotels_json = json.load(open(hotels_data_file))
            for hotel in hotels_json:
                self.hotels[hotel['id']] = hotel
        except FileNotFoundError: 
            exit(f"\033[0;31mError: File '{hotels_file}' not found.\033[0m")
        try:
            bookings_json = json.load(open(bookings_data_file))
            self.bookings = bookings_json
        except FileNotFoundError:
            exit(f"\033[0;31mError: File '{bookings_file}' not found.\033[0m")

    def print_hotels(self):
        print(f"\033[1m\n{'ID':6}{'NAME':24}{'ROOM TYPES'}\033[0m")
        for hotel in self.hotels.values():
            print(f"{hotel['id']:6}{hotel['name']:24}",end="")
            for room_type in hotel['roomTypes']:
                print(f"({room_type['code']}) {room_type['description']}",end=", ")
            print()

    def print_bookings(self):
        print(f"\033[1m\n{'HOTEL ID':12}{'ARRIVAL':12}{'DEPARTURE':12}{'ROOM TYPE':12}{'ROOM RATE':12}\033[0m")
        for booking in self.bookings:
            print(f"{booking['hotelId']:12}{booking['arrival']:12}{booking['departure']:12}{booking['roomType']:12}{booking['roomRate']:12}")

    def __get_room_types_codes(self,hotel_id:str):

        if hotel_id not in self.hotels:
            print(f"\033[0;31mError: Hotel with id '{hotel_id}' not found.\033[0m")
            return

        res = []
        for room_type in self.hotels[hotel_id]['roomTypes']:
            res.append(room_type['code'])
        return res

    def availability(self, hotel_id:str, arrival:int, departure:int, room_type:str):
        
        if hotel_id not in self.hotels:
            print(f"\033[0;31mError: Hotel with id '{hotel_id}' not found.\033[0m")
            return

        if room_type not in self.__get_room_types_codes(hotel_id):
            print(f"\033[0;31mError: Room type '{room_type}' not found in hotel with id '{hotel_id}'.\033[0m")
            return

        if not arrival <= departure:
            print(f"\033[0;31mError: Arrival date must be before departure date or equal.\033[0m")
            return

        if len(str(arrival)) != 8 or len(str(departure)) != 8:
            print(f"\033[0;31mError: Arrival and departure dates must be in the format YYYYMMDD.\033[0m")
            return

        yy,mm,dd = int(str(arrival)[0:4]), int(str(arrival)[4:6]), int(str(arrival)[6:8])
        if yy not in range(2000,2100) or mm not in range(1,13) or dd not in range(1,32):
            print(f"\033[0;31mError: Arrival year, month and day must be in ranges 2000-2100, 01-12 and 01-31.\033[0m")
            return

        yy,mm,dd = int(str(departure)[0:4]), int(str(departure)[4:6]), int(str(departure)[6:8])
        if yy not in range(2000,2100) or mm not in range(1,13) or dd not in range(1,32):
            print(f"\033[0;31mError: Departure year, month and day must be in ranges 2000-2100, 01-12 and 01-31.\033[0m")
            return
        
        #rooms owned by selected hotel and type
        rooms_owned = 0
        for room in self.hotels[hotel_id]['rooms']:
            if room['roomType'] == room_type:
                rooms_owned += 1
        
        #rooms that are booked in the given period with selected hotel and type
        rooms_booked = 0
        for booking in self.bookings:
            if booking['hotelId'] == hotel_id and booking['roomType'] == room_type:
                start,end = int(booking['arrival']),int(booking['departure'])              
                if arrival == departure and arrival >= start and arrival <= end:
                    rooms_booked += 1
                elif not( arrival < start and departure < start ) \
                     and not( arrival > end and departure > end ):
                    rooms_booked += 1
        
        return rooms_owned - rooms_booked



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Process hotels and bookings data.")
    parser.add_argument("-ht","--hotels", required=True, help="Path to the hotels JSON file.")
    parser.add_argument("-b","--bookings", required=True, help="Path to the bookings JSON file.")
    args = parser.parse_args()    
    
    menager = HotelMenager(args.hotels, args.bookings)

    while(True):

        command = input("\nEnter command: ")
        
        if command == "": 
            exit()

        elif command.lower() == "printhotels" or command.lower() == "h":
            menager.print_hotels()
            continue

        elif command.lower() == "printbookings"  or command.lower() == "b":
            menager.print_bookings()
            continue

        elif command[0:12].lower() == "availability" or command[0:2].lower() == "a(":
            arguments = command.rstrip(")").split("(")[1].split(",")

            if len(arguments) == 3:
                arguments.append(arguments[2])
                arguments[2] = arguments[1]

            try:
                res = menager.availability(arguments[0],int(arguments[1]),int(arguments[2]),arguments[3])
                print(f"\nAvailability: {res}")
            except:
                print(f"\033[0;31mError: Wrong arguments.\033[0m")
        else:
            print(f"\033[0;31mError: Invalid command.\033[0m")



