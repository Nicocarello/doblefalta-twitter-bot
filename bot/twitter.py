import tweepy
from bot.config import TWITTER_CONFIG

class TwitterClient:
    def __init__(self):
        # Para API v2
        self.client = tweepy.Client(
            consumer_key=TWITTER_CONFIG["consumer_key"],
            consumer_secret=TWITTER_CONFIG["consumer_secret"],
            access_token=TWITTER_CONFIG["access_token"],
            access_token_secret=TWITTER_CONFIG["access_token_secret"]
        )

    def publicar_tweet(self, texto, in_reply_to_tweet_id=None):
        """Publica un tweet en la cuenta configurada. Soporta hilos."""
        if not texto:
            return None
        
        try:
            if in_reply_to_tweet_id:
                response = self.client.create_tweet(text=texto, in_reply_to_tweet_id=in_reply_to_tweet_id)
            else:
                response = self.client.create_tweet(text=texto)
            print(f"✅ Tweet publicado: {response.data['id']}")
            return response.data['id']
        except Exception as e:
            print(f"❌ Error al publicar tweet: {e}")
            return None

_cliente = None

def publicar_tweet(texto, in_reply_to_tweet_id=None):
    global _cliente
    if _cliente is None:
        _cliente = TwitterClient()
    return _cliente.publicar_tweet(texto, in_reply_to_tweet_id)
