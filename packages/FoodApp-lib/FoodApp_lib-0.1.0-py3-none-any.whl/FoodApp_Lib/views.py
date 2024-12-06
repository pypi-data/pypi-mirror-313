from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .forms import RegistrationForm, LoginForm, ProductForm
import uuid
import boto3
from boto3.dynamodb.conditions import Attr
# Initialize DynamoDB
AWS_REGION = 'us-west-2'  # Replace with your AWS region
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

# DynamoDB Tables
EMPLOYEE_TABLE = dynamodb.Table('employee')
PRODUCT_TABLE = dynamodb.Table('product')
CART_TABLE = dynamodb.Table('cart')
CART_ITEM_TABLE = dynamodb.Table('cart_item')
AWS_REGION = 'us-west-2'
SNS_TOPIC_ARN = 'arn:aws:sns:us-west-2:481665109829:MySNSTopic'

# Initialize boto3 clients
sns_client = boto3.client('sns', region_name=AWS_REGION)
sqs_client = boto3.client('sqs', region_name=AWS_REGION)

def send_email_notification_via_sns(subject, body):
    """
    Sends an email notification via SNS.
    """
    try:
        # SNS doesn't have a separate subject field for email, include it in the message
        message = f"Subject: {subject}\n\n{body}"
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message
        )
        print(f"Email notification sent! Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending email notification via SNS: {str(e)}")


def fetch_sqs_notifications(queue_url):
    """
    Fetches messages from the SQS Queue.
    """
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20  # Long polling
        )
        messages = response.get('Messages', [])
        notifications = []
        if messages:
            for message in messages:
                receipt_handle = message['ReceiptHandle']
                notifications.append(message['Body'])
                # Delete the message after processing
                sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
        return notifications
    except Exception as e:
        print(f"Error fetching SQS messages: {str(e)}")
        return []



def login_register_view(request):
    login_form = LoginForm()
    registration_form = RegistrationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']

                try:
                    # Fetch employee using a scan operation
                    response = EMPLOYEE_TABLE.scan(
                        FilterExpression=Attr('email').eq(email)
                    )
                    items = response.get('Items', [])
                    
                    if items:
                        employee = items[0]  # Assume email is unique
                        if check_password(password, employee['password']):
                            request.session['employee_id'] = employee['employee_id']
                            return redirect('home')
                        else:
                            messages.error(request, 'Invalid email or password.')
                    else:
                        messages.error(request, 'Invalid email or password.')
                except Exception as e:
                    messages.error(request, f"Error fetching employee: {str(e)}")

        elif 'register' in request.POST:
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                password = registration_form.cleaned_data['password']
                hashed_password = make_password(password)

                employee_id = str(uuid.uuid4())  # Generate UUID as string
                new_employee = {
                    'employee_id': employee_id,
                    'name': registration_form.cleaned_data['name'],
                    'email': registration_form.cleaned_data['email'],
                    'phone': registration_form.cleaned_data['phone'],
                    'password': hashed_password,
                    'balance': 0  # Default balance
                }

                try:
                    # Save to DynamoDB
                    EMPLOYEE_TABLE.put_item(Item=new_employee)
                    messages.success(request, 'Registration successful! Please login now.')
                    return redirect('login_register')
                except Exception as e:
                    messages.error(request, f"Error during registration: {str(e)}")
            else:
                messages.error(request, 'Registration failed. Please try again.')

    return render(request, 'login_register.html', {
        'login_form': login_form,
        'registration_form': registration_form,
    })


def home_view(request):
    # Fetch SNS notifications from SQS
    # notifications = fetch_sqs_notifications(SQS_QUEUE_URL)
    
    # Get employee_id from the session
    employee_id = request.session.get('employee_id')

    if employee_id:
        try:
            # Fetch employee details from DynamoDB
            response = EMPLOYEE_TABLE.get_item(Key={'employee_id': employee_id})
            employee = response.get('Item')

            if employee:
                balance = employee.get('balance', 0)  # Default balance to 0
                return render(request, 'home.html', {
                    'employee': employee,
                    'balance': balance,
                                 # Add notifications to the context
                })
            else:
                messages.error(request, "Employee not found.")
        except Exception as e:
            messages.error(request, f"Error fetching employee: {str(e)}")
    
    # Redirect to login/register page if no employee_id is found
    return redirect('login_register')



def logout_view(request):
    if 'employee_id' in request.session:
        del request.session['employee_id']
    return redirect('login_register')


