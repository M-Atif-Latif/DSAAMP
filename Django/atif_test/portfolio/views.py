from django.shortcuts import render

def index(request):
    """
    Renders the index page.
    """
    return render(request, 'portfolio/index.html')

def about(request):
    """
    Renders the about page.
    """
    return render(request, 'portfolio/about.html')

def contact(request):
    """
    Renders the contact page and handles the contact form submission.
    """
    success = False
    if request.method == "POST":
        # In a real app, you would process/store/send the message here
        success = True
    return render(request, 'portfolio/contact.html', {'success': success})
