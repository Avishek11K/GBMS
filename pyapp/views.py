# from django.shortcuts import render

# Create your views here.

#models,impport hashpassword creator,or query and packaages imported AK
from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
from pyapp.models import Home
from django.contrib import messages
from django.contrib.auth.models import User, Group
# from django.contrib.auth.models import User
from pyapp.models import Home, Landlord, roomseeker, HomeImage
from django.contrib.auth import logout as logout_auth
from django.db.models import Q  # Import Q for OR operations
from django.contrib.auth import authenticate, login as login_auth
from django.http import HttpResponse
from pyapp.models import Contact,Application
from django.contrib import messages
from pyapp.models import Landlord
# fieldfile or contentfile is supported instead of pillow so:

# from django.core.files import ImageFile
# from PIL import image
# from django.core.files.base import ContentFile


# # If you have a PIL Image object
# image_file = ImageFile(pil_image_object)
# Home.image = image_file

# # Or save to BytesIO and use ContentFile
# from io import BytesIO
# buffer = BytesIO()
# pil_image_object.save(buffer, format='JPEG')
# Home.image.save('image.jpg', ContentFile(buffer.getvalue()), save=False)   

# ends here

#fetches the data from Home database and sent to the fomefetch :AD
def home_data(request):
    homedata=Home.objects.all()
    return render(request,'home.html',{'homefetch':homedata})

#Main dynamic routing :AK
def view_details(request,pk):
    det=get_object_or_404(Home, pk=pk)
    # print("det", det)
    return render(request,"viewhtml.html",{
        "vd":det
    })

def pyapp(request):
    context={
        "variable1":"Avishek",
        "variable2":"AVishek Karki"
    }
    return render(request, 'pyapp.html',context)
    # return HttpResponse("Hello, Avishek is learning Django!!")
    #Httpresponse return gardaa text matra display vatyo vane render le euta template ko html,css lai nai as a whole display garxa


#by :JC here,normal rendering relevant pages 
def home(request):
    return render(request,'home.html')
    # return HttpResponse("Home page")

def contact(request):
    return render(request,'contact.html')
    # return HttpResponse("Contact Page")
def profile(request):
    return render(request,"profile.html")
def about(request):
    return render(request,'about.html')


#Register the user or lanlord according to the role AK
def register(request):
    if request.method=="POST":
        role=request.POST.get('role',"")
        username=request.POST.get('username',"")
        email=request.POST.get('email',"")
        password=request.POST.get('password')
        if User.objects.filter(Q(username=username)|Q(email=email)).exists():
            # messages.error(request,"Username or email already exists")
            return render (request,'register.html',{
                "error":"Username or email already existed!"
            })
        
        
        if not role:    
            return render(request,"register.html",{
                "blankrole":"Role need to be selected!"
            })
        if not username:
            # username=username.strip()
         return render(request,"register.html",{
                "blankuser":"Username shouldnt be empty!"
            })
        if not email:
            # email=email.strip()
            return render(request,"register.html",{
                "blankemail":"Email shouldnt be empty!"
            })
        if not password:
            # password=password.strip()
            return render(request,"register.html",{
                "blankpassword":"Password shouldnt be empty!"
            })
        user=User.objects.create_user(
        username=username,
        email=email,
        password=password
        )
        # landlord.objects.create(user=user)

        group,created=Group.objects.get_or_create(name=role)

        user.groups.add(group)

        if role=="landlord":
            Landlord.objects.create(user=user)
        if role=="rentseeker":
            roomseeker.objects.create(name=username,email=email,password=make_password(password))
        return redirect('loginUser')
    return render(request,'register.html')

#Login ensuring correctness from the register by the data JC
def loginUser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if not user:
             return render(request,"loginUser.html",{
        "crerror":"Credentials didnt matched!"
      })
        if user is not None:
            if user.groups.filter(name="rentseeker").exists():    
                login_auth(request,user)
                return redirect("home.html")
                
            elif user.groups.filter(name="landlord").exists():
               login_auth(request,user)
               return redirect("llhome")
            else:
               return  redirect("register")
    return render(request,"loginUser.html")


def process_apply(request, pk):
    if request.user.is_authenticated:
        house = get_object_or_404(Home, pk=pk)
        
        # according to model saving application
        Application.objects.create(
            user=request.user,  # roomseeker
            house=house        # to which home applied
        )
        
        #sending succession message
        messages.success(request, "Applied successfully!")
        return redirect('home.html')  


def viewhtml(request):
    return render(request,'viewhtml.html')

def add(request):
    if request.method=="POST":
        ll=Landlord.objects.get(user_id=request.user.id)
        # print(ll.pk)
        # print(request.user.pk)
        title=request.POST.get('title',"")
        location=request.POST.get('location')
        price=request.POST.get('price')
        description=request.POST.get('desc')
        image=request.FILES.getlist('image')

        addhome=Home.objects.create(
                landlord=ll,
                title=title,
                location=location,
                price=price,
                description=description
            )
        for img in image:
            HomeImage.objects.create(
                home=addhome,
                image=img
            )
            return redirect("home")
    return render(request,"add.html")
def llhome(request):
    # user is filtered,fetched according to the order of applied time  stored to notifications
    notifications = Application.objects.filter(user=request.user).order_by('-applied_at')
    
    return render(request, 'llhome.html', {'notifications': notifications})

# def notify(request):
#     return(request)
def llprofile(request):
    return render (request,"llprofile.html")

#views for others,simple rendering only
def about(request):
    return render (request,"about.html")

def notify(request):
    return render(request,'notify.html')

def logout(request):
    logout_auth(request)
    return render(request,"loginUser.html")



