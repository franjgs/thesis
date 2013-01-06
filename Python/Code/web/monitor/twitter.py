from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

from web import config

def get_auth():
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    return auth

class Listener(StreamListener):
    
    def __init__(self, n):
        self.n = n
        self.counter = 0
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
            if type(data) == dict:
                if 'delete' not in data.keys() and data.get('lang') == 'en':
                    self.buffer.append(data)
                    self.counter = self.counter + 1
            if self.counter >= self.n:
                return False
            return True
    
    def on_error(self, status):
        print "Error in " + str(self) + " => " + status
    
    def on_timeout(self):
        return False
