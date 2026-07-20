# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout as logout_auth
from django.contrib.auth import authenticate, login as login_auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse

from pyapp.models import Home, landlord, RoomSeekerProfile, HomeImage, Contact, Application


# ---------- Small role-check helpers ----------

def is_landlord(user):
    return user.is_authenticated and user.groups.filter(name="landlord").exists()


def is_roomseeker(user):
    return user.is_authenticated and user.groups.filter(name="rentseeker").exists()


# ---------- Public / general pages ----------

# just a test function for the view to send the variable to template
def pyapp(request):
    context = {
        "variable1": "Avishek",
        "variable2": "AVishek Karki"
    }
    return render(request, 'pyapp.html', context)
# test function ends here

# contact function which would be in use later,not on use 
def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            password='',
            feedback=request.POST.get('textarea', ''),
        )
        messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
        return redirect('contact')
    return render(request, 'contact.html')
# contact function ends here

def profile(request):
    # rsp as relevant variable roomseekerprofile
    # roomseekerprofile is the model where the objects ie model manager helps to interact with the model ,model manager(object) function filter helps to fetch user by requesting firstly
    rsp = RoomSeekerProfile.objects.filter(user=request.user).first()
    # as view recieves user request. process, manages data from model and store it in variable which is passed to the template ie rsp
    return render(request, "profile.html", {"rsp": rsp})


def about(request):
    return render(request, 'about.html')

# ---------- Register / Login / Logout ----------

