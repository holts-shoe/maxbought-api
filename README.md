# maxbought-api
Python API wrapper and documentation for MaxSold's hidden APIs. MaxSold is a Series-B startup solving the challenge of selling large amounts of personal belongings. What used to be a slow and unenjoyable experience is now easy and fun, for all parties involved.
This package will you give you the power to:
1) Autogenerate API credentials
2) Get auctions data
3) Get items data
- Partially nspired by this xkcd comic

![image](https://user-images.githubusercontent.com/21085160/162097116-0f121895-ef78-47f1-8feb-51a0205ed754.png)

# 🚀 Quick Start
``` python
#create an instance of the API Class
maxsold = API()
#generate tokens
maxsold.generate_tokens()

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
```
# 🤝 Discussion
Currently, only live data is supported by the wrapper - however historical data is available via the APIs and will be integrated into the wrapper in future. 
