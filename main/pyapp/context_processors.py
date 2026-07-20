from pyapp.models import Application, landlord


def landlord_notifications(request):
    """Makes 'pending_count' available in every template automatically,
    so the notification badge shows up in the landlord sidebar everywhere."""
    if request.user.is_authenticated and request.user.groups.filter(name="landlord").exists():
        try:
            ll = landlord.objects.get(user=request.user)
            count = Application.objects.filter(house__landlord=ll, status='pending', landlord_read=False).count()
            return {'pending_count': count}
        except landlord.DoesNotExist:
            return {'pending_count': 0}
    return {}

def roomseeker_notifications(request):
    """Makes 'notify_count' available on every page automatically,
    so the roomseeker's badge shows up no matter which page they're on."""
    if request.user.is_authenticated and request.user.groups.filter(name="rentseeker").exists():
        count = Application.objects.filter(
            user=request.user
        ).exclude(status='pending').filter(roomseeker_read=False).count()
        return {'notify_count': count}
    return {}