✅ README.md (Full Combined Version)
markdown
Copy
Edit
# 🧾 Savana Python (Django) Service Documentation

A backend API service for managing customers, products, product categories, and orders, authorization and authentication built with Django and PostgreSQL. Includes GraphQL endpoints, Discord-based authentication, and optional Docker + Kubernetes deployment.

---

## 📦 Project Overview

**Project Name:** Savana Inventory Service  
**Purpose:** A backend API service for managing customers, products, product categories, and orders, authorization and authentication built with Django and PostgreSQL. GraphQL endpoints, Discord-based authentication, and  Docker + Kubernetes deployment.

**Tech Stack:** Python, Django, PostgreSQL, GraphQL, OpenID Connect, Discord OAuth2

> A web app for managing customers, products, and orders, built with Django and PostgreSQL.

---

## 🔧 Prerequisites

To run this project, ensure you have the following:

- Python 3.10+
- Django 5.x
- PostgreSQL or SQLite
- Git and GitHub Actions
- Virtual environment tool (venv)
- Docker and Docker Compose
- Kubernetes (Minikube)

---

## 🚀 Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/Agikedwin/savanadevservice
cd savanadevservice
Create and Activate a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate
Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Configure Environment Variables
Create a .env file or set environment variables manually:

ini
Copy
Edit
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=YOUR EMAIL
EMAIL_HOST_PASSWORD=YOUR PASSWORD

AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=YOUR API KEY
Apply Migrations and Create a Superuser
bash
Copy
Edit
python manage.py migrate
python manage.py createsuperuser
Run the Development Server
bash
Copy
Edit
python manage.py runserver
Visit http://127.0.0.1:8000 to confirm the app is running.

🐳 Run with Docker
Ensure Docker and Docker Compose are installed. Then:

bash
Copy
Edit
docker compose up --build -d
This will build the image and fire up the application in containers.

☸️ Deploy with Kubernetes (Minikube)
Ensure kubectl and Minikube are installed.

bash
Copy
Edit
minikube start --driver=docker
cd deploy
kubectl apply -k .
kubectl get services
minikube service savana
Copy the URL provided and paste it into your browser.

🔐 Authorization and Authentication
Navigate to: http://<MINIKUBE_IP>:8000/oauth2/login

You will be redirected to Discord (or OpenID Connect) for authentication.

After login and authorization, your user data will be saved to the database.

You will be redirected to the GraphQL endpoint:

http://localhost:8000/graphql/

📡 Consuming the GraphQL API Endpoints
Create User
graphql
Copy
Edit
mutation {
  createUser(name:"savana user", description:"Admin user", role:1) {
    user {
      userId
      name
      role
    }
  }
}
Create Customer
graphql
Copy
Edit
mutation {
  createNewCustomer(
    customerContact:"0717569866",
    customerEmail:"savana@gmail.com",
    customerName:"Savana Dev",
    customerType:"active",
    userId: 2
  ) {
    customer {
      customerName
      user {
        userId
        name
      }
    }
  }
}
Create Product Category
graphql
Copy
Edit
mutation {
  createCategory(
    categoryName:"Hardware",
    categoryType:"Durable",
    description:"Can last longer",
    userId:2
  ) {
    category {
      categoryId
      categoryName
      categoryType
    }
  }
}
Create Product
graphql
Copy
Edit
mutation {
  createProduct(
    categoryId:4,
    price:4500,
    productName:"Iron sheet",
    userId:2
  ) {
    product {
      productName
      price
    }
  }
}
Create Order
graphql
Copy
Edit
mutation {
  createOrder(customerId:2, productId:4, userId:2) {
    order {
      orderId
      product {
        productName
        price
      }
    }
  }
}
📧 Once the order is placed, an email notification is sent to the admin and an SMS is sent to the customer.

Queries
Return Average Product Price for a Given Category
graphql
Copy
Edit
query {
  averagePriceByCategory(categoryId:1)
}
Get All Users, Categories, and Customer by ID
graphql
Copy
Edit
query {
  allUsers {
    userId
    name
  }

  allProdCategories {
    categoryId
    categoryName
    categoryType
    description
  }

  customerById(id:1) {
    customerId
  }
}
🧩 Data Models
👤 Users Model
Represents users of the system, such as admins, salespeople, etc.

python
Copy
Edit
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.TextField()
    role = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return str(self.user_id)
👥 Customers Model
Stores information about customers who place orders.

python
Copy
Edit
class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_contact = models.CharField(max_length=13)
    customer_email = models.EmailField()
    customer_type = models.CharField(max_length=255, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer_id)
🗂️ ProductCategory Model
Defines categories for organizing products.

python
Copy
Edit
class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.category_id)
📦 Products Model
Represents individual products available for order.

python
Copy
Edit
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id)
🧾 Orders Model
Tracks product orders placed by customers.

python
Copy
Edit
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)
🔁 Model Relationships
Users are linked to Customers, Product Categories, Products, and Orders.

Products belong to Product Categories.

Orders connect Customers, Products, and the Users who placed them.

📬 Contact
GitHub Repository: https://github.com/Agikedwin/savanadevservice