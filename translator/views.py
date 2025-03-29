from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from googletrans import Translator, LANGUAGES
from .forms import TranslationForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Translation, Profile

@login_required
def home(request):
    """
    View for the translation homepage.
    Processes translation requests and displays the translation result.
    If the user is authenticated, the translation record is linked to the user.
    """
    # Retrieve any stored translation result from the session (set after a POST)
    translated_text = request.session.pop('result', None)

    if request.method == 'POST':
        form = TranslationForm(request.POST)
        if form.is_valid():
            try:
                # Initialize the translator instance
                translator = Translator()
                text = form.cleaned_data['text']
                target_lang = form.cleaned_data['target_lang']
                # Detect the source language and translate the text
                detection = translator.detect(text)
                translated = translator.translate(text, dest=target_lang)

                # Save the translation to the database.
                # User is authenticated due to login_required
                Translation.objects.create(
                    user=request.user,
                    original_text=text,
                    translated_text=translated.text,
                    source_lang=detection.lang,
                    target_lang=target_lang
                )

                # Store the result in the session to display after redirecting
                request.session['result'] = {
                    'original': text,
                    'translated': translated.text,
                    'src_lang': LANGUAGES.get(detection.lang, 'Unknown'),
                    'tgt_lang': LANGUAGES.get(target_lang, 'Unknown')
                }
                messages.success(request, _("Translation successful!"))
                
                # Redirect after processing POST to follow the POST-Redirect-GET Pattern.
                return redirect('home')
            except Exception as e:
                messages.error(request, _("Translation error: %(error)s") % {'error': str(e)})
                # Redirect to clear POST data and avoid form resubmission
                return redirect('home')
    else:
        # Pre-fill target_lang from user's profile
        form = TranslationForm(initial={'target_lang': request.user.profile.preferred_target_language})

    return render(request, 'home.html', {
        'form': form,
        'result': translated_text,
        'languages': LANGUAGES,
    })


def register(request):
    """
    View for user registration.
    Uses UserRegistrationForm (which extends Django's built-in UserCreationForm)
    to register a new user, logs them in, and redirects to the home page.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            
            # Create empty profile for new user
            Profile.objects.create(user=user)
            messages.success(request, f"Your account has been created! You can now log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
    

@login_required
def profile(request):
    # Get or create profile if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Count translations associated with the user via the related name 'translations'
    translation_count = request.user.translations.count()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'profile': profile,
        'translation_count': translation_count,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'translator/profile.html', context)


@login_required
def translation_history(request):
    """
    View to display the logged-in user's translation history.
    Retrieves all Translation records associated with the user,
    ordered by the most recent first.
    """
    history = request.user.translations.order_by('-created_at')
    return render(request, 'translator/translation_history.html', {'history': history})


@login_required
def delete_translation(request, translation_id):
    translation = get_object_or_404(Translation, id=translation_id, user=request.user)

    if request.method == 'POST':
        translation.delete()
        messages.success(request, _("Translation deleted successfully."))
        return redirect('translation_history')
        
    return render(request, 'translator/translation_confirm_delete.html', {'translation': translation})
