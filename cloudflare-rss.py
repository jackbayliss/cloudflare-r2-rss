import requests
from feedgen.feed import FeedGenerator
from dateutil import parser as dateparser

API_URL = "https://www.cloudflarestatus.com/api/v2/incidents.json"
RSS_FILE = "r2-incidents.xml"

def fetch_r2_incidents():
    response = requests.get(API_URL)
    response.raise_for_status()
    incidents = response.json().get("incidents", [])

    r2_incidents = []
    for incident in incidents:
        name = incident.get("name", "")
        updates = incident.get("incident_updates", [])
        for update in updates:
            body_texts = " ".join(update.get("body", ""))
        if "r2" in name.lower() or "r2" in body_texts.lower():
            r2_incidents.append(incident)
    return r2_incidents

def generate_rss(incidents):
    fg = FeedGenerator()
    fg.title("Cloudflare R2 Incidents")
    fg.link(href="https://www.cloudflarestatus.com/", rel="alternate")
    fg.description("RSS feed of Cloudflare incidents related to R2")
    fg.language("en")

    for incident in incidents:
        fe = fg.add_entry()
        fe.title(incident.get("name", "No Title"))
        fe.link(href=f"https://www.cloudflarestatus.com/incidents/{incident.get('id')}")
        latest_update = incident.get("incident_updates", [{}])[0]
        fe.description(latest_update.get("body", "No update available."))

        try:
            pub_date = dateparser.parse(incident["created_at"])
            fe.pubDate(pub_date)
        except Exception as e:
            print(f"[Warning] Date parsing failed for incident {incident.get('id')}: {e}")

    fg.rss_file(RSS_FILE)
    print(f"RSS feed written to: {RSS_FILE}")

if __name__ == "__main__":
    print("Fetching R2 incidents from Cloudflare...")
    incidents = fetch_r2_incidents()
    print(f"Found {len(incidents)} R2-related incidents.")
    generate_rss(incidents)
