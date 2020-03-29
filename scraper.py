from craigslist import CraigslistHousing
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
from util import post_listing_to_slack, find_points_of_interest
from slackclient import SlackClient
import time
import settings
import google_sheets

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    area = Column(String)
    bart_stop = Column(String)
    should_include = Column(Boolean)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
num_rows_deleted = session.query(Listing).delete()
session.commit()

def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    #  get the google sheet object
    sheet = google_sheets.open_sheet()

    counter = 0

    cl_h = CraigslistHousing(site=settings.CRAIGSLIST_SITE, area=area, category=settings.CRAIGSLIST_HOUSING_SECTION,
                             filters=settings.FILTERS)


    results = []
    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=1000)

    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            print('exception')
            continue

        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()
        # Don't store the listing if it already exists.

        if listing is None:
            # if result["where"] is None:
            #     # If there is no string identifying which neighborhood the result is from, skip it.
            #     continue

            lat = 0
            lon = 0
            if result["geotag"] is not None:
                # Assign the coordinates.
                lat = result["geotag"][0]
                lon = result["geotag"][1]

                # Annotate the result with information about the area it's in and points of interest near it.
                geo_data = find_points_of_interest(result["geotag"], result["where"])
                result.update(geo_data)
            else:
                result["area"] = ""
                result["google_stop"] = ""
                result["google_dist"] = ""
                result["fb_stop"] = ""
                result["fb_dist"] = ""
                result["fb_walktime"] = "Unknown"
                result["google_walktime"] = "Unknown"
                result["adi_drivetime"] = "Unknown"
                result["address"] = "Unknown"

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass


            #include result if within our area or if there is no location infroamtion
            should_include = False
            if len(result["area"]) > 0 or lat == 0:
                should_include = True

            # Create the listing object.
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                lat=lat,
                lon=lon,
                name=result["name"],
                price=price,
                location=result["where"],
                cl_id=result["id"],
                area=result["area"],
                # bart_stop=result["bart"],
                # min_bedrooms=settings.MIN_BEDROOMS,
                # min_bathrooms=settings.MIN_BATHROOMS,
                should_include = should_include,
                # bedrooms = result['bedrooms'],
                # bathrooms = result['bathrooms'],
                # sq_ft = result['sq_ft'],
                # amenities = result['amenities'],
                # available_date = result['available_date'],

            )

            result_to_return = {
                'link': result["url"],
                'created':parse(result["datetime"]),
                'lat':lat,
                'lon':lon,
                'name':result["name"],
                'price':price,
                'location':result["where"],
                'cl_id':result["id"],
                'tagged_location':result["area"],
                # 'bart_stop':result["bart"],
                # 'bart_dist':result["bart_dist"],
                # 'min_bedrooms':settings.MIN_BEDROOMS,
                # 'min_bathrooms':settings.MIN_BATHROOMS,
                'should_include': should_include,
                'available_date': "-",
                'bedrooms': 0,
                'bedrooms': 0,
                'bathrooms': 0,
                'amenities': "-",
                'sq_ft': 0,
                'google_stop': result['google_stop'],
                'google_dist': result['google_dist'],
                'fb_stop': result['fb_stop'],
                'fb_dist': result['fb_dist'],
                'fb_walktime': result['fb_walktime'],
                'google_walktime': result['google_walktime'],
                'adi_drivetime': result['adi_drivetime'],
                'address': result['address']
            }

            print("Adding %s..."%result['name'])
            google_sheets.add_new_record(sheet, result_to_return)

            # print result_to_return

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()

            # Return the result if it's near a bart station, or if it is in an area we defined.
            # if len(result["bart"]) > 0 or len(result["area"]) > 0:
            #     results.append(result)
            if should_include:
                results.append(result_to_return)

        else:
            print("Skipping %s..."%result['name'])

        # counter = counter + 1
        # # get new credentials
        # if counter % 50 == 0:
        #     sheet = google_sheets.open_sheet()

    return results

def do_scrape():
    """
    Runs the craigslist scraper, and posts data to slack.
    """

    # Create a slack client.
    # sc = SlackClient(settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    all_results = []
    for area in settings.AREAS:
        all_results += scrape_area(area)

    print("{}: Got {} results".format(time.ctime(), len(all_results)))
