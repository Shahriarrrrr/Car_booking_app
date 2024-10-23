First thing first, 
Make the necessary imports correctly, if i had used docker , then it would have been easier.
In database connect i was checking for some error with history and debugging them,So do ignore that , you can comment out that part

Connection details and all the related collection you will find in databaseConnect.py file.
At first i tried to implement the whole project with pymongo. I almost implemented everything with that then i got stuck while 
i was making a new booking, reason for that is in the create_booking , i also wanted to create a record and i called record_create() 
which leaded to an error.Then switched to motor client.



For the Program,
There is a,

POST request to make a booking
PUT request to make a booking
GET request to view bookings by date
POST request to make a history (Test Purpose)
Note: DELETE method i couldn't finsih due to time shortage.(Will add later)
Note: Implemeted a total history of creation & update history but didn't add a GET method due to time shortage.

For now, 
i made every input and stored as a string, but made some errors while inserting car_id , 
Should have used the number plate of the car that i generated would have been easier, would have 
been easier.

I tried to intregrate the logic by using FastAPi and Mongodb. I created a random data set which you can find in CRUD folder. There i have
inserted data for Employee and Cars manually through a loop. Also i have assigned a Driver while inserting car details.

About Logic ->
I have made so that a employer after he books a car on a specific date, he/she can update the date of his/her booking but cant update it on the day of the booking and also added so that it cant select a past date also,
It keeps track of the bookings that are available.
In there there is also a route to check all the ACTIVE bookings by date.
Implemeted a total history of creation & update history but didn't add a GET method due to time shortage.

For more queries contact here: shahriarazamkhan@gmail.com

