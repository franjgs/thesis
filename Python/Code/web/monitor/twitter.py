from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

from web import config
from web import settings

def get_auth():
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    return auth

class Listener(StreamListener):
    
    def __init__(self, n):
        self.n = n
        self.msg_count = 0
        self.buffer = list()
        super(Listener, self).__init__()
    
    def on_data(self, data):
        try:
            true = True; false = False; null = None;
            data = eval(data)
        except Exception as e:
            print "Exception: " + e.message + " => " + data
            return False
        else:
            if self.msg_count < settings.MAX_TWEETS_MSG_COUNT:
                self.msg_count = self.msg_count + 1
                if len(self.buffer) >= self.n:
                    return False
                if type(data) == dict:
                    if 'delete' not in data.keys():
                        if data.get('user'):
                            if data.get('user').get('lang') == 'en':
                                self.buffer.append(data)
                        return True
                    else:
                        return True
            else:
                return False
    
    def on_error(self, status):
        print "Error in " + str(self) + " => " + str(status)
        return False
    
    def on_timeout(self):
        return False
