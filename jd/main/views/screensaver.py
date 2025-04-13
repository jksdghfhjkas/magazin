from django.shortcuts import render

def ScreensaverView(request):
    return render(request, "main/screensaver.html")

