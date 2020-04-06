import spacy
from spacy import displacy
import parsedatetime
import re, string
import datetime

FOOD_TYPES = ["swiss", "indian", "mexican", "asian", "western", "italian", "thai", "chinese", "spanish", "indonesian", "peranakan"]
FOOD_TERMS = ["food", "restaurant", "dining", "cuisine"]
MUSIC = ["jazz", "pop music", "western music", "asian music", "classical music", "rock music", "kpop"]
SPORTS = ["rugby", "golf", "football", "basketball", "f1", "cricket", "tennis", "yoga"]
INVESTMENT = ["Impactful investment", "ESG product", "ESG investment", "Penny stock", "High dividend yield", "Renewable energy", "Tech stock", "Healthcare stock", "Private Equity", "Structured product", "Health care stock", "Tech companies", "Private companies", "Green bond"]
PREFERENCE_TERMS = ["interest", "like", "prefer", "want", "enjoy", "excite", "love", "fancy", "appreciate"]
LOAN_TERMS = ["loan", "buy house", "purchase house", "invest on house", "dividend"]
NEWBORN_TERMS = ["newborn", "new born", "new child", "new baby", "baby boy", "baby girl", "born"]
MARRAIGE_TERMS = ["got married", "engaged", "married", "tied the knot"]
SNOOZE_TERMS = ["holiday", "overseas", "travelling", "time off", "summer break", "conference", "vacation", "dnd", "summit"]
RELATION_TERMS = ["child", "father", "mother", "friend", "professional", "spouse", "daughter", "grandson", "granddaughter"]

additional_relation_mapping = {
    "wife": "spouse",
    "husband": "spouse",
    "daughter": "child"
}
additional_relation_terms = list(additional_relation_mapping.keys())

def get_spacy_model():
    return spacy.load("en_core_web_md")

