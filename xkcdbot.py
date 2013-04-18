#!/home/javafant/scripts/xkcdbot/venv/bin/python -u
from rssbot import RSSBot
import configparser

xkcd_feed = 'http://xkcd.com/rss.xml'

config = configparser.ConfigParser()
config.read('config')

pod = config['XKCD']['pod']
user = config['XKCD']['user']
password = config['XKCD']['password']


if __name__ == '__main__':
    xkcdbot = RSSBot(xkcd_feed, ['#xkcd', '#comic'], pod, user, password)
    xkcdbot.start()
