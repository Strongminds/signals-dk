from enum import Enum

class TranslationKey(Enum):
    email_title_prefix = 'Uw melding'
    email_body_prefix = 'Bedankt voor uw melding'
    email_template_body_help_text = 'Het is mogelijk om Markdown en template variabelen te gebruiken'

translations = {
    'en': {
        TranslationKey.email_title_prefix.value: 'Your message',
        TranslationKey.email_body_prefix.value: 'Thank you for your message!',
        TranslationKey.email_template_body_help_text.value: 'It is possible to use Markdown and template variables',
    },
    'da': {
        TranslationKey.email_title_prefix.value: 'Din besked',
        TranslationKey.email_body_prefix.value: 'Tak for din besked!',
        TranslationKey.email_template_body_help_text.value: 'Det er muligt at bruge Markdown og skabelonvariabler',
    }
}

def translate(key: TranslationKey, lang='da'):
    return translations.get(lang, {}).get(key.value, key.value)
