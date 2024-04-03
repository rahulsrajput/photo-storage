from django.shortcuts import render, redirect, HttpResponse
from .models import Category, Photo
from django.contrib import messages

def home(request):
    try:
        if request.user.is_authenticated:
            user = request.user
            categories = Category.objects.filter(user=user)

            category = request.GET.get('category')
            if category is not None:
                photos = Photo.objects.filter(category__name=category, category__user=user)
            else:
                photos = Photo.objects.filter(category__user=user)

            context={
                'categories':categories,
                'photos':photos
            }
            return render(request, 'app/home.html',context)
        else:
            return redirect('/login')
    
    except Exception as e:
        raise e
        return HttpResponse(e)


def uploads(request):
    try:
        if request.user.is_authenticated:
            user = request.user
            categories = Category.objects.filter(user=user)

            if request.method == 'POST':
                data = request.POST
                images = request.FILES.getlist('images')

                # print(images)

                if data['category'] != 'none':
                    category = Category.objects.get(id=data['category'])
                elif data['category_new'] != '':
                    category, created = Category.objects.get_or_create(
                        user = user,
                        name = data['category_new']
                    )
                else:
                    messages.error(request,'you have to create or select category')
                    return redirect('/uploads')

                
                for image in images:
                    photo = Photo.objects.create(
                        category = category,
                        image = image
                    )
                
                return redirect('/')

            context= {
                'categories':categories
            }
            return render(request, 'app/upload.html', context)
        else:
            return redirect('/login')

    except Exception as e:
        raise e
        return HttpResponse(e)