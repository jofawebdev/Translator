from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Define all language choices here to match forms.py
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

class Translation(models.Model):
    """
    Model to store translation records. Each translation can be linked to a user
    (if the translation was performed by an authenticated user) and marked as a favorite.
    """
    # Optional association to a user. If left blank, the translation can be considered anonymous.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='translations',
        null=True,
        blank=True,
        help_text=_("User who performed the translation. Leave empty for anonymous translations.")
    )
    original_text = models.TextField(verbose_name=_("Original Text"))
    translated_text = models.TextField(verbose_name=_("Translated Text"))
    source_lang = models.CharField(max_length=10, verbose_name=_("Source Language"))
    target_lang = models.CharField(max_length=10, verbose_name=_("Target Language"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    # Allows the user to mark a translation as favorite
    is_favorite = models.BooleanField(
        default=False,
        verbose_name=_("Favorite"),
        help_text=_("Mark this translation as a favorite.")
    )

    def __str__(self):
        return f"{self.source_lang} to {self.target_lang}"


class Profile(models.Model):
    """
    Profile model that extends the built-in User model with additional preferences.
    Each Profile is linked via a one-to-one relationship with a User.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    preferred_target_language = models.CharField(
        max_length=10,
        choices=LANG_CHOICES,
        default='en',
        verbose_name=_("Preferred Target Language")
    )
    favorite_phrases = models.TextField(
        blank=True,
        default='',
        verbose_name=_("Favorite Phrases"),
        help_text=_("Enter favorite phrases separated by newlines.")
    )

    def __str__(self):
        return f"{self.user.username} Profile"