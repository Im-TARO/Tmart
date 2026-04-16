import csv
import random
from datetime import datetime, timedelta

OUTPUT_FILE = "customers.csv"
NUM_CUSTOMERS = 300

# -------------------------
# REAL CITY / STATE / ZIP COMBINATIONS
# -------------------------

locations = [
    ("Raleigh", "NC", "27601", "Wake"),
    ("Raleigh", "NC", "27604", "Wake"),
    ("Raleigh", "NC", "27606", "Wake"),
    ("Raleigh", "NC", "27607", "Wake"),
    ("Raleigh", "NC", "27612", "Wake"),
    ("Raleigh", "NC", "27614", "Wake"),
    ("Raleigh", "NC", "27615", "Wake"),
    ("Raleigh", "NC", "27616", "Wake"),
    ("Apex", "NC", "27502", "Wake"),
    ("Fuquay-Varina", "NC", "27526", "Wake"),
    ("Lillington", "NC", "27546", "Harnett"),
    ("Dunn", "NC", "28334", "Harnett"),
    ("Angier", "NC", "27501", "Harnett"),
    ("Erwin", "NC", "28339", "Harnett"),
    ("Broadway", "NC", "27505", "Harnett"),
    ("Cary", "NC", "27511", "Wake"),
    ("Cary", "NC", "27513", "Wake"),
    ("Clayton", "NC", "27520", "Johnston"),
    ("Sanford", "NC", "27330", "Lee"),
    ("Durham", "NC", "27701", "Durham"),
    ("Durham", "NC", "27704", "Durham"),
    ("Holly Springs", "NC", "27540", "Wake"),
    ("Garner", "NC", "27529", "Wake"),
    ("Morrisville", "NC", "27560", "Wake")

]

# -------------------------
# NAMES
# -------------------------

first_names = [
    "James","Mary","John","Patricia","Robert","Jennifer","Michael","Florence",
    "William","Elizabeth","David","Barbara","Richard","Susan","Joseph","Jessica",
    "Thomas","Sarah","Charles","Karen","Christopher","Nancy","Daniel","Lisa",
    "Jason","Matthew","Andrew","Stephanie","Liam","Charlotte","Luna","Randy"
]

last_names = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
    "Rodriguez","Martinez","Hernandez","Lopez","White","Allen","Anderson",
    "Hill","Baker","Lee","Martin","Wilson","Thomas","Green","Taylor","Moore",
    "Clark","Adams","Carter","Edwards","Cooper","Kelly","James","Bell"
]

# -------------------------
# STREET NAMES (FAKE)
# -------------------------

street_names = [
    "Main St","Oak St","Pine St","Maple Ave","Cedar Ln",
    "Elm St","Washington St", "Lincoln Ave", "Lakeview Dr",
    "Dogwood St","Cardinal Ave","Church St", "Laurel Rd",
    "Magnolia Rd", "Walnut Ave", "Birch St", "Spruce Ln",
    "State St", "Hummingbird Dr", "Shady Ln", "Circle Dr",
    "Jefferson St", "Park St", "Chestnut St", "Central Ave"
]

# -------------------------
# FAKE EMAIL DOMAINS
# -------------------------

fake_domains = [
    "offlinemail.com",
    "nachomail.net",
    "fakeinbox.net",
    "fakemail.com",
    "notinbox.net"
]

# -------------------------
# HELPERS
# -------------------------

def random_phone():
    return f"{random.randint(200,499)}-555-{random.randint(1000,9999)}"


def random_address():
    return f"{random.randint(100,99999)} {random.choice(street_names)}"


def random_email(first, last):
    num = random.randint(1, 999)
    domain = random.choice(fake_domains)
    username = random.choice([last, first, first+(last[:1]), (first[:1])+last, first+last, last+first])
    return f"{username.lower()}{num}@{domain}"


def random_dob():
    start_date = datetime(1940, 1, 1)
    end_date = datetime(2007, 12, 31)

    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    dob = start_date + timedelta(days=random_days)
    return dob.strftime("%Y-%m-%d")


# -------------------------
# GENERATE DATA
# -------------------------

rows = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    first = random.choice(first_names)
    last = random.choice(last_names)

    city, state, zipcode, county = random.choice(locations)

    address = random_address()
    phone = random_phone()
    email = random_email(first, last)
    dob = random_dob()

    is_active = random.choice([0, 1, 1, 1])  # ~75% active

    loyalty_member = random.choice([0, 1, 1])  # ~66% active

    date_created = datetime.now() - timedelta(days=random.randint(0, 3650))

    rows.append([
        customer_id,
        first,
        last,
        phone,
        email,
        address,
        city,
        state,
        zipcode,
        county,
        dob,
        is_active,
        loyalty_member,
        date_created
    ])

# -------------------------
# WRITE CSV
# -------------------------

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "customer_id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "address",
        "city",
        "state",
        "zipcode",
        "county",
        "date_of_birth",
        "is_active",
        "loyalty_member",
        "date_created"
    ])

    writer.writerows(rows)

print(f"{NUM_CUSTOMERS} customers written to {OUTPUT_FILE}")