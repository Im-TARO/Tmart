import csv
import random
import string

TARGET_PRODUCTS = 10000
OUTPUT_FILE = "tmart_products.csv"

# -----------------------------
# CATEGORY / SUBCATEGORY STRUCTURE
# -----------------------------

catalog = {
    "Food and Beverages": {
        "Dairy":{
            "brands":["GoldenVale Farms","PureHarvest","Aurora Fields","SunVale Kitchen","EverBloom Foods",
                      "Lunafresh","Crescent Grove","VitaVerde","BrightBerry","NaturaPress","Tmart"],
            "products":{
                "Whole Milk":["32 oz","64 oz","1 gal"],
                "Skim Milk":["32 oz","64 oz","1 gal"],
                "Chocolate Milk":["32 oz","64 oz"],
                "Greek Yogurt":["5 oz","16 oz","32 oz"],
                "Vanilla Yogurt":["5 oz","16 oz","32 oz"],
                "Plain Yogurt":["5 oz","16 oz","32 oz"],
                "Cheddar Cheese":["8 oz","16 oz"],
                "Mozzarella Cheese":["8 oz","16 oz"],
                "Unsalted Butter":["8 oz","16 oz"],
                "Salted Butter":["8 oz","16 oz"],
                "Large Brown Eggs":["6 ct","12 ct", "18 ct"],
                "Large White Eggs":["6 ct","12 ct", "18 ct"],
                "Sour Cream": ["8 oz", "16 oz"],
                "Cottage Cheese": ["8 oz", "16 oz"],
                "Cream Cheese": ["8 oz", "16 oz"],
                "Whipped Cream": ["7 oz", "14 oz"],
                "Buttermilk": ["1 qt", "1/2 gal"],
                "Heavy Cream":["16 oz","32 oz"],
                "Half and Half":["32 oz","1 qt"],
                "String Cheese":["12 ct","24 ct"],
                "Parmesan Cheese":["5 oz","8 oz"],
                "Baby Swiss Cheese":["8 oz","16 oz"],
                "Egg Bites":["4 ct","8 ct"],
                "Almond Milk":["32 oz","64 oz"],
                "Oat Milk":["32 oz","64 oz"]                              
            }
        },
        "Baked Goods":{
            "brands":["GoldenVale Bakery","SunVale Kitchen","EverBloom Foods","Aurora Fields","PureHarvest",
                      "Crescent Grove","Lunafresh","VitaVerde","BrightBerry","NaturaPress","Tmart"],
            "products":{
                "Plain Bagels": ["4 ct", "6 ct"],
                "Croissants": ["4 ct", "6 ct"],
                "Muffins": ["4 ct", "6 ct"],            
                "Dinner Rolls": ["6 ct", "12 ct"],            
                "Cinnamon Raisin Bagels":["6 ct"],
                "Hot Dog Buns":["8 ct","16 ct"],
                "Hamburger Buns":["4 ct","8 ct","16 ct"],
                "Flour Tortillas":["8 ct","12 ct","20 ct"],
                "Corn Tortillas":["10 ct","12 ct","20 ct"],
                "White Bread":["16 oz","20 oz"],
                "Whole Wheat Bread":["16 oz","20 oz"],
                "English Muffins":["6 ct"],
                "Sliced Rye Bread":["16 oz","20 oz"],
                "Sourdough Bread":["16 oz","24 oz"],
                "Brioche Buns":["4 ct","8 ct"],
                "Slider Buns":["12 ct"],
                "Pita Bread":["6 ct","12 ct"],
                "Naan Bread":["4 ct","8 ct"],
                "Baguettes":["16 oz"],
                "Brownies":["6 ct","12 ct"],
                "Donuts": ["6 ct", "12 ct"]                             
            }
        },        
        "Snacks":{
            "brands":["BrightBerry","PureHarvest","GoldenVale","Crescent Grove","EverBloom Foods",
                      "SunVale Kitchen","Aurora Fields","Lunafresh","VitaVerde","NaturaPress","Tmart"],
            "products":{
                "Potato Chips": ["6 oz", "10 oz", "16 oz"],
                "Kettle Chips": ["6 oz", "10 oz", "16 oz"],
                "Tortilla Chips": ["8 oz", "12 oz", "16 oz"],
                "Popcorn": ["4 oz", "8 oz", "12 oz"],
                "Pretzels": ["6 oz", "12 oz"],
                "Beef Jerky": ["3 oz", "6 oz"],               
                "Barbecue Potato Chips":["5 oz","8 oz","12 oz"],
                "Chocolate Chip Cookies":["8 oz","12 oz","16 oz"],
                "Butter Cookies":["8 oz","12 oz"],
                "Grahams Crackers":["8 oz","12 oz"],
                "Raisins": ["6 ct", "20 oz"],
                "Dried Cranberries": ["6 oz", "18 oz"],
                "Cheddar Crackers": ["12 oz","20 oz","10 ct","20 ct"],
                "Roasted Cashews": ["10 oz","16 oz","30 oz"],
                "Dry Roasted Peanuts": ["10 oz","16 oz","30 oz"],
                "Butter Cookies":["12 ct","24 ct"], 
                "Cheese Puffs": ["6 oz", "10 oz"],
                "Rice Cakes": ["6 ct", "14 ct"],
                "Fruit Snacks": ["10 ct", "20 ct"],
                "Peanut Butter Crackers": ["6 ct", "12 ct"],
                "Veggie Straws": ["4 oz", "8 oz"],
                "Kettle Corn": ["6 oz", "12 oz"],
                "Turkey Jerky": ["3 oz", "6 oz"],
                "Mixed Nuts": ["10 oz", "16 oz"]                              
            }
        },
        "Produce":{
            "brands":["SunVale Farms","GoldenVale","Aurora Fields","EverBloom Foods","PureHarvest",
                      "Crescent Grove","BrightBerry","VitaVerde","Lunafresh","NaturaPress","Tmart"],
            "products":{
                "Apples": ["1 lb", "3 lb", "5 lb"],
                "Bananas": ["1 lb", "3 lb"],
                "Oranges": ["3 lb", "5 lb"],
                "Grapes": ["1 lb", "2 lb"],
                "Strawberries": ["1 pt", "2 pt"],
                "Lettuce": ["1 ct", "2 ct"],
                "Tomatoes": ["1 lb", "2 lb"],
                "Carrots": ["1 lb", "2 lb"],
                "Broccoli": ["1 lb", "2 lb"],
                "Blueberries": ["1 pt", "2 pt"],
                "Avocados": ["2 ct", "4 ct"],
                "Lemons": ["1 lb", "2 lb"],
                "Cucumbers": ["1 ct", "2 ct"],
                "Bell Peppers": ["2 ct", "4 ct"],
                "Onions": ["1 lb", "3 lb"],
                "Potatoes": ["3 lb", "5 lb", "10 lb"],
                "Spinach": ["8 oz", "16 oz"],
                "Celery": ["1 ct"],
                "Mushrooms": ["8 oz", "16 oz"],
                "Watermelon":["ea"],
                "Raspberries": ["6 oz", "12 oz"],
                "Pineapple": ["ea"],
                "Sweet Potatoes": ["3 lb", "5 lb"],
                "Cauliflower": ["ea", "2 ct"],
                "Green Beans": ["1 lb", "2 lb"],
                "Zucchini": ["1 lb", "2 lb"],
                "Asparagus": ["1 lb", "2 lb"],
                "Kale": ["8 oz", "16 oz"],
                "Cabbage": ["ea"],
                "Corn on Cob": ["4 ct", "6 ct"]                
            }
        },
        "Meat":{
            "brands":["GoldenVale Farms","EverBloom Foods","PureHarvest","SunVale Meats","Crescent Grove",
                      "Aurora Fields","Lunafresh","NaturaPress","VitaVerde","BrightBerry","Tmart"],
            "products":{
                "Beef Steaks": ["1 lb", "2 lb"],
                "Ground Beef": ["1 lb", "2 lb"],
                "Chicken Breast": ["1 lb", "2 lb"],
                "Chicken Thighs": ["1 lb", "2 lb"],
                "Pork Chops": ["1 lb", "2 lb"],
                "Ground Turkey": ["1 lb", "2 lb"],
                "Bacon": ["12 oz", "16 oz"],
                "Sausages": ["12 oz", "16 oz"],
                "Ham Slices": ["8 oz", "16 oz"],
                "Deli Turkey": ["8 oz", "16 oz"],
                "Chicken Wings": ["2 lb", "4 lb"],
                "Pork Ribs": ["2 lb", "4 lb"],
                "Salmon Fillets": ["8 oz", "16 oz"],
                "Turkey Bacon": ["12 oz"],
                "Italian Sausage": ["16 oz", "32 oz"],
                "Chicken Drumsticks": ["1 lb", "2 lb"],
                "Beef Roast": ["2 lb", "3 lb"],
                "Pork Tenderloin": ["1 lb", "2 lb"],
                "Shrimp": ["1 lb"],
                "Deli Ham": ["8 oz", "16 oz"],
                "Ground Pork": ["1 lb", "2 lb"],
                "Lamb Chops": ["1 lb", "2 lb"],
                "Bratwurst": ["12 oz", "16 oz"],
                "Cornish Hen": ["20 oz", "40 oz"],
                "Sirloin Steak": ["1 lb", "2 lb"],
                "Chicken Legs": ["1 lb", "2 lb"],
                "T-Bone Steak": ["1.5 lb", "2.5 lb"],
                "Hot Dogs": ["12 oz", "16 oz"],
                "Polish Sausage": ["12 oz", "16 oz"]                               
            }
        },
        "Breakfast and Cereal":{
            "brands":["SunVale Kitchen","PureHarvest","BrightBerry","Crescent Grove","GoldenVale","Aurora Fields",
                      "EverBloom Foods","VitaVerde","Lunafresh","NaturaPress","Tmart"],
            "products":{
                "Corn Flakes":["14 oz","25 oz"],
                "Crispy Rice Cereal":["12 oz","25 oz"],
                "Shredded Wheat":["14 oz","25 oz"],
                "Nut and Nut Granola":["8 oz","12 oz"],
                "Granola Bars":["4 ct","8 ct","16 ct"],
                "Granola": ["8 oz", "12 oz", "16 oz"],
                "Oatmeal": ["10 oz", "16 oz", "32 oz"],
                "Pancake Mix": ["16 oz", "32 oz"],
                "Waffle Mix": ["16 oz", "32 oz"],
                "Instant Oats": ["8 ct", "12 ct"],
                "Maple Syrup": ["8 oz", "12 oz"],
                "Honey": ["8 oz", "16 oz"]              
            }
        },  
        "Pantry":{
            "brands":["PureHarvest","GoldenVale","EverBloom Foods","NaturaPress","SunVale Kitchen",
                      "Crescent Grove","Lunafresh","BrightBerry","VitaVerde","Aurora Fields","Tmart"],
            "products":{
                "Spaghetti": ["12 oz", "16 oz", "32 oz"],
                "Flour": ["2 lb", "5 lb"],
                "Sugar": ["2 lb", "4 lb"],
                "Canned Vegetables": ["12 oz", "15 oz"],
                "Canned Soup": ["10 oz", "18 oz"],
                "Peanut Butter": ["12 oz", "16 oz"],               
                "Penne Pasta":["12 oz","16 oz"],
                "White Rice":["1 lb","2 lb","5 lb"],
                "Brown Rice":["1 lb","2 lb","5 lb"],
                "Pasta Sauce":["16 oz","24 oz"],
                "Garlic Powder":["2.5 oz","11 oz"],
                "Iodized Salt":["16 oz","26 oz"],
                "Black Pepper":["3 oz","16 oz"],
                "Canned Black Beans":["15 oz","30 oz"],
                "Minced Garlic":["8 oz","32 oz"],
                "Canola Oil": ["16 oz","48 oz","1 gal"],
                "Olive Oil": ["16 oz","48 oz","1 gal"],
                "Avocado Oil": ["16 oz","48 oz","1 gal"],
                "Coconut Oil": ["16 oz","48 oz","1 gal"],
                "Baking Powder": ["8 oz", "16 oz"],
                "Baking Soda": ["1 lb", "4 lb"],
                "Cornstarch": ["12 oz", "24 oz"],
                "Vanilla Extract": ["2 oz", "4 oz"],
                "Chicken Broth": ["14 oz", "32 oz"],
                "Beef Broth": ["14 oz", "32 oz"],
                "Canned Tuna": ["5 oz", "12 oz"],
                "Quinoa": ["1 lb", "2 lb"],
                "Lentils": ["1 lb", "2 lb"],
                "Soy Sauce": ["10 oz", "20 oz"]                
            }
        },                                 
        "Soda":{
            "brands":["EverSip","BloomCrest","SunVale Beverages","GoldenDrop","PurePeak Drinks","VitaVerde",
                      "Crescent Brew","BrightBerry","BlueHaven","Lunafresh","Tmart"],
            "products":{
                "Cola": ["12 oz", "16 oz", "2 L"],
                "Diet Cola": ["12 oz", "16 oz", "2 L"],
                "Lemon Lime Soda": ["12 oz", "16 oz", "2 L"],
                "Orange Soda": ["12 oz", "16 oz", "2 L"],
                "Ginger Ale": ["12 oz", "16 oz", "2 L"],
                "Root Beer": ["12 oz", "16 oz", "2 L"],
                "Cream Soda": ["12 oz", "16 oz"],
                "Grapefruit Soda": ["12 oz", "16 oz"],
                "Cherry Soda": ["12 oz", "16 oz"],
                "Club Soda": ["12 oz", "16 oz", "1 L"],
                "Strawberry Soda": ["12 oz", "16 oz"],
                "Vanilla Cream Soda": ["12 oz", "16 oz"],
                "Raspberry Soda": ["12 oz", "16 oz"],
                "Peach Soda": ["12 oz", "16 oz"],
                "Lime Soda": ["12 oz", "16 oz"],
                "Zero Sugar Cola": ["12 oz", "16 oz"],
                "Diet Root Beer": ["12 oz", "16 oz"],
                "Cherry Cola": ["12 oz", "16 oz"]                
            }
        },
        "Juice":{
            "brands":["VitaVerde","PureHarvest","SunVale Juices","GoldenDrop","Lunafresh","BloomCrest",
                      "NaturaPress","Citrabella","EverSip","BrightBerry","Tmart"],
            "products":{
                "Orange Juice": ["12 oz", "32 oz", "64 oz"],
                "Apple Juice": ["12 oz", "32 oz", "64 oz"],
                "Grape Juice": ["12 oz", "32 oz"],
                "Cranberry Juice": ["12 oz", "32 oz"],
                "Pineapple Juice": ["12 oz", "32 oz"],
                "Mango Juice": ["12 oz", "32 oz"],
                "Mixed Berry Juice": ["12 oz", "32 oz"],
                "Tropical Blend": ["12 oz", "32 oz"],
                "Pomegranate Juice": ["12 oz", "32 oz"],
                "Lemonade": ["32 oz", "64 oz"],
                "Passion Fruit Juice": ["12 oz", "32 oz"],
                "Carrot Juice": ["12 oz", "32 oz"],
                "Tomato Juice": ["46 oz", "64 oz"],
                "Guava Juice": ["12 oz", "32 oz"],
                "Grapefruit Juice": ["12 oz", "32 oz"]
            }
        },
        "Coffee":{
            "brands":["RoastHaven","Veloro Coffee Co.","MorningVale","Crescent Brew","Auralis Roasters",
                      "PurePeak Coffee","Golden Ember","NaturaBean","Solterra Roastery","EverBrew","Tmart"],
            "products":{
                "Ground Coffee": ["12 oz", "16 oz", "32 oz"],
                "Whole Bean Coffee": ["12 oz", "16 oz", "32 oz"],
                "Instant Coffee": ["4 oz", "8 oz"],
                "Espresso Roast": ["12 oz", "16 oz"],
                "Cold Brew Concentrate": ["12 oz", "32 oz"],
                "Single Serve Pods": ["10 ct", "20 ct"],
                "Decaf Coffee": ["12 oz", "16 oz"],
                "Flavored Coffee": ["12 oz", "16 oz"],
                "Iced Coffee": ["12 oz", "16 oz", "32 oz"],
                "Coffee Capsules": ["10 ct", "20 ct"]            
            }
        },  
        "Tea":{
            "brands":["Verdantia","Aurora Leaf","SilkenSteep","GoldenVale","Lunaris Tea Co.",
                      "PureHaven Teas","ZenSol Leafworks","WillowMist","Satori Bloom","EverHerb","Tmart"],
            "products":{
                "Black Tea": ["20 ct", "40 ct"],
                "Green Tea": ["20 ct", "40 ct"],
                "Herbal Tea": ["20 ct", "40 ct"],
                "Chai Tea": ["20 ct"],
                "White Tea": ["20 ct"],
                "Oolong Tea": ["20 ct"],
                "Matcha Tea": ["2 oz", "4 oz"],
                "Iced Tea Mix": ["6 ct", "12 ct"],
                "Detox Tea": ["20 ct"]
            }
        }, 
        "Water":{
            "brands":["Aqualis Pure","BlueHaven Springs","CrystalVea","Orium Waters","Vellora Springs",
                      "LustraDrop","EverMist","ClearVale","HorizonBlue","Purevia","Tmart"],
            "products":{
                "Sparkling Water":["6 ct","12 ct"],
                "Spring Water":["6 ct","24 ct"],
                "Purified Water":["6 ct","24 ct"],
                "Mineral Water": ["12 oz", "1 L"],
                "Alkaline Water": ["12 oz", "1 L"],
                "Electrolyte Water": ["12 oz", "16 oz", "1 L"],
                "Distilled Water": ["1 L", "5 L"]
            }
        }, 
    }, 
    "Personal Care and Beauty":{
        "Hair Care":{
            "brands":["Velora Naturals","PureMist Botanica","Silvane Organics","Aurela Essence","LustraLeaf",
                      "MiraBloom","EverLush","NaturaGlow","Zenvana Botanics","TrueVale"],
            "products":{
            "Shampoo": ["10 oz", "16 oz", "24 oz"],
            "Conditioner": ["10 oz", "16 oz"],
            "Dry Shampoo": ["6 oz", "10 oz"],
            "Hair Serum": ["2 oz", "4 oz"],
            "Leave-In Conditioner": ["8 oz", "12 oz"],
            "Hair Mask": ["6 oz", "10 oz"],
            "Styling Gel": ["8 oz", "12 oz"],
            "Hair Oil": ["3 oz", "6 oz"],
            "Heat Protectant Spray": ["6 oz", "10 oz"],
            "Volumizing Mousse": ["8 oz", "12 oz"]
            }
        },
        "Bath and Body":{
            "brands":["Auralis Organics","BloomThera","Serenique Botanicals","PureHaven","Velvessa",
                      "NaturaSoothe","Crescent Bloom","AmberVale Naturals","Solivana","Lunelle Essence","Tmart"],
            "products":{
                "Body Wash":["12 oz","18 oz","24 oz"],
                "Body Scrub": ["6 oz", "10 oz"],
                "Bath Salt": ["8 oz", "16 oz"],
                "Hand Soap":["8 oz","12 oz"],
                "Bar Soap":["3 ct","6 ct","12 ct"],
                "Hand Wipes":["20 ct","40 ct","90 ct"],
                "Hand Sanitizer":["2 oz","8 oz"],
                "Bath Bomb": ["1 ct", "3 ct", "6 ct"]
            }
        },
        "Skin Care":{
            "brands":["Lunavia Botanics","EternaGlow","Solenne Naturals","Arvella Essence","PureSilque",
                      "Velique Organics","Nuvéra","Clarity Bloom","Seraphyne","Opalis Skin"],
            "products":{
                "Sunscreen": ["2 oz", "4 oz", "8 oz"],
                "Face Wash":["12 oz","16 oz"],
                "Witch Hazel":["8 oz","16 oz"],
                "Make-up Remover":["9 oz","12 oz"],
                "Face Serum": ["1 oz", "2 oz"],
                "Night Cream": ["2 oz", "4 oz"],
                "Eye Cream": ["0.5 oz", "1 oz"],
                "Face Mask": ["1 ct", "3 ct", "6 ct"],
                "Face Moisturizers":["5 oz","8 oz","16 oz"]
            }
        },                
        "Oral Care":{
            "brands":["BrightenWell","PureVanta","LustraDent","Auralis Smile","VividMouth",
                      "Dentavive","FrescaMint","HaleBright","NaturaDent","EverPearl"],
            "products":{
                "Toothpaste": ["3 oz", "6 oz", "8 oz"],
                "Mouthwash": ["8 oz", "16 oz", "32 oz"],
                "Toothbrush": ["1 ct", "2 ct", "4 ct"],
                "Floss": ["30 m", "50 m"],
                "Whitening Strips": ["10 ct", "20 ct"],
                "Tooth Powder": ["2 oz", "4 oz"],
                "Dental Picks": ["25 ct", "50 ct"],
                "Tongue Cleaner": ["1 ct", "2 ct"],
                "Mouth Spray": ["1 oz", "2 oz"],
                "Whitening Pen": ["0.1 oz", "0.2 oz"]
            }
        },
        "Deodorant":{
            "brands":["AureMist","PureScent Naturals","Velonix","Freshora","Celavive",
                      "NaturaBreeze","Scentelle","Auralift","Zenvive","BrightAura"],
            "products":{
                "Stick Deodorant": ["2 oz", "3 oz"],
                "Spray Deodorant": ["3 oz", "6 oz"],
                "Roll-On Deodorant": ["2 oz", "3 oz"],
                "Cream Deodorant": ["2 oz", "4 oz"],
                "Gel Deodorant": ["2 oz", "3 oz"],
                "Natural Deodorant": ["2 oz", "3 oz"],
                "Deodorant Wipes": ["10 ct", "30 ct"],
                "Travel Size Deodorant": ["1 oz", "2 oz"]
            }
        }        
    },
    "Household Goods and Cleaning Products":{
        "Cleaning Supplies":{
            "brands":["PureLuxe Home","BrightNest","EverClean","Freshora","Auralift",
                      "Lunafresh","NaturaPress","SunVale Home","Crescent Grove","GoldenVale","Tmart"],
            "products":{
                "All Purpose Cleaner":["16 oz","32 oz","56 oz"],
                "Glass Cleaner":["16 oz","32 oz","67 oz","20 ct"],
                "Disinfecting Wipes":["12 ct","35 ct","75 ct"],
                "Dish Liquid":["12 oz","32 oz","90 oz"],
                "Dishwasher Detergent":["75 oz","120 oz"],
                "Bathroom Cleaner":["19 oz","30 oz"],
                "Drain Cleaner":["17 oz","32 oz","80 oz"],
                "Kitchen Degreaser": ["16 oz", "32 oz"],
                "Toilet Bowl Cleaner": ["16 oz", "24 oz"],
                "Floor Cleaner": ["32 oz", "64 oz"]
            }
        },
        "Laundry":{
            "brands":["EverClean","BrightNest","PureLuxe Home","Freshora","Lunafresh","Auralift",
                      "SunVale Home","Crescent Grove","GoldenVale","NaturaPress","Tmart"],
            "products":{
                "Laundry Detergent": ["32 oz", "64 oz", "128 oz"],
                "Fabric Softener": ["32 oz", "64 oz"],
                "Laundry Pods": ["20 ct", "40 ct"],
                "Bleach": ["32 oz", "64 oz"],
                "Stain Remover Spray": ["16 oz", "32 oz"],    
                "Fabric Refresher": ["16 oz", "32 oz"],
                "Laundry Sanitizer": ["32 oz", "64 oz"],
                "Dryer Sheets":["60 ct","120 ct","240 ct"]                            
            }
        },               
        "Paper Products":{
            "brands":["SunVale Home","EverClean","BrightNest","PureLuxe Home","GoldenVale","Freshora",
                      "Crescent Grove","Lunafresh","NaturaPress","Auralift","Tmart"],
            "products":{
                "Paper Towels": ["1 roll", "6 roll", "12 roll"],
                "Toilet Paper": ["4 roll", "12 roll", "24 roll"],
                "Facial Tissues": ["2 ct", "4 ct", "6 ct"],
                "Napkins": ["100 ct", "250 ct"],
                "Paper Plates": ["50 ct", "100 ct"],
                "Paper Cups": ["25 ct", "50 ct"],
                "Paper Bowls": ["25 ct", "50 ct"],
                "Paper Lunch Bags": ["50 ct", "100 ct"]
            }
        },
        "Trash Bags":{
            "brands":["SunVale Home","EverClean","BrightNest","PureLuxe Home","GoldenVale","Freshora",
                      "Crescent Grove","Lunafresh","NaturaPress","Auralift","Tmart"],
            "products":{
                "Tall Kitchen Bags": ["20 ct", "40 ct"],
                "Large Trash Bags": ["10 ct", "20 ct"],
                "Yard Waste Bags": ["10 ct", "20 ct"],
                "Outdoor Contractor Bags": ["10 ct", "20 ct"],
                "Small Trash Bags": ["40 ct"],
                "Compostable Bags": ["25 ct", "20 ct"],
                "Recycling Bags": ["20 ct", "10 ct"],
                "Scented Trash Bags": ["20 ct", "40 ct"],
                "Heavy Duty Trash Bags": ["10 ct"]
            } 
        },
        "Food Storages and Wraps":{
            "brands":["SunVale Home","EverClean","BrightNest","PureLuxe Home","GoldenVale","Freshora",
                      "Crescent Grove","Lunafresh","NaturaPress","Auralift","Tmart"],
            "products":{
                "Sandwich Bags": ["50 ct", "100 ct"],
                "Snack Bags": ["50 ct", "100 ct"],
                "Quart Storage Bags": ["25 ct", "50 ct"],
                "Gallon Storage Bags": ["15 ct", "30 ct"],
                "Freezer Bags": ["15 ct", "30 ct"],
                "Plastic Wrap": ["100 ft", "200 ft"],
                "Aluminum Foil": ["75 ft", "150 ft"],
                "Wax Paper": ["75 ft", "150 ft"],
                "Parchment Paper": ["50 ft", "100 ft"],
                "Food Storage Containers": ["4 ct", "8 ct"]
            } 
        },
        "Disposable Tableware":{
            "brands":["SunVale Home","BrightNest","EverClean","PureLuxe Home","GoldenVale","Freshora",
                      "Crescent Grove","Lunafresh","NaturaPress","Auralift","Tmart"],
            "products":{
                "Paper Plates": ["50 ct", "100 ct"],
                "Paper Bowls": ["25 ct", "50 ct"],
                "Plastic Cups": ["25 ct", "50 ct"],
                "Plastic Utensils": ["24 ct", "48 ct"],
                "Plastic Plates": ["25 ct", "50 ct"],
                "Party Cups": ["20 ct", "40 ct"],
                "Paper Napkins": ["100 ct", "250 ct"],
                "Cutlery Sets": ["24 ct", "48 ct"],
                "Compostable Plates": ["25 ct", "50 ct"]
            } 
        },
        "Air Fresheners":{
            "brands":["Freshora","EverClean","BrightNest","PureLuxe Home","SunVale Home","Auralift",
                      "GoldenVale","Lunafresh","NaturaPress","Crescent Grove","Tmart"],
            "products":{
                "Lavendar Plug-In Refill": ["2 ct", "4 ct"],
                "Candle": ["4 oz", "8 oz"],
                "Wax Melts": ["6 ct", "12 ct"],
                "Reed Diffuser": ["3 oz", "6 oz"],
                "Automatic Spray Refill": ["2 ct", "4 ct"],
                "Car Vent Clip": ["2 ct", "4 ct"],
                "Deodorizing Beads": ["12 oz", "20 oz"],
                "Citrus Scent Air Freshener":["8 oz","10 oz"],
                "Lavender Scent Air Freshener":["8 oz","10 oz"],
                "Tropical Scent Air Freshener":["8 oz","10 oz"],
                "Ocean Breeze Gel Cone Air Freshener":["6 oz","12 oz"],
                "Lavendar Gel Cone Air Freshener":["6 oz","12 oz"],
                "Citrus Gel Cone Air Freshener":["6 oz","12 oz"]
            } 
        }                               
    },
    "Health and Wellness Products":{
        "Vitamins and Supplements":{
            "brands":["PureLuxe Naturals","EverWell","NaturaPress","VitaVerde","GoldenVale Health",
                      "Lunafresh","BrightNest","Auralift Wellness","SunVale Naturals","Crescent Grove"],
            "products":{
                "Multivitamin": ["30 ct", "60 ct", "120 ct"],
                "Vitamin C": ["60 ct", "120 ct"],
                "Vitamin D": ["60 ct", "120 ct"],
                "Calcium": ["60 ct", "120 ct"],
                "Magnesium": ["60 ct", "120 ct"],
                "Fish Oil": ["60 ct", "120 ct"],
                "Probiotic": ["30 ct", "60 ct"],
                "Collagen Supplement": ["6 oz", "12 oz"],
                "Protein Powder": ["1 lb", "2 lb"],
                "Herbal Supplement": ["30 ct", "60 ct"]
            }
        },
        "Allergy and Sinus":{
            "brands":["EverWell","ClearBreathe","SinusEase","Auralift Wellness","PureRelief",
                      "Lunafresh","AirVista","NaturaPress","VitaVerde","GoldenVale Health"],
            "products":{
                "Allergy Relief Tablets": ["12 ct", "24 ct", "48 ct"],
                "Non-Drowsy Antihistamine": ["14 ct", "28 ct"],
                "Allergy Nasal Spray": ["0.5 oz", "1 oz"],
                "Saline Nasal Spray": ["1.5 oz", "3 oz"],
                "Decongestant Tablets": ["12 ct", "24 ct"],
                "Sinus Relief Capsules": ["10 ct", "20 ct"],
                "Allergy Eye Drops": ["0.33 oz", "0.5 oz"],            
                "Daytime Allergy and Sinus": ["12 ct", "24 ct"],
                "Nighttime Allergy and Sinus": ["12 ct", "24 ct"]
            }
        },
        "Cold and Flu":{
            "brands":["EverWell","ClearBreathe","PureRelief","Auralift Wellness","Lunafresh",
                      "GoldenVale Health","NaturaPress","VitaVerde","ComfortCure","SinusEase"],
            "products":{
                "Daytime Cold and Flu": ["12 ct", "24 ct"],
                "Nighttime Cold and Flu": ["12 ct", "24 ct"],
                "Multi-Symptom Cold Relief": ["12 ct", "24 ct"],
                "Cough Syrup": ["4 oz", "8 oz"],
                "Throat Lozenges": ["16 ct", "32 ct"],
                "Cough Drops": ["20 ct", "40 ct"],
                "Nasal Decongestant Spray": ["0.5 oz", "1 oz"],
                "Chest Rub Ointment": ["1.7 oz", "3.5 oz"],
                "Immune Support Powder": ["10 ct", "20 ct"]
            }
        },
        "Pain Relief":{
            "brands":["EverWell","PureRelief","GoldenVale Health","Auralift Wellness","NaturaPress",
                      "ComfortCure","Lunafresh","VitaVerde","ClearBreathe","CalmaLife"],
            "products":{
                "Acetaminophen Tablets": ["24 ct", "50 ct", "100 ct"],
                "Ibuprofen Tablets": ["24 ct", "50 ct", "100 ct"],
                "Naproxen Caplets": ["20 ct", "50 ct"],
                "Topical Pain Relief Cream": ["2 oz", "4 oz"],
                "Muscle and Joint Gel": ["2 oz", "4 oz"],
                "Headache Relief Caplets": ["24 ct", "50 ct"],
                "Back Pain Relief Patches": ["4 ct", "8 ct"],
                "Heat Therapy Patches": ["3 ct", "6 ct"],
                "Arthritis Relief Tablets": ["24 ct", "50 ct"]
            }                      
        },
        "First Aid":{
            "brands":["EverWell","PureRelief","GoldenVale Health","Auralift Wellness","NaturaPress",
                      "ComfortCure","Lunafresh","VitaVerde","ClearBreathe","MediSafe"],
            "products":{
                "Adhesive Bandages": ["40 ct", "100 ct"],
                "Gauze Pads": ["10 ct", "25 ct"],
                "Antiseptic Wipes": ["25 ct", "50 ct"],
                "First Aid Tape": ["5 yd", "10 yd"],
                "Instant Cold Packs": ["4 ct", "8 ct"],
                "Hydrocortisone Cream": ["1 oz"],
                "Antibiotic Ointment": ["0.5 oz", "1 oz"],
                "Burn Gel": ["1 oz", "4 oz"],
                "Tweezers": ["1 ct"],
                "First Aid Kit": ["ea"]
            }                      
        }         
    },         
    "Pet Care Products":{
        "Dogs":{
            "brands":["EverWell Pets","PurePaw Naturals","GoldenVale Canine","Auralift Pets","NaturaPress Paws",
                      "Lunafresh Dogs","VitaVerde Pets","BrightNest Canine","ComfortCure Pets","PawBloom"],
            "products":{
                "Dry Dog Food": ["5 lb", "15 lb", "30 lb"],
                "Wet Dog Food": ["13 oz", "22 oz"],
                "Dog Treats": ["8 oz", "16 oz"],
                "Chew Toys": ["1 ct", "3 ct"],
                "Dog Shampoo": ["8 oz", "16 oz"],
                "Flea and Tick Drops": ["3 ct", "6 ct"],
                "Dental Chews": ["12 ct", "30 ct"],
                "Dog Beds": ["Small", "Medium", "Large"],
                "Leashes": ["4 ft", "6 ft"],
                "Waste Bags": ["100 ct", "200 ct"]
            }
        },
        "Cats":{
            "brands":["EverWell Pets","PurePaw Naturals","GoldenVale Feline","Auralift Pets","NaturaPress Paws",
                      "Lunafresh Cats","VitaVerde Pets","BrightNest Feline","ComfortCure Pets","CatBloom"],
            "products":{
                "Dry Cat Food": ["3 lb", "7 lb", "15 lb"],
                "Wet Cat Food": ["3 oz", "5.5 oz"],
                "Cat Treats": ["3 oz", "6 oz"],
                "Catnip Toys": ["3 ct", "6 ct"],
                "Cat Shampoo": ["8 oz", "16 oz"],
                "Flea and Tick Drops": ["3 ct", "6 ct"],
                "Litter Box Filler": ["10 lb", "20 lb", "40 lb"],
                "Cat Scratching Post": ["Small", "Medium"],
                "Cat Litter Scoop": ["1 ct"],
                "Cat Beds": ["Small", "Medium", "Large"]
            }
        },
        "Birds":{
            "brands":["EverWell Aviary","PureFeather Naturals","GoldenVale Wings","Auralift Birds","NaturaPress Aviary",
                      "Lunafresh Feathers","VitaVerde Birds","BrightNest Aviary","ComfortCure Wings","FeatherBloom"],
            "products":{
                "Bird Seed Mix": ["2 lb", "5 lb", "10 lb"],
                "Bird Treats": ["4 oz", "8 oz"],
                "Bird Toys": ["3 ct", "6 ct"],            
                "Bird Bath": ["1 ct"],
                "Cage Liners": ["50 ct", "100 ct"]
            }
        },
        "Fish":{
            "brands":["EverWell Aquatics","PureFin Naturals","GoldenVale Aqua","Auralift Fish","NaturaPress Aquatics",
                      "Lunafresh Fins","VitaVerde Fish","BrightNest Aqua","ComfortCure Aquatics","FinBloom"],
            "products":{
                "Flake Fish Food": ["1 oz", "2 oz"],
                "Pellet Fish Food": ["2 oz", "8 oz"],
                "Water Conditioner": ["4 oz", "16 oz"],
                "Aquarium Heater": ["25W", "50W"],
                "Fish Tank Filter": ["Small", "Medium"],
                "Aquarium Gravel": ["5 lb", "20 lb"],
                "Live Plants": ["3 ct", "6 ct"],
                "Fish Net": ["2 in", "4 in"]
            }
        }                 
    },
    "Baby and Childcare":{
        "Food and Formula":{
            "brands":["EverWell Baby","PureNourish","GoldenVale Infant","Auralift Baby","NaturaPress Tots",
                      "Lunafresh Baby","VitaVerde Infant","BrightNest Baby","ComfortCure Kids","LittleBloom","Tmart"],
            "products":{
                "Infant Formula Powder": ["12 oz", "19 oz", "36 oz"],
                "Ready-to-Feed Formula": ["32 oz"],
                "Organic Baby Cereal": ["8 oz", "16 oz"],
                "Stage 1 Purees": ["4 oz 6 ct", "4 oz 12 ct"],
                "Fruit Purees": ["4 oz 6 ct"],
                "Vegetable Purees": ["4 oz 6 ct"],
                "Baby Yogurt": ["3.5 oz 4 ct"],
                "Pouch Meals": ["4 oz 8 ct"],
                "Finger Foods": ["1.5 oz 6 ct"]
            }
        },    
        "Beverages":{
            "brands":["EverWell Baby","PureNourish","GoldenVale Infant","Auralift Baby","NaturaPress Tots",
                      "Lunafresh Baby","VitaVerde Infant","BrightNest Baby","ComfortCure Kids","LittleBloom","Tmart"],
            "products":{
                "Toddler Milk Drink": ["19 oz", "32 oz"],
                "Electrolyte Solution": ["8 oz", "33 oz"],
                "Diluted Fruit Juice": ["32 oz"],
                "Toddler Apple Juice":["6 ct","32 oz","64 oz"],
                "Toddler Pear Juice":["6 ct","32 oz","64 oz"],
                "Baby Water": ["16 oz"]
            }
        },            
        "Diapers and Wipes":{
            "brands":["EverWell Baby","PureNourish","GoldenVale Infant","Auralift Baby","NaturaPress Tots",
                      "Lunafresh Baby","VitaVerde Infant","BrightNest Baby","ComfortCure Kids","LittleBloom"],
            "products":{
                "Newborn Diapers": ["40 ct", "80 ct"],
                "Size 1 Diapers": ["50 ct", "100 ct"],
                "Size 2 Diapers": ["60 ct", "120 ct"],
                "Overnight Diapers": ["30 ct", "60 ct"],
                "Swim Diapers": ["10 ct", "20 ct"],
                "Baby Wipes": ["72 ct", "168 ct"],
                "Sensitive Wipes": ["56 ct", "120 ct"],
                "Training Pants": ["20 ct", "40 ct"]
            }
        },
        "Bottles and Cups":{
            "brands":["EverWell Baby","PureNourish","GoldenVale Infant","Auralift Baby","NaturaPress Tots",
                      "Lunafresh Baby","VitaVerde Infant","BrightNest Baby","ComfortCure Kids","LittleBloom"],
            "products":{
                "Newborn Bottles": ["4 oz", "5 oz"],
                "Standard Baby Bottles": ["8 oz", "9 oz"],
                "Wide-Neck Bottles": ["8 oz", "12 oz"],
                "Anti-Colic Bottles": ["9 oz"],
                "Glass Baby Bottles": ["4 oz", "8 oz"],
                "Sippy Cups": ["6 oz", "9 oz"],
                "Transition Cups": ["10 oz"],
                "Straw Cups": ["9 oz", "12 oz"]
            }
        },  
        "Toys":{
            "brands":["EverWell Baby","PureNourish","GoldenVale Infant","Auralift Baby","NaturaPress Tots",
                      "Lunafresh Baby","VitaVerde Infant","BrightNest Baby","ComfortCure Kids","LittleBloom"],
            "products":{
                "Rattles": ["1 ct", "3 ct"],
                "Teethers": ["1 ct", "2 ct"],
                "Stacking Rings": ["Small", "Large"],
                "Shape Sorters": ["6 shapes", "12 shapes"],
                "Activity Gyms": ["1 ct"],
                "Push Toys": ["1 ct"],
                "Soft Blocks": ["6 ct", "12 ct"],
                "Board Books": ["1 ct", "3 ct"],
                "Bath Toys": ["5 ct", "10 ct"],
                "Plush Toys": ["Small", "Medium"]
            }
        },              
        "Bathing and Skin Care":{
            "brands":["EverWell Baby","PureNourish","GoldenVale Infant","Auralift Baby","NaturaPress Tots",
                      "Lunafresh Baby","VitaVerde Infant","BrightNest Baby","ComfortCure Kids","LittleBloom"],
            "products":{
                "Baby Wash": ["8 oz", "15 oz"],
                "Baby Shampoo": ["8 oz", "15 oz"],
                "Baby Lotion": ["6 oz", "12 oz"],
                "Baby Oil": ["4 oz", "8 oz"],
                "Baby Powder": ["4 oz", "10 oz"],
                "Diaper Rash Cream": ["2 oz", "4 oz"],
                "Baby Bath Foam": ["12 oz"],
                "Moisturizing Cream": ["4 oz", "8 oz"],
                "Baby Bath Salts": ["6 oz"]
            }
        },
        "Health & Wellnes":{
            "brands":["EverWell Baby","PureNourish","GoldenVale Infant","Auralift Baby","NaturaPress Tots",
                      "Lunafresh Baby","VitaVerde Infant","BrightNest Baby","ComfortCure Kids","LittleBloom"],
            "products":{
                "Baby Thermometer": ["1 ct"],
                "Nasal Aspirator": ["1 ct"],
                "Baby Vitamins": ["2 oz"],
                "Baby Probiotic Drops": ["0.5 oz"],
                "Baby Oral Care": ["2 oz"],
                "Humidifier Refills": ["6 ct"],
                "Baby Sunscreen": ["3 oz", "6 oz"]
            }
        }        
    }
}

