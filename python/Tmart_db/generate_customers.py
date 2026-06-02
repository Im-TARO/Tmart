"""
generate_customers.py
---------------------
Generates a CSV file of synthetic customer records for testing/demo purposes.
All names, addresses, emails, and phone numbers are fabricated.
Locations use real city/state/ZIP combinations in central North Carolina.

Usage
-----
Default (no arguments):
    python generate_customers.py

With optional overrides:
    python generate_customers.py \
        --num-customers 100 \
        --dob-start-year 1960 \
        --created-start 2020-01-01 \
        --created-end   2024-12-31

Arguments
---------
--dob-start-year  INT        First year of the DOB range  (default: 1940)
--created-start   YYYY-MM-DD Earliest possible date_created (default: 10 years ago)
--created-end     YYYY-MM-DD Latest  possible date_created (default: today)
"""

import argparse
import csv
import random
from datetime import datetime, timedelta

# ── Configuration ─────────────────────────────────────────────────────────────

OUTPUT_FILE   = "customers.csv"
NUM_CUSTOMERS = 300

# Seed for reproducibility (remove or set to None for random output each run)
# random.seed(42)

# Fixed end-of-DOB range — upper bound stays constant regardless of dob-start-year
DOB_END = datetime(2007, 12, 31)

# ── Reference Data ────────────────────────────────────────────────────────────

# (city, state, zip_code, county) — real NC locations
LOCATIONS = [
    ("Raleigh",         "NC", "27601", "Wake"),
    ("Raleigh",         "NC", "27604", "Wake"),
    ("Raleigh",         "NC", "27606", "Wake"),
    ("Raleigh",         "NC", "27607", "Wake"),
    ("Raleigh",         "NC", "27612", "Wake"),
    ("Raleigh",         "NC", "27614", "Wake"),
    ("Raleigh",         "NC", "27615", "Wake"),
    ("Raleigh",         "NC", "27616", "Wake"),
    ("Apex",            "NC", "27502", "Wake"),
    ("Fuquay-Varina",   "NC", "27526", "Wake"),
    ("Lillington",      "NC", "27546", "Harnett"),
    ("Dunn",            "NC", "28334", "Harnett"),
    ("Angier",          "NC", "27501", "Harnett"),
    ("Erwin",           "NC", "28339", "Harnett"),
    ("Broadway",        "NC", "27505", "Harnett"),
    ("Cary",            "NC", "27511", "Wake"),
    ("Cary",            "NC", "27513", "Wake"),
    ("Clayton",         "NC", "27520", "Johnston"),
    ("Sanford",         "NC", "27330", "Lee"),
    ("Durham",          "NC", "27701", "Durham"),
    ("Durham",          "NC", "27704", "Durham"),
    ("Holly Springs",   "NC", "27540", "Wake"),
    ("Garner",          "NC", "27529", "Wake"),
    ("Morrisville",     "NC", "27560", "Wake"),
]

# Names split by gender so we can derive gender from first name
MALE_FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard",
    "Joseph", "Thomas", "Charles", "Christopher", "Daniel", "Jason",
    "Matthew", "Andrew", "Liam", "Randy",
]

FEMALE_FIRST_NAMES = [
    "Mary", "Patricia", "Jennifer", "Florence", "Elizabeth", "Barbara",
    "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Stephanie",
    "Charlotte", "Luna",
]

# Combined pool used when picking a random first name
FIRST_NAMES = MALE_FIRST_NAMES + FEMALE_FIRST_NAMES

# Lookup for O(1) gender inference after a name is chosen
GENDER_MAP: dict[str, str] = (
    {name: "M" for name in MALE_FIRST_NAMES}
    | {name: "F" for name in FEMALE_FIRST_NAMES}
)

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "White", "Allen", "Anderson",
    "Hill", "Baker", "Lee", "Martin", "Wilson", "Thomas", "Green", "Taylor", "Moore",
    "Clark", "Adams", "Carter", "Edwards", "Cooper", "Kelly", "James", "Bell",
]

STREET_NAMES = [
    "Main St", "Oak St", "Pine St", "Maple Ave", "Cedar Ln",
    "Elm St", "Washington St", "Lincoln Ave", "Lakeview Dr",
    "Dogwood St", "Cardinal Ave", "Church St", "Laurel Rd",
    "Magnolia Rd", "Walnut Ave", "Birch St", "Spruce Ln",
    "State St", "Hummingbird Dr", "Shady Ln", "Circle Dr",
    "Jefferson St", "Park St", "Chestnut St", "Central Ave",
]

# Fake domains prevent accidental email delivery
FAKE_DOMAINS = [
    "offlinemail.com",
    "nachomail.net",
    "fakeinbox.net",
    "fakemail.com",
    "notinbox.net",
]

# ── CSV Column Headers ────────────────────────────────────────────────────────

FIELDNAMES = [
    "customer_id",
    "first_name",
    "last_name",
    "gender",           # <-- inserted after last_name
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
    "date_created",
]

# ── Helper Functions ──────────────────────────────────────────────────────────

def random_phone() -> str:
    """Return a fake NANP-style phone number (200–499 area code, 555 exchange)."""
    return f"{random.randint(200, 499)}-555-{random.randint(1000, 9999)}"


