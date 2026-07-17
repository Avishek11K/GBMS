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
