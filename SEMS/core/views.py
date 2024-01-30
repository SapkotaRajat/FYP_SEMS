from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def custom_404(request, exception=None):
    return render(request, 'error.html', status=404)
def error(request):
    return render(request, 'error.html')
def plan_your_visit(request):
    return render(request, 'plan-your-visit.html')
def about(request):
    return render(request, 'about.html')