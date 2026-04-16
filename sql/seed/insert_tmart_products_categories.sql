USE tmart;

INSERT INTO products_categories
(name, description)
VALUES
('Food and Beverages','Groceries, snacks, drinks'),
('Personal Care and Beauty', 'Hygiene, grooming'),
('Household Goods and Cleaning Products', 'Cleaning and home maintenace supplies'),
('Health and Wellness Products', 'Non-prescription medications, wellness products'),
('Pet Care Products', 'Pet food, treats, grooming supplies, hygience products'),
('Baby and Childcare', 'Diapers, wipes, formulas, baby food');

-- Food and Beverages
INSERT INTO tmart.products_subcategories
(category_id, name, description)
VALUES
(1, 'Dairy', 'Cheese, milk, yogurt, butter, eggs'),
(1, 'Baked Goods', 'Pastries, bread, cakes'),
(1, 'Snacks', 'Chips, cookies, crackers, candy, nuts, salsa and dips'),
(1, 'Produce', 'Fruits and vegetables'),
(1, 'Meat', 'Meat products'),
(1, 'Breakfast and Cereal', 'Cereal, granola, energy bars'),
(1, 'Pantry', 'Canned goods, Dry goods, grains, spices, baking essentials'),
(1, 'Soda', 'Carbonated drink'),
(1, 'Juice', 'Juice, punch, juice powder'),
(1, 'Coffee', 'Coffee products'),
(1, 'Tea', 'Tea products'),
(1, 'Water', 'Bottled water');

-- Personal Care Products
INSERT INTO tmart.products_subcategories
(category_id, name, description)
VALUES
(2, 'Hair Care', 'Shampoos, conditioners, hair treatments, hair dye, styling tools'),
(2, 'Bath and Body', 'Soap, lotion, hand sanitizers'),
(2, 'Skin Care', 'Face moisturizers, face wash, face treatments, sun care'),
(2, 'Oral Care', 'Toothpaste, mouthwash, denture care'),
(2, 'Deodorant', 'Deodorant');

-- Household Products
INSERT INTO tmart.products_subcategories
(category_id, name, description)
VALUES
(3, 'Cleaning Supplies', 'Dish detergen, cleaning wipes, cleaning tools, bathroom cleaners, glass cleaners'),
(3, 'Laundry', 'Laundry detergent, fabric softeners, bleach, stain removers'),
(3, 'Paper Products', 'Toilet paper, paper towels, facial tissues, napkins'),
(3, 'Trash Bags', 'Trash bags'),
(3, 'Food Storages and Wraps', 'Food storage containers, wrap and foil, food storage bags'),
(3, 'Disposable Tableware', 'Cups, plates and bowls, plastic cutlery'),
(3, 'Air Fresheners', 'Air Fresheners');


-- Health and Wellness Products
INSERT INTO tmart.products_subcategories
(category_id, name, description)
VALUES
(4, 'Vitamins and Supplements', 'Vitamins, multi-vitamins, minerals'),
(4, 'Allergy and Sinus', 'Allergy and Sinus'),
(4, 'Cold and Flu', 'Cold and Flu, cough, throat relief, lip balm'),
(4, 'Pain Relief', 'Asprin, pain and fever reducers'),
(4, 'First Aid', 'Bandages, antiseptics, wound care, first aid kits');

-- Pet Care Products
INSERT INTO tmart.products_subcategories
(category_id, name, description)
VALUES
(5, 'Dogs', 'Food, treats, toys'),
(5, 'Cats', 'Food, treats, litter, toys'),
(5, 'Birds', 'Food, toys'),
(5, 'Fish', 'Food');

-- Baby and Childcare
INSERT INTO tmart.products_subcategories
(category_id, name, description)
VALUES
(6, 'Food and Formula', 'Food, formula, snacks, cereal'),
(6, 'Beverages', 'Beverages'),
(6, 'Diapers and Wipes', 'Diapers, wipes'),
(6, 'Bottles and Cups', 'Bottles, cups, tableware'),
(6, 'Toys', 'Toys'),
(6, 'Bathing and Skin Care', 'Creams, ointments, shampoo, soap, lotion'),
(6, 'Health & Wellnes', 'Laundry, medicine, pacifiers, oral care');









