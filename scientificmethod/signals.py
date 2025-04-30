from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import VersionHistory

@receiver(pre_save)
def auto_log_save(sender, instance, **kwargs):
    # Only log models from our app, not Django built-in models
    if not sender._meta.app_label == 'scientificmethod':
        return

    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        fields = [f.name for f in sender._meta.get_fields() if hasattr(f, 'attname')]

        for field in fields:
            old_value = getattr(old_instance, field, None)
            new_value = getattr(instance, field, None)

            # Compare ignoring timestamps
            if field not in ['created_at', 'updated_at'] and old_value != new_value:
                VersionHistory.objects.create(
                    content_type=ContentType.objects.get_for_model(sender),
                    object_id=instance.pk,
                    field_name=field,
                    old_value=str(old_value) if old_value is not None else '',
                    new_value=str(new_value) if new_value is not None else '',
                    edited_by='System',  # You can replace with request.user later if you capture it
                    change_reason='Auto change detected'
                )