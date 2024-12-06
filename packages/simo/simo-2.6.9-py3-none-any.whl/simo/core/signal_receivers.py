import os
import shutil
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from actstream import action
from simo.users.models import PermissionsRole
from .models import Instance, Gateway, Component, Icon, Zone, Category


@receiver(post_save, sender=Instance)
def create_instance_defaults(sender, instance, created, **kwargs):
    if not created:
        return

    from simo.users.middleware import get_current_user
    actor = get_current_user()
    action.send(
        actor, target=instance, verb="instance created",
        instance_id=instance.id,
        action_type='management_event'
    )

    # Create default zones

    for zone_name in (
        'Living Room', 'Kitchen', 'Bathroom', 'Porch', 'Garage', 'Yard',
    ):
        Zone.objects.create(instance=instance, name=zone_name)

    other_zone = Zone.objects.create(instance=instance, name='Other')

    core_dir_path = os.path.dirname(os.path.realpath(__file__))
    imgs_folder = os.path.join(
        core_dir_path, 'static/defaults/category_headers'
    )

    categories_media_dir = os.path.join(settings.MEDIA_ROOT, 'categories')
    if not os.path.exists(categories_media_dir):
        os.makedirs(categories_media_dir)

    # Create default categories
    climate_category = None
    other_category = None
    for i, data in enumerate([
        ("All", 'star'), ("Climate", 'temperature-half'),
        ("Lights", 'lightbulb'), ("Security", 'eye'),
        ("Watering", 'faucet'), ("Other", 'flag-pennant')
    ]):
        shutil.copy(
            os.path.join(imgs_folder, "%s.jpg" % data[0].lower()),
            os.path.join(
                settings.MEDIA_ROOT, 'categories', "%s.jpg" % data[0].lower()
            )
        )
        cat = Category.objects.create(
            instance=instance,
            name=data[0], icon=Icon.objects.get(slug=data[1]),
            all=i == 0, header_image=os.path.join(
                'categories', "%s.jpg" % data[0].lower()
            ), order=i + 10
        )
        if cat.name == 'Climate':
            climate_category = cat
        if cat.name == 'Other':
            other_category = cat

    # Create generic gateway and components

    generic, new = Gateway.objects.get_or_create(
        type='simo.generic.gateways.GenericGatewayHandler'
    )
    dummy, new = Gateway.objects.get_or_create(
        type='simo.generic.gateways.DummyGatewayHandler'
    )
    automation, new = Gateway.objects.get_or_create(
        type='simo.automation.gateways.AutomationsGatewayHandler'
    )
    weather_icon = Icon.objects.get(slug='cloud-bolt-sun')

    Component.objects.create(
        name='Weather', icon=weather_icon,
        zone=other_zone,
        category=climate_category,
        gateway=generic, base_type='weather',
        controller_uid='simo.generic.controllers.Weather',
        config={'is_main': True}
    )

    state_comp = Component.objects.create(
        name='State', icon=Icon.objects.get(slug='home'),
        zone=other_zone,
        category=other_category,
        gateway=generic, base_type='state-select',
        controller_uid='simo.generic.controllers.StateSelect',
        value='day',
        config={"states": [
            {
                "icon": "sunrise", "name": "Morning", "slug": "morning",
                'help_text': "6:00 AM to sunrise. Activates only in dark time of a year."
            },
            {
                "icon": "house-day", "name": "Day", "slug": "day",
                'help_text': "From sunrise to sunset."
            },
            {
                "icon": "house-night", "name": "Evening", "slug": "evening",
                'help_text': "From sunrise to midnight"
            },
            {
                "icon": "moon-cloud", "name": "Night", "slug": "night",
                'help_text': "From midnight to sunrise or 6:00 AM."
            },
            {"icon": "snooze", "name": "Sleep time", "slug": "sleep"},
            {"icon": "house-person-leave", "name": "Away", "slug": "away"},
            {"icon": "island-tropical", "name": "Vacation", "slug": "vacation"}
        ], "is_main": True}
    )


    auto_state_code = render_to_string(
        'automations/auto_state_script.py', {'state_comp_id': state_comp.id}
    )
    Component.objects.create(
        name='Auto state', icon=Icon.objects.get(slug='bolt'),
        zone=other_zone,
        category=other_category, show_in_app=False,
        gateway=automation, base_type='script',
        controller_uid='simo.automation.controllers.Script',
        config={
            "code": auto_state_code, 'autostart': True, 'keep_alive': True,
            "notes": f"""
            The script automatically controls the states of the "State" component (ID:{state_comp.id}) — 'morning', 'day', 'evening', 'night'. 
            
            """
        }
    )

    code = render_to_string(
        'automations/phones_sleep_script.py', {'state_comp_id': state_comp.id}
    )
    Component.objects.create(
        name='Sleep mode when owner phones are charge',
        icon=Icon.objects.get(slug='bolt'), zone=other_zone,
        category=other_category, show_in_app=False,
        gateway=automation, base_type='script',
        controller_uid='simo.automation.controllers.Script',
        config={
            "code": code, 'autostart': True, 'keep_alive': True,
            "notes": f"""
Automatically sets State component (ID: {state_comp.id}) to "Sleep" if it is later than 10pm and all home owners phones who are at home are put on charge.
Sets State component back to regular state as soon as none of the home owners phones are on charge and it is 6am or later. 

"""
        }
    )

    code = render_to_string(
        'automations/auto_away.py', {'state_comp_id': state_comp.id}
    )
    Component.objects.create(
        name='Auto Away State',
        icon=Icon.objects.get(slug='bolt'), zone=other_zone,
        category=other_category, show_in_app=False,
        gateway=automation, base_type='script',
        controller_uid='simo.automation.controllers.Script',
        config={
            "code": code, 'autostart': True, 'keep_alive': True,
            "notes": f"""
    Automatically set mode to "Away" there are no users at home and there was no motion for more than 30 seconds.
    Set it back to a regular mode as soon as somebody comes back home or motion is detected.

    """
        }
    )

    # Create default User permission roles

    PermissionsRole.objects.create(
        instance=instance, name="Admin", is_owner=True, is_superuser=True
    )
    PermissionsRole.objects.create(
        instance=instance, name="Owner", is_owner=True, is_default=True
    )
    PermissionsRole.objects.create(
        instance=instance, name="Guest", is_owner=False
    )
    generic.start()
    dummy.start()