# -----------------------------
# HELPERS
# -----------------------------

def generate_sku(existing):

    while True:
        sku=''.join(random.choices(string.ascii_uppercase+string.digits,k=12))
        if sku not in existing:
            existing.add(sku)
            return sku
    

def generate_price(category):

    ranges={
        "Food and Beverages":(1.50,9.99),
        "Household Goods and Cleaning Products":(3.99,18.99),
        "Personal Care and Beauty":(4.99,14.99),
        "Pet Care Products":(6.99,34.99),
        "Baby and Childcare":(6.99,29.99),
        "Health and Wellness Products":(1.99,19.99)
    }

    low,high=ranges[category]

    return round(random.uniform(low,high),2)

# -----------------------------
# GENERATION
# -----------------------------

sku_set=set()
name_unit_set=set()

rows=[]

product_id=1

while len(rows)<TARGET_PRODUCTS:

    category=random.choice(list(catalog.keys()))

    subcategory=random.choice(list(catalog[category].keys()))

    data=catalog[category][subcategory]

    brand=random.choice(data["brands"])

    product=random.choice(list(data["products"].keys()))

    unit=random.choice(data["products"][product])

    name=f"{brand} {product}"

    combo=f"{brand}:{product}:{unit}"

    if combo in name_unit_set:
        continue

    name_unit_set.add(combo)

    sku=generate_sku(sku_set)

    price=generate_price(category)

    stock=random.randint(20,300)

    rows.append([
        product_id,
        category,
        subcategory,
        name,
        brand,
        sku,
        unit,
        price,
        stock,
        1
    ])

    print(f"product_id: {product_id} {combo}")
    product_id+=1


# -----------------------------
# WRITE CSV
# -----------------------------

with open(OUTPUT_FILE,"w",newline="",encoding="utf-8") as f:

    writer=csv.writer(f)

    writer.writerow([
        "product_id",
        "category",
        "subcategory",
        "name",
        "brand",
        "sku",
        "unit_size",
        "price",
        "stock_quantity",
        "is_active"
    ])

    writer.writerows(rows)

print(f"{len(rows)} products written to {OUTPUT_FILE}")