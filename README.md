# Customer and Order Management System with OIDC Authentication and Africa's Talking Integration

## Project Description
This project is a Django-based application that manages customers and orders. It includes OIDC (OpenID Connect) authentication for secure login and integrates Africa's Talking API to send SMS messages. The system allows users to authenticate via OIDC, manage customer data, place orders, and send notifications.

## Key Features
- **OIDC Authentication:** Secure authentication via OpenID Connect.
- **Order Management:** Manage customer orders, including placing and tracking.
- **Customer Management:** Manage customer profiles, contact details, etc.
- **Africa's Talking Integration:** Send SMS notifications for order updates.
- **API Endpoints:** Testable API endpoints for customer and order management using Postman.

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.x
- Django 4.x
- pip (Python package manager)
- Africa's Talking API credentials (for SMS integration)
- OIDC credentials for authentication

## Installation Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2. **Set up a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate  # For Windows
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables** (for OIDC and Africa's Talking credentials):
    - Create a `.env` file in the root directory and add:
      ```env
      OIDC_CLIENT_ID=your_client_id
      OIDC_CLIENT_SECRET=your_client_secret
      OIDC_PROVIDER_URL=your_oidc_provider_url
      AFRICAS_TALKING_API_KEY=your_africas_talking_api_key
      AFRICAS_TALKING_SENDER_ID=your_sender_id
      ```

5. **Run migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The server will be accessible at `http://127.0.0.1:8000`.

## Testing Endpoints with Postman
Use Postman to test the API endpoints.
- Example: To authenticate a user via OIDC, send a POST request to `http://127.0.0.1:8000/auth/token/` with the necessary OIDC parameters.

## API Endpoints
- `POST /auth/token/`: Get OIDC authentication token.
- `GET /customers/`: List all customers.
- `POST /customers/`: Create a new customer.
- `GET /orders/`: List all orders.
- `POST /orders/`: Place a new order.
- `POST /sms/send/`: Send an SMS notification using Africa's Talking.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
