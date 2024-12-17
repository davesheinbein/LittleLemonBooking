# Little Lemon Booking

Little Lemon Booking is a Django-based web application for managing restaurant reservations and menu items. The platform aims to simplify the booking process for customers while providing restaurant owners with tools to manage reservations and their menu seamlessly.

## Features

- **View and Manage Reservations**: A streamlined interface for both customers and staff to view, create, and manage table reservations.
- **Browse and Manage Menu Items**: Add, update, or remove menu items with ease.
- **User Authentication**: Secure user registration, login, and role-based access for staff and customers.
- **Responsive Design**: Optimized for both desktop and mobile devices to ensure a seamless user experience.
- **Customizable Settings**: Easily configure restaurant-specific settings, such as opening hours and table availability.

## Setup Instructions

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/davesheinbein/LittleLemonBooking.git
cd LittleLemonBooking
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to isolate dependencies. Run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate   # For Linux/MacOS
venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies

Install the required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and set the following variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=127.0.0.1, localhost
DATABASE_URL=sqlite:///db.sqlite3  # Update if using a different database
```

### 5. Apply Database Migrations

Run the migrations to set up the database:

```bash
python manage.py migrate
```

### 6. Load Initial Data (Optional)

If provided, you can load sample data to test the application:

```bash
python manage.py loaddata initial_data.json
```

### 7. Run the Development Server

Start the development server:

```bash
python manage.py runserver
```

Visit the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Running Tests

To run the tests for the project, use the following command:

```bash
python manage.py test
```

## Deployment

To deploy the application to a production environment, follow these additional steps:

1. Set `DEBUG=False` in the `.env` file.
2. Configure a production-ready database and update `DATABASE_URL`.
3. Set up a web server (e.g., Gunicorn) and reverse proxy (e.g., Nginx).
4. Configure static file handling with `collectstatic`.
5. Secure the application with HTTPS.