def menu_view(request):
    try:
        # Fetch all products from DynamoDB
        response = PRODUCT_TABLE.scan()
        raw_products = response.get('Items', [])
        
        # Map DynamoDB items to a Django-compatible structure
        products = [
            {
                'id': item['product_id'],  # Map product_id to id
                'name': item.get('name', 'Unnamed Product'),  # Provide a default name if missing
                'price': item.get('price', '0.00'),  # Default price if missing
                'image': item.get('image', None),  # Ensure image URL is included
            }
            for item in raw_products
        ]
    except Exception as e:
        messages.error(request, f"Error fetching products: {str(e)}")
        products = []

    return render(request, 'menu.html', {'products': products})



def add_to_cart(request, product_id):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        messages.error(request, 'You need to be logged in to add items to your cart.')
        return redirect('login_register')

    try:
        # Fetch product details from DynamoDB
        response = PRODUCT_TABLE.get_item(Key={'product_id': product_id})
        product = response.get('Item')
        if not product:
            messages.error(request, "Product not found.")
            return redirect('menu')

        # Add item to cart
        cart_response = CART_TABLE.get_item(Key={'cart_id': employee_id})
        cart = cart_response.get('Item')
        if not cart:
            CART_TABLE.put_item(Item={'cart_id': employee_id, 'items': []})

        CART_ITEM_TABLE.put_item(Item={
            'cart_item_id': str(uuid.uuid4()),  # Unique cart item ID
            'cart_id': employee_id,
            'product_id': product_id,
            'quantity': 1
        })

        # Send email notification via SNS
        subject = "Cart Update Notification"
        body = f"Product '{product['name']}' has been added to the cart by user {employee_id}."
        send_email_notification_via_sns(subject, body)

        messages.success(request, f'{product["name"]} added to your cart. Email notification sent!')
    except Exception as e:
        messages.error(request, f"Error adding to cart: {str(e)}")

    return redirect('view_cart')


def checkout_view(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        messages.error(request, 'You need to be logged in to proceed with checkout.')
        return redirect('login_register')

    try:
        # Process checkout (fetch cart items, calculate total, etc.)
        cart_response = CART_TABLE.get_item(Key={'cart_id': employee_id})
        cart = cart_response.get('Item')

        if cart:
            # Placeholder for processing payment, updating stock, etc.
            # For simplicity, assume checkout is successful

            # Send email notification via SNS
            subject = "Checkout Notification"
            body = f"User {employee_id} has successfully completed their checkout."
            send_email_notification_via_sns(subject, body)

            messages.success(request, 'Checkout successful! Email notification sent!')
        else:
            messages.error(request, 'Your cart is empty.')

    except Exception as e:
        messages.error(request, f"Error during checkout: {str(e)}")

    return redirect('home')



def view_cart(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        messages.error(request, 'You need to be logged in to view your cart.')
        return redirect('login_register')

    try:
        # Fetch cart items from DynamoDB
        response = CART_ITEM_TABLE.scan(
            FilterExpression='cart_id = :cart_id',
            ExpressionAttributeValues={':cart_id': employee_id}
        )
        cart_items = response.get('Items', [])

        # Fetch product details for each cart item and calculate total price
        cart_total = 0
        for item in cart_items:
            product_id = item.get('product_id')
            product_response = PRODUCT_TABLE.get_item(Key={'product_id': product_id})
            product = product_response.get('Item')
            
            # Add product details to each cart item
            item['product_name'] = product.get('name')
            item['product_price'] = product.get('price')
            item['product_image_url'] = product.get('image_url')  # Make sure product has an image URL

            # Calculate total price for each item and add to cart total
            item['total_price'] = item['product_price'] * item['quantity']
            cart_total += item['total_price']

    except Exception as e:
        messages.error(request, f"Error fetching cart items: {str(e)}")
        cart_items = []
        cart_total = 0

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'cart_total': cart_total})






def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Prepare for DynamoDB
            product_id = str(uuid.uuid4())  # Generate UUID for product
            new_product = {
                'product_id': product_id,
                'name': product.name,

                'price': product.price,
                'image': product.image.url if product.image else None
            }
            try:
                # Save product to DynamoDB
                PRODUCT_TABLE.put_item(Item=new_product)
                messages.success(request, 'New product added successfully!')
                return redirect('menu')
            except Exception as e:
                messages.error(request, f"Error adding product: {str(e)}")
        else:
            messages.error(request, 'Error adding product.')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})
