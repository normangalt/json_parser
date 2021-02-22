'''
The module is for retrieving json file from Twitter API.
'''

import requests

def api_file_retriever(appendix: str, user_name: str):
    '''
    Returns a dictionary of a json file from Twitter API
using given user name and resource url ending.

    >>> len(list(api_file_retriever('friends/list.json', '@BarackObama').items()))
    6
    '''
    base_url = 'https://api.twitter.com/'
    access_token = '''AAAAAAAAAAAAAAAAAAAAAJmp\
MwEAAAAAzOMPOTJlHaJF880r\
Ufgj%2BClXFAQ%3Do16zw9su\
1B7UKGYLyM6homsX4WSHP63Y\
ZzsGOarKNcDiRVTw8u'''

    search_headers = {
        'Authorization':'Bearer {}'.format(access_token)
        }

    search_params = {
        'screen_name': user_name,
        }

    search_url = '{0}1.1/{1}'.format(base_url, appendix)

    response = requests.get(search_url, headers=search_headers, params=search_params)

    json_response = response.json()

    return json_response

if __name__ == '__main__':
    import doctest
    doctest.testmod()
