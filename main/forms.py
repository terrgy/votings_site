from datetime import datetime, date, time

from django import forms
from django.core.exceptions import ValidationError
from django.forms import MultiValueField
from django.forms import TextInput, Textarea, Select, ModelForm, HiddenInput
from django.forms.utils import from_current_timezone
from django_registration.forms import RegistrationForm

from main.models import Voting, Image
from .models import User, Complaint


class DateSelectorWidget(forms.MultiWidget):
    DAY_CHOICES = [(day, day) for day in range(1, 32)]
    MONTH_CHOICES = [(month, month) for month in range(1, 13)]
    YEAR_CHOICES = [(year, year) for year in range(2020, datetime.today().year + 5)]
    HOUR_CHOICES = [(hour, hour) for hour in range(24)]
    MINUTE_CHOICES = [(minute, minute) for minute in range(60)]
    SECOND_CHOICES = [(second, second) for second in range(60)]

    def __init__(self, attrs=None):
        widgets = [
            forms.Select(attrs=attrs, choices=self.DAY_CHOICES),
            forms.Select(attrs=attrs, choices=self.MONTH_CHOICES),
            forms.Select(attrs=attrs, choices=self.YEAR_CHOICES),
            forms.Select(attrs=attrs, choices=self.HOUR_CHOICES),
            forms.Select(attrs=attrs, choices=self.MINUTE_CHOICES),
            forms.Select(attrs=attrs, choices=self.SECOND_CHOICES),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, datetime):
            return [value.day, value.month, value.year, value.hour, value.minute, value.second]
        elif isinstance(value, str):
            date_str, time_and_tz_str = value.split()
            time_str, tz_str = value.split('+')
            year, month, day = date_str.split('-')
            hour, minute, second = time_str.split(':')
            return [day, month, year, hour, minute, second]
        return [None, None, None, None, None, None]


class MyDateTimeField(MultiValueField):
    def __init__(self, **kwargs):
        attrs = kwargs.pop('attrs', None)
        self.widget = DateSelectorWidget(attrs)
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        fields = (
            forms.ChoiceField(choices=self.widget.DAY_CHOICES,
                              localize=localize),
            forms.ChoiceField(choices=self.widget.MONTH_CHOICES,
                              localize=localize),
            forms.ChoiceField(choices=self.widget.YEAR_CHOICES,
                              localize=localize),
            forms.ChoiceField(choices=self.widget.HOUR_CHOICES,
                              localize=localize),
            forms.ChoiceField(choices=self.widget.MINUTE_CHOICES,
                              localize=localize),
            forms.ChoiceField(choices=self.widget.SECOND_CHOICES,
                              localize=localize),
        )
        super().__init__(fields, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values:
                raise ValidationError('Некорректный день', code='invalid_date')
            if data_list[1] in self.empty_values:
                raise ValidationError('Некорректный месяц', code='invalid_date')
            if data_list[2] in self.empty_values:
                raise ValidationError('Некоррекный год', code='invalid_date')
            if data_list[3] in self.empty_values:
                raise ValidationError('Некоррекный час', code='invalid_time')
            if data_list[4] in self.empty_values:
                raise ValidationError('Некоррекная минута', code='invalid_time')
            if data_list[5] in self.empty_values:
                raise ValidationError('Некоррекная секунда', code='invalid_time')
            try:
                combined_date = date(int(data_list[2]), int(data_list[1]), int(data_list[0]))
            except ValueError:
                raise ValidationError('Такой даты не существует', code='invalid_date')
            try:
                combined_time = time(int(data_list[3]), int(data_list[4]), int(data_list[5]))
            except ValueError:
                raise ValidationError('Такого времени не существует', code='invalid_time')
            result = datetime.combine(combined_date, combined_time)
            return from_current_timezone(result)
        return None


class VotingMainSettingsForm(forms.Form):
    TYPE_CHOICES = [(1, 'Дискретное'), (2, 'Выбор одного'), (3, 'Выбор многих')]
    voting_title = forms.CharField(max_length=50, required=True, label='Название',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'aria-describedby': 'voting_title_help'
                                   }),
                                   help_text='Ваша визитная карточка, его видно в первую очередь')
    voting_description = forms.CharField(max_length=500, label='Описание', required=False,
                                         widget=forms.Textarea(attrs={
                                             'class': 'form-control',
                                             'aria-describedby': 'voting_description_help',
                                             'style': 'min-height: 130px;'
                                         }),
                                         help_text='Расскажите людям о теме')
    voting_type = forms.ChoiceField(label='Тип', choices=TYPE_CHOICES, required=True,
                                    widget=forms.Select(attrs={
                                        'class': 'form-select'
                                    }))
    voting_finish_time = MyDateTimeField(label='Окончание голосования', required=True,
                                         attrs={
                                             'class': 'form-select mx-1'
                                         },
                                         help_text='Формат: День/Месяц/Год/Час/Минута/Секунда')
    voting_is_active = forms.BooleanField(label='Видно в поиске', required=False,
                                          widget=forms.CheckboxInput(attrs={
                                              'class': 'form-check-input'
                                          }))

    def __init__(self, data=None):
        if data is not None:
            if data.get('request', '') != 'get':
                new_data = data.copy()
                super(VotingMainSettingsForm, self).__init__(data=new_data)
                return
            super(VotingMainSettingsForm, self).__init__()
            self.fields['voting_title'].initial = data.get('voting_title', '')
            self.fields['voting_description'].initial = data.get('voting_description', '')
            self.fields['voting_type'].initial = data.get('voting_type', [])
            self.fields['voting_finish_time'].initial = data.get('voting_finish_time', datetime.now())
            self.fields['voting_is_active'].initial = data.get('voting_is_active', False)
        else:
            super(VotingMainSettingsForm, self).__init__()


