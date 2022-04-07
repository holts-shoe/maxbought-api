import requests
import time as notdatetime
import datetime
import matplotlib.pyplot as plt
# uses Algolia for API

class API():
    def __init__(self):
        self.base_url = 'https://bwhj2cu1lu-dsn.algolia.net/1/indexes/hpitem/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.11.0)%3B%20Browser'
        self.api_key = None
        self.app_id = None
    def generate_tokens(self):
        url = 'https://www.maxsold.com/main.14c22a1d14637769c939.js'
        response = requests.get(url)
        tokens = {'algoliaApplicationId':'', 'algoliaSearchAPIKey':''}
        for token in tokens.keys():
            start = response.text.find(f'{token}:"') + len(f'{token}:"')
            end = start + response.text[start:].find('"')
            tokens[token] = response.text[start:end]
        self.api_key = tokens['algoliaSearchAPIKey']
        self.app_id = tokens['algoliaApplicationId']
    def set_tokens_manually(self, api_key, app_id):
        self.api_key = api_key
        self.app_id = app_id
        if self.test_search().status_code == 200:
            pass
        else:
            self.api_key = None
            self.app_id = None
            raise Exception(f"Either {self.api_key} api_key or {self.app_id} app_id don't work")
    def test_search(self): #test to see if tokens are valid. search methods require api-key and application-id tokens, get methods do not
        headers = {
            'User-Agent': "Erik's API wrapper",
            'x-algolia-api-key': self.api_key,
            'x-algolia-application-id': self.app_id,
        }
        data = f'{{}}'
        response = requests.post('https://bwhj2cu1lu-dsn.algolia.net/1/indexes/hpitem/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.11.0)%3B%20Browser', headers=headers, data=data)
        return response

    def search(self, search_type='auctions', query='', location='', country=False, page=0): #search for some listings based on query and location, leave fields blank to get all auctions
        if search_type.lower() not in ['auctions','items']:
            raise Exception("Search by 'auctions' (default) or 'items'")
        search_type = ['hpauction', 'hpitem'][['auctions','items'].index(search_type.lower())]
        headers = {
            'User-Agent': "Erik's API wrapper",
            'x-algolia-api-key': self.api_key,
            'x-algolia-application-id': self.app_id,
        }
        start_date = int(notdatetime.time()) # basically the time range of auctions you want to see, not super useful so not a function parameter
        end_date = start_date - 900 # 900 seconds because that's how it's in production
        query = query.replace('"',r'\"') #escape quotations
        country_string = ''
        if country:
            country_string = ' AND country:\\"{country}\\"'
        data = f'{{"query":"","filters":"start_date <= {start_date} AND end_date > {end_date}{country_string}","facetFilters":["auction_phase:-cancelledAuction"],"hitsPerPage":100,"page":{page},"aroundLatLng":"{location}","aroundLatLngViaIP":false,"aroundRadius":100000}}'
        url = f'https://bwhj2cu1lu-dsn.algolia.net/1/indexes/{search_type}/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.11.0)%3B%20Browser'
        response = requests.post(url, headers=headers, data=data)
        return response.json()
    def get_auction_items(self, auction_id, page_id=False): #get auction items for a given auction
        headers = {
            'User-Agent': "Erik's API wrapper",
        }
        if not page_id:
            page_id = 1
        data = {
            'auction_id': f'{auction_id}',
            'filters[page]': f'{page_id}',
            'item_type': 'itemlist',
            'lotnum': '0',
            'close_groups': '',
            'show_closed': 'closed',
            'perpetual': ''
        }
        response = requests.post('https://maxsold.maxsold.com/api/getitems', headers=headers, data=data)
        return response.json()
    def get_item(self, item_id): #get details from one item for a given listing
        headers = {
            'User-Agent': "Erik's API wrapper",
        }
        data = {
            'item_id': item_id
        }
        response = requests.post('https://maxsold.maxsold.com/api/itemdata', headers=headers, data=data)
        return response.json()
    def get_bidding(self, item_data):
        title = item_data['title']
        description = item_data['item_description']
        starting_bid = item_data['starting_bid']
        current_bid = item_data['current_bid']
        minimum_bid = item_data['minimum_bid']
        bidding = item_data['bid_history']
        bidding_data = {}
        for bid in reversed(bidding):
            time = datetime.datetime.fromtimestamp(int(bid['time_of_bid_unix']))
            price = bid['bid']
            bidding_data[time] = price
        plt.plot(bidding_data.keys(), bidding_data.values(), linewidth=3)
        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel('$ Price')

        number_of_bids = len(bidding)
        bidding_time_days = (int(notdatetime.time()) - int(bidding[-1]['time_of_bid_unix'])) / 3600 / 24
        bids_per_day = number_of_bids / bidding_time_days
        return {'title': title, 'description': description, 'starting_bid': starting_bid, 'current_bid': current_bid, 'minimum_bid': minimum_bid, 'bidding_data': bidding_data, 
        'bidding_plt': plt, 'number_of_bids': number_of_bids, 'bidding_time_days': bidding_time_days, 'bids_per_day': bids_per_day}




#create an instance of the API Class
maxsold = API()
#generate tokens, can also be set manually with: maxsold.set_tokens()
maxsold.generate_tokens() #print(maxsold.api_key, maxsold.app_id)
#search for auctions, not using any arguments (search filtuers) will return the most results
auctions = maxsold.search()
#let's narrow these results down for demonstration. we'll search for Estate, put our longitude/latitude string, and look at the first page (pages use 0 indexing)
auctions = maxsold.search(query='Estate', location='42.3144556, -71.0403236', country=False, page=0)
#now lets search for items, the same parameters apply for searching for a list of auctions, or a list of items. we set search_type to 'items', from the default 'auctions'
items = maxsold.search(search_type='items', query='Car')
#let's get 1) the id of the first auction, 2) the id of the first item from the list of items
auction_id = auctions['hits'][0]['am_auction_id']
item_id = items['hits'][0]['objectID']
#we can also get a list of items from a specific auction (auction items)
auction_items = maxsold.get_auction_items(auction_id)
#let's get the first item id from that auction
auction_item_id = auction_items['items'][0]['id']
#let's get the item data
item_data = maxsold.get_item(auction_item_id)
#let's get item data specific to bidding
bidding_data = maxsold.get_bidding(item_data)
print('done')