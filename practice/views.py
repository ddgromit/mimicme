from django.shortcuts import render

def practice(request):
    return render(request,'practice.html',{})

def sets(request):
    return render(request,'sets.html',{})

def review(request):
    return render(request,'review.html',{})

