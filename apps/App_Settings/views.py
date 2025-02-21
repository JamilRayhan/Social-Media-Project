from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def settings(request):
    if request.method == 'POST':
        # Delete User Account
        if 'delete_account' in request.POST:
            user = request.user
            user.delete()
            logout(request)  # Logout the user after deleting the account
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('home')

    return render(request, 'App_Settings/settings.html')