def random_address() -> str:
    """Return a fake street address with a random house number and street name."""
    return f"{random.randint(100, 99999)} {random.choice(STREET_NAMES)}"


def random_email(first: str, last: str) -> str:
    """
    Build a fake email address from common username patterns.
    A random number suffix (1–999) is appended to reduce collisions.
    """
    username_choices = [
        last,
        first,
        first + last[0],   # e.g. janes
        first[0] + last,   # e.g. jsmith
        first + last,      # e.g. janesmith
        last + first,      # e.g. smithjane
    ]
    username = random.choice(username_choices).lower()
    suffix   = random.randint(1, 999)
    domain   = random.choice(FAKE_DOMAINS)
    return f"{username}{suffix}@{domain}"


def random_dob(dob_start: datetime) -> str:
    """
    Return a random date of birth between dob_start and DOB_END as YYYY-MM-DD.

    Args:
        dob_start: Earliest possible birth date (derived from --dob-start-year).
    """
    range_days = (DOB_END - dob_start).days
    dob = dob_start + timedelta(days=random.randint(0, range_days))
    return dob.strftime("%Y-%m-%d")


def random_date_created(created_start: datetime, created_end: datetime) -> datetime:
    """
    Return a random account-creation datetime within [created_start, created_end].

    Args:
        created_start: Earliest possible creation date.
        created_end:   Latest  possible creation date.
    """
    range_days = (created_end - created_start).days
    return created_start + timedelta(days=random.randint(0, range_days))


def infer_gender(first_name: str) -> str:
    """
    Return 'M' or 'F' based on the first name using GENDER_MAP.
    Falls back to 'U' (unknown) for any name not in the map.
    """
    return GENDER_MAP.get(first_name, "U")


# ── Record Generation ─────────────────────────────────────────────────────────

def generate_customer(
    customer_id: int,
    dob_start: datetime,
    created_start: datetime,
    created_end: datetime,
) -> list:
    """
    Build and return a single customer row.

    Weighted random choices:
      is_active      — 75 % True  (weights: 1×False, 3×True)
      loyalty_member — 67 % True  (weights: 1×False, 2×True)

    Args:
        customer_id:   Sequential record identifier.
        dob_start:     Earliest possible birth date.
        created_start: Earliest possible account-creation date.
        created_end:   Latest  possible account-creation date.
    """
    first  = random.choice(FIRST_NAMES)
    last   = random.choice(LAST_NAMES)
    gender = infer_gender(first)
    city, state, zipcode, county = random.choice(LOCATIONS)

    return [
        customer_id,
        first,
        last,
        gender,                                               # derived from first name
        random_phone(),
        random_email(first, last),
        random_address(),
        city,
        state,
        zipcode,
        county,
        random_dob(dob_start),
        random.choices([0, 1], weights=[1, 3])[0],           # is_active      (~75 %)
        random.choices([0, 1], weights=[1, 2])[0],           # loyalty_member (~67 %)
        random_date_created(created_start, created_end),
    ]


# ── Argument Parsing ──────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """Define and parse command-line arguments."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    parser = argparse.ArgumentParser(
        description="Generate synthetic customer CSV data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--num-customers",
        type=int,
        default=NUM_CUSTOMERS,
        metavar="N",
        help=f"Number of customer records to generate  (default: {NUM_CUSTOMERS})",
    )
    parser.add_argument(
        "--dob-start-year",
        type=int,
        default=1940,
        metavar="YEAR",
        help="First year of the DOB range, e.g. 1960  (default: 1940)",
    )
    parser.add_argument(
        "--created-start",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=today - timedelta(days=3650),   # 10 years ago
        metavar="YYYY-MM-DD",
        help="Earliest possible date_created  (default: 10 years ago)",
    )
    parser.add_argument(
        "--created-end",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=today,
        metavar="YYYY-MM-DD",
        help="Latest possible date_created  (default: today)",
    )

    return parser.parse_args()


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    """Parse arguments, generate records, and write the CSV."""
    args = parse_args()

    # Validate date ordering
    if args.created_start > args.created_end:
        raise ValueError(
            f"--created-start ({args.created_start.date()}) must be "
            f"on or before --created-end ({args.created_end.date()})."
        )

    dob_start = datetime(args.dob_start_year, 1, 1)
    if dob_start >= DOB_END:
        raise ValueError(
            f"--dob-start-year {args.dob_start_year} must be before "
            f"{DOB_END.year} (the fixed DOB end year)."
        )

    # Validate customer count
    if args.num_customers < 1:
        raise ValueError("--num-customers must be at least 1.")

    # Generate all rows
    rows = [
        generate_customer(cid, dob_start, args.created_start, args.created_end)
        for cid in range(1, args.num_customers + 1)
    ]

    # Write to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDNAMES)
        writer.writerows(rows)

    print(
        f"{args.num_customers} customers written to '{OUTPUT_FILE}'\n"
        f"  DOB range      : {dob_start.date()} → {DOB_END.date()}\n"
        f"  Created range  : {args.created_start.date()} → {args.created_end.date()}"
    )


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
