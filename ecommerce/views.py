from django.shortcuts import redirect

def get_default(request):
    return redirect('home')