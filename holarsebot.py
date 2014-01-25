#!/home/javafant/scripts/holarsebot/venv/bin/python -u
from rssbot import RSSBot
import re
import configparser

holarse_feed = 'http://www.holarse-linuxgaming.de/rss.xml'
tags = ['#holarse', '#linuxgaming', '#videogames']

config = configparser.ConfigParser()
config.read('config')

pod = config['Holarse']['pod']
user = config['Holarse']['user']
password = config['Holarse']['password']


class HolarseBot(RSSBot):
    def html_to_markdown(self, text):
        # remove media at the end

        m = re.match(r'(.*?)<fieldset', text, flags=re.DOTALL)
        if m:
            text = m.group(1)

        return super(HolarseBot, self).html_to_markdown(text)

if __name__ == '__main__':
    holarsebot = HolarseBot(holarse_feed, tags, pod, user, password)
    holarsebot.start()
