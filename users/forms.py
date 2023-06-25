from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile, Specialty, Order, Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['order', 'photo1', 'photo2', 'photo3', 'comment']
        widgets = {
            'order': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class OrderForm(forms.ModelForm):
    description = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'class': ' ml-1 shadow appearance-none border rounded w-72 h-14 text-white leading-tight focus:outline-none ',
                
            }
        )
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'shadow appearance-none border rounded w-12 text-white leading-tight focus:outline-none focus:shadow-outline',
                
            }
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'shadow appearance-none border rounded w-24  text-white leading-tight focus:outline-none focus:shadow-outline',
               
            }
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'shadow appearance-none border rounded w-24  text-white leading-tight focus:outline-none focus:shadow-outline',
                
            }
        )
    )
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        empty_label='Выбрать специальность',
        widget=forms.Select(
            attrs={
                'class': 'shadow appearance-none border rounded w-32 text-white leading-tight focus:outline-none focus:shadow-outline',
            }
        )
    )

    class Meta:
        model = Order
        fields = ['description', 'price', 'address', 'phone', 'specialty']


class ProfileSettingsForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        empty_label='Выбрать специальность'
    )

    class Meta:
        model = Profile
        fields = ['bio', 'specialty']


class CustomUserCreationForm(UserCreationForm):
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'is_worker', 'photo')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        

