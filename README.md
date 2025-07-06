
# 🛍️ ShopFast - E-commerce Backend API

A secure and scalable backend API for an e-commerce platform built using **FastAPI** and **MongoDB**, featuring full authentication, product management, cart and order systems, and role-based access control.

---

##  Project Overview

ShopFast is a **RESTful backend** for an online shopping platform. It supports features like user registration/login, admin-level product control, and user-based cart and order management. All endpoints are protected using **JWT authentication** and **role-based authorization**.

---

## 🛠️ Tech Stack

| Layer         | Technology       |
|---------------|------------------|
| Backend       | FastAPI         |
| Database      | MongoDB  (via Motor async) |
| Auth Security | JWT (via `python-jose`)  |
| Password Hash | Passlib (bcrypt)  |
| Testing UI    | Swagger (`/docs`)  |
| Config        | `.env` using `python-dotenv` |

---

##  Features

### 👥 **Authentication**
- User registration and login (`/auth/register`, `/auth/login`)
- JWT-based token generation and validation
- Secure password hashing using bcrypt
- Role-based access control (`user`, `admin`)

### 👤 **User**
- View profile from token
- Full profile view and update
- Password change
- Admin-only area

### 🛍️ **Products**
- Admin-only: Add, update, delete products
- Public: Get all products or by ID
- Search and filter products by name, description, price, and stock

### 🛒 **Cart**
- Add product to cart
- View user’s cart
- Remove product from cart

### 📦 **Orders**
- Place an order from cart
- View user's orders

---

## 🧩 Project Structure
```
ShopFast/
│
├── auth/ # JWT auth logic
│ ├── auth_bearer.py
│ └── auth_handler.py
│
├── database/ # MongoDB connection
│ └── connect.py
│
├── models/ # MongoDB collection references
├── routes/ # All API route handlers
├── schemas/ # Pydantic data validation models
├── main.py # FastAPI app entry point
├── requirements.txt # All Python dependencies
├── .env # Environment variables (excluded)
├── .gitignore # Git ignored files
└── README.md # hey!,You're here,Nice to see you
```

---

## ⚙️ Setup Instructions

###  1. Clone the Repository

```bash
git clone https://github.com/karthikeya-proj/ShopFast.git
cd ShopFast
```

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

###  3. Install Dependencies
```
pip install -r requirements.txt

```

### 4. Setup .env File
```
MONGO_URL=-----
SECRET_KEY=-----
ALGORITHM=------
ACCESS_TOKEN_EXPIRE_MINUTES= ----

```
#### ⚠️ .env is hidden from GitHub via .gitignore

### 5. Start the Server
```
uvicorn main:app --reload

```
#### Visit Swagger docs at 👉 http://127.0.0.1:8000/docs


### API Documentation
#### FastAPI provides interactive docs via Swagger UI:

* GET /docs – Swagger Interface

* GET /redoc – ReDoc Interface

* You can test all endpoints with JWT tokens directly here.

### Authentication Workflow
* Register → /auth/register

* Login → /auth/login → Get JWT

* For protected routes, set header:

```
Authorization: Bearer <your_token>
```
### Collections in MongoDB
```users```  – Stores user info & roles

```products``` – Admin-added products

```cart``` – Per-user cart data

```orders``` – Order history
```
````````````
### Conclusion

####  If this backend is part of a bigger system, you can connect it with a React/Vue frontend using fetch or axios, and manage CORS using FastAPI middleware.
* **Author** :Karthikeya
* **GitHub**: @karthikeya-proj
* **GMail**: eyakarthik872@gmail.com

