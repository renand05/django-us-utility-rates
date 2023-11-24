from django.shortcuts import render

def website_demo(request):
    return render(request, 'website_demo.html', {
        'new_user_address': request.POST.get('user_address', ''),
        'new_user_consumption': request.POST.get('user_consumption', ''),
        'new_user_percentage_scale': request.POST.get('user_percentage_scale', ''),
    })