"""
Context Processors for User Profile App
Provides additional context data to all templates
"""

def menu_language(request):
    """
    Provides menu language context based on user nationality
    """
    if request.user.is_authenticated:
        if request.user.nationality == 'japanese':
            return {
                'menu_lang': 'ja',
                'is_japanese': True,
                'is_vietnamese': False
            }
        else:
            return {
                'menu_lang': 'vi',
                'is_japanese': False,
                'is_vietnamese': True
            }
    else:
        return {
            'menu_lang': 'en',
            'is_japanese': False,
            'is_vietnamese': False
        }
