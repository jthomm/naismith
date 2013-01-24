import requests
import gzip
import simplejson as json


def replace_out_of_range(text):
    return u''.join(c if ord(c) in range(128) else ' ' for c in text)


def json_datetime_default(obj):
    try:
        return obj.isoformat()
    except AttributeError:
        return obj


class FetchRawException(Exception):
    """There was an ambiguous exception that occurred while handling 
    your request."""


class ResourceABC(object):

    def __init__(self, resource_id):
        self.resource_id = resource_id

    def load(self):
        try:
            return self.open_scraped()
        except IOError:
            try:
                raw = self.open_raw()
            except IOError:
                try:
                    raw = self.fetch_raw()
                except:
                    # TODO: differentiate between connection timeouts and
                    # bad URLs...
                    raise FetchRawException()
                else:
                    self.save_raw(raw)
            scraped = self.scrape(raw)
            self.save_scraped(scraped)
            return scraped

    def fetch_raw(self):
        """Required: implement `.url`
        """
        return requests.get(self.url).text

    def open_raw(self):
        """Required: implement `.raw_file_path`
        """
        return gzip.open(self.raw_file_path, 'rb').read()

    def save_raw(self, raw):
        with gzip.open(self.raw_file_path, 'wb') as f:
            f.write(replace_out_of_range(raw))

    def open_scraped(self):
        """Required: implement `.scraped_file_path`
        """
        encoded = gzip.open(self.scraped_file_path, 'rb').read()
        return self.decode(encoded)

    def save_scraped(self, scraped):
        encoded = self.encode(scraped)
        with gzip.open(self.scraped_file_path, 'wb') as f:
            f.write(replace_out_of_range(encoded))

    def encode(self, scraped):
        """Optional: implement your own encode/decode protocol
        """
        return json.dumps(scraped, default=json_datetime_default, indent=2)

    def decode(self, encoded):
        return json.loads(encoded)
