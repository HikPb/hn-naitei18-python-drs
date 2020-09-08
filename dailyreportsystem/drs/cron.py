from .models import Form


def auto_update():
    Form.objects.filter(status='p').update(status='a')
    Form.save()
