from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Educational starter database. Always follow your local municipality's rules.
WASTE_DB = {
    "plastic bottle": {
        "category": "DRY / RECYCLABLE WASTE", "bin": "BLUE BIN",
        "icon": "♻️", "why": "Clean plastic bottles may be collected and processed into new products. Empty and rinse them if your local recycling service requires it.",
        "instructions": "Empty the bottle, rinse if needed, and place it with accepted dry recyclables."
    },
    "water bottle": {
        "category": "DRY / RECYCLABLE WASTE", "bin": "BLUE BIN",
        "icon": "♻️", "why": "Many water bottles are made from recyclable plastic, but acceptance depends on local collection rules.",
        "instructions": "Empty it and check whether your local service accepts the plastic type."
    },
    "paper": {
        "category": "DRY / RECYCLABLE WASTE", "bin": "BLUE BIN",
        "icon": "📄", "why": "Clean, dry paper can often be pulped and made into new paper products.",
        "instructions": "Keep paper dry. Greasy or food-soiled paper may not be recyclable."
    },
    "newspaper": {
        "category": "DRY / RECYCLABLE WASTE", "bin": "BLUE BIN",
        "icon": "📰", "why": "Newspapers are commonly recyclable when kept clean and dry.",
        "instructions": "Bundle or place with paper recyclables according to local rules."
    },
    "cardboard": {
        "category": "DRY / RECYCLABLE WASTE", "bin": "BLUE BIN",
        "icon": "📦", "why": "Clean cardboard can be pulped and reused to make paperboard products.",
        "instructions": "Flatten boxes and keep them dry. Remove food-contaminated sections."
    },
    "glass bottle": {
        "category": "DRY / RECYCLABLE WASTE", "bin": "BLUE BIN / GLASS COLLECTION",
        "icon": "🍾", "why": "Glass can often be recycled repeatedly, but collection systems differ by location.",
        "instructions": "Do not put broken glass loose into a bin. Use your local glass collection method."
    },
    "metal can": {
        "category": "DRY / RECYCLABLE WASTE", "bin": "BLUE BIN / METAL COLLECTION",
        "icon": "🥫", "why": "Aluminium and steel can often be recycled into new metal products.",
        "instructions": "Empty the can and follow local guidance for rinsing and sorting metals."
    },
    "aluminium can": {
        "category": "DRY / RECYCLABLE WASTE", "bin": "BLUE BIN / METAL COLLECTION",
        "icon": "🥫", "why": "Aluminium is valuable to recover and can be recycled when accepted by local facilities.",
        "instructions": "Empty the can and place it with accepted metal recyclables."
    },
    "banana peel": {
        "category": "ORGANIC / BIODEGRADABLE WASTE", "bin": "GREEN BIN",
        "icon": "🌱", "why": "Food scraps can break down naturally and may be composted.",
        "instructions": "Put it in a food-waste or compost collection container where available."
    },
    "vegetable scraps": {
        "category": "ORGANIC / BIODEGRADABLE WASTE", "bin": "GREEN BIN",
        "icon": "🥬", "why": "Many vegetable scraps can be composted into a soil amendment.",
        "instructions": "Keep them separate from plastic and other non-compostable materials."
    },
    "food waste": {
        "category": "ORGANIC / BIODEGRADABLE WASTE", "bin": "GREEN BIN",
        "icon": "🍎", "why": "Separating food waste allows it to be composted or treated separately.",
        "instructions": "Use your local food-waste collection or composting system."
    },
    "eggshell": {
        "category": "ORGANIC / BIODEGRADABLE WASTE", "bin": "GREEN BIN",
        "icon": "🥚", "why": "Eggshells can be added to many home compost systems.",
        "instructions": "Check your composting system's guidance."
    },
    "food wrapper": {
        "category": "RESIDUAL / CHECK LOCAL RULES", "bin": "OTHER / RESIDUAL WASTE",
        "icon": "🧃", "why": "Many flexible or multi-layer wrappers are difficult to recycle through ordinary household collection.",
        "instructions": "Check local take-back or recycling programmes before placing it in residual waste."
    },
    "chip packet": {
        "category": "RESIDUAL / CHECK LOCAL RULES", "bin": "OTHER / RESIDUAL WASTE",
        "icon": "🍟", "why": "Snack packets are often made from multiple bonded layers that are not accepted in standard recycling.",
        "instructions": "Use a specialist collection programme if one is available."
    },
    "thermocol": {
        "category": "SPECIAL / CHECK LOCAL RULES", "bin": "SPECIAL COLLECTION IF AVAILABLE",
        "icon": "🧊", "why": "Expanded polystyrene is bulky and is not accepted by many household recycling programmes.",
        "instructions": "Check with your local waste service before disposal."
    },
    "battery": {
        "category": "HAZARDOUS / E-WASTE", "bin": "BATTERY COLLECTION POINT",
        "icon": "🔋", "why": "Batteries may contain reactive chemicals and metals, and can cause fires if damaged or mixed with general waste.",
        "instructions": "Never burn or puncture a battery. Keep terminals protected and take it to an authorised collection point."
    },
    "lithium battery": {
        "category": "HAZARDOUS / E-WASTE", "bin": "BATTERY COLLECTION POINT",
        "icon": "🔋", "why": "Lithium batteries can catch fire if crushed, short-circuited, or damaged.",
        "instructions": "Do not put it in household bins. Keep it away from heat and use an authorised battery collection point."
    },
    "mobile phone": {
        "category": "E-WASTE", "bin": "AUTHORISED E-WASTE COLLECTION",
        "icon": "📱", "why": "Phones contain reusable materials and components, as well as parts that need safe handling.",
        "instructions": "Back up and erase personal data, remove SIM/memory cards, and use an authorised e-waste recycler."
    },
    "laptop": {
        "category": "E-WASTE", "bin": "AUTHORISED E-WASTE COLLECTION",
        "icon": "💻", "why": "Computers contain recoverable metals and electronic parts that should not be mixed with household waste.",
        "instructions": "Back up and securely erase personal data, then use an authorised e-waste collection service."
    },
    "charger": {
        "category": "E-WASTE", "bin": "AUTHORISED E-WASTE COLLECTION",
        "icon": "🔌", "why": "Chargers contain wires, plastics, and electronic components that can be recovered or treated safely.",
        "instructions": "Keep it out of general waste and take it to an authorised e-waste collection point."
    },
    "earphones": {
        "category": "E-WASTE", "bin": "AUTHORISED E-WASTE COLLECTION",
        "icon": "🎧", "why": "Earphones combine wires, plastics, and electronic components that need specialist handling.",
        "instructions": "Use an e-waste collection point or retailer take-back scheme where available."
    },
    "keyboard": {
        "category": "E-WASTE", "bin": "AUTHORISED E-WASTE COLLECTION",
        "icon": "⌨️", "why": "Keyboards contain electronic components and mixed materials that can be separated by specialist recyclers.",
        "instructions": "Take it to an authorised e-waste recycler."
    },
    "mouse": {
        "category": "E-WASTE", "bin": "AUTHORISED E-WASTE COLLECTION",
        "icon": "🖱️", "why": "Computer mice contain electronic parts and mixed materials.",
        "instructions": "Take it to an authorised e-waste collection point."
    },
    "bulb": {
        "category": "SPECIAL WASTE", "bin": "SPECIAL COLLECTION POINT",
        "icon": "💡", "why": "Some bulbs, especially fluorescent lamps, may contain hazardous substances and need special handling.",
        "instructions": "Do not break it. Check local guidance for the bulb type and collection method."
    },
    "medicine": {
        "category": "SPECIAL / PHARMACEUTICAL WASTE", "bin": "PHARMACY OR AUTHORISED TAKE-BACK",
        "icon": "💊", "why": "Medicines can harm people and the environment if disposed of incorrectly.",
        "instructions": "Ask a pharmacy or local authority about safe medicine disposal; do not flush unless specifically instructed."
    },
    "cloth": {
        "category": "REUSE / TEXTILE COLLECTION", "bin": "TEXTILE COLLECTION OR DONATION",
        "icon": "👕", "why": "Wearable textiles may be reused, while damaged textiles may need a specialist collection route.",
        "instructions": "Donate clean wearable clothes or check local textile recycling options."
    },
    "wood": {
        "category": "REUSABLE / BULKY WASTE", "bin": "LOCAL BULKY-WASTE COLLECTION",
        "icon": "🪵", "why": "Untreated wood may be reused or recycled, but painted or treated wood may need different handling.",
        "instructions": "Separate untreated wood where possible and check local collection rules."
    },
}


