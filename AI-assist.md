# AI Assist Usage

1. **Architecture & Planning:** 
   - Antigravity structured the initial approach focusing on Stripe Checkout to avoid complex frontend configurations while still retaining control over double-spends by verifying the session states on success callbacks.
2. **Environment & App Setup:** 
   - Code generation for Docker Compose and Django setup was performed by AI.
   - The AI diagnosed that Docker on Windows might not have the Daemon running, allowing for a graceful fallback onto an SQLite environment using PowerShell commands.
3. **Template & View Code:** 
   - Bootstrap frontend components were quickly scaffolded by the AI.
   - Views including Stripe callback handlers with proper database verification were drafted by AI based on `stripe.checkout.Session` documentation to prevent double charging on refreshing of the `checkout_success` url.
