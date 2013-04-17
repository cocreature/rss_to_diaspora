import re
from threading import Timer

import feedparser
import diaspy


class RSSBot(object):
    def get_feed(self, feed_url):
        return feedparser.parse(feed_url)

    def rss_to_markdown(self, item):
        title = "## [{0}]({1})\n".format(item.title, item.link)
        description = "{0}\n".format(self.html_to_markdown(item.description))
        tags = '\n#holarse #linuxgames'
        markdown = title + description + tags
        return markdown

    def html_to_markdown(self, text):
        """ Should be overwritten and customized for your rss feed.
        """
        # replace paragraphs
        text = re.sub(r'<p>(.*?)</p>',
                      r'\1\n\n',
                      text,
                      flags=re.DOTALL)

        # replace links
        text = re.sub(r'<a.*?href="(.*?)">(.*?)</a>',
                      self.replace_links,
                      text)

        # replace linebreaks
        text = re.sub(r'<br ?/?>',
                      r'\n\n',
                      text)

        # replace headings
        text = re.sub(r'<h1>(.*?)</h1>',
                      r'# \1',
                      text)
        text = re.sub(r'<h2>(.*?)</h2>',
                      r'## \1',
                      text)
        text = re.sub(r'<h[3456]>(.*?)</h[3456]>',
                      r'### \1',
                      text)

        # remove additional newlines
        text = text.strip()
        return text

    def post_entry(self, entry):
        print('Try to post entry')
        c = diaspy.client.Client(self.pod_url, self.username, self.password)
        post = self.rss_to_markdown(entry)
        c.post(post)

    def check_for_new_feed_item(self):
        print('Checking for new feeds')
        try:
            feed = self.get_feed(self.feed_url)
        except:
            print('Feed could not be fetched')
            Timer(60.0, self.check_for_new_feed_item).start()
            return
        # Test if there's a new feed item
        try:
            with open(self.file_location, 'r') as f:
                old_id = f.read()
                if feed.entries[0].id != old_id:
                    self.post_entry(feed.entries[0])
                    f.close()
                    with open(self.file_location, 'w') as fw:
                        fw.write(feed.entries[0].id)
        except IOError:
            with open(self.file_location, 'w') as f:
                f.write(feed.entries[0].id)
            self.post_entry(feed.entries[0])
        Timer(60.0, self.check_for_new_feed_item).start()

    def replace_links(self, match_obj):
        if match_obj.group(1)[0] == '/':
            return ("[{0}](http://www.holarse-linuxgaming.de{1})"
                    .format(match_obj.group(2), match_obj.group(1)))
        return "[{0}]({1})".format(match_obj.group(2), match_obj.group(1))

    def start(self):
        self.check_for_new_feed_item()

    def __init__(self,
                 feed_url,
                 pod_url,
                 username,
                 password,
                 file_location='feedid'):
        self.feed_url = feed_url
        self.pod_url = pod_url
        self.username = username
        self.password = password
        self.file_location = file_location
