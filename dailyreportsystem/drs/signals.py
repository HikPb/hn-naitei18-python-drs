from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from .models import Form, Report, Notification, User, Timeline

@receiver(post_save, sender=Form)
def event_when_create_request(instance, created, **ksargs):
    if created:
        # create notification
        noti_receiver = instance.receiver
        user_id = instance.sender
        noti_form_id = instance
        noti_type = "nr"
        noti_content = "New request: {}".format(instance.title)
        tl_content = "You created new request: {}".format(instance.title)
        created_at = timezone.now()
        Notification.objects.create(sender=user_id, receiver=noti_receiver, created_at=created_at,
                                    form_id=noti_form_id, type_notification=noti_type, content=noti_content)
        Timeline.objects.create(user_id=user_id, created_at=created_at,
                                event="create", content=tl_content)

@receiver(pre_delete, sender=Form)
def event_when_delete_request(instance, **ksargs):
    if instance.sender:
        user_id = instance.sender
        tl_content = "You deleted request: {}".format(instance.title)
        created_at = timezone.now()
        Timeline.objects.create(user_id=user_id, created_at=created_at,
                                event="delete", content=tl_content)

@receiver(post_save, sender=Report)
def event_when_create_report(sender, instance, created, **ksargs):
    if created:
        noti_receiver = instance.receiver
        user_id = instance.sender
        noti_type = "r"
        noti_content = "New report: {}".format(instance.plan)
        tl_content = "You created new report: {}".format(instance.plan)
        created_at = timezone.now()
        Notification.objects.create(sender=user_id, receiver=noti_receiver, created_at=created_at,
                                   type_notification=noti_type, content=noti_content)
        Timeline.objects.create(user_id=user_id, created_at=created_at,
                                event="create", content=tl_content)

@receiver(pre_delete, sender=Report)
def event_when_delete_report(sender, instance, **ksargs):
    if instance.sender:
        user_id = instance.sender
        tl_content = "You deleted report: {}".format(instance.plan)
        created_at = timezone.now()
        Timeline.objects.create(user_id=user_id, created_at=created_at,
                                event="delete", content=tl_content)


# @receiver(post_save, sender=Notification)
# def send_notification_info(sender, instance, created, **ksargs):
#     if created:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "notification_group_{}".format(instance.sender.id), {
#                 'type':'notification_info'
#             }
#         )

@receiver(post_save, sender=Notification)
def send_mail_when_has_new_form(sender, instance, created, **ksargs):
    if created:
        mail_subject = "Request Notification"
        message = render_to_string('notification/notification_form_mail.html', {
				'noti_title': instance.content,
			})
        to_email = instance.receiver.email
        email = EmailMessage(
            mail_subject, message, to=[to_email],
        )
        email.content_subtype = "html"
        email.send()
