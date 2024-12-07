import json

from pathlib import Path
from pprint import pprint


with Path("resume_old.json").open("r") as f:
    resume = json.loads(f.read())

timeline_entries = [r for r in resume if r["model"] == "resume.timelineentry"]

freelance_timeline = [r for r in timeline_entries if r["fields"]["timeline"] == 1]
employed_timeline = [r for r in timeline_entries if r["fields"]["timeline"] == 2]

# print("Freelance Timeline Entries:")
# pprint(freelance_timeline)

def migrate_timeline(old):
    new = []
    for item in old:
        fields = item["fields"]
        new_item = {
            "id": str(item["pk"]),
            "company_name": fields["company_name"],
            "company_url": fields["company_url"],
            "role": fields["role"],
            "position": fields["position"],
            "start": str(fields["start"]),
            "end": str(fields["end"]),
            "description": fields["description"],
            "badges": fields["badges"].split(",") if fields["badges"] else [],
        }
        new.append(new_item)
    return new


# print("\nEmployed Timeline Entries:")
employed_timeline = migrate_timeline(employed_timeline)
employed_timeline = sorted(employed_timeline, key=lambda item: item.get("position", 0), reverse=True)
freelance_timeline = migrate_timeline(freelance_timeline)
for item in freelance_timeline:
    item["position"] = 14 - item["position"]
freelance_timeline = sorted(freelance_timeline, key=lambda item: item.get("position", 0), reverse=True)

person = {
    "model": "django_resume.person",
    "pk": 1,
    "fields": {
        "name": "Jochen Wersdörfer",
        "slug": "jochen",
        "plugin_data": {
            "employed_timeline": {
                "flat": {
                    "title": "Employed Timeline",
                },
                "items": employed_timeline,
            },
            "freelance_timeline": {
                "flat": {
                    "title": "Freelance Timeline",
                },
                "items": freelance_timeline,
            },
        },
    },
}

# print("\nPerson:")
person_as_json = json.dumps([person], indent=4)
Path("person.fixture.json").write_text(person_as_json)