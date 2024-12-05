from django import forms
from django.forms import formset_factory
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from simo.core.forms import HiddenField, BaseComponentForm
from simo.core.models import Icon, Component
from simo.core.controllers import (
    NumericSensor, MultiSensor, Switch, Dimmer
)
from dal import forward
from simo.core.utils.config_values import config_to_dict
from simo.core.utils.formsets import FormsetField
from simo.core.utils.helpers import get_random_string
from simo.core.utils.form_fields import ListSelect2Widget
from simo.core.form_fields import (
    Select2ModelChoiceField, Select2ListChoiceField,
    Select2ModelMultipleChoiceField
)


ACTION_METHODS = (
    ('turn_on', "Turn ON"), ('turn_off', "Turn OFF"),
    ('play', "Play"), ('pause', "Pause"), ('stop', "Stop"),
    ('open', 'Open'), ('close', 'Close'),
    ('lock', "Lock"), ('unlock', "Unlock"),
)


class ThermostatConfigForm(BaseComponentForm):
    temperature_sensor = Select2ModelChoiceField(
        queryset=Component.objects.filter(
            base_type__in=(
                NumericSensor.base_type,
                MultiSensor.base_type
            )
        ),
        url='autocomplete-component',
        forward=(
            forward.Const([
                NumericSensor.base_type,
                MultiSensor.base_type
            ], 'base_type'),
        )
    )
    heater = Select2ModelChoiceField(
        queryset=Component.objects.filter(base_type=Switch.base_type),
        required=False,
        url='autocomplete-component',
        forward=(
            forward.Const([
                Switch.base_type,
            ], 'base_type'),
        )
    )
    cooler = Select2ModelChoiceField(
        queryset=Component.objects.filter(base_type=Switch.base_type),
        required=False,
        url='autocomplete-component',
        forward=(
            forward.Const([
                Switch.base_type,
            ], 'base_type'),
        )

    )
    mode = forms.ChoiceField(
        choices=(('heater', "Heater"), ('cooler', "Cooler"), ('auto', "Auto"),),
        initial='heater'
    )
    reaction_difference = forms.FloatField(initial=0.5)
    min = forms.IntegerField(initial=3)
    max = forms.IntegerField(initial=36)
    use_real_feel = forms.BooleanField(
        label=_("Use real feel as target temperature"), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['mode'].initial = \
                self.instance.config['user_config']['mode']
            temperature_sensor = Component.objects.filter(
                pk=self.instance.config.get('temperature_sensor', 0)
            ).first()
            if temperature_sensor \
            and temperature_sensor.base_type == MultiSensor.base_type:
                self.fields['use_real_feel'].initial = self.instance.config[
                    'user_config'
                ].get('use_real_feel')
            else:
                self.fields['use_real_feel'].disabled = True

    def save(self, commit=True):
        self.instance.value_units = self.cleaned_data[
            'temperature_sensor'
        ].value_units
        if not self.instance.config.get('user_config'):
            from .controllers import Thermostat
            self.instance.config['user_config'] = config_to_dict(
                Thermostat(self.instance)._get_default_user_config()
            )
        self.instance.config['user_config']['mode'] = self.cleaned_data['mode']
        self.instance.config['has_real_feel'] = True if self.cleaned_data[
            'temperature_sensor'
        ].base_type == MultiSensor.base_type else False
        self.instance.config['user_config']['use_real_feel'] = \
        self.cleaned_data.get('use_real_feel', False)
        return super().save(commit)


class AlarmBreachEventForm(forms.Form):
    uid = HiddenField(required=False)
    component = Select2ModelChoiceField(
        queryset=Component.objects.all(),
        url='autocomplete-component',
    )
    breach_action = forms.ChoiceField(
        initial='turn_on', choices=ACTION_METHODS
    )
    disarm_action = forms.ChoiceField(
        required=False, initial='turn_off', choices=ACTION_METHODS
    )
    delay = forms.IntegerField(
        label="Delay (s)",
        min_value=0, max_value=600, initial=0,
        help_text="Event will not fire if alarm group is disarmed "
                  "within given timeframe of seconds after the breach."
    )
    prefix = 'breach_events'

    def clean(self):
        if not self.cleaned_data.get('component'):
            return self.cleaned_data
        if not self.cleaned_data.get('breach_action'):
            return self.cleaned_data
        component = self.cleaned_data.get('component')
        if not getattr(component, self.cleaned_data['breach_action'], None):
            self.add_error(
                'breach_action',
                f"{component} has no {self.cleaned_data['breach_action']} action!"
            )
        if self.cleaned_data.get('disarm_action'):
            if not getattr(component, self.cleaned_data['disarm_action'], None):
                self.add_error(
                    'disarm_action',
                    f"{component} has no "
                    f"{self.cleaned_data['disarm_action']} action!"
                )
        if not self.cleaned_data.get('uid'):
            self.cleaned_data['uid'] = get_random_string(6)
        return self.cleaned_data


# TODO: create control widget for admin use.
class AlarmGroupConfigForm(BaseComponentForm):
    components = Select2ModelMultipleChoiceField(
        queryset=Component.objects.filter(
            Q(alarm_category__isnull=False) | Q(base_type='alarm-group')
        ),
        required=True,
        url='autocomplete-component',
        forward=(
            forward.Const(['security', 'fire', 'flood', 'other'], 'alarm_category'),
        )
    )
    is_main = forms.BooleanField(
        required=False,
        help_text="Defines if this is your main/top global alarm group."
    )
    arm_on_away = forms.ChoiceField(
        required=False,
        choices=(
            (None, "No"),
            ('on_away', "Yes"),
            ('on_away_and_locked', "Yes, but only if at least one arming lock is Locked."),
            ('on_away_and_locked_all', "Yes, but only if all arming locks are Locked."),
        ),
        help_text="Arm automatically as soon as everybody leaves.<br>"
    )
    arming_locks = Select2ModelMultipleChoiceField(
        queryset=Component.objects.filter(base_type='lock'),
        label="Arming locks", required=False,
        url='autocomplete-component',
        forward=(
            forward.Const(['lock'], 'base_type'),
        ),
        help_text="Alarm group will get armed automatically whenever "
                  "any of assigned locks changes it's state to locked. <br>"
                  "If Arm on away is enabled and set to work with arming locks, "
                  "arming will take effect only after everybody leaves."
    )
    disarming_locks = Select2ModelMultipleChoiceField(
        queryset=Component.objects.filter(base_type='lock'),
        label="Disarming locks", required=False,
        url='autocomplete-component',
        forward=(
            forward.Const(['lock'], 'base_type'),
        ),
        help_text="Alarm group will be disarmed automatically whenever "
                  "any of assigned locks changes it's state to unlocked. "
    )
    notify_on_breach = forms.IntegerField(
        required=False, min_value=0,
        help_text="Notify active users on breach if "
                  "not disarmed within given number of seconds. <br>"                  
                  "Leave this empty to disable breach notifications."
    )
    breach_events = FormsetField(
        formset_factory(
            AlarmBreachEventForm, can_delete=True, can_order=True, extra=0
        ), label='Breach events'
    )
    has_alarm = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .controllers import AlarmGroup
        if not self.instance.pk:
            first_alarm_group = bool(
                not Component.objects.filter(
                    controller_uid=AlarmGroup.uid,
                    config__is_main=True
                ).count()
            )
            if 'is_main' in self.fields:
                self.fields['is_main'].initial = first_alarm_group
                if first_alarm_group:
                    self.fields['is_main'].widget.attrs['disabled'] = 'disabled'
        else:
            if self.instance.config.get('is_main'):
                self.fields['is_main'].widget.attrs['disabled'] = 'disabled'


    def recurse_check_alarm_groups(self, components, start_comp=None):
        for comp in components:
            check_cmp = start_comp if start_comp else comp
            if comp.pk == self.instance.pk:
                raise forms.ValidationError(
                    "Can not cover self. Please remove - [%s]" % str(check_cmp)
                )
            if comp.base_type == 'alarm-group':
                self.recurse_check_alarm_groups(
                    comp.get_children(), check_cmp
                )

    def clean_components(self):
        self.recurse_check_alarm_groups(self.cleaned_data['components'])
        return self.cleaned_data['components']


    def save(self, *args, **kwargs):
        self.instance.value_units = 'status'
        from .controllers import AlarmGroup
        if 'is_main' in self.cleaned_data:
            if self.fields['is_main'].widget.attrs.get('disabled'):
                self.cleaned_data['is_main'] = self.fields['is_main'].initial
        obj = super().save(*args, **kwargs)
        if obj.config.get('is_main'):
            for c in Component.objects.filter(
                controller_uid=AlarmGroup.uid,
                config__is_main=True
            ).exclude(pk=obj.pk):
                c.config['is_main'] = False
                c.save(update_fields=('config',))
        if obj.id:
            comp = Component.objects.get(id=obj.id)
            comp.refresh_status()
        return obj


class IPCameraConfigForm(BaseComponentForm):
    rtsp_address = forms.CharField(
        required=True,
        help_text="Use lower resolution stream. Include user credentials if needed. <br><br>"
                  "HKVISION Example: rtsp://admin:Passw0rd!@192.168.1.210:554/Streaming/Channels/2",
        widget=forms.TextInput(attrs={'style': 'width: 500px'})

    )

class WeatherForm(BaseComponentForm):
    is_main = forms.BooleanField(
        required=False,
        help_text="Defines if this is your main/top global weather."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .controllers import Weather
        if not self.instance.pk:
            first_weather = bool(
                not Component.objects.filter(
                    controller_uid=Weather.uid,
                    config__is_main=True
                ).count()
            )
            self.fields['is_main'].initial = first_weather
            if first_weather:
                self.fields['is_main'].widget.attrs['disabled'] = 'disabled'
        else:
            if self.instance.config.get('is_main'):
                self.fields['is_main'].widget.attrs['disabled'] = 'disabled'


    def save(self, *args, **kwargs):
        self.instance.value_units = 'status'
        from .controllers import Weather
        if 'is_main' in self.fields and 'is_main' in self.cleaned_data:
            if self.fields['is_main'].widget.attrs.get('disabled'):
                self.cleaned_data['is_main'] = self.fields['is_main'].initial
        obj = super().save(*args, **kwargs)
        if obj.config.get('is_main'):
            for c in Component.objects.filter(
                controller_uid=Weather.uid,
                config__is_main=True
            ).exclude(pk=obj.pk):
                c.config['is_main'] = False
                c.save(update_fields=('config',))
        return obj



class ContourForm(forms.Form):
    uid = forms.CharField(widget=forms.HiddenInput(), required=False)
    color = forms.CharField(widget=forms.HiddenInput(), required=False)

    name = forms.CharField()
    switch = Select2ModelChoiceField(
        queryset=Component.objects.filter(
            base_type__in=(Switch.base_type, Dimmer.base_type)
        ),
        url='autocomplete-component',
        forward=(
            forward.Const([Switch.base_type], 'base_type'),
        )
    )
    runtime = forms.IntegerField(
        min_value=0,
        help_text="Contour runtime in minutes. "
                  "Users can adjust this later in the app."
    )
    occupation = forms.IntegerField(
        min_value=1, max_value=100, initial=100,
        help_text="How much in % of total water stream does this contour "
                  "occupies when opened."
    )

    prefix = 'contours'


class WateringConfigForm(BaseComponentForm):
    COLORS = [
        "#00E1FF", "#FF00FF", "#9A00FF", "#45FFD6", "#D1FF00",
        "#0000FF", "#FF0000", "#00E1FF", "#E0AAFF", "#00E139",
        "#E0E1FF", "#921D3E", "#F15A29", "#FBB040", "#F9ED32",
        "#8DC63F", "#006838", "#1C75BC", "#9E1F63", "#662D91"
    ]
    contours = FormsetField(
        formset_factory(ContourForm, can_delete=True, can_order=True, extra=0)
    )
    ai_assist = forms.BooleanField(
        label="Enabled/disabled AI assist",
        required=False, initial=True,
        help_text="Save water by skipping scheduled watering events based "
                  "on previous, current and predicted weather in your area."
    )
    # https://www.boughton.co.uk/products/topsoils/soil-types/
    soil_type = forms.ChoiceField(
        choices=(
            ('loamy', 'Loamy'),
            ('silty', "Silty Soil"),
            ('sandy', "Sandy Soil"),
            ('clay', "Clay Soil"),
            ('peaty', "Peaty Soil"),
            ('chalky', "Chalky Soil"),
        )
    )
    ai_assist_level = forms.IntegerField(
        min_value=0, max_value=100, initial=50,
        help_text="0 - do not skip watering, unless it was cold and raining for weeks. <br>"
                  "100 - try to save as much water as possible by avoiding "
                  "watering program as much as possible. "
    )

    def clean_contours(self):
        contours = self.cleaned_data['contours']
        names = set()
        for i, cont in enumerate(contours):
            if cont['name'] in names:
                raise forms.ValidationError('Contour names must be unique!')
            names.add(cont['name'])
            if not cont['color']:
                cont['color'] = self.COLORS[i % len(self.COLORS)]
            if not cont['uid']:
                cont['uid'] = get_random_string(6)
        return contours

    def save(self, commit=True):
        if 'contours' in self.cleaned_data:
            self.instance.config['program'] = self.controller._build_program(
                self.cleaned_data['contours']
            )
        obj = super().save(commit=commit)
        if commit and 'contours' in self.cleaned_data:
            obj.slaves.clear()
            for contour in self.cleaned_data['contours']:
                obj.slaves.add(
                    Component.objects.get(pk=contour['switch'])
                )
        return obj


class StateForm(forms.Form):
    icon = forms.CharField(
        widget=ListSelect2Widget(
            url='autocomplete-icon', attrs={'data-html': True}
        )
    )
    slug = forms.SlugField(required=True)
    name = forms.CharField(required=True)
    help_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    prefix = 'states'


class StateSelectForm(BaseComponentForm):
    states = FormsetField(
        formset_factory(StateForm, can_delete=True, can_order=True, extra=0)
    )
    is_main = forms.BooleanField(
        initial=False, required=False,
        help_text="Will be displayed in the app "
                  "right top corner for quick access."
    )

    def save(self, commit=True):
        if commit and self.cleaned_data['is_main']:
            from .controllers import StateSelect
            for c in Component.objects.filter(controller_uid=StateSelect.uid):
                c.config['is_main'] = False
                c.save()
        return super().save(commit)


class AlarmClockEventForm(forms.Form):
    uid = HiddenField(required=False)
    enabled = forms.BooleanField(initial=True)
    name = forms.CharField(max_length=30)
    component = Select2ModelChoiceField(
        queryset=Component.objects.all(),
        url='autocomplete-component'
    )
    play_action = forms.ChoiceField(
        initial='turn_on', choices=ACTION_METHODS
    )
    reverse_action = forms.ChoiceField(
        required=False, initial='turn_off', choices=ACTION_METHODS
    )
    offset = forms.IntegerField(min_value=-120, max_value=120, initial=0)

    prefix = 'default_events'

    def clean(self):
        if not self.cleaned_data.get('component'):
            return self.cleaned_data
        if not self.cleaned_data.get('play_action'):
            return self.cleaned_data
        component = self.cleaned_data.get('component')
        if 'play_action' in self.cleaned_data:
            if not hasattr(component, self.cleaned_data['play_action']):
                self.add_error(
                    'play_action',
                    f"{component} has no {self.cleaned_data['play_action']} action!"
                )
        if 'reverse_action' in self.cleaned_data:
            if self.cleaned_data.get('reverse_action'):
                if not hasattr(component, self.cleaned_data['reverse_action']):
                    self.add_error(
                        'reverse_action',
                        f"{component} has no "
                        f"{self.cleaned_data['reverse_action']} action!"
                    )
        return self.cleaned_data


class AlarmClockConfigForm(BaseComponentForm):
    default_events = FormsetField(
        formset_factory(
            AlarmClockEventForm, can_delete=True, can_order=True, extra=0
        ), label='Default events'
    )

    def clean_default_events(self):
        events = self.cleaned_data['default_events']
        for i, cont in enumerate(events):
            if not cont.get('uid'):
                cont['uid'] = get_random_string(6)
        return events

    def save(self, commit=True):
        obj = super().save(commit=commit)
        if commit and 'default_events' in self.cleaned_data:
            obj.slaves.clear()
            for comp in self.cleaned_data['default_events']:
                c = Component.objects.filter(pk=comp['component']).first()
                if c:
                    obj.slaves.add(c)
        return obj
