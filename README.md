# E-Commerce Auction Platform

## Overview
This is a full-stack web application that allows users to create, bid on, and close auctions for various items. Users can register, log in, add listings, place bids, and manage their watchlists. The platform provides an engaging experience for online bidding with real-time updates.

## Features
- **User Authentication:** Users can register, log in, and log out.
- **Auction Listings:** Users can create new auction listings with a title, description, image URL, and starting bid.
- **Bidding System:** Users can place bids on active auctions.
- **Watchlist:** Users can add and remove listings from their watchlist.
- **Auction Closing:** The auction creator can close the auction, determining the highest bidder as the winner.
- **Real-Time Updates:** The application uses Django channels for real-time notifications.

## Technologies Used
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript (with Bootstrap and React)
- **Database:** SQLite (default) or PostgreSQL
- **Authentication:** Django built-in authentication system
- **WebSockets:** Django Channels for real-time updates

## Installation
### Prerequisites
- Python 3.x
- Django
- Virtual Environment (optional but recommended)

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ecommerce-auction.git
   cd ecommerce-auction
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser (for admin access):
   ```sh
   python manage.py createsuperuser
   ```
   Follow the prompts to set up an admin user.
6. Run the development server:
   ```sh
   python manage.py runserver
   ```
7. Open your browser and go to `http://127.0.0.1:8000/` to use the application.

## Usage
- **Register/Login**: Create an account or log in.
- **Create a Listing**: Fill out the form to list an item for auction.
- **Bid on Items**: View active listings and place bids.
- **Manage Watchlist**: Add/remove items from your watchlist.
- **Close Auctions**: If you created a listing, you can close the auction to declare a winner.


## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add new feature'`
4. Push to your branch: `git push origin feature-name`
5. Submit a pull request.

## License
This project is licensed under the MIT License. Feel free to modify and use it as you wish.

## Contact
For any questions, feel free to reach out via GitHub Issues or email: KristopherPoston@example.com



