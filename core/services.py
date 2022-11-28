
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.reverse import reverse

from django.contrib.sites.shortcuts import get_current_site

def send_verification(user_data, request):

    user = User.objects.get(email=user_data['email'])
    token = RefreshToken.for_user(user).access_token
    
    current_site = get_current_site(request).domain

    # Get the url of the "email-verify" view
    relativeLink = reverse('accounts:email-verify')

    # Sum up the final url for verification
    absurl = 'http://'+current_site+relativeLink+"?token="+str(token)

    email_body = f"Hi {user.email} Use the link below to verify your email\n{absurl}" 

    data = {'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Verify your email'}
    
    send_email(data)


def send_email(data):
    print(data)
    


    