def register(request):
    if request.method == "POST":
        role = request.POST.get('role', "")
        username = request.POST.get('username', "")
        email = request.POST.get('email', "")
        phone = request.POST.get('phone', "")
        password = request.POST.get('password')

        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            return render(request, 'register.html', {
                "error": "Username or email already existed!"
            })
        if not role:
            return render(request, "register.html", {
                "blankrole": "Role need to be selected!"
            })
        if not username:
            return render(request, "register.html", {
                "blankuser": "Username shouldnt be empty!"
            })
        if not email:
            return render(request, "register.html", {
                "blankemail": "Email shouldnt be empty!"
            })
        if not password:
            return render(request, "register.html", {
                "blankpassword": "Password shouldnt be empty!"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        group, created = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        if role == "landlord":
            landlord.objects.create(user=user, phone=phone)
        if role == "rentseeker":
            RoomSeekerProfile.objects.create(user=user, phone=phone)

        messages.success(request, "Account created! Please log in.")
        return redirect('loginUser')
    return render(request, 'register.html')


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return render(request, "loginUser.html", {
                "crerror": "Credentials didnt matched!"
            })

        if user.groups.filter(name="rentseeker").exists():
            login_auth(request, user)
            return redirect("home.html")
        elif user.groups.filter(name="landlord").exists():
            login_auth(request, user)
            return redirect("llhome")
        else:
            login_auth(request, user)
            return redirect("register")
    return render(request, "loginUser.html")


def logout(request):
    logout_auth(request)
    return redirect("loginUser")


# ---------- Roomseeker views ----------

@login_required
def home_data(request):
    """Roomseeker home: browse available houses, with price/location filters."""
    homedata = Home.objects.filter(is_available=True).select_related('landlord', 'landlord__user')

    q = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if q:
        homedata = homedata.filter(Q(title__icontains=q) | Q(location__icontains=q))
    if min_price:
        try:
            homedata = homedata.filter(price__gte=int(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            homedata = homedata.filter(price__lte=int(max_price))
        except ValueError:
            pass

    applied_house_ids = set(
        Application.objects.filter(user=request.user).values_list('house_id', flat=True)
    )

    return render(request, 'home.html', {
        'homefetch': homedata,
        'applied_house_ids': applied_house_ids,
        'q': q,
        'min_price': min_price,
        'max_price': max_price,
    })


@login_required
def view_details(request, pk):
    # rs=User.groups.get(name="roomseeker")
    # landl=User.groups.get(name="landlord")
    det = get_object_or_404(Home, pk=pk)
    already_applied = Application.objects.filter(house=det, user=request.user).exists()
    return render(request, "viewhtml.html", {
        "vd": det,
        "already_applied": already_applied,
        # "rent":rs,
        "is_landlord":request.user.groups.filter(name="landlord"),
    })

# @login_required
# def home(request):
#     homes = Home.objects.all()

#     notify_count = Application.objects.filter(
#         user=request.user
#     ).exclude(status='pending').count()

#     return render(request, "home.html", {
#         "homefetch": homes,
#         "notify_count": notify_count,
#     })

@login_required
def process_apply(request, pk):
    house = get_object_or_404(Home, pk=pk)

    if Application.objects.filter(user=request.user, house=house).exists():
        messages.info(request, "You have already applied for this house.")
        return redirect('view_details', pk=pk)

    Application.objects.create(
        user=request.user,
        house=house,
        landlord_read=False,
    )
    messages.success(request, "Applied successfully! The landlord has been notified.")
    return redirect('view_details', pk=pk)


@login_required
def my_applications(request):
    """Roomseeker's own 'notifications' page: status of everything they've applied for."""
    applications = Application.objects.filter(user=request.user).select_related('house', 'house__landlord__user')
    applications.filter(roomseeker_read=False).update(roomseeker_read=True)
    return render(request, 'my_applications.html', {'applications': applications})

def llapplications(request):
    """Landlord's own 'notifications' page: status of everything they've applied for."""
    ll = landlord.objects.get(user=request.user)
    applications = Application.objects.filter(house__landlord=ll).select_related('user', 'house')
    applications.filter(landlord_read=False).update(landlord_read=True)
    return render(request, 'llapplications.html', {'applications': applications})

# ---------- Landlord views ----------

@login_required
def add(request):
    ll = landlord.objects.get(user=request.user)
    if request.method == "POST":
        title = request.POST.get('title', "")
        location = request.POST.get('location')
        price = request.POST.get('price')
        description = request.POST.get('desc')
        images = request.FILES.getlist('image')

        addhome = Home.objects.create(
            landlord=ll,
            title=title,
            location=location,
            price=price,
            description=description
        )
        for img in images:
            HomeImage.objects.create(
                home=addhome,
                image=img
            )
        messages.success(request, "House listed successfully!")
        return redirect("llhome")
    return render(request, "add.html")

# notification count for landlord and roomseeker
@login_required
def llhome(request):
    """Landlord's own listings page."""
    ll = landlord.objects.get(user=request.user)
    homes = Home.objects.filter(landlord=ll)
    pending_count = Application.objects.filter(house__landlord=ll, status='pending').count()
    return render(request, 'llhome.html', {
        'homefetch': homes,
        'pending_count': pending_count,
    })

@login_required
def notify(request):
    """Landlord's notifications page: applications on their houses, Accept/Decline."""
    ll = landlord.objects.get(user=request.user)
    applications = Application.objects.filter(house__landlord=ll).select_related('user', 'house')
    applications.filter(landlord_read=False).update(landlord_read=True)
    return render(request, 'notify.html', {'applications': applications})
@login_required
def home(request):
    homes = Home.objects.all()
    notify_count = Application.objects.filter(
        user=request.user
    ).exclude(status='pending').filter(roomseeker_read=False).count()
    return render(request, "home.html", {
        "homefetch": homes,
        "notify_count": notify_count,
    })

@login_required
def rs_notifications(request):
    notifications = Application.objects.filter(
        user=request.user
    ).exclude(status='pending').order_by('-applied_at').select_related('house', 'house__landlord__user')
    notifications.filter(roomseeker_read=False).update(roomseeker_read=True)
    return render(request, "rs_notifications.html", {
        "notifications": notifications
    })

# notification end for landlord and roomseeker
def rsupdate_application_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if status in ['accepted', 'declined','pending']:
        application.status = status
        application.roomseeker_read = True
        application.save()
        messages.success(request, f"Application {status}.")
    return redirect('my_applications')

@login_required
def update_application_status(request, pk, status):
    ll = landlord.objects.get(user=request.user)
    application = get_object_or_404(Application, pk=pk, house__landlord=ll)
    if status in ['accepted', 'declined', 'pending']:
        application.status = status
        application.roomseeker_read = True  # roomseeker gets a fresh notification
        application.save()
        messages.success(request, f"Application {status}.")
    return redirect('notify')


@login_required
def llprofile(request):
    ll = landlord.objects.get(user=request.user)
    return render(request, "llprofile.html", {"ll": ll})


# edit and delete 
@login_required
def edit_home(request, pk):
    ll=landlord.objects.get(user=request.user)
    home=get_object_or_404(Home, pk=pk, landlord=ll)
    if request.method=="POST":
        home.title=request.POST.get("title","")
        home.location=request.POST.get("location","")
        home.price=request.POST.get("price","")
        home.description=request.POST.get("desc","")
        home.is_available=request.POST.get("is_available")=="on"

        home.save()
        
        images=request.FILES.getlist("image")
        for img in images:
            HomeImage.objects.create(home=home, image=img)
            messages.success(request,"House updated successfully")
            return redirect("llhome")
    return render(request,"edit_home.html",{"home":home})
    
@login_required
def delete_home(request,pk):
    ll=landlord.objects.get(user=request.user)
    home=get_object_or_404(Home,pk=pk,landlord=ll)
    if request.method=="POST":
        home.delete()
        messages.success(request,"Deleted successfully")
        return redirect("llhome")
    return render(request,"delete_home.html",{"home":home})

def cancel_application(request,pk):
    application=get_object_or_404(Application, pk=pk, user=request.user)
    if application.status=="pending":
        application.delete()
        messages.success(request,"Application cancelled successfully")
    else:
        messages.error(request,"Cannot cancel application that has been processed.")
    return redirect("my_applications")

def ll_cancel_application(request,pk):
    ll=landlord.objects.get(user=request.user)
    application=get_object_or_404(Application,pk=pk,house__landlord=ll)
    if application.status=="pending":
        application.delete()
        messages.success(request,"Application cancelled successfully")
    else:
        messages.error(request,"Cannot cancel application that has been processed.")
    return redirect("llapplications")
