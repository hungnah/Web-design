def user_language_context(request):
    """
    Context processor to set the appropriate language for menu display
    based on user's nationality
    """
    if request.user.is_authenticated:
        # Set language based on user's nationality
        if request.user.nationality == 'japanese':
            return {
                'user_language': 'ja',
                'is_japanese_user': True,
                'is_vietnamese_user': False
            }
        elif request.user.nationality == 'vietnamese':
            return {
                'user_language': 'vi',
                'is_japanese_user': False,
                'is_vietnamese_user': True
            }
    
    # Default to Vietnamese for unauthenticated users
    return {
        'user_language': 'vi',
        'is_japanese_user': False,
        'is_vietnamese_user': True
    }
