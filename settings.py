import os

# filters
FILTERS = {
    'min_bathrooms': 1,
    'min_bedrooms': 3
}
## Location preferences

# The Craigslist site you want to search on.
# For instance, https://sfbay.craigslist.org is SF and the Bay Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'sfbay'

# What Craigslist subdirectories to search on.
# For instance, https://sfbay.craigslist.org/eby/ is the East Bay, and https://sfbay.craigslist.org/sfc/ is San Francisco.
# You only need the last three letters of the URLs.
AREAS = ["sfc"]

# A list of neighborhoods and coordinates that you want to look for apartments in.  Any listing that has coordinates
# attached will be checked to see which area it is in.  If there's a match, it will be annotated with the area
# name.  If no match, the neighborhood field, which is a string, will be checked to see if it matches
# anything in NEIGHBORHOODS.
BOXES = {
    "mission": [
        [37.747808, -122.429121],
        [37.772749, -122.407797]
    ]
}

# A list of neighborhood names to look for in the Craigslist neighborhood name field. If a listing doesn't fall into
# one of the boxes you defined, it will be checked to see if the neighborhood name it was listed under matches one
# of these.  This is less accurate than the boxes, because it relies on the owner to set the right neighborhood,
# but it also catches listings that don't have coordinates (many listings are missing this info).
NEIGHBORHOODS = ["berkeley north", "berkeley", "rockridge", "adams point", "oakland lake merritt", "cow hollow", "piedmont", "pac hts", "pacific heights", "lower haight", "inner sunset", "outer sunset", "presidio", "palo alto", "richmond / seacliff", "haight ashbury", "alameda", "twin peaks", "noe valley", "bernal heights", "glen park", "sunset", "mission district", "potrero hill", "dogpatch"]

## Transit preferences

# The farthest you want to live from a transit stop.
MAX_TRANSIT_DIST = 2 # kilometers

# Transit stations you want to check against.  Every coordinate here will be checked against each listing,
# and the closest station name will be added to the result and posted into Slack.
GOOGLE_STOPS = {
    "Van Ness @ Union": [37.798656,-122.424156],
    "Van Ness @ Sacramento": [37.791363,-122.422707],
    "Columbus @ Powell": [37.800591,-122.410721],
    "San Francisco Office": [37.791172,-122.389923],
    "Soma": [37.777119,-122.395134],
    "Civic Center": [37.778316,-122.414398],
    "Stanyan @ Frederick": [37.766594,-122.45295],
    "Haight @ Divisadero": [37.771225,-122.436745],
    "Hayes @ Steiner": [37.775612,-122.432495],
    "24th @ Castro": [37.75124,-122.433762],
    "24th @ Church": [37.751598,-122.427704],
    "30th @ Dolores": [37.742188,-122.424614],
    "18th & Dolores": [37.76125,-122.42585],
    "24th @ Valencia": [37.752033,-122.420387],
    "Park Presido @ Geary": [37.780266,-122.47245],
    "19th @ Kirkham": [37.759975,-122.476974],
    "19th @ Taraval": [37.743191,-122.475822],
    "Glen Park BART": [37.733131,-122.434143],
    "San Francisco Office Pickup": [37.789299,-122.388672],
    "Valencia @ 24th": [37.751945,-122.420769],
    "14th and Market (Late AM Quad, Sweep, & Evening Drop Off)": [37.768764,-122.427574],
    "18th & Castro": [37.760788,-122.434914],
    "201 Toland Street": [37.745743,-122.397133],
    "18th & Dolores": [37.761444,-122.426628],
    "Jackson Playground": [37.765011,-122.399948],
    "Potrero & 18th": [37.761635,-122.407318],
    "Potrero & 23rd": [37.753986,-122.406586],
    "Lombard @ Pierce": [37.799282,-122.439499],
    "Market @ Dolores": [37.768872,-122.427169]
}

FB_STOPS = {
    "SOMA-1": [37.785083,-122.419667],
    "SOMA-2": [37.778306,-122.414389],
    "SOMA-3": [37.778056,-122.397056],
    "SOMA-4": [37.774417,-122.404444],
    "Mission-1": [37.76427,-122.430571],
    "Mission-2": [37.748643,-122.420834],
    "Mission-3": [37.748095,-122.418281],
    "Mission-4": [37.751702,-122.427492],
    "Mission-5": [37.765028,-122.419278],
    "Hayes Valley-1": [37.773118,-122.44628],
    "Hayes Valley-2": [37.777639,-122.42325],
    "Hayes Valley-3": [37.773778,-122.432083],
    "Hayes Valley-4": [37.780352,-122.438784],
    "Hayes Valley-5": [37.784972,-122.424667],
    "Portero-1": [37.765028,-122.399861],
    "Portero-2": [37.761889,-122.41025],
    "Portero-3": [37.755722,-122.409528]
}

## Search type preferences

# The Craigslist section underneath housing that you want to search in.
# For instance, https://sfbay.craigslist.org/search/apa find apartments for rent.
# https://sfbay.craigslist.org/search/sub finds sublets.
# You only need the last 3 letters of the URLs.
CRAIGSLIST_HOUSING_SECTION = 'sub'

## System settings

# How long we should sleep between scrapes of Craigslist.
# Too fast may get rate limited.
# Too slow may miss listings.
SLEEP_INTERVAL = 20 * 60 # 20 minutes

# Which slack channel to post the listings into.
SLACK_CHANNEL = "#housing"

# The token that allows us to connect to slack.
# Should be put in private.py, or set as an environment variable.
SLACK_TOKEN = os.getenv('SLACK_TOKEN', "")

# Any private settings are imported here.

OFFICE_ADDRESS = '1965 Charleston Road Mountain View, CA 94043';

try:
    from private import *
except Exception:
    pass

# Any external private settings are imported from here.
try:
    from config.private import *
except Exception:
    pass