# Download Twitter friends or followers

Using the Twitter API, this Python3 script will output a CSV file for friends (who a user is following), followers (who follows the user), or both.

This repo is based on [code](https://github.com/brienna/twitter-helper-scripts) made in a tutorial by Brienna Herold: [How to Download Twitter Followers or Friends for Free](https://towardsdatascience.com/how-to-download-twitter-friends-or-followers-for-free-b9d5ac23812)

Requirements: Python 3, pip3, [Tweepy](https://docs.tweepy.org/) and [Pandas](https://pandas.pydata.org/) Python libraries, [Twitter API credentials](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)

This has been tested with Python 3.10.7, Tweepy versions 4.4.0 and 4.12.1, and Pandas versions 1.3.4 and 1.5.1.


## Instructions
1. Clone this repository
2. Install dependencies Tweepy and Pandas:
```
pip3 install -r requirements.txt
```
3. Execute the Python script with a username and optional type. Type can be `followers`, `friends`, or `both`, but defaults to `followers`. Either shortened or spelled out arguments are acceptable, like so:

```
python3 download_friends_or_followers.py -u username -t [type]

python3 download_friends_or_followers.py --user username --type [type]
```


Please be aware of the Twitter API [rate limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits). This script fails if limits are exceeded.

## License
[Original code](https://github.com/brienna/twitter-helper-scripts) is by [Brienna Herold](https://github.com/brienna). All changes by Michael Weinberg are dedicated to the public domain in accordance with [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).