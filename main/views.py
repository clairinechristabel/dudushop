from django.shortcuts import render

def show_main(request):
    context = {
        'shop' : "dudushop",
        'name' : 'Clairine Christabel Lim',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)