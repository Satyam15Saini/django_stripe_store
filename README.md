# 🛒 Django Stripe Store

A **production-ready e-commerce application** built with Django that enables secure purchasing of physical and digital products using **Stripe Checkout** with asynchronous webhook handling.



## 🚀 Deployment

🌐 Live Demo - https://django-stripe-store.vercel.app/

---

## ✨ Features

* Dynamic product checkout (physical & digital goods)
* Secure payments via Stripe Checkout
* Webhook-based payment confirmation
* PCI-compliant payment flow (no card data stored)
* Reliable order lifecycle management (PENDING → PAID)
* Fully deployed on serverless infrastructure (Vercel)



## 🛠 Tech Stack

* **Backend:** Django 6.0
* **Database:** Neon (Serverless PostgreSQL)
* **Payments:** Stripe Checkout API + Webhooks
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Deployment:** Vercel (Serverless Python Functions)
* **Static Files:** WhiteNoise

---

## 🏗 Architecture

### Payment Flow

1. Order is created with `PENDING` status
2. User completes payment via Stripe Checkout
3. Server verifies payment using Stripe API
4. Webhook (`checkout.session.completed`) confirms and updates order to `PAID`

### Reliability

* Payment status is verified via Stripe API (not blindly trusted)
* Webhooks ensure order completion even if user leaves the page
* Prevents duplicate charges and missed confirmations


## 🗄 Database

* Uses **Neon PostgreSQL** for persistent storage
* Required due to Vercel’s serverless, non-persistent environment

---

## 📌 Assumptions

* The application handles a small product catalog managed in Django
* Users are authenticated before placing orders
* Focus is on payment flow and order consistency, not full e-commerce features
* SQLite is used for local development, PostgreSQL for production
* External database is required due to Vercel’s serverless environment

---

## 💳 Payment Flow Choice

**Chosen:** Stripe Checkout  

* Provides hosted payment page (no card handling)
* Ensures PCI compliance automatically
* Faster and simpler integration
* Supports modern payment methods (Apple Pay / Google Pay)

**Not chosen:** Payment Intents  
* Requires custom frontend and more complexity  
* Not necessary for this assignment scope  

---

## 🛡️ Preventing Double Charges / Inconsistent State

* Order is created first with `PENDING` status  
* Stripe session is linked using `client_reference_id`  
* On success:
  - Backend verifies payment using Stripe API  
  - Only updates order if payment is confirmed  
* Webhook (`checkout.session.completed`) acts as backup  
* Order is updated only if not already `PAID`  

---

## ⚙️ Setup & Run

### 1. Clone repository
```bash
git clone https://github.com/Satyam15Saini/django_stripe_store.git
cd django_stripe_store

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create .env file
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

SECRET_KEY=your_django_secret
DEBUG=True

### 5. Run migrations
python manage.py migrate

### 6. Start server
python manage.py runserver

### 7. Run Stripe webhook locally
stripe listen --forward-to localhost:8000/webhook/

### 🧠 Code Quality & Logic
Clean Django structure (models, views, templates)
Clear order lifecycle management
Secure backend validation of payments
Webhook ensures reliability in async scenarios


### 🤖 AI Assistance
ChatGPT used for:
README structuring
Debugging support (Stripe / Vercel setup)
Minor code explanations

All logic was implemented, reviewed, and tested manually.

### ⏱ Time Spent

Total Time: 8–10 hours

### 📄 License

MIT License
