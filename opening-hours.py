import csv
import re

input_file = "shops-select2.csv"
output_file = "shops-reviews2.csv"

#regex podmínky pro jednotlivé kategorie na základě textu v recenzích
re_vegan = r"(?<!\bno )(?<!\bchyb[ií] )(?<!\bdon’t offer )vegan|(?<!\bchyb[ií] )rostlin|(?<!\bno )(?<!\bchyb[ií] )plant\s?-?\s?based|(?<!\bchyb[ií] )(?<!\bnenab[íi]z[íi] )bezlakt|(?<!\bchyb[ií]) lakt|(?<!\bno )(?<!\bchyb[ií] )(?<!\bnot have an alternative for )lact"
re_celiak = r"(?<!\bchyb[ií] )(?<!\bnemaj[íi] )(?<!\nenab[íi]z[íi] )bez ?lepk(?!.*?\bnic\b.{0,10})(?!.*?\bnem[ěea][lj].?\b.{0,10})(?!.*?\bnena[sšb][leí][laz].?\b.{0,10})|(?<!\bno )(?<!\bchyb[ií] )gluten"
re_except = r"Jediný bezlepkový zákusek byl chia puding, u kterého bylo napsáno, že obsahuje lepek.|neví, co je rostlinné mléko|sell him sandwich with gluten|jestli mohou dát do kávy mléko bez laktózy|rudely"


def parse_block(s: str) -> list[int]:
    """
    Zpracovává jednotlivé časové bloky, vrací dvojici otevření a uzavření
    v daném bloku v minutách od počátku dne. Příklady:

    7:00 až 15:00
    [420, 900]

    8:00 až 12:00, 13:00 až 24:00
    [480, 720, 780, 1440]

    nonstop
    [0, 1440]
    """

    if s == "Open 24 hours":
        return [0, 1440]
    elif s == "Closed":
        return []
    elif s == '':
        return [-1]


    s = s.replace("a.m.", "am").replace("p.m.", "pm").lower()

    try:
        start, end = s.split(" to ")
    except:
        print("###" + s)
        exit()
# přidaná výjimka na 12. hodinu, která má v defaultu PM ale nevztahuje se na ní vzorec pro "afternoon"
    if end.startswith ("12"):
        end_afternoon = False
    else:
        end_afternoon = end.endswith("pm")

    if start.endswith("am"):
        start_afternoon = False
# druhá podmínka pro 12. hodinu (viz komentář výše)
    elif start.startswith("12"):
        start_afternoon = False
    elif start.endswith("pm"):
        start_afternoon = True
    else:
        start_afternoon = end_afternoon

    start = start.replace("am", "").replace("pm", "")
    end = end.replace("am", "").replace("pm", "")
    start_split = [int(x) for x in start.split(":")]
    end_split = [int(x) for x in end.split(":")]

    start_mm = start_split[1] if len(start_split) > 1 else 0
    start_min = (start_split[0] + 12 * start_afternoon) * 60 + start_mm

    end_mm = end_split[1] if len(end_split) > 1 else 0
    end_min = (end_split[0] + 12 * end_afternoon) * 60 + end_mm

    return [start_min, end_min]


def parse_opening_hours(s: str) -> list[int]:
    result = []
    blocks = s.split(", ")
    for b in blocks:
        result.extend(parse_block(b))
    return result


# test funkce parse_opening_hours
# samples = [
#     "7 am to 11 am",
#     "7 to 11 am",
#     "7 am to 2 pm",
#     "7:15 am to 2 pm",
#     "7 am to 2 pm, 3 pm to 5 pm",
#     "2 pm to 6 pm",
#     "2 to 6 pm",
#     "7 am to 12 pm",
#     "12 pm to 6 pm",
#     "12 to 6 pm",
#     "12:30 pm to 6 pm",
#     "12:30 to 6 pm",
#     "Open 24 hours",
# ]

# for s in samples:
#     print(parse_opening_hours(s))


shops = []

with open(input_file, encoding="utf8") as file_in:
    reader = csv.DictReader(file_in)
    for shop in reader:
        title = shop["title"]
        url = shop["url"]
        address = shop["address"]
        keep = False
        reviews = []
        for field, value in shop.items():
            if field.startswith("reviews_") and value:
                reviews.append(value)

        output_dict = {
            "title": title,
            "url": url,
            "vegan": False,
            "celiatic": False,
        }
# rozdělení podniků do kategorií podle KW v recenzích
        review_re = []
        for review in reviews:
            if re.search(re_vegan, review, re.IGNORECASE) and not re.search(re_except, review, re.IGNORECASE):
                keep = True
                output_dict["vegan"] = True
                review_re.append(review)
            if re.search(re_celiak, review, re.IGNORECASE) and not re.search(re_except, review, re.IGNORECASE):
                keep = True
                output_dict["celiatic"] = True
                review_re.append(review)
        output_dict["reviews"] = review_re
# zápis opening hours do samostatných sloupců po dnech
        for n in range(7):
            key = f"openingHours_{n}_hours"
            output_dict[f"day{n}openhours"] = parse_opening_hours(shop[key])
# extrakce mesta z adresy a tvorba noveho sloupce            
        match = re.search(r'\d{3}\s?\d{2},?\s\d{0,2}([^,\d]+)', address)
        if match:
            output_dict["city_output"] = match.group(1).strip()

        if keep:
            shops.append(output_dict)

print(shops)
# Export do CSV file
with open(output_file, "w", newline="", encoding="utf8") as file_out:
    writer = csv.DictWriter(file_out, fieldnames=output_dict.keys())
    writer.writeheader()
    for shop in shops:
        writer.writerow(shop)