class AddVoteVariantForm(forms.Form):
    vote_variant_description = forms.CharField(max_length=100, required=True,
                                               widget=forms.TextInput(attrs={
                                                   'class': 'form-control'
                                               }))

    def __init__(self, data=None):
        if data is not None:
            if data.get('request', '') != 'get':
                new_data = data.copy()
                super(AddVoteVariantForm, self).__init__(data=new_data)
                return
            super(AddVoteVariantForm, self).__init__()
            self.fields['vote_variant_description'].initial = data.get('vote_variant_description', '')
        else:
            super(AddVoteVariantForm, self).__init__()


class SaveVoteVariantForm(forms.Form):
    vote_variant_new_description = forms.CharField(max_length=100, required=True,
                                                   widget=forms.TextInput(attrs={
                                                       'class': 'form-control'
                                                   }))
    vote_variant_save_id = forms.CharField(widget=forms.HiddenInput, required=True)

    def __init__(self, data=None):
        if data is not None:
            if data.get('request', '') != 'get':
                new_data = data.copy()
                super(SaveVoteVariantForm, self).__init__(data=new_data)
                return
            super(SaveVoteVariantForm, self).__init__()
            self.fields['vote_variant_new_description'].initial = data.get('vote_variant_new_description', '')
            self.fields['vote_variant_save_id'].initial = data.get('vote_variant_save_id', '-1')
        else:
            super(SaveVoteVariantForm, self).__init__()


class DeleteVoteVariantForm(forms.Form):
    vote_variant_delete_id = forms.CharField(widget=forms.HiddenInput, required=True)

    def __init__(self, data=None):
        if data is not None:
            if data.get('request', '') != 'get':
                new_data = data.copy()
                super(DeleteVoteVariantForm, self).__init__(data=new_data)
                return
            super(DeleteVoteVariantForm, self).__init__()
            self.fields['vote_variant_delete_id'].initial = data.get('vote_variant_delete_id', '-1')
        else:
            super(DeleteVoteVariantForm, self).__init__()


class SingleVariantVoteForm(forms.Form):
    vote_variants = forms.ChoiceField(widget=forms.RadioSelect, choices=[])

    def __init__(self, data=None, choices=None):
        if data is not None:
            if data.get('request', '') != 'get':
                new_data = data.copy()
                super(SingleVariantVoteForm, self).__init__(data=new_data)
                self.fields['vote_variants'].choices = choices
                return
            super(SingleVariantVoteForm, self).__init__()
            self.fields['vote_variants'].initial = data.get('vote_variants', '')
        else:
            super(SingleVariantVoteForm, self).__init__()
        if choices is None:
            choices = []
        self.fields['vote_variants'].choices = choices


class MultiVariantVoteForm(forms.Form):
    vote_variants = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])

    def __init__(self, data=None, choices=None):
        if data is not None:
            if data.get('request', '') != 'get':
                new_data = data.copy()
                super(MultiVariantVoteForm, self).__init__(data=new_data)
                self.fields['vote_variants'].choices = choices
                return
            super(MultiVariantVoteForm, self).__init__()
            self.fields['vote_variants'].initial = data.getlist('vote_variants', [])
        else:
            super(MultiVariantVoteForm, self).__init__()
        if choices is None:
            choices = []
        self.fields['vote_variants'].choices = choices


class AddForm(ModelForm):
    class Meta:
        model = Voting
        fields = ['name', 'description', 'type', 'finished', 'author']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }
        field_classes = {
            'finished': MyDateTimeField,
        }
        widgets = {
            'author': HiddenInput(),
            'name': TextInput(attrs={
                'class': 'form-control'
            }),
            'description': Textarea(attrs={
                'class': 'form-control'
            }),
            'type': Select(attrs={
                'class': 'form-select'
            }, choices=VotingMainSettingsForm.TYPE_CHOICES),
            'finished': DateSelectorWidget(
                attrs={
                    'class': 'form-select mx-1'
                }
            )
        }


class ComplaintsForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['description', 'status', 'voting', 'author']
        labels = {
            'description': 'Жалоба',

        }
        widgets = {
            'author': HiddenInput(),
            'voting': HiddenInput(),
            'status': HiddenInput(),
            'description': Textarea(attrs={
                'class': 'form-control'
            }),
        }


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }


class RegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class RedactForm(ModelForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'status']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин',
            'status': 'Статус'
        }
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'username': TextInput(attrs={
                'class': 'form-control',
                'read-only': ''
            }),
            'status': TextInput(attrs={
                'class': 'form-control'
            }),
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "old_password",
        'class': "form-control"
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "new_password1",
        'class': "form-control"
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "new_password2",
        'class': "form-control"
    }))


class RegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
