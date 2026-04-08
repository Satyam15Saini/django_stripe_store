# Django Stripe Store

![Vercel Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge&logo=vercel)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django)
![Stripe](https://img.shields.io/badge/Stripe-Checkout-6772E5?style=for-the-badge&logo=stripe)
![PostgreSQL](https://img.shields.io/badge/Neon-PostgreSQL-336791?style=for-the-badge&logo=postgresql)

A fully functional e-commerce application built in Django that processes physical/digital goods via **Stripe Checkout** dynamically using asynchronous webhooks. 

## 🌐 Live Application
The project is officially deployed and functional on Vercel:
**[View Live Application here: https://django-stripe-store.vercel.app/](https://django-stripe-store.vercel.app/)**

## 🛠 Tech Stack

- **Backend Framework:** Django 6.0
- **Database:** Neon (Serverless PostgreSQL)
- **Payment Processing:** Stripe Checkout API & Stripe Webhooks
- **Frontend / UI:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- **Deployment & Hosting:** Vercel (Serverless Python Functions)
- **Static File Handling:** WhiteNoise

## 💡 Architecture & Assumptions

### Avoid Double Charges & Robust States
- The order is first created with a `PENDING` status prior to redirecting the user to Stripe.
- Upon returning to the `checkout_success` view, instead of simply marking it as paid blindly on load, the server directly fetches the Stripe Session status from the Stripe API to securely interrogate true payment state.
- A secondary, asynchronous `stripe_webhook` handles `checkout.session.completed` payloads behind-the-scenes. This provides bulletproof order fulfillment even if the client's browser crashes or they close the tab before being redirected.

### Flow Chosen: Stripe Checkout
Stripe Checkout was specifically selected over raw Payment Intents to automatically handle PCI Compliance obligations off-site. It provides an optimized and localized payment UI for conversion, supports Apple Pay/Google Pay dynamically, and avoids processing complex raw card PANs natively within the Django environment.

### Database Strategy
Vercel operates as a serverless fleet of ephemeral containers. For this deployment, the database transitions from local SQLite into **Neon's Cloud PostgreSQL** to ensure transactions and users survive function-spindowns across isolated workers.
