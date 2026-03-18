import csv
import json
import collections

# coordinates dict
COORDS = {
    "China": [104.195397, 35.86166],
    "United States": [-95.712891, 37.09024],
    "USA": [-95.712891, 37.09024],
    "Canada": [-106.346771, 56.130366],
    "Germany": [10.451526, 51.165691],
    "Australia": [133.775136, -25.274398],
    "United Kingdom": [-3.435973, 55.378051],
    "India": [78.96288, 20.593684],
    "Spain": [-3.74922, 40.463667],
    "Hong Kong": [114.169361, 22.319304],
    "Netherlands": [5.291266, 52.132633],
    "South Korea": [127.766922, 35.907757],
    "Iran": [53.688046, 32.427908],
    "Taiwan": [120.960515, 23.69781],
    "Japan": [138.252924, 36.204824],
    "Finland": [25.748151, 61.92411],
    "Belgium": [4.469936, 50.503887],
    "Turkey": [35.243322, 38.963745],
    "Italy": [12.56738, 41.87194],
    "France": [2.213749, 46.227638],
    "Brazil": [-51.92528, -14.235004],
    "Sweden": [18.643501, 60.128161],
    "Switzerland": [8.227512, 46.818188],
    "Egypt": [30.802498, 26.820553],
    "Greece": [21.824312, 39.074208],
    "Austria": [14.550072, 47.516231],
    "Poland": [19.145136, 51.919438],
    "Saudi Arabia": [45.079162, 23.885942],
    "New Zealand": [174.885971, -40.900557],
    "Malaysia": [101.975766, 4.210484],
    "Norway": [8.468946, 60.472024],
    "Singapore": [103.819836, 1.352083],
    "Pakistan": [69.345116, 30.375321],
    "Ireland": [-8.24389, 53.41291],
    "Czech Republic": [15.472962, 49.817492],
    "Denmark": [9.501785, 56.26392],
    "South Africa": [22.937506, -30.559482],
    "Portugal": [-8.224454, 39.399872],
    "Israel": [34.851612, 31.046051],
    "Mexico": [-102.552784, 23.634501]
}

data = {
    "papers": [],
    "countries": {},
    "yearlyStats": {},
    "authorNationality": {}
}

country_counts = collections.Counter()
yearly_stats_dict = collections.defaultdict(collections.Counter)

valid_years = set()

with open("ALL_articles_Scopus_Enriched.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        year_str = row.get("Year", "").strip()
        if not year_str or not year_str.isdigit():
            continue
        year = int(year_str)
        # Maybe filter years to >= 2003 because very early ones might be sparse
        if year < 2003 or year > 2025: continue
        valid_years.add(year)
        
        authors_names = [x.strip() for x in row.get("Scopus_Authors", "").split(";")]
        authors_countries = [x.strip() for x in row.get("Scopus_Countries", "").split(";")]
        
        paper_authors = []
        for i, (name, c_str) in enumerate(zip(authors_names, authors_countries)):
            if not name or name == "Unknown": continue
            # handle multiple countries for one author
            primary_c = "Unknown"
            if c_str and c_str != "Unknown":
                parts = c_str.split(" & ")
                primary_c = parts[0].strip()
                if primary_c == "USA": primary_c = "United States"
                
                # accumulate all countries
                for c in parts:
                    c = c.strip()
                    if c == "USA": c = "United States"
                    country_counts[c] += 1
                    yearly_stats_dict[year][c] += 1
            
            paper_authors.append({
                "name": name,
                "nationality": primary_c
            })
            data["authorNationality"][name] = primary_c
            
        data["papers"].append({
            "year": year,
            "title": row.get("Title", ""),
            "url": row.get("URL", ""),
            "access": row.get("Access", ""),
            "authors": paper_authors
        })

total_authors = sum(country_counts.values())
for c, count in country_counts.items():
    if c in COORDS:
        data["countries"][c] = {
            "count": count,
            "percentage": round(count / total_authors * 100, 2),
            "coords": COORDS[c]
        }
    else:
        # Fallback fake coords
        data["countries"][c] = {
            "count": count,
            "percentage": round(count / total_authors * 100, 2),
            "coords": [0, 0]
        }

for y in sorted(list(valid_years)):
    data["yearlyStats"][str(y)] = dict(yearly_stats_dict[y])

with open("visualization_data_scopus.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("Scopus visualization data generated successfully.")
