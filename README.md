# Django Stripe Store

A Django application for purchasing fixed products using Stripe Checkout. Features a seamless Bootstrap UI for product listing and order history.

## Assumptions

- We are selling physical/digital singular goods with predefined prices where the site calculates `price * quantity = total` and passes `unit_amount` and `quantity` to Stripe.
- Docker was attempted but for seamless cross-platform execution (especially when Docker Daemon isn't running on Windows environments by default), the setup supports simple local virtual environment initialization with SQLite. It also has a `docker-compose.yml` for Postgres deployment.
- Authentication was implemented to associate orders with users, providing a better "My Orders" layout.
- The UI handles the primary requirement (a single page showing products, quantities, buy buttons, and order history).

## Flow Chosen: Stripe Checkout vs Payment Intents

**Flow Chosen:** Stripe Checkout is used because it automatically handles PCI compliance, provides an optimized and localized payment UI for conversion, supports newer payment methods out of the box (like Apple Pay/Google Pay), and reduces the complexity of managing forms strictly within the application. Using Stripe Checkout also means less frontend JS and no need to handle raw card logic.

## Avoiding Double Charge / Inconsistent State

1. The order is first created with a `PENDING` status prior to redirecting to Stripe.
2. The Stripe Session ID is attached to the pending order.
3. Upon returning to the `checkout_success` view, instead of simply marking it as paid blindly on load, the view:
   - Fetches the Stripe Session from the Stripe API directly.
   - Validates that `session.payment_status == 'paid'`.
   - Before updating, it checks if the order is already in a `PAID` state.
   - By verifying both the Stripe backend status and skipping the DB update/fulfillment logic if already processed, refreshing the success page will not duplicate the charge or fulfillment.