# Expanded product catalogue: 50 additional examples in each of six categories.
# Entries use cautious, educational guidance because local collection rules differ.
PRODUCT_GROUPS = {
    "DRY / RECYCLABLE WASTE": {
        "bin": "BLUE BIN / LOCAL RECYCLING COLLECTION", "icon": "♻️",
        "why": "This item may contain material that can be recovered and processed when clean and accepted by a local recycling service.",
        "instructions": "Empty and clean it when appropriate, keep it dry, and check local acceptance rules.",
        "items": [
            "plastic milk jug", "detergent bottle", "shampoo bottle", "conditioner bottle", "clean yogurt tub",
            "plastic food container", "plastic takeaway container", "plastic lid", "plastic bucket", "plastic plant pot",
            "newspaper insert", "magazine", "office paper", "writing paper", "envelope",
            "paper bag", "paperboard box", "cereal box", "egg carton", "greeting card",
            "telephone directory", "catalogue", "corrugated box", "shipping box", "paper packaging",
            "glass jar", "jam jar", "sauce bottle", "beverage glass bottle", "glass food jar",
            "aluminium foil clean", "aluminium tray clean", "steel food tin", "soup can", "soda can",
            "metal lid", "metal jar lid", "scrap aluminium", "scrap steel", "copper wire clean",
            "metal hanger", "small metal pot", "metal pan", "metal food tin", "empty aerosol can",
            "plastic detergent container", "plastic cooking oil bottle", "clear plastic container", "hard plastic packaging", "recyclable beverage carton"
        ]
    },
    "ORGANIC / BIODEGRADABLE WASTE": {
        "bin": "GREEN BIN / COMPOST COLLECTION", "icon": "🌱",
        "why": "This organic material can often break down naturally and may be suitable for composting or food-waste treatment.",
        "instructions": "Keep it separate from plastic and other contaminants. Check what your local compost service accepts.",
        "items": [
            "apple core", "orange peel", "lemon peel", "mango peel", "watermelon rind",
            "pineapple skin", "papaya peel", "grape stems", "strawberry tops", "avocado skin",
            "potato peels", "carrot peels", "onion skins", "garlic skins", "cucumber ends",
            "tomato scraps", "lettuce leaves", "cabbage leaves", "spinach stems", "corn husk",
            "corn cob", "tea leaves", "used tea bag compostable", "coffee grounds", "coffee filter paper",
            "rice leftovers", "bread scraps", "plain cooked pasta", "plain cooked rice", "oatmeal leftovers",
            "fruit scraps", "salad leftovers", "stale bread", "crushed eggshells", "nut shells",
            "coconut husk", "dry leaves", "grass clippings", "small twigs", "flower stems",
            "wilted flowers", "houseplant leaves", "untreated sawdust", "untreated wood shavings", "small weeds",
            "pumpkin seeds", "bean pods", "pea pods", "herb stems", "uncoated paper napkin food-soiled"
        ]
    },
    "RESIDUAL / CHECK LOCAL RULES": {
        "bin": "OTHER / RESIDUAL WASTE", "icon": "🗑️",
        "why": "This item may not be accepted in ordinary recycling or compost collection because of mixed materials, contamination, or local restrictions.",
        "instructions": "Reduce and reuse where possible. Check local guidance before placing it in residual waste.",
        "items": [
            "used tissue", "paper towel greasy", "greasy pizza box", "wax-coated paper cup", "disposable coffee cup",
            "plastic straw", "plastic cutlery", "plastic toothbrush", "toothpaste tube", "squeezable food pouch",
            "multi-layer snack wrapper", "candy wrapper", "instant noodle packet", "biscuit wrapper", "plastic cling film",
            "contaminated plastic wrap", "dirty takeaway box", "foam food tray", "foam cup", "broken ceramic mug",
            "ceramic plate", "porcelain bowl", "mirror shard safely wrapped", "window glass shard safely wrapped", "broken drinking glass safely wrapped",
            "vacuum cleaner dust", "sweeping dust", "pet litter", "dog waste bag", "sanitary pad",
            "diaper", "wet wipe", "cotton swab", "cotton ball", "bandage",
            "disposable mask", "rubber glove", "sponge", "scouring pad", "cigarette butt",
            "chewing gum", "ballpoint pen", "marker pen", "laminated paper", "plastic-coated gift wrap",
            "glitter paper", "broken plastic toy mixed materials", "contaminated foil", "small mixed-material packaging"
        ]
    },
    "HAZARDOUS / SPECIAL WASTE": {
        "bin": "AUTHORISED SPECIAL-WASTE COLLECTION", "icon": "⚠️",
        "why": "This item may contain chemicals, sharp parts, or substances that need special handling to protect people and the environment.",
        "instructions": "Do not pour chemicals down drains or mix products. Keep the item safely contained and contact an authorised collection service.",
        "items": [
            "button cell battery", "alkaline battery", "rechargeable battery", "car battery", "damaged lithium battery",
            "fluorescent tube", "compact fluorescent bulb", "halogen bulb", "thermometer mercury", "paint can with paint",
            "leftover paint", "paint thinner", "solvent container", "pesticide container", "insecticide spray",
            "weed killer", "pool chemical", "bleach concentrate", "drain cleaner", "oven cleaner",
            "motor oil", "used engine oil", "oil filter", "fuel container residue", "antifreeze",
            "brake fluid", "car polish chemical", "nail polish", "nail polish remover", "aerosol pesticide",
            "pressurised gas canister", "fire extinguisher", "smoke detector", "chemical cleaner residue", "strong acid container",
            "strong alkali container", "laboratory chemical", "photographic chemical", "expired medicine", "unused medicine",
            "syringe", "medical needle sharps container", "medical waste", "chemical-soaked rag", "contaminated absorbent",
            "old firework", "pool chlorine tablet", "wood preservative", "lead-acid power pack", "unknown chemical bottle"
        ]
    },
    "E-WASTE": {
        "bin": "AUTHORISED E-WASTE COLLECTION", "icon": "💻",
        "why": "Electronic products contain circuit boards, metals, plastics, and sometimes batteries that need specialist recovery or treatment.",
        "instructions": "Do not put electronics in ordinary bins. Remove personal data where relevant and use an authorised e-waste recycler or take-back service.",
        "items": [
            "desktop computer", "computer monitor", "lcd monitor", "television", "smart watch",
            "tablet", "digital camera", "video camera", "printer", "scanner",
            "fax machine", "router", "wifi router", "modem", "network switch",
            "external hard drive", "usb flash drive", "memory card", "computer motherboard", "graphics card",
            "ram module", "computer processor", "power supply unit", "computer fan", "webcam",
            "microphone electronic", "speaker", "bluetooth speaker", "radio", "stereo system",
            "dvd player", "game console", "game controller", "remote control", "digital alarm clock",
            "electric toothbrush", "hair dryer", "electric shaver", "electric kettle", "microwave oven",
            "electric iron", "toaster", "blender", "food processor", "electric drill",
            "power bank", "solar garden light", "led strip light", "smart home sensor", "electronic toy"
        ]
    },
    "REUSE / TEXTILE / BULKY WASTE": {
        "bin": "REUSE, DONATION OR LOCAL BULKY-WASTE COLLECTION", "icon": "🧺",
        "why": "This item may be reusable, repairable, or accepted by a specialist textile or bulky-waste service rather than a standard household bin.",
        "instructions": "Donate clean usable items, repair them where practical, or check local collection arrangements for damaged or bulky items.",
        "items": [
            "cotton t-shirt", "jeans", "wool sweater", "jacket", "coat",
            "dress", "skirt", "shorts", "socks", "towel",
            "bedsheet", "pillowcase", "blanket", "curtain", "fabric scraps",
            "handbag", "backpack", "belt", "pair of shoes", "sandals",
            "soft toy", "stuffed animal", "curtain rod", "small wooden chair", "wooden table",
            "bookshelf", "wooden drawer", "plastic storage box", "suitcase", "carpet",
            "rug", "foam mattress", "mattress", "pillow", "office chair",
            "desk", "wooden door", "wooden frame", "bicycle", "push scooter",
            "baby stroller", "baby cot", "plastic garden chair", "garden hose", "old sports equipment",
            "tennis racket", "football", "musical instrument", "reusable water flask", "repairable toy"
        ]
    }
}

