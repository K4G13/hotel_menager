Python version: 3.11.9

# run
```
$ python hotel_menager_app.py --hotels data/hotels_example.json --bookings data/bookings_example.json
```

# usage
commands: <br>
1. <b>printhotels</b> or <b>h</b> - print all hotels with room types. <br>
2. <b>printbookings</b> or <b>b</b> - print all bookings. <br>
3. <b>availability( [hotel_id] , [arrival] , [departure] , [room_type] )</b> - print number of available rooms for given hotel, arrival date, departure date and room type.<br> Departure argument is optional and can be skipped, in that case arrival date will replace it. Also command can be shortened to <b>a(...)</b>. <br>