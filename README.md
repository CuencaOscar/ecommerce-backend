# Ecommerce Backend Project

## Description
This backend part of the Ecommerce project is designed to manage product listings, user authentication, shopping cart functionalities, and order processing. It's built using Django and Django REST Framework to provide a robust API for the frontend part.

## Features
- **Product Catalog:** Manage a catalog of products with descriptions, prices, and images.
- **User Management:** Handle user sign-up, login, and profile management.
- **Shopping Cart:** Users can add products to their shopping cart and checkout.
- **Order Processing:** Process orders and manage order statuses.
- **Payment Integration:** Interface with payment gateways for transaction processing.

## Technologies Used
- **Framework:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** Django's built-in authentication system & JWT for APIs
- **Other:** CORS headers for API security

## Project Setup

### Requirements
- Python 3.8 or higher
- Django 3.2 or higher
- Django REST Framework
- PostgreSQL

### Installation and Setup

1. Clone the repository and navigate to the backend directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Setup your PostgreSQL database.
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server by specifying the environment using the `--settings` option:
   - For local development:
     ```bash
     python manage.py runserver --settings=ecommerce.settings.local
     ```
   - For development environment:
     ```bash
     python manage.py runserver --settings=ecommerce.settings.development
     ```
   - For production environment:
     ```bash
     python manage.py runserver --settings=ecommerce.settings.production
     ```

## Contributing
Contributions are welcome. Please refer to the CONTRIBUTING.md file for more details.

## License
This project is licensed under the MIT License. See the LICENSE.md file for more details.