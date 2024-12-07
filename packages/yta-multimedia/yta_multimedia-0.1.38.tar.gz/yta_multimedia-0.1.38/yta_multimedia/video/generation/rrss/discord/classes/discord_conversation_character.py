class DiscordConversationCharacter:
    def __init__(self, username: str, avatar_url: str):
        if not username:
            raise Exception('No "username" provided.')
        
        if not avatar_url:
            raise Exception('No "avatar_url" provided.')
        
        # TODO: Check if 'avatar_url' is valid

        # TODO: Maybe if they don't provide this information we
        # could auto-generate it
        self.username = username
        self.avatar_url = avatar_url