from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from account.models import Account
from django.db.models import Q
from django.template.defaultfilters import slugify

class UniqueUserEmailField(forms.EmailField):
    """
    An EmailField which only is valid if no Account has that email.
    """

    def validate(self, value):
        super().validate(value)
        try:
            Account.objects.get(email=value)
            raise forms.ValidationError("A user with that email already exists.")
        except Account.MultipleObjectsReturned:
            raise forms.ValidationError("A user with that email already exists.")
        except Account.DoesNotExist:
            pass

class UsernameExistsField(UsernameField):
    """
    An UsernameField that raises an error when the name is 
    not registered on the database.
    """

    def validate(self, value):
        super().validate(value)
        try:
            Account.objects.get(username=value)
        except Account.DoesNotExist:
            raise forms.ValidationError("There's no user registered with that username.")


class UniqueUsernameField(UsernameField):
    """
    An UsernameField that raises an error when the 
    name is already in use.
    """

    def validate(self, value):
        super().validate(value)
        try:
            Account.objects.get(slug=slugify(value))
            raise forms.ValidationError("There's already an user registered with that username.")
        except Account.MultipleObjectsReturned:
            raise forms.ValidationError("There's already an user registered with that username.")
        except Account.DoesNotExist:
            pass

class UserRegisterForm(UserCreationForm):
    """
    Extends the built in UserCreationForm to include the Account email 
    and the form-control class in each widget.
    """

    email = UniqueUserEmailField(required=True, label='Email address')
    username = UniqueUsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )

    class Meta:
        model = Account
        fields = ("username", "email")    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control'})

class UserAuthenticationForm(AuthenticationForm):
    """
    Extends the built in AuthenticationForm to add 
    the form-control class in each widget.
    """

    username = UsernameExistsField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
