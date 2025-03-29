from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Import the Profile model from your app's models
from .models import Profile

# Centralized language choices with translation support
LANG_CHOICES = [
    ('af', _('Afrikaans')),
    ('sq', _('Albanian')),
    ('am', _('Amharic')),
    ('ar', _('Arabic')),
    ('hy', _('Armenian')),
    ('az', _('Azerbaijani')),
    ('eu', _('Basque')),
    ('be', _('Belarusian')),
    ('bn', _('Bengali')),
    ('bs', _('Bosnian')),
    ('bg', _('Bulgarian')),
    ('ca', _('Catalan')),
    ('ceb', _('Cebuano')),
    ('zh-hans', _('Chinese (Simplified)')),
    ('zh-hant', _('Chinese (Traditional)')),
    ('co', _('Corsican')),
    ('hr', _('Croatian')),
    ('cs', _('Czech')),
    ('da', _('Danish')),
    ('nl', _('Dutch')),
    ('en', _('English')),
    ('eo', _('Esperanto')),
    ('et', _('Estonian')),
    ('fi', _('Finnish')),
    ('fr', _('French')),
    ('fy', _('Frisian')),
    ('gl', _('Galician')),
    ('ka', _('Georgian')),
    ('de', _('German')),
    ('el', _('Greek')),
    ('gu', _('Gujarati')),
    ('ht', _('Haitian Creole')),
    ('ha', _('Hausa')),
    ('he', _('Hebrew')),
    ('hi', _('Hindi')),
    ('hmn', _('Hmong')),
    ('hu', _('Hungarian')),
    ('is', _('Icelandic')),
    ('ig', _('Igbo')),
    ('id', _('Indonesian')),
    ('ga', _('Irish')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('jv', _('Javanese')),
    ('kn', _('Kannada')),
    ('kk', _('Kazakh')),
    ('km', _('Khmer')),
    ('rw', _('Kinyarwanda')),
    ('ko', _('Korean')),
    ('ku', _('Kurdish')),
    ('ky', _('Kyrgyz')),
    ('lo', _('Lao')),
    ('la', _('Latin')),
    ('lv', _('Latvian')),
    ('lt', _('Lithuanian')),
    ('lb', _('Luxembourgish')),
    ('mk', _('Macedonian')),
    ('mg', _('Malagasy')),
    ('ms', _('Malay')),
    ('ml', _('Malayalam')),
    ('mt', _('Maltese')),
    ('mi', _('Maori')),
    ('mr', _('Marathi')),
    ('mn', _('Mongolian')),
    ('my', _('Myanmar (Burmese)')),
    ('ne', _('Nepali')),
    ('no', _('Norwegian')),
    ('ny', _('Nyanja (Chichewa)')),
    ('or', _('Odia (Oriya)')),
    ('ps', _('Pashto')),
    ('fa', _('Persian')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('pa', _('Punjabi')),
    ('ro', _('Romanian')),
    ('ru', _('Russian')),
    ('sm', _('Samoan')),
    ('gd', _('Scots Gaelic')),
    ('sr', _('Serbian')),
    ('st', _('Sesotho')),
    ('sn', _('Shona')),
    ('sd', _('Sindhi')),
    ('si', _('Sinhala')),
    ('sk', _('Slovak')),
    ('sl', _('Slovenian')),
    ('so', _('Somali')),
    ('es', _('Spanish')),
    ('su', _('Sundanese')),
    ('sw', _('Swahili')),
    ('sv', _('Swedish')),
    ('tl', _('Tagalog (Filipino)')),
    ('tg', _('Tajik')),
    ('ta', _('Tamil')),
    ('tt', _('Tatar')),
    ('te', _('Telugu')),
    ('th', _('Thai')),
    ('tr', _('Turkish')),
    ('tk', _('Turkmen')),
    ('uk', _('Ukrainian')),
    ('ur', _('Urdu')),
    ('ug', _('Uyghur')),
    ('uz', _('Uzbek')),
    ('vi', _('Vietnamese')),
    ('cy', _('Welsh')),
    ('xh', _('Xhosa')),
    ('yi', _('Yiddish')),
    ('yo', _('Yoruba')),
    ('zu', _('Zulu')),
]

class TranslationForm(forms.Form):
    """
    Form for translating input text into a selected target language.
    """
    text = forms.CharField(
        label=_("Text to Translate"),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Enter text to translate'),
            'rows': 4,
        })
    )
    target_lang = forms.ChoiceField(
        label=_("Target Language"),
        choices=LANG_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username', 'email']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Username or Email')
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password')
        })
    )



class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user preferences (Profile), such as the preferred target language
    and favorite phrases.
    """
    class Meta:
        model = Profile
        fields = ("preferred_target_language", "favorite_phrases")
        labels = {
            "preferred_target_language": _("Preferred Target Language"),
            "favorite_phrases": _("Favorite Phrases"),
        }
        widgets = {
            "preferred_target_language": forms.Select(attrs={"class": "form-control"}),
            "favorite_phrases": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": _("Enter your favorite phrases, one per line"),
            }),
        }
