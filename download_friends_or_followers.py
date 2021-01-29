import argparse
import configparser
import pandas as pd
from tweepy import API, Cursor, OAuthHandler, TweepError

class Bot(object):
    '''Saves friends and/or followers of a Twitter handle to CSV file(s).'''

    def __init__(self):
        self.authenticate()
        
    def authenticate(self):
        '''Authenticates Tweepy API.'''
        # Read in authentication keys, tokens and secrets
        configs = configparser.ConfigParser()
        configs.read('./config.ini')
        keys = configs['TWITTER']
        consumer_key = keys['CONSUMER_KEY'] 
        consumer_secret = keys['CONSUMER_SECRET'] 
        access_token = keys['ACCESS_TOKEN']
        access_secret = keys['ACCESS_SECRET'] 

        # Get tweepy.OAuthHandler object that will help authenticate
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        
        # Authenticate and set API 
        self.api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def get_follower_ids(self, screen_name):
        '''Returns follower ids of passed screen_name.'''
        follower_ids = []
        for fid in Cursor(self.api.followers_ids, screen_name=screen_name, count=5000).items():
            follower_ids.append(fid)
        return follower_ids

    def get_friend_ids(self, screen_name):
        '''Returns friend ids of passed screen_name.'''
        friend_ids = []
        for fid in Cursor(self.api.friends_ids, screen_name=screen_name, count=5000).items():
            friend_ids.append(fid)
        return friend_ids

    def get_user_info(self, user_ids):
        '''Gets all user info. 
        API.lookup_users has a rate limit of about 100 * 180 = 18K lookups each 15 min window.
        It only accepts 100 user ids at a time.'''
        user_info = []
        for i in range(0, len(user_ids), 100):
            try:
                chunk = user_ids[i:i+100]
                user_info.extend(self.api.lookup_users(user_ids=chunk))
            except:
                import traceback
                traceback.print_exc()
                print('Something went wrong, skipping...')
        return user_info
    
    def download_friends(self, handle):
        '''Downloads friends of passed handle.'''
        filepath = handle + '_friends.csv'
        ids = self.get_friend_ids(handle)
        self.download(ids, filepath)
        
    def download_followers(self, handle):
        '''Downloads followers of passed handle.'''
        filepath = handle + '_followers.csv'
        ids = self.get_follower_ids(handle)
        self.download(ids, filepath)
        
    def download(self, ids, filepath):
        '''Downloads passed users.'''
        data = [x._json for x in self.get_user_info(ids)]
        df = pd.DataFrame(data)
        df = df[['id', 'name', 'screen_name', 'location', 'description', 'url', 
                 'followers_count', 'friends_count', 'created_at', 'verified']]
        df.to_csv(filepath, index=False)
        
    def execute(self, handle, which):
        '''Runs bot.'''
        if which == 'friends':
            self.download_friends(handle)
        elif which == 'followers':
            self.download_followers(handle)
        elif which == 'both':
            self.download_friends(handle)
            self.download_followers(handle)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='Twitter handle for which to download followers and/or friends.', required=True)
    parser.add_argument('-t', '--type', help='Accepts three options: followers, friends, both. Defaults to followers only.', default='followers')
    args = parser.parse_args()

    # Run the bot
    bot = Bot()
    bot.execute(args.user, args.type)