@receiver(post_save, sender=Zone)
@receiver(post_save, sender=Category)
def post_save_actions_dispatcher(sender, instance, created, **kwargs):
    from simo.users.middleware import get_current_user
    actor = get_current_user()
    if created:
        verb = 'created'
    else:
        verb = 'modified'
    action.send(
        actor, target=instance, verb=verb,
        instance_id=instance.instance.id,
        action_type='management_event'
    )


@receiver(post_save, sender=Component)
@receiver(post_save, sender=Gateway)
def post_save_change_events(sender, instance, created, **kwargs):
    target = instance
    from .events import ObjectChangeEvent
    dirty_fields = target.get_dirty_fields()
    for ignore_field in (
        'change_init_by', 'change_init_date', 'change_init_to', 'last_update'
    ):
        dirty_fields.pop(ignore_field, None)

    def post_update():
        if not dirty_fields:
            return

        if type(target) == Gateway:
            ObjectChangeEvent(
                None, target,
                dirty_fields=dirty_fields,
            ).publish()
        elif type(target) == Component:
            data = {}
            for field_name in (
                'value', 'last_change', 'arm_status',
                'battery_level', 'alive', 'meta'
            ):
                data[field_name] = getattr(target, field_name, None)
            ObjectChangeEvent(
                target.zone.instance, target,
                dirty_fields=dirty_fields,
                **data
            ).publish()
            for master in target.masters.all():
                data = {}
                for field_name in (
                    'value', 'last_change', 'arm_status',
                    'battery_level', 'alive', 'meta'
                ):
                    data[field_name] = getattr(master, field_name, None)
                ObjectChangeEvent(
                    master.zone.instance,
                    master, slave_id=target.id,
                    **data
                ).publish()

    transaction.on_commit(post_update)


@receiver(post_save, sender=Gateway)
def gateway_post_save(sender, instance, created, *args, **kwargs):
    def start_gw():
        if created:
            gw = Gateway.objects.get(pk=instance.pk)
            gw.start()

    transaction.on_commit(start_gw)


@receiver(post_delete, sender=Gateway)
def gateway_post_delete(sender, instance, *args, **kwargs):
    instance.stop()