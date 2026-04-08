# 🛒 Django Stripe Store

A **production-ready e-commerce application** built with Django that enables secure purchasing of physical and digital products using **Stripe Checkout** with asynchronous webhook handling.



## 🚀 Deployment

🌐 Live Demo - https://django-stripe-store.vercel.app/



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



## 📄 License

MIT License
