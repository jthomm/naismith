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


class DataManager(object):

    def load(self, data_id):
        try:
            return self.open_scraped(data_id)
        except IOError:
            try:
                raw = self.open_raw(data_id)
            except IOError:
                try:
                    raw = self.fetch_raw(data_id)
                except:
                    # TODO: differentiate between connection timeouts and 
                    # bad URLs...
                    raise FetchRawException()
                else:
                    self.save_raw(raw, data_id)
            scraped = self.scrape(raw)
            self.save_scraped(scraped, data_id)
            return scraped

    def encode(self, scraped):
        return json.dumps(scraped, default=json_datetime_default)

    def decode(self, encoded):
        return json.loads(encoded)

    def fetch_raw(self, data_id):
        return requests.get(self.url_for(data_id)).text

    def open_raw(self, data_id):
        return gzip.open(self.raw_file_path(data_id), 'rb').read()

    def save_raw(self, raw, data_id):
        with gzip.open(self.raw_file_path(data_id), 'wb') as f:
            #f.write(raw)
            f.write(replace_out_of_range(raw))

    def open_scraped(self, data_id):
        encoded = gzip.open(self.scraped_file_path(data_id), 'rb').read()
        return self.decode(encoded)

    def save_scraped(self, scraped, data_id):
        encoded = self.encode(scraped)
        with gzip.open(self.scraped_file_path(data_id), 'wb') as f:
            f.write(encoded)
