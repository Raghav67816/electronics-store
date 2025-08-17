import json
import random
from datetime import datetime, timedelta

products = [
    ("Laptop", "Electronics"), 
    ("Smartphone", "Electronics"),
    ("Tablet", "Electronics"), 
    ("Smartwatch", "Wearables"), 
    ("Headphones", "Audio"),
    ("Wireless Mouse", "Accessories"), 
    ("Keyboard", "Accessories"),
    ("Monitor", "Electronics"), 
    ("External Hard Drive", "Storage"),
    ("USB Flash Drive", "Storage"), 
    ("Printer", "Office"), 
    ("Camera", "Photography"),
    ("Bluetooth Speaker", "Audio"), 
    ("Gaming Console", "Gaming"),
    ("Fitness Tracker", "Wearables"), 
    ("Drone", "Electronics"), 
    ("Smart TV", "Electronics"),
    ("Router", "Networking"), 
    ("Power Bank", "Accessories"), 
    ("Graphics Card", "Electronics")
]

retailers = ["TechWorld", "GadgetHub", "ElectroMart", "DeviceSpot", "Digital Plaza"]

reviews_samples = [
    "Great quality!", 
    "Worth the price.", 
    "Battery life could be better.", 
    "Highly recommend.",
    "Not as described.", 
    "Fast shipping!", 
    "Excellent customer service."
]

usernames = ["techlover", "gadgetgeek", "shopaholic", "reviewking", "digitaldiva", "buyer101", "qualityhunter"]

data = []
for _ in range(50):
    name, category = random.choice(products)
    price = round(random.uniform(50, 2000), 2)
    rating = round(random.uniform(1, 5), 1)
    date_published = (datetime.now() - timedelta(days=random.randint(1, 1000))).strftime("%Y-%m-%d")
    retailer = random.choice(retailers)
    is_available = random.choice([True, False])

    # Create structured reviews
    reviews = []
    for _ in range(random.randint(1, 4)):
        username = random.choice(usernames)
        review_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        profile_pic = f"https://example.com/profiles/{username}.png"
        review_text = random.choice(reviews_samples)
        reviews.append({
            "username": username,
            "profile_pic": profile_pic,
            "date_posted": review_date,
            "review_text": review_text
        })

    product_entry = {
        "name": name,
        "category": category,
        "price": price,
        "product_img": "https://fillthis.io/i/600x400",
        "reviews": reviews,
        "rating": rating,
        "date_published": date_published,
        "retailer": retailer,
        "is_available": is_available
    }
    data.append(product_entry)

# Save to JSON
file_path = "./test_products.json"
with open(file_path, "w") as f:
    json.dump(data, f, indent=4)

file_path
