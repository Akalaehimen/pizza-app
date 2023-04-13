# pizza app

Here's a revised README file for pizza ordering and delivery application using Flask and SQLAlchemy:

Pizza App
This is a pizza ordering and delivery application. It allows users to sign up, log in, and order pizza. 
The app is fully authenticated, so only registered users can place orders.
Users can cancel an order, update an order to their preferred choice, and track the status of an order in real-time.

The app is built using the following technologies:
Backend: Python, Flask, and SQLAlchemy
Database: SQLite


How to use the app
Clone the repository to your local machine
Navigate to the project directory
Create a virtual environment using python -m venv venv
Activate the virtual environment using source venv/bin/activate
Install the dependencies using pip install -r requirements.txt
Start the server using flask run
Open your web browser and go to http://localhost:5000
Endpoints

The following endpoints are available in the app:
GET /api/orders - Get a list of all orders
GET /api/orders/<int:order_id> - Get details for a specific order
POST /api/orders - Place a new order
PUT /api/orders/<int:order_id> - Update an existing order
DELETE /api/orders/<int:order_id> - Cancel an order

Additional features
Some possible additional features that i would love to add to the app include:
Payment integration
Email notifications
SMS notifications
Special deals and promotions
Credits
This app was created by AKALA EHIMEN EMMANUEL. If you have any questions or suggestions, please feel free to contact me at ehimenakala45@gmail.com.
Thanks for using the app!

