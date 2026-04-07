import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def index(request):
    products = Product.objects.all()
    orders = []
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, status='PAID').order_by('-created_at')
    
    return render(request, 'store/index.html', {
        'products': products,
        'orders': orders,
    })

@login_required
def create_checkout_session(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
            
        if quantity < 1:
            quantity = 1
            
        total_price_cents = product.price_cents * quantity
        
        # Create an Order in DB as PENDING
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price_cents=total_price_cents,
            status='PENDING'
        )
        
        success_url = request.build_absolute_uri(reverse('checkout_success')) + f"?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}"
        cancel_url = request.build_absolute_uri(reverse('checkout_cancel')) + f"?order_id={order.id}"
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': product.name,
                                'description': product.description,
                            },
                            'unit_amount': product.price_cents,
                        },
                        'quantity': quantity,
                    },
                ],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=str(order.id)
            )
            
            # Save the session id so we can reference it
            order.stripe_session_id = checkout_session.id
            order.save()
            
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})
            
    return redirect('index')

@login_required
def checkout_success(request):
    session_id = request.GET.get('session_id')
    order_id = request.GET.get('order_id')
    
    if not session_id or not order_id:
        return redirect('index')
        
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check session status from Stripe to prevent double fulfillment on refresh
    if order.status != 'PAID':
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                order.status = 'PAID'
                order.save()
        except Exception as e:
            print("Error retrieving stripe session:", e)
            
    return render(request, 'store/success.html', {'order': order})

@login_required
def checkout_cancel(request):
    order_id = request.GET.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == 'PENDING':
            order.status = 'CANCELLED'
            order.save()
            
            
    return render(request, 'store/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event.type == 'checkout.session.completed':
        session = event.data.object
        
        # client_reference_id contains our order ID
        client_reference_id = getattr(session, 'client_reference_id', None)
        if client_reference_id:
            try:
                order = Order.objects.get(id=int(client_reference_id))
                if order.status != 'PAID':
                    order.status = 'PAID'
                    order.save()
                    print(f"Webhook explicitly verified Order {order.id} as PAID.")
            except Order.DoesNotExist:
                print(f"Webhook unable to find Order {client_reference_id}")
            except Exception as e:
                print("WEBHOOK 500 ERROR:", str(e))
                import traceback
                traceback.print_exc()
                return HttpResponse(status=500)

    return HttpResponse(status=200)