def get_entities(text, nlp, cal):
    doc = nlp(text)
    html = displacy.render(doc, style="ent",jupyter=False, options={"ents":["PERSON","FAC","ORG","GPE","LOC","PRODUCT","EVENT","WORK_OF_ART","DATE","TIME","MONEY"]}).replace("\n","")
    #Highlight loan as concept, newborn as event
    for loan_term in LOAN_TERMS + SNOOZE_TERMS:
        case_insensitive = re.compile(re.escape(loan_term), re.IGNORECASE)
        html = case_insensitive.sub('''<mark class="entity" style="background: #ffeb80; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone"> {} <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">EVENT</span></mark>'''.format(loan_term), html)
    for marraige_term in MARRAIGE_TERMS:
        case_insensitive = re.compile(re.escape(marraige_term), re.IGNORECASE)
        html = case_insensitive.sub('''<mark class="entity" style="background: #ffeb80; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone"> {} <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">EVENT</span></mark>'''.format(marraige_term), html)
    for newborn_term in NEWBORN_TERMS:
        case_insensitive = re.compile(re.escape(newborn_term), re.IGNORECASE)
        html = case_insensitive.sub('''<mark class="entity" style="background: #ffeb80; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone"> {} <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">EVENT</span></mark>'''.format(newborn_term), html)
    # Food
    for food in FOOD_TYPES:
        for term in FOOD_TERMS:
            food_term = food + " " + term
            case_insensitive = re.compile(re.escape(food_term), re.IGNORECASE)
            html = case_insensitive.sub('''<mark class="entity" style="background: #1aa3ff; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone"> {} <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">PREFERENCE</span></mark>'''.format(food_term.capitalize()), html)
    # Music
    for music_term in MUSIC:
        case_insensitive = re.compile(re.escape(music_term), re.IGNORECASE)
        html = case_insensitive.sub('''<mark class="entity" style="background: #1aa3ff; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone"> {} <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">PREFERENCE</span></mark>'''.format(music_term.capitalize()), html)
    # Sports
    for sport_term in SPORTS:
        case_insensitive = re.compile(re.escape(sport_term), re.IGNORECASE)
        html = case_insensitive.sub('''<mark class="entity" style="background: #1aa3ff; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone"> {} <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">PREFERENCE</span></mark>'''.format(sport_term.capitalize()), html)
    # Investment
    for investment_term in INVESTMENT:
        case_insensitive = re.compile(re.escape(investment_term.lower()), re.IGNORECASE)
        html = case_insensitive.sub('''<mark class="entity" style="background: #1aa3ff; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone"> {} <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">PREFERENCE</span></mark>'''.format(investment_term), html)
    # Relation
    for relation_term in RELATION_TERMS + additional_relation_terms:
        case_insensitive = re.compile(re.escape(relation_term.lower()), re.IGNORECASE)
        html = case_insensitive.sub('''<mark class="entity" style="background: #ffb3d9; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone"> {} <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">RELATION</span></mark>'''.format(relation_term), html)
    data = []
    for sent in doc.sents:
        sentence_data = {
            "sentence": sent.text,
            "entities": []
        }
        for ent in sent.ents:
            if ent.label_ == "DATE":
                dates = [x.strip() for x in ent.text.split("to")]
                for date in dates:
                    time_struct, parse_status = cal.parse(date)
                    sentence_data['entities'].append({
                        "date": datetime.datetime(*time_struct[:6]).strftime("%Y-%m-%d %H:%M:%S"),
                        "text": date,
                        "label": ent.label_
                    })
            else:
                sentence_data['entities'].append({
                    "text": ent.text,
                    "label": ent.label_
                })
        for loan in LOAN_TERMS:
            if loan in sent.text.lower():
                sentence_data['entities'].append({
                    "text": loan,
                    "label": "LOAN"
                })
                if len(list(filter(lambda x: x['label'] == "DATE", sentence_data['entities']))) == 0:
                    sentence_data['entities'].append({
                        "text": "now",
                        "label": "DATE",
                        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
        for newborn in NEWBORN_TERMS:
            if newborn in sent.text.lower():
                sentence_data['entities'].append({
                    "text": "newborn",
                    "label": "EVENT"
                })
        for marraige in MARRAIGE_TERMS:
            if marraige in sent.text.lower():
                sentence_data['entities'].append({
                    "text": "got married",
                    "label": "EVENT"
                })
        for snooze in SNOOZE_TERMS:
            if snooze in sent.text.lower():
                sentence_data['entities'].append({
                    "text": snooze,
                    "label": "SNOOZE_EVENT"
                })
        for relation in RELATION_TERMS + additional_relation_terms:
            if relation in additional_relation_mapping:
                relation_term = additional_relation_mapping[relation]
            else:
                relation_term = relation
            if relation in sent.text.lower():
                sentence_data['entities'].append({
                    "text": relation_term.capitalize(),
                    "label": "RELATION"
                })
        for term in PREFERENCE_TERMS:
            if term in sent.text.lower():
                sentence_data['entities'].append({
                    "text": term,
                    "label": "PREFERENCE_TERM"
                })
        for food in FOOD_TYPES:
            for term in FOOD_TERMS:
                food_term = food + " " + term
                if food_term in sent.text.lower():
                    sentence_data['entities'].append({
                        "text": food.capitalize() + " Dining",
                        "label": "PREFERENCE",
                        "type": "dining"
                    })
        for music in MUSIC:
            if music in sent.text.lower():
                sentence_data['entities'].append({
                    "text": music.capitalize().split()[0] + " Music",
                    "label": "PREFERENCE",
                    "type": "music"
                })
        for sport in SPORTS:
            if sport in sent.text.lower():
                sentence_data['entities'].append({
                    "text": sport.capitalize(),
                    "label": "PREFERENCE",
                    "type": "sports"
                })
        for investment in INVESTMENT:
            if investment.lower() in sent.text.lower():
                sentence_data['entities'].append({
                    "text": investment,
                    "label": "PREFERENCE",
                    "type": "investment"
                })
        data.append(sentence_data)
    return html, data