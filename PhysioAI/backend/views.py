import re
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.core import serializers
from django.http import JsonResponse


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        # Get user data from request
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')

        # Check if required parameters are present
        if not username:
            return JsonResponse({'error': 'Username is required.'})
        if not password:
            return JsonResponse({'error': 'Password is required.'})
        if not mobile:
            return JsonResponse({'error': 'Mobile number is required.'})
        if not name:
            return JsonResponse({'error': 'Name is required.'})
        if not address:
            return JsonResponse({'error': 'Address is required.'})
        if not email:
            return JsonResponse({'error': 'Email address is required.'})

        # Validate username
        if not username.isalpha():
            return JsonResponse({'error': 'Username should only contain alphabets.'})

        # Validate mobile number
        if not mobile.isdigit() or len(mobile) != 10:
            return JsonResponse({'error': 'Invalid mobile number.'})

        # Validate email address
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return JsonResponse({'error': 'Invalid email address.'})

        # Validate password
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return JsonResponse({'error': 'Password should contain at least 8 characters, one alphabet, one digit, and one special character.'})

        # Hash password
        hashed_password = make_password(password)

        # Create user object
        user = User(username=username, password=hashed_password, mobile=mobile, name=name, address=address, email=email)

        # Save user to database
        user.save()

        # Send email to user with password
        send_mail(
            'Welcome to MyApp',
            f'Hi {name},\n\nYour account has been created successfully. Your password is {password}.',
            'noreply@myapp.com',
            [email],
            fail_silently=False,
        )

        # Return user ID
        return JsonResponse({'user_id': user.id})

    return JsonResponse({'error': 'Invalid request method.'})


def login(request):
    if request.method == 'POST':
        # Retrieve the username and password from the request data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Look for the user in the database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist.'})

        # Check if the password is correct
        if user.password != password:
            return JsonResponse({'error': 'Incorrect password.'})

        # Return a success response if the login is valid
        return JsonResponse({'success': True})
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method.'})


def select_users(request):
    if request.method == 'GET':
        # Get all the users from the database
        users = User.objects.all()

        # Serialize the users to JSON
        user_json = serializers.serialize('json', users)

        # Return the users as a JSON response
        return JsonResponse(user_json, safe=False)
    else:
        # Return an error response if the request method is not GET
        return JsonResponse({'error': 'Invalid request method.'})


