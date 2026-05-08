import tweepy
from bot.config import TWITTER_CONFIG

class TwitterClient:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(
            TWITTER_CONFIG["consumer_key"],
            TWITTER_CONFIG["consumer_secret"]
        )
        self.auth.set_access_token(
            TWITTER_CONFIG["access_token"],
            TWITTER_CONFIG["access_token_secret"]
        )
        self.api = tweepy.API(self.auth)
        # Para API v2
        self.client = tweepy.Client(
            consumer_key=TWITTER_CONFIG["consumer_key"],
            consumer_secret=TWITTER_CONFIG["consumer_secret"],
            access_token=TWITTER_CONFIG["access_token"],
            access_token_secret=TWITTER_CONFIG["access_token_secret"]
        )

    def publicar_tweet(self, texto):
        """Publica un tweet en la cuenta configurada."""
        if not texto:
            return
        
        try:
            # Intentar con v2 primero
            response = self.client.create_tweet(text=texto)
            print(f"✅ Tweet publicado: {response.data['id']}")
            return response.data['id']
        except Exception as e:
            print(f"❌ Error al publicar tweet: {e}")
            return None
