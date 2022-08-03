LINK = 'https://www.zillow.com/search/GetSearchPageState.htm?'

PARAMS = {
    'searchQueryState': {
        "pagination": {
            'currentPage': 1,
        },
        "usersSearchTerm": "99501",
        "mapBounds": {
                "west": "",
                "east": "",
                "south": "",
                "north": "",
        },
        # "regionSelection": [{"regionId": 100220, "regionType": 7}],
        "isListVisible": True,
        "mapZoom": 11
    },
    'wants': {"cat1": ["listResults"]},
    'requestId': 2
}