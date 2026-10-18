import requests
import json
import re
from bs4 import BeautifulSoup

TARGET_USERNAME = "antisalotto_culturale"
OUTPUT_FILE = "dossier_targets.json"

SESSION_ID = "65109002163%3AvPXujYpfzZH6cS%3A28%3AAYlfQS6U4XVzl_uBNSaABRIaY2CyYDALgwz0px8Mz6A"

def get_profile_data(username):
    url = f"https://www.instagram.com/{username}/"
    
    session = requests.Session()
    session.cookies.set("sessionid", SESSION_ID, domain=".instagram.com")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.instagram.com/"
    }

    print(f"[INFO] Download e analisi pagina per: {username}...")
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[ERRORE] Errore HTTP: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Cerchiamo nei tag script la struttura JSON nativa di Instagram
    followers, following, posts = "N/D", "N/D", "N/D"
    full_name, biography = "", ""

    for script in soup.find_all("script"):
        text = script.string or ""
        if "edge_followed_by" in text or "biography" in text:
            try:
                # Estrazione tramite espressioni regolari dei campi chiave nel JSON interno
                f_match = re.search(r'"edge_followed_by":\s*\{\s*"count":\s*(\d+)\s*\}', text)
                if f_match:
                    followers = f_match.group(1)

                g_match = re.search(r'"edge_follow":\s*\{\s*"count":\s*(\d+)\s*\}', text)
                if g_match:
                    following = g_match.group(1)

                p_match = re.search(r'"edge_owner_to_timeline_media":\s*\{\s*"count":\s*(\d+)', text)
                if p_match:
                    posts = p_match.group(1)

                b_match = re.search(r'"biography":\s*"([^"]+)"', text)
                if b_match:
                    biography = b_match.group(1).encode().decode('unicode-escape')

                n_match = re.search(r'"full_name":\s*"([^"]+)"', text)
                if n_match:
                    full_name = n_match.group(1).encode().decode('unicode-escape')
            except Exception:
                pass

    # Fallback sui meta tag se lo script non è stato intercettato
    if followers == "N/D":
        meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_desc and meta_desc.get("content"):
            desc = meta_desc["content"]
            match = re.search(r'([\d\.\,\sKMB]+)\s+(?:Followers|follower),.*?([\d\.\,\sKMB]+)\s+(?:Following|seguiti),.*?([\d\.\,\sKMB]+)\s+(?:Posts|post)', desc, re.IGNORECASE)
            if match:
                followers = match.group(1).strip()
                following = match.group(2).strip()
                posts = match.group(3).strip()
                biography = desc

    return {
        "anagrafica": {
            "username": username,
            "nome": full_name,
            "bio": biography,
            "avatar_url": ""
        },
        "statistiche": {
            "post": posts,
            "follower": followers,
            "seguiti": following
        }
    }

if __name__ == "__main__":
    profile = get_profile_data(TARGET_USERNAME)
    
    if profile:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([profile], f, indent=4, ensure_ascii=False)
        print(f"\n[SUCCESSO] Dossier aggiornato in '{OUTPUT_FILE}'!")
    else:
        print("\n[ERRORE] Estrazione fallita.")
