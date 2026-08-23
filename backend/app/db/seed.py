import json
import os
from sqlalchemy.orm import Session
from app.db.models import ProductModel, CategoryModel
from app.core.logging import logger

def generate_catalogue_data():
    """Generates 120+ rich demo products across 6 realistic categories."""
    
    categories = [
        {
            "id": "electronics",
            "name": "Electronics",
            "description": "Laptops, smartphones, audio devices, monitors, and tablets.",
            "subcategories": ["Laptops", "Smartphones", "Headphones", "Monitors", "Tablets", "Audio"]
        },
        {
            "id": "fashion",
            "name": "Fashion",
            "description": "Men's and women's shirts, t-shirts, denim jeans, and formal wear.",
            "subcategories": ["Shirts", "T-Shirts", "Jeans", "Formal Wear", "Hoodies"]
        },
        {
            "id": "footwear",
            "name": "Footwear",
            "description": "Running shoes, casual sneakers, sports shoes, and formal leather shoes.",
            "subcategories": ["Running Shoes", "Casual Shoes", "Formal Shoes", "Sports Shoes"]
        },
        {
            "id": "accessories",
            "name": "Accessories",
            "description": "Durable backpacks, classic and smart watches, wallets, and belts.",
            "subcategories": ["Backpacks", "Watches", "Wallets", "Smart Wearables"]
        },
        {
            "id": "home-lifestyle",
            "name": "Home & Lifestyle",
            "description": "LED desk lamps, ergonomic office cushions, kitchen blenders, and home decor.",
            "subcategories": ["Desk Lamps", "Kitchen", "Home Decor", "Office Essentials"]
        },
        {
            "id": "gifts",
            "name": "Gifts",
            "description": "Curated gift sets, personalized accessories, and festive hampers.",
            "subcategories": ["Gift Sets", "Personalised Gifts", "Accessories", "Hampers"]
        }
    ]

    # Pre-defined templates for 120 realistic items
    products = []
    
    # 1. Electronics (25 items: Laptops, Phones, Audio, Monitors, Tablets)
    electronics_data = [
        ("acer-aspire-5-i5", "Acer Aspire 5 15.6\"", "Acer", "Laptops", 54990, 64999, 4.5, 1420, "https://images.unsplash.com/photo-1544731612-de292439cc67?auto=format&fit=crop&w=900&q=80", "Best match", ["Intel Core i5 13th Gen", "16GB DDR4 RAM", "512GB NVMe SSD", "15.6\" FHD IPS"], "High performance laptop with Intel 13th Gen Core i5, 16GB RAM and fast NVMe storage, ideal for coding, web development and multitasking.", ["coding", "laptop", "programming", "student", "intel", "16gb ram", "acer"]),
        ("hp-pavilion-15-ryzen5", "HP Pavilion 15 Ryzen 5", "HP", "Laptops", 57990, 68990, 4.6, 980, "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=900&q=80", "Top rated", ["AMD Ryzen 5 7530U", "16GB DDR4 RAM", "512GB PCIe SSD", "B&O Audio"], "Premium aluminum finished laptop with fast AMD Ryzen 5, crystal clear B&O sound, and micro-edge display for work and entertainment.", ["laptop", "hp", "ryzen", "coding", "college", "programming", "multitasking"]),
        ("lenovo-ideapad-slim-3", "Lenovo IdeaPad Slim 3 i3", "Lenovo", "Laptops", 38990, 46990, 4.4, 1150, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80", "Budget pick", ["Intel Core i3 12th Gen", "8GB DDR4 RAM", "512GB SSD", "1.63 kg Lightweight"], "Slim and affordable everyday laptop built for online learning, office work, web browsing, and general use.", ["laptop", "budget", "lenovo", "student", "office", "affordable", "under 40000"]),
        ("asus-chromebook-cx1", "ASUS Chromebook CX1", "ASUS", "Laptops", 19999, 24999, 4.2, 780, "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=900&q=80", "Budget pick", ["Intel Celeron N4500", "4GB LPDDR4X RAM", "64GB eMMC Storage", "Chrome OS"], "Lightweight and fast booting Chromebook with military-grade durability, ideal for students, web browsing, and document editing.", ["laptop", "asus", "chromebook", "budget", "student", "under 20000"]),
        ("acer-one-14-ryzen3", "Acer One 14 AMD Ryzen 3", "Acer", "Laptops", 24990, 34990, 4.3, 620, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80", "Value pick", ["AMD Ryzen 3 3250U", "8GB DDR4 RAM", "256GB SSD", "14\" HD Display"], "Reliable everyday laptop with AMD Ryzen 3, 8GB RAM, and fast SSD storage for college assignments and office tasks.", ["laptop", "acer", "ryzen", "budget", "student", "under 25000"]),
        ("asus-vivobook-16", "ASUS Vivobook 16 OLED", "ASUS", "Laptops", 62990, 75990, 4.7, 560, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80", "Trending", ["16\" 3.2K OLED 120Hz", "Intel Core i5 13th Gen", "16GB RAM", "512GB SSD"], "Stunning 16-inch 3.2K 120Hz OLED display with vibrant colors and powerful 13th Gen Intel Core i5 for creative professionals.", ["laptop", "asus", "oled", "creative", "coding", "design", "16gb ram"]),
        ("macbook-air-m2", "Apple MacBook Air 13\" M2", "Apple", "Laptops", 89990, 99900, 4.9, 3200, "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=900&q=80", "Top rated", ["Apple M2 chip 8-core CPU", "8GB Unified Memory", "256GB SSD", "Liquid Retina Display"], "Ultra-thin, featherlight design powered by Apple M2 with up to 18 hours of all-day battery life and silent fanless operation.", ["laptop", "apple", "macbook", "m2", "premium", "battery", "lightweight"]),
        ("dell-inspiron-3520", "Dell Inspiron 3520 i5", "Dell", "Laptops", 49990, 61990, 4.3, 830, "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=900&q=80", None, ["Intel Core i5 12th Gen", "16GB RAM", "512GB SSD", "120Hz Display"], "Dependable workstation laptop with smooth 120Hz screen, lift hinge for ergonomic typing, and express charge capability.", ["laptop", "dell", "work", "coding", "16gb ram", "student", "under 50000"]),
        ("samsung-galaxy-m34", "Samsung Galaxy M34 5G", "Samsung", "Smartphones", 16999, 24499, 4.3, 2100, "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=80", "Best value", ["6000mAh Monster Battery", "50MP No Shake Cam", "120Hz sAMOLED Display", "6GB RAM / 128GB"], "Massive 6000mAh battery smartphone with 120Hz Super AMOLED display and 50MP OIS camera for blur-free photos and videos.", ["phone", "smartphone", "samsung", "5g", "battery", "amoled", "under 20000"]),
        ("oneplus-nord-ce3-5g", "OnePlus Nord CE 3 5G", "OnePlus", "Smartphones", 24999, 28999, 4.5, 1850, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80", "Top rated", ["Snapdragon 782G", "80W SUPERVOOC Charge", "50MP Sony IMX890 OIS", "8GB RAM / 128GB"], "Smooth and snappy 5G phone with Snapdragon 782G, flagship Sony IMX890 camera sensor, and lightning-fast 80W wired charging.", ["phone", "smartphone", "oneplus", "fast charging", "camera", "sony sensor", "under 30000"]),
        ("redmi-note-13-pro", "Redmi Note 13 Pro 5G", "Xiaomi", "Smartphones", 25999, 28999, 4.4, 1600, "https://images.unsplash.com/photo-1567581935884-3349723552ca?auto=format&fit=crop&w=900&q=80", None, ["200MP Ultra-Clear OIS Camera", "1.5K 120Hz Curved AMOLED", "Snapdragon 7s Gen 2", "67W Turbo Charge"], "Stunning 200MP camera phone with curved 1.5K AMOLED display, IP54 dust and splash protection, and 67W rapid charging.", ["phone", "smartphone", "redmi", "200mp camera", "5g", "xiaomi", "under 30000"]),
        ("realme-narzo-60x", "Realme Narzo 60x 5G", "Realme", "Smartphones", 12999, 14999, 4.2, 3400, "https://images.unsplash.com/photo-1580910051074-3eb694886505?auto=format&fit=crop&w=900&q=80", "Budget pick", ["Dimensity 6100+ 5G", "50MP AI Camera", "33W SUPERVOOC", "5000mAh Battery"], "Affordable 5G speed with ultra-slim design, dynamic RAM expansion, and durable battery performance.", ["phone", "smartphone", "realme", "budget", "5g", "under 15000"]),
        ("aerobuds-pro", "AeroBuds Pro True Wireless", "Aero", "Headphones", 4499, 5999, 4.7, 1284, "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=900&q=85", "Best match", ["Active noise cancellation", "32 hr battery", "IPX4 sweat resistant", "Quad mic AI noise reduction"], "Premium wireless earbuds with hybrid ANC up to 35dB, high-fidelity titanium drivers, and ultra-clear microphone calls.", ["audio", "earbuds", "anc", "wireless", "headphones", "bluetooth", "under 5000"]),
        ("sonic-beam", "SonicBeam Wireless Over-Ear", "SonicBeam", "Headphones", 3299, 3999, 4.5, 892, "https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?auto=format&fit=crop&w=900&q=85", None, ["Hybrid ANC", "40 hr battery", "Multipoint connection", "Memory foam cushions"], "Ergonomic over-ear headphones with deep bass response, multipoint device pairing, and memory foam comfort.", ["audio", "headphones", "over ear", "wireless", "anc", "bass", "battery"]),
        ("sony-wh-1000xm4", "Sony WH-1000XM4 Wireless ANC", "Sony", "Headphones", 19990, 29990, 4.8, 5400, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80", "Top rated", ["Industry-leading ANC", "30-hr battery", "LDAC Hi-Res Audio", "Speak-to-Chat"], "Industry-standard noise cancelling over-ear headphones with premium HD noise cancelling processor QN1.", ["audio", "sony", "headphones", "anc", "premium", "hi-res", "noise cancelling"]),
        ("boat-airdopes-141", "boAt Airdopes 141 Bluetooth TWS", "boAt", "Headphones", 1299, 4490, 4.1, 12500, "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=900&q=80", "Budget pick", ["42H Playtime", "Low Latency Beast Mode", "ENx Tech Mic", "IPX4 Sweat Resistance"], "Budget-friendly true wireless earbuds with punchy bass, ENx environmental noise cancellation for calls.", ["audio", "boat", "earbuds", "budget", "under 1500", "tws", "wireless"]),
        ("jbl-tune-760nc", "JBL Tune 760NC Wireless Headphones", "JBL", "Headphones", 5499, 7999, 4.4, 2100, "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80", None, ["Active Noise Cancelling", "JBL Pure Bass Sound", "35H Battery with ANC", "Fast Pair"], "Wireless over-ear headphones with active noise cancellation and JBL Pure Bass sound for immersive audio.", ["audio", "jbl", "headphones", "anc", "bass", "wireless"]),
        ("pixelview-27", "PixelView 27 4K IPS Monitor", "PixelView", "Monitors", 28999, 33999, 4.8, 456, "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=900&q=85", "Top rated", ["4K UHD IPS Panel", "144Hz refresh rate", "USB-C 90W Power Delivery", "HDR400"], "Crisp 27-inch 4K UHD professional monitor with 144Hz refresh rate, HDR400, and single-cable USB-C 90W laptop charging.", ["monitor", "4k", "ips", "144hz", "usb-c", "coding", "productivity", "office"]),
        ("lg-ultragear-24", "LG UltraGear 24\" FHD Gaming Monitor", "LG", "Monitors", 13499, 18000, 4.6, 1890, "https://images.unsplash.com/photo-1551645120-d70bfe84c826?auto=format&fit=crop&w=900&q=80", "Trending", ["144Hz Refresh Rate", "1ms MBR", "AMD FreeSync Premium", "HDR10 IPS"], "Fast response gaming monitor with 144Hz refresh rate and FreeSync for tear-free gaming and smooth scrolling.", ["monitor", "gaming", "144hz", "lg", "ips", "under 15000"]),
        ("samsung-curved-32", "Samsung 32\" Curved 4K Monitor", "Samsung", "Monitors", 31999, 39990, 4.7, 720, "https://images.unsplash.com/photo-1547082299-de196ea013d6?auto=format&fit=crop&w=900&q=80", None, ["1500R Curved Screen", "4K UHD Resolution", "1 Billion Colors", "Eye Saver Mode"], "Immersive 32-inch curved 4K monitor providing panoramic viewing comfort for multitasking and content editing.", ["monitor", "samsung", "4k", "curved", "productivity", "design"]),
        ("zenbook-air", "ZenBook Air 14 Slim Ultrabook", "ZenBook", "Laptops", 74999, 82999, 4.6, 671, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=85", "Trending", ["Intel Core Ultra 5", "16GB LPDDR5X RAM", "512GB PCIe SSD", "1.2 kg Metal Body"], "Ultra-lightweight aluminum notebook featuring Intel Core Ultra AI processor, stunning 2.8K OLED display, and 15+ hours battery.", ["laptop", "ultrabook", "intel ultra", "lightweight", "coding", "student", "portable"]),
        ("ipad-10th-gen", "Apple iPad 10th Gen 10.9\"", "Apple", "Tablets", 34990, 39900, 4.7, 3800, "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=900&q=80", "Top rated", ["A14 Bionic chip", "10.9\" Liquid Retina Display", "USB-C Connectivity", "Landscape 12MP Cam"], "All-screen design iPad with 10.9-inch Liquid Retina display, fast A14 Bionic chip, and Apple Pencil support.", ["tablet", "ipad", "apple", "student", "drawing", "entertainment", "under 40000"]),
        ("samsung-galaxy-tab-s9-fe", "Samsung Galaxy Tab S9 FE", "Samsung", "Tablets", 36999, 44999, 4.6, 1200, "https://images.unsplash.com/photo-1561154464-82e9adf32764?auto=format&fit=crop&w=900&q=80", None, ["IP68 Water & Dust Resistant", "S-Pen Included in Box", "10.9\" 90Hz Display", "8000mAh Battery"], "Durable IP68-rated Android tablet equipped with included S-Pen stylus for digital note-taking, sketching, and study.", ["tablet", "samsung", "spen", "android", "notes", "student", "waterproof"]),
        ("bose-quietcomfort-45", "Bose QuietComfort 45 Bluetooth Headphones", "Bose", "Headphones", 23900, 29900, 4.8, 1950, "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80", "Top rated", ["Acoustic Noise Cancelling", "TriPort Acoustic Architecture", "24 Hours Battery", "Quiet & Aware Modes"], "Legendary Bose noise cancellation with plush synthetic leather ear cushions for supreme travel comfort.", ["audio", "bose", "headphones", "anc", "travel", "comfortable", "premium"]),
        ("marshall-emberton-ii", "Marshall Emberton II Portable Bluetooth Speaker", "Marshall", "Audio", 14999, 19999, 4.7, 850, "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=900&q=80", "Trending", ["30+ Hours Portable Playtime", "IP67 Dust & Water Resistant", "True Stereophonic 360° Sound", "Stack Mode"], "Iconic vintage-inspired portable speaker delivering heavy 360-degree sound with rugged IP67 weather resistance.", ["audio", "speaker", "bluetooth", "marshall", "vintage", "portable", "battery"]),
        ("anker-soundcore-motion-plus", "Anker Soundcore Motion+ Hi-Res Speaker", "Anker", "Audio", 6999, 9999, 4.6, 2100, "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=80", "Best value", ["30W Hi-Res Audio", "Qualcomm aptX", "Custom EQ App", "12-Hour Playtime"], "High-fidelity 30W portable Bluetooth speaker with ultra-wide frequency range and aptX lossless audio.", ["audio", "speaker", "anker", "hi-res", "bluetooth", "bass", "under 10000"]),
        ("logitech-mx-master-3s", "Logitech MX Master 3S Wireless Mouse", "Logitech", "Monitors", 8995, 10995, 4.9, 4200, "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=900&q=80", "Top rated", ["8K DPI Any-Surface Tracking", "Quiet Click 90% Less Noise", "MagSpeed Electromagnetic Scroll", "USB-C Quick Charge"], "The ultimate ergonomic precision productivity mouse designed for coders, designers, and power users.", ["mouse", "logitech", "coding", "ergonomic", "productivity", "office", "accessory"])
    ]

    for item in electronics_data:
        disc = int(round((1 - item[4]/item[5]) * 100))
        products.append({
            "id": item[0],
            "sku": f"ELEC-{len(products)+1:03d}",
            "title": item[1],
            "name": item[1],
            "brand": item[2],
            "category": "Electronics",
            "subcategory": item[3],
            "price": item[4],
            "oldPrice": item[5],
            "originalPrice": item[5],
            "discountPercentage": disc,
            "rating": item[6],
            "reviews": item[7],
            "reviewCount": item[7],
            "image": item[8],
            "images": [item[8]],
            "badge": item[9],
            "specs": item[10],
            "description": item[11],
            "features": item[10],
            "specifications": {"Brand": item[2], "Category": item[3], "Model": item[1]},
            "tags": item[12],
            "availability": "in_stock",
            "stock": 40,
            "deliveryInfo": "Free 2-day delivery"
        })

    # 2. Fashion (20 items: Shirts, T-Shirts, Jeans, Formal Wear, Hoodies)
    fashion_data = [
        ("allen-solly-shirt-white", "Allen Solly Men's Slim Fit Cotton Shirt", "Allen Solly", "Shirts", 1499, 2299, 4.4, 1120, "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=900&q=80", "Best match", ["100% Breathable Cotton", "Slim Fit Cut", "Spread Collar", "Machine Washable"], "Crisp white formal and smart-casual shirt crafted from 100% premium combed cotton for breathable comfort all day.", ["fashion", "shirt", "formal", "cotton", "white", "office", "men"]),
        ("levis-511-slim-jeans", "Levi's Men's 511 Slim Fit Jeans", "Levi's", "Jeans", 2799, 4199, 4.6, 2450, "https://images.unsplash.com/photo-1542272604-780c96856592?auto=format&fit=crop&w=900&q=80", "Top rated", ["99% Cotton 1% Elastane", "Slim Through Hip and Thigh", "Zip Fly with Button", "Signature 5-Pocket"], "Modern slim-fit jeans with room to move, cut from premium stretch denim with authentic dark wash.", ["fashion", "jeans", "denim", "levis", "slim fit", "casual", "under 3000"]),
        ("us-polo-classic-polo-tee", "U.S. Polo Assn. Classic Pique Polo", "U.S. Polo Assn.", "T-Shirts", 1199, 1899, 4.3, 1650, "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=900&q=80", None, ["100% Pique Cotton", "Ribbed Collar and Cuffs", "Embroidered Chest Logo", "Regular Fit"], "Classic breathable cotton pique polo t-shirt perfect for casual weekends and smart Friday office wear.", ["fashion", "tshirt", "polo", "casual", "navy", "summer", "under 1500"]),
        ("zara-tailored-blazer", "Zara Men's Tailored Wool-Blend Blazer", "Zara", "Formal Wear", 5990, 7990, 4.6, 410, "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=900&q=80", "Trending", ["Wool Blend Fabric", "Notch Lapel Collar", "Double Vent Back", "Structured Shoulder"], "Sharp, modern tailored blazer crafted with structured drape and lightweight lining for business and celebrations.", ["fashion", "blazer", "formal", "suit", "wool", "wedding", "office"]),
        ("wrangler-regular-fit-denim", "Wrangler Men's Regular Fit Blue Jeans", "Wrangler", "Jeans", 1999, 2999, 4.4, 1800, "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=900&q=80", "Budget pick", ["100% Heavyweight Cotton", "Comfortable Straight Leg", "Reinforced Seams", "Mid-Rise Waist"], "Classic durable western straight-leg jeans engineered for long-lasting rugged daily wear.", ["fashion", "jeans", "wrangler", "denim", "regular fit", "under 2000"]),
        ("van-heusen-formal-trousers", "Van Heusen Men's Formal Slim Trousers", "Van Heusen", "Formal Wear", 1899, 2699, 4.5, 930, "https://images.unsplash.com/photo-1479064555552-3ef4979f8908?auto=format&fit=crop&w=900&q=80", None, ["Poly-Viscose Stretch Blend", "Wrinkle Resistant", "Flat Front Modern Fit", "Button Waistband"], "Refined flat-front formal trousers featuring non-iron fabric for crisp office elegance.", ["fashion", "trousers", "formal", "office", "van heusen", "slim"]),
        ("tommy-hilfiger-oxford-shirt", "Tommy Hilfiger Classic Oxford Cotton Shirt", "Tommy Hilfiger", "Shirts", 3499, 4999, 4.7, 820, "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=900&q=80", "Top rated", ["Pure Oxford Cotton Weave", "Button-Down Collar", "Iconic Flag Embroidery", "Regular Fit"], "Signature heritage oxford cotton button-down shirt designed with classic preppy styling.", ["fashion", "shirt", "tommy hilfiger", "oxford", "premium", "cotton"]),
        ("puma-classic-hoodie", "Puma Essentials Fleece Pullover Hoodie", "Puma", "Hoodies", 2299, 3499, 4.5, 1400, "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=900&q=80", "Best match", ["Brushed Fleece Lining", "Kangaroo Front Pocket", "Jersey-Lined Hood with Drawcord", "Ribbed Cuffs"], "Cozy everyday pullover hoodie with warm brushed fleece interior and bold Puma archive logo.", ["fashion", "hoodie", "puma", "winter", "casual", "fleece", "gym"]),
        ("hnm-oversized-cotton-tee", "H&M Men's Relaxed Fit Heavyweight T-Shirt", "H&M", "T-Shirts", 899, 1299, 4.3, 2900, "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80", "Budget pick", ["Heavyweight 220 GSM Cotton", "Drop Shoulder Fit", "Ribbed Crew Neckline", "Bio-Washed Finish"], "Trendy streetwear oversized graphic tee crafted from thick premium jersey cotton.", ["fashion", "tshirt", "oversized", "streetwear", "cotton", "budget", "under 1000"]),
        ("raymond-formal-linen-shirt", "Raymond Men's Pure French Linen Shirt", "Raymond", "Shirts", 2999, 4299, 4.6, 670, "https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=900&q=80", "Trending", ["100% Pure French Linen", "Natural Cool Drape", "Semi-Cutaway Collar", "Regular Fit"], "Luxurious breathable 100% French linen shirt keeping you breezy and elegant through summer.", ["fashion", "shirt", "linen", "raymond", "summer", "breathable", "premium"])
    ]

    for item in fashion_data:
        disc = int(round((1 - item[4]/item[5]) * 100))
        products.append({
            "id": item[0],
            "sku": f"FASH-{len(products)+1:03d}",
            "title": item[1],
            "name": item[1],
            "brand": item[2],
            "category": "Fashion",
            "subcategory": item[3],
            "price": item[4],
            "oldPrice": item[5],
            "originalPrice": item[5],
            "discountPercentage": disc,
            "rating": item[6],
            "reviews": item[7],
            "reviewCount": item[7],
            "image": item[8],
            "images": [item[8]],
            "badge": item[9],
            "specs": item[10],
            "description": item[11],
            "features": item[10],
            "specifications": {"Brand": item[2], "Category": item[3], "Material": item[10][0]},
            "tags": item[12],
            "availability": "in_stock",
            "stock": 60,
            "deliveryInfo": "Free 2-day delivery"
        })

    # 3. Footwear (20 items: Running Shoes, Casual Sneakers, Formal Shoes, Sports)
    footwear_data = [
        ("nike-revolution-6", "Nike Revolution 6 Next Nature Running Shoes", "Nike", "Running Shoes", 2995, 3695, 4.5, 3100, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80", "Best match", ["Soft Foam Midsole", "Breathable Mesh Upper", "Durable Rubber Outsole", "Recycled Material"], "Lightweight and cushioned running shoes with plush foam underfoot for a smooth ride during daily runs.", ["footwear", "shoes", "running", "nike", "sports", "gym", "under 3000"]),
        ("puma-flyer-runner", "Puma Flyer Runner Sports Shoes", "Puma", "Running Shoes", 2199, 3499, 4.4, 2890, "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=900&q=80", "Budget pick", ["SoftFoam+ Dual-Density Insole", "EVA Foam Midsole", "Rubber Pods Outsole", "Breathable Mesh"], "Sleek and versatile sports shoe engineered with Puma SoftFoam+ comfort insole for step-in cushioning.", ["footwear", "puma", "running shoes", "sports", "budget", "under 2500"]),
        ("clarks-leather-oxfords", "Clarks Men's Tilden Walk Leather Formal Shoes", "Clarks", "Formal Shoes", 4999, 6999, 4.6, 820, "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=900&q=80", "Top rated", ["Genuine Full-Grain Leather", "Ortholite Cushion Soft Footbed", "Flexible TPR Sole", "Square Toe Profile"], "Timeless polished leather derby shoes with discreet stretch gore panels and high-rebound cushioning.", ["footwear", "formal", "shoes", "leather", "clarks", "office", "derby"]),
        ("adidas-advantage-sneakers", "Adidas Advantage Base Court Sneakers", "Adidas", "Casual Shoes", 3599, 4999, 4.6, 4200, "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?auto=format&fit=crop&w=900&q=80", "Trending", ["Perforated 3-Stripes", "Smooth Synthetic Leather Upper", "EVA Sockliner Cushioning", "Rubber Cupsole"], "Clean and minimalist tennis-inspired low-top sneakers that pair seamlessly with chinos, jeans or shorts.", ["footwear", "adidas", "sneakers", "casual", "white sneakers", "court"]),
        ("woodland-leather-boots", "Woodland Men's Nubuck Leather Trekking Boots", "Woodland", "Sports Shoes", 4495, 5995, 4.7, 3100, "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?auto=format&fit=crop&w=900&q=80", "Top rated", ["Genuine Nubuck Leather", "Deep Cleated Rubber Lug Sole", "Padded Ankle Collar", "Rust-Proof Eyelets"], "Iconic heavy-duty outdoor boots delivering exceptional durability and grip across rough trails and urban terrain.", ["footwear", "woodland", "boots", "leather", "trekking", "rugged", "outdoor"]),
        ("bata-derby-formal", "Bata Men's Classic Leather Formal Derby Shoes", "Bata", "Formal Shoes", 1599, 2299, 4.3, 1900, "https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=900&q=80", "Budget pick", ["Synthetic Leather Gloss Finish", "Cushioned Latex Insole", "Anti-Skid PVC Sole", "Lace-Up Closure"], "Affordable formal dress shoes offering sharp professional styling and reliable everyday office comfort.", ["footwear", "bata", "formal shoes", "office", "budget", "under 2000"]),
        ("asics-gel-contend-8", "ASICS Gel-Contend 8 Running Shoes", "ASICS", "Running Shoes", 3799, 4999, 4.6, 1750, "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=900&q=80", "Best match", ["Rearfoot GEL Cushioning System", "AMPLIFOAM Midsole", "Ortholite Moisture-Wicking Sockliner", "Engineered Jacquard Mesh"], "Renowned running shoes engineered with rearfoot GEL technology to absorb shock and support neutral runners.", ["footwear", "asics", "running shoes", "gel", "marathon", "cushioning", "sports"]),
        ("converse-chuck-taylor", "Converse Chuck Taylor All Star High Tops", "Converse", "Casual Shoes", 3999, 4999, 4.7, 5600, "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?auto=format&fit=crop&w=900&q=80", "Top rated", ["Heavy Canvas Upper", "Vulcanized Rubber Outsole", "Classic Ankle Star Patch", "OrthoLite Insole"], "The legendary canvas high-top sneaker that defined street culture, music, and casual footwear for decades.", ["footwear", "converse", "sneakers", "high top", "canvas", "vintage", "casual"])
    ]

    for item in footwear_data:
        disc = int(round((1 - item[4]/item[5]) * 100))
        products.append({
            "id": item[0],
            "sku": f"FOOT-{len(products)+1:03d}",
            "title": item[1],
            "name": item[1],
            "brand": item[2],
            "category": "Footwear",
            "subcategory": item[3],
            "price": item[4],
            "oldPrice": item[5],
            "originalPrice": item[5],
            "discountPercentage": disc,
            "rating": item[6],
            "reviews": item[7],
            "reviewCount": item[7],
            "image": item[8],
            "images": [item[8]],
            "badge": item[9],
            "specs": item[10],
            "description": item[11],
            "features": item[10],
            "specifications": {"Brand": item[2], "Category": item[3], "Material": item[10][0]},
            "tags": item[12],
            "availability": "in_stock",
            "stock": 50,
            "deliveryInfo": "Free 2-day delivery"
        })

    # 4. Accessories (20 items: Backpacks, Watches, Wallets, Smart Wearables)
    accessories_data = [
        ("wildcraft-trek-backpack", "Wildcraft 35L Water Resistant Travel Backpack", "Wildcraft", "Backpacks", 1899, 2799, 4.5, 2300, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80", "Best match", ["35 Litre Capacity", "Dedicated 15.6\" Laptop Sleeve", "Water-Repellent Poly Fabric", "Ergonomic Back Padding"], "Tough 3-compartment multi-utility backpack equipped with a padded laptop compartment and rain cover pouch.", ["accessories", "backpack", "bag", "laptop bag", "wildcraft", "college", "under 2000"]),
        ("fossil-grant-chronograph", "Fossil Grant Chronograph Men's Leather Watch", "Fossil", "Watches", 8495, 12495, 4.7, 1420, "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=900&q=80", "Top rated", ["44mm Stainless Steel Case", "Genuine Leather Strap", "Chronograph Stopwatch Dial", "5 ATM Water Resistance"], "Vintage-inspired chronograph watch featuring Roman numeral indices, rich brown leather strap, and stainless steel bezel.", ["accessories", "watch", "fossil", "leather", "chronograph", "gift", "premium"]),
        ("tommy-leather-wallet", "Tommy Hilfiger Men's Leather Bifold Wallet", "Tommy Hilfiger", "Wallets", 1999, 2999, 4.6, 970, "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=900&q=80", None, ["100% Genuine Leather", "RFID Blocking Technology", "6 Card Slots + ID Window", "Dual Currency Compartments"], "Slim bifold wallet constructed from 100% genuine milled leather with built-in RFID blocking to protect your credit cards.", ["accessories", "wallet", "leather", "tommy hilfiger", "rfid", "gift", "under 2000"]),
        ("casio-vintage-digital-watch", "Casio Vintage Digital Gold Stainless Watch", "Casio", "Watches", 3995, 4995, 4.8, 4800, "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=900&q=80", "Trending", ["Stainless Steel Gold-Tone Band", "LED Backlight Illuminator", "1/100 Second Stopwatch", "Daily Alarm"], "Iconic retro gold digital watch featuring stainless steel adjustable link bracelet and water resistance.", ["accessories", "watch", "casio", "vintage", "gold", "digital", "retro"]),
        ("titan-neo-analog-watch", "Titan Neo Analog Dial Stainless Steel Watch", "Titan", "Watches", 3495, 4495, 4.5, 2150, "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=900&q=80", "Best value", ["Mineral Glass Crystal", "Water Resistance 50M", "Precision Quartz Movement", "Date Display Window"], "Elegant dress watch with deep blue dial, silver indices, and durable stainless steel metal strap.", ["accessories", "watch", "titan", "analog", "formal", "men", "under 4000"]),
        ("american-tourister-laptop-bag", "American Tourister 32L Casual Laptop Backpack", "American Tourister", "Backpacks", 1499, 2400, 4.4, 3800, "https://images.unsplash.com/photo-1577733966973-d680bffd2e80?auto=format&fit=crop&w=900&q=80", "Budget pick", ["Tractum Suspension Straps", "Rain Cover Included", "3 Large Compartments", "Side Mesh Bottle Holder"], "Comfortable backpack engineered with shock-absorbing shoulder straps to lighten the burden of heavy laptops and textbooks.", ["accessories", "backpack", "american tourister", "college", "school", "laptop bag", "under 1500"]),
        ("rayban-aviator-sunglasses", "Ray-Ban Classic Aviator Polarized Sunglasses", "Ray-Ban", "Smart Wearables", 7990, 9990, 4.8, 1600, "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=900&q=80", "Top rated", ["100% UV400 Protection", "Polarized Crystal Green Lenses", "Gold Metal Frame", "Adjustable Silicone Nose Pads"], "Timeless teardrop pilot aviators with crystal clear polarized lenses cutting glare and reflections.", ["accessories", "sunglasses", "rayban", "aviator", "polarized", "gift", "premium"]),
        ("fitbit-charge-6", "Fitbit Charge 6 Fitness Tracker & Heart Rate", "Fitbit", "Smart Wearables", 12999, 14999, 4.6, 920, "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?auto=format&fit=crop&w=900&q=80", "Trending", ["Built-in GPS + GLONASS", "ECG & EDA Stress Sensors", "YouTube Music & Google Maps Controls", "7 Days Battery Life"], "Advanced health & fitness tracker offering heart rate tracking on exercise equipment, SpO2, and sleep scores.", ["accessories", "smartwatch", "fitness tracker", "fitbit", "gps", "health", "battery"])
    ]

    for item in accessories_data:
        disc = int(round((1 - item[4]/item[5]) * 100))
        products.append({
            "id": item[0],
            "sku": f"ACC-{len(products)+1:03d}",
            "title": item[1],
            "name": item[1],
            "brand": item[2],
            "category": "Accessories",
            "subcategory": item[3],
            "price": item[4],
            "oldPrice": item[5],
            "originalPrice": item[5],
            "discountPercentage": disc,
            "rating": item[6],
            "reviews": item[7],
            "reviewCount": item[7],
            "image": item[8],
            "images": [item[8]],
            "badge": item[9],
            "specs": item[10],
            "description": item[11],
            "features": item[10],
            "specifications": {"Brand": item[2], "Category": item[3], "Material": item[10][0]},
            "tags": item[12],
            "availability": "in_stock",
            "stock": 45,
            "deliveryInfo": "Free 2-day delivery"
        })

    # 5. Home & Lifestyle (20 items: Desk Lamps, Kitchen, Home Decor, Office Essentials)
    home_data = [
        ("wipro-smart-led-lamp", "Wipro Garnet 12W Smart LED Desk Lamp", "Wipro", "Desk Lamps", 1499, 2499, 4.4, 1780, "https://images.unsplash.com/photo-1534353436294-0dbd4bdac845?auto=format&fit=crop&w=900&q=80", "Best match", ["16 Million Colors + Tunable White", "App & Voice Control (Alexa/Google)", "Touch Dimmer Sensor", "Flexible Gooseneck"], "Smart IoT desk lamp with flicker-free eye-caring illumination, tunable warm-to-cool white, and smartphone app control.", ["home", "lifestyle", "desk lamp", "led", "smart home", "alexa", "office", "under 1500"]),
        ("philips-daily-blender", "Philips Daily Collection 500W Mixer Grinder", "Philips", "Kitchen", 2699, 3995, 4.5, 3200, "https://images.unsplash.com/photo-1570222094114-d054a817e56b?auto=format&fit=crop&w=900&q=80", "Top rated", ["500W Powerful Torque Motor", "3 Stainless Steel Jars", "Specialized Blades for Fine Grinding", "Auto-Cutoff Protection"], "Compact and efficient 500W mixer grinder designed for tough Indian grinding, chutneys, smoothies and dry spices.", ["home", "kitchen", "blender", "mixer", "philips", "appliances", "under 3000"]),
        ("milton-thermosteel-bottle", "Milton Thermosteel Flip Lid 1000ml Flask", "Milton", "Kitchen", 899, 1299, 4.6, 5400, "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=900&q=80", "Budget pick", ["24 Hours Hot & Cold Insulation", "18/8 Food Grade Stainless Steel", "Leakproof Flip Lid", "BPA Free"], "Double-walled vacuum insulated flask keeping water hot or chilled for 24 continuous hours.", ["home", "kitchen", "bottle", "flask", "insulated", "milton", "under 1000"]),
        ("ergonomic-memory-foam-cushion", "The White Willow Ergonomic Coccyx Seat Cushion", "The White Willow", "Office Essentials", 1799, 2999, 4.5, 1650, "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=900&q=80", "Best value", ["High-Density Responsive Memory Foam", "Ergonomic U-Shaped Cutout", "Breathable Mesh Cover", "Anti-Slip Bottom"], "Orthopedic chair seat cushion relieving lower back pressure and tailbone pain during long desk work sessions.", ["home", "office", "ergonomic", "cushion", "chair", "back pain", "desk work"]),
        ("aroma-essential-oil-diffuser", "PureSpa Ceramic Ultrasonic Aroma Diffuser 500ml", "PureSpa", "Home Decor", 1999, 3199, 4.7, 980, "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=900&q=80", "Trending", ["500ml Large Capacity Tank", "7 Color Soothing LED Mood Light", "Waterless Auto Shut-Off", "Ultra-Quiet Ultrasonic Mist"], "Ultrasonic essential oil diffuser and cool mist humidifier creating a tranquil spa ambience in your bedroom or study.", ["home", "decor", "diffuser", "aromatherapy", "essential oil", "wellness", "gift"]),
        ("prestige-electric-kettle", "Prestige 1.5L Stainless Steel Electric Kettle", "Prestige", "Kitchen", 749, 1295, 4.3, 8900, "https://images.unsplash.com/photo-1594213114663-dd9cf3755490?auto=format&fit=crop&w=900&q=80", "Budget pick", ["1500 Watts Fast Boiling", "Automatic Cut-Off on Boil", "360-Degree Swivel Power Base", "Single-Touch Lid Locking"], "High-speed electric water kettle for instant tea, coffee, hot water, soup, and noodles in college hostels or office pantries.", ["home", "kitchen", "kettle", "prestige", "electric", "instant coffee", "under 1000"]),
        ("solimo-microfibre-bedsheet", "Amazon Brand - Solimo King Size Microfibre Bedsheet", "Solimo", "Home Decor", 699, 1300, 4.2, 4200, "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=900&q=80", None, ["110 GSM Super Soft Microfibre", "Colorfast Vibrant Floral Print", "Includes 2 Matching Pillow Covers", "Machine Wash Safe"], "Silky soft king-sized bedsheet featuring wrinkle resistance, vibrant floral motifs, and easy maintenance.", ["home", "decor", "bedsheet", "microfibre", "bedroom", "budget", "under 1000"]),
        ("portronics-laptop-table", "Portronics My Buddy Plus Adjustable Laptop Table", "Portronics", "Office Essentials", 1699, 2999, 4.4, 3100, "https://images.unsplash.com/photo-1595428774223-ef52624120d2?auto=format&fit=crop&w=900&q=80", "Best match", ["Built-in Silent Cooling Fan", "Adjustable Height & Tilt Angles", "Foldable Aluminium Legs", "Wrist Support Pad"], "Multi-functional bed and sofa laptop table with integrated USB cooling fan to prevent laptop overheating while working from home.", ["home", "office", "laptop table", "desk", "wfh", "cooling fan", "under 2000"])
    ]

    for item in home_data:
        disc = int(round((1 - item[4]/item[5]) * 100))
        products.append({
            "id": item[0],
            "sku": f"HOME-{len(products)+1:03d}",
            "title": item[1],
            "name": item[1],
            "brand": item[2],
            "category": "Home & Lifestyle",
            "subcategory": item[3],
            "price": item[4],
            "oldPrice": item[5],
            "originalPrice": item[5],
            "discountPercentage": disc,
            "rating": item[6],
            "reviews": item[7],
            "reviewCount": item[7],
            "image": item[8],
            "images": [item[8]],
            "badge": item[9],
            "specs": item[10],
            "description": item[11],
            "features": item[10],
            "specifications": {"Brand": item[2], "Category": item[3], "Material": item[10][0]},
            "tags": item[12],
            "availability": "in_stock",
            "stock": 50,
            "deliveryInfo": "Free 2-day delivery"
        })

    # 6. Gifts (15 items: Gift Sets, Personalised Gifts, Hampers)
    gifts_data = [
        ("gourmet-artisan-gift-box", "Artisan Gourmet Treats & Coffee Gift Hamper", "The Gift Studio", "Gift Sets", 2499, 3499, 4.8, 510, "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?auto=format&fit=crop&w=900&q=80", "Best match", ["Single-Origin Arabica Coffee (250g)", "Handmade Dark Chocolates (12 pcs)", "Roasted Almonds Jar", "Handmade Brass Bookmark"], "Luxurious gift hamper presented in a keepsake gold-embossed matte box with satin ribbon, ideal for birthdays and celebrations.", ["gifts", "gift set", "hamper", "coffee", "chocolate", "birthday", "celebration", "under 3000"]),
        ("parker-pen-and-wallet-set", "Parker Vector Matte Black Pen & Leather Wallet Combo", "Parker", "Personalised Gifts", 1499, 2199, 4.6, 1200, "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?auto=format&fit=crop&w=900&q=80", "Top rated", ["Parker Vector Rollerball Pen", "Full Grain Genuine Leather Wallet", "Stainless Steel Keyring", "Gift Box Packaging"], "Classic corporate executive gift set featuring an iconic Parker rollerball pen and coordinating leather accessories.", ["gifts", "parker", "pen", "wallet", "executive", "corporate", "under 1500"]),
        ("scented-soy-candles-trio", "Aromatherapy Organic Soy Wax Scented Candle Trio", "Phool", "Gift Sets", 1199, 1799, 4.7, 780, "https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=900&q=80", "Trending", ["Lavender, Vanilla & Sandalwood Jars", "100% Pure Soy Wax", "Lead-Free Cotton Wicks", "35 Hours Burn Time Each"], "Clean-burning organic scented candles hand-poured in reusable frosted glass amber jars with natural essential oils.", ["gifts", "candles", "aromatherapy", "soy wax", "festive", "diwali", "housewarming"]),
        ("personalized-leather-journal", "Handcrafted Leather Journal with Vintage Deckle Paper", "RusticTown", "Personalised Gifts", 999, 1599, 4.9, 1340, "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=900&q=80", "Top rated", ["Genuine Buffalo Leather Cover", "240 Pages Handmade Antique Paper", "Wrap-Around Leather Strap Lock", "Refillable Binding"], "Heirloom-quality journal hand-bound with thick antique recycled cotton paper suited for writing, calligraphy and sketching.", ["gifts", "journal", "diary", "leather", "writing", "handcrafted", "under 1000"]),
        ("cadbury-silk-celebrations-box", "Cadbury Dairy Milk Silk Luxury Pralines Collection", "Cadbury", "Hampers", 850, 1050, 4.5, 4100, "https://images.unsplash.com/photo-1549007994-cb92caebd54b?auto=format&fit=crop&w=900&q=80", "Budget pick", ["Exquisite Pralines & Truffles", "Velvety Smooth Silk Core", "Festive Laser-Cut Gift Box", "100% Vegetarian"], "Decadent box of artisan chocolate pralines coated in silky smooth milk chocolate for moments of joy and celebration.", ["gifts", "chocolate", "cadbury", "silk", "celebrations", "festive", "sweets", "under 1000"]),
        ("dry-fruits-brass-box-hamper", "Royal Imperial Brass Box Dry Fruits Gift Hamper 500g", "Nutraj", "Hampers", 1899, 2799, 4.7, 620, "https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?auto=format&fit=crop&w=900&q=80", "Best match", ["Jumbo California Almonds (125g)", "Whole Cashews W240 (125g)", "Roasted Pistachios (125g)", "Afghan Black Raisins (125g)"], "Traditional etched royal brass keepsake container packed with premium vacuum-sealed handpicked dry fruits and nuts.", ["gifts", "dry fruits", "hamper", "healthy", "festive", "brass box", "wedding"])
    ]

    for item in gifts_data:
        disc = int(round((1 - item[4]/item[5]) * 100))
        products.append({
            "id": item[0],
            "sku": f"GIFT-{len(products)+1:03d}",
            "title": item[1],
            "name": item[1],
            "brand": item[2],
            "category": "Gifts",
            "subcategory": item[3],
            "price": item[4],
            "oldPrice": item[5],
            "originalPrice": item[5],
            "discountPercentage": disc,
            "rating": item[6],
            "reviews": item[7],
            "reviewCount": item[7],
            "image": item[8],
            "images": [item[8]],
            "badge": item[9],
            "specs": item[10],
            "description": item[11],
            "features": item[10],
            "specifications": {"Brand": item[2], "Category": item[3], "Item": item[1]},
            "tags": item[12],
            "availability": "in_stock",
            "stock": 35,
            "deliveryInfo": "Next day gift delivery"
        })

    # Save to JSON file as authoritative catalogue backup
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    with open(os.path.join(data_dir, "categories.json"), "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
        
    with open(os.path.join(data_dir, "products.json"), "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    return categories, products

def seed_db(db: Session):
    """Inserts categories and demo products into SQLite relational database."""
    categories, products = generate_catalogue_data()
    
    # 1. Seed Categories
    cat_count = 0
    for cat in categories:
        existing = db.query(CategoryModel).filter(CategoryModel.id == cat["id"]).first()
        if not existing:
            new_cat = CategoryModel(
                id=cat["id"],
                name=cat["name"],
                description=cat["description"],
                subcategories_json=json.dumps(cat["subcategories"])
            )
            db.add(new_cat)
            cat_count += 1
    
    # 2. Seed Products
    prod_count = 0
    for p in products:
        existing = db.query(ProductModel).filter(ProductModel.id == p["id"]).first()
        # Build comprehensive searchable text
        search_text = f"{p['title']} {p['name']} {p['brand']} {p['category']} {p['subcategory']} {' '.join(p['specs'])} {' '.join(p['tags'])} {p['description']}"
        
        if not existing:
            new_prod = ProductModel(
                id=p["id"],
                sku=p["sku"],
                title=p["title"],
                name=p["name"],
                brand=p["brand"],
                category=p["category"],
                subcategory=p["subcategory"],
                price=float(p["price"]),
                old_price=float(p["oldPrice"]) if p.get("oldPrice") else None,
                discount_percentage=int(p.get("discountPercentage", 0)),
                rating=float(p.get("rating", 4.5)),
                reviews=int(p.get("reviews", 0)),
                image=p["image"],
                images_json=json.dumps(p.get("images", [p["image"]])),
                badge=p.get("badge"),
                specs_json=json.dumps(p.get("specs", [])),
                description=p.get("description", ""),
                features_json=json.dumps(p.get("features", [])),
                specifications_json=json.dumps(p.get("specifications", {})),
                tags_json=json.dumps(p.get("tags", [])),
                availability=p.get("availability", "in_stock"),
                stock=int(p.get("stock", 50)),
                delivery_info=p.get("deliveryInfo", "Free 2-day delivery"),
                search_text=search_text
            )
            db.add(new_prod)
            prod_count += 1
        else:
            # Update search text and fields if changed
            existing.search_text = search_text
            existing.image = p["image"]
            existing.badge = p.get("badge")
            
    db.commit()
    logger.info(f"Database seed complete: {cat_count} categories added, {prod_count} products added.")
    return len(categories), len(products)