for _category, _group in PRODUCT_GROUPS.items():
    for _name in _group["items"]:
        _key = _name.lower().strip()
        WASTE_DB.setdefault(_key, {
            "category": _category,
            "bin": _group["bin"],
            "icon": _group["icon"],
            "why": _group["why"],
            "instructions": _group["instructions"]
        })

ALIASES = {
    "plastic": "plastic bottle", "bottle": "plastic bottle", "pet bottle": "plastic bottle",
    "water bottle": "water bottle", "newspaper": "newspaper", "paper sheet": "paper",
    "box": "cardboard", "carton": "cardboard", "tin can": "metal can", "can": "metal can",
    "aluminium": "aluminium can", "aluminum can": "aluminium can", "steel can": "metal can",
    "banana": "banana peel", "peels": "vegetable scraps", "vegetable waste": "vegetable scraps",
    "leftover food": "food waste", "scraps": "food waste", "wrapper": "food wrapper",
    "snack packet": "chip packet", "cell phone": "mobile phone", "smartphone": "mobile phone",
    "phone": "mobile phone", "computer": "laptop", "notebook computer": "laptop",
    "usb charger": "charger", "charging cable": "charger", "headphones": "earphones",
    "computer mouse": "mouse", "fluorescent bulb": "bulb", "light bulb": "bulb",
    "clothes": "cloth", "shirt": "cloth", "timber": "wood"
}

def classify_item(raw_item):
    item = re.sub(r"\s+", " ", (raw_item or "").strip().lower())
    if not item:
        return None
    if item in WASTE_DB:
        canonical = item
    elif item in ALIASES:
        canonical = ALIASES[item]
    else:
        # Match known item names inside longer user input.
        matches = sorted(
            [key for key in list(WASTE_DB) + list(ALIASES) if key in item],
            key=len, reverse=True
        )
        if not matches:
            return {
                "item": item.title(),
                "category": "ITEM NOT RECOGNISED",
                "bin": "CHECK LOCAL WASTE GUIDANCE",
                "icon": "🔎",
                "why": "The assistant does not yet have a reliable match for this item.",
                "instructions": "Try a simpler item name, or ask your local waste authority how to dispose of it."
            }
        found = matches[0]
        canonical = ALIASES.get(found, found)
    result = dict(WASTE_DB[canonical])
    result["item"] = canonical.title()
    result["matched_key"] = canonical
    return result

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json(silent=True) or request.form
    result = classify_item(data.get("item", ""))
    if result is None:
        return jsonify({"error": "Please enter a waste item."}), 400
    return jsonify(result)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "items": len(WASTE_DB)})

if __name__ == "__main__":
    app.run(debug=True)
