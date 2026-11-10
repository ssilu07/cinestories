"""
Viral Social Push Toolkit for CineStories.
Generates copy-paste viral distribution assets for WhatsApp, Pinterest, Reddit, and Twitter/X
tailored to break through the zero-traffic barrier and trigger Google Discover momentum.

Usage:
    python social_push_toolkit.py [--slug panchayat-season-3] [--all]
"""

import argparse
import sys
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VIRAL_PROMOTIONS: List[Dict[str, Any]] = [
    {
        "slug": "panchayat-season-3",
        "title": "Panchayat Season 3",
        "hook": "Did Pradhan Ji Stage His Own Shooting? Panchayat S3 Ending Decoded",
        "url": "https://cinematicbites.com/articles/panchayat-season-3/",
        "story_url": "https://cinematicbites.com/stories/panchayat-season-3/",
        "image": "https://image.tmdb.org/t/p/w1280/lPbFwNohpsCNeLXpzV8ZS3mnI0X.jpg",
        "whatsapp": (
            "🔥 *Panchayat Season 3 Ending Mystery Solved!*\n\n"
            "Bus stand par Pradhan Ji par kisne goli chalwayi thi? Kya Pradhan Ji ne khud election sympathy ke liye hit stage karwaya tha? 😱\n\n"
            "Check out the 3 hidden clues that reveal the truth:\n"
            "👉 https://cinematicbites.com/articles/panchayat-season-3/\n\n"
            "⚡ Visual Web Story: https://cinematicbites.com/stories/panchayat-season-3/"
        ),
        "pinterest": {
            "title": "Did Pradhan Ji Stage His Own Shooting? Panchayat S3 Ending Decoded",
            "desc": "Unpack the 3 crucial visual clues behind the bus stand shooting of Pradhan Ji in Panchayat Season 3. Why Vidhayak might be innocent and how Season 4 election politics will unfold. #PanchayatS3 #PanchayatSeason3 #AmazonPrimeVideo #JitendraKumar #EndingExplained",
            "link": "https://cinematicbites.com/articles/panchayat-season-3/"
        },
        "reddit": {
            "subreddit": "r/IndianOTTbestof, r/bollywood",
            "title": "[Theory] Did Pradhan Ji stage his own assassination attempt in Panchayat Season 3? Look at clue #1",
            "body": (
                "After rewatching the bus stand shootout scene in Panchayat S3, there are 3 details that don't add up:\n\n"
                "1. Point-blank range yet a clean shoulder wound instead of center mass.\n"
                "2. Banrakas Bhushan's frantic panic proved even the opposition camp was blind-sided.\n"
                "3. The massive sympathy wave that completely turned Manju Devi's election numbers.\n\n"
                "Wrote down a complete breakdown of the scene clues and director hints here:\n"
                "https://cinematicbites.com/articles/panchayat-season-3/\n\n"
                "What do you guys think? Was it Vidhayak or a masterstroke political setup by Phulera's camp?"
            )
        },
        "twitter": (
            "Did Pradhan Ji stage his own shooting in #PanchayatS3? 😱\n\n"
            "The assassins had point-blank range, yet chose the shoulder. Here are the 3 hidden clues that decode the Phulera climax & Season 4 roadmap:\n\n"
            "👉 https://cinematicbites.com/articles/panchayat-season-3/\n\n"
            "#PanchayatSeason3 #Panchayat"
        )
    },
    {
        "slug": "mirzapur-season-3",
        "title": "Mirzapur Season 3",
        "hook": "Why Kaleen Bhaiya Killed Sharad Shukla: The Hidden Deal in Mirzapur 3!",
        "url": "https://cinematicbites.com/articles/mirzapur-season-3/",
        "story_url": "https://cinematicbites.com/stories/mirzapur-season-3/",
        "image": "https://image.tmdb.org/t/p/w1280/lPbFwNohpsCNeLXpzV8ZS3mnI0X.jpg",
        "whatsapp": (
            "👑 *Mirzapur Season 3 Climax Shock!*\n\n"
            "Sharad Shukla touched the Mirzapur throne for just 10 seconds before Kaleen Bhaiya shot him. But why did Kaleen betray his savior?\n\n"
            "The secret pact with Madhuri Yadav revealed:\n"
            "👉 https://cinematicbites.com/articles/mirzapur-season-3/\n\n"
            "⚡ Visual Web Story: https://cinematicbites.com/stories/mirzapur-season-3/"
        ),
        "pinterest": {
            "title": "Why Kaleen Bhaiya Betrayed Sharad Shukla: Mirzapur S3 Ending Explained",
            "desc": "The shocking climax betrayal in Mirzapur Season 3 decoded. Inside Chief Minister Madhuri Yadav's secret deal and Maqbool's return. #Mirzapur3 #MirzapurSeason3 #KaleenBhaiya #PankajTripathi #EndingExplained",
            "link": "https://cinematicbites.com/articles/mirzapur-season-3/"
        },
        "reddit": {
            "subreddit": "r/IndianOTTbestof, r/bollywood",
            "title": "Why Kaleen Bhaiya had to kill Sharad Shukla: Unpacking Madhuri's hidden condition in Mirzapur 3",
            "body": (
                "A lot of viewers were shocked when Kaleen Bhaiya pulled the trigger on Sharad right after being crowned. But if you watch the CM house confrontation in episode 9, the foreshadowing was clear.\n\n"
                "Here is the full breakdown of Madhuri's immunity deal and what it means for Guddu Pandit in Season 4:\n"
                "https://cinematicbites.com/articles/mirzapur-season-3/\n\n"
                "Did Sharad deserve that ending or was he done dirty?"
            )
        },
        "twitter": (
            "Sharad Shukla touched the Mirzapur throne for 10 seconds before a bullet ended him. 👑💥\n\n"
            "Why did Kaleen Bhaiya betray his savior? The hidden deal with Madhuri Yadav decoded:\n\n"
            "👉 https://cinematicbites.com/articles/mirzapur-season-3/\n\n"
            "#Mirzapur3 #MirzapurSeason3 #KaleenBhaiya"
        )
    },
    {
        "slug": "stree-2",
        "title": "Stree 2: Sarkate Ka Aatank",
        "hook": "Is Akshay Kumar the 'Thanos' of Maddock Universe? Stree 2 Post-Credits Decoded!",
        "url": "https://cinematicbites.com/articles/stree-2/",
        "story_url": "https://cinematicbites.com/stories/stree-2/",
        "image": "https://image.tmdb.org/t/p/w1280/nfnhwfUEFuSOxxf4jDdBlY6Lccw.jpg",
        "whatsapp": (
            "👻 *Stree 2 Post-Credits & Climax Decoded!*\n\n"
            "Sarkata ki raakh (ashes) ko pagalkhane mein kisne inhale kiya? Kya Akshay Kumar Maddock Horror Universe ka 'Thanos' banne wala hai?\n\n"
            "Read full post-credits breakdown & Bhediya crossover clues:\n"
            "👉 https://cinematicbites.com/articles/stree-2/\n\n"
            "⚡ Visual Web Story: https://cinematicbites.com/stories/stree-2/"
        ),
        "pinterest": {
            "title": "Is Akshay Kumar the Villain of Maddock Universe? Stree 2 Post-Credits Decoded",
            "desc": "Stree 2 post-credits scene explained: Sarkata's ashes, Shraddha Kapoor's secret name, and Akshay Kumar's descent into darkness setting up Stree 3. #Stree2 #ShraddhaKapoor #RajkummarRao #MaddockSupernaturalUniverse #EndingExplained",
            "link": "https://cinematicbites.com/articles/stree-2/"
        },
        "reddit": {
            "subreddit": "r/bollywood",
            "title": "Stree 2 Post-Credits Breakdown: How Akshay Kumar's cameo sets up the Avengers-level showdown of Maddock Universe",
            "body": (
                "The post-credits scene where Akshay Kumar inhales Sarkata's ashes at the mental asylum wasn't just a comedic gag—Amar Kaushik confirmed it's the anchor for Stree 3 and Bhediya 2.\n\n"
                "Full breakdown of the lore, Shraddha's parentage hints, and what's next:\n"
                "https://cinematicbites.com/articles/stree-2/\n\n"
                "Who do you think will team up against him first: Bhediya or Stree?"
            )
        },
        "twitter": (
            "Is Akshay Kumar officially the 'Thanos' of Bollywood's horror universe? 👻⚡\n\n"
            "The mental asylum scene, Sarkata's ashes, and Shraddha's secret parentage decoded in this #Stree2 post-credits breakdown:\n\n"
            "👉 https://cinematicbites.com/articles/stree-2/\n\n"
            "#Stree2 #ShraddhaKapoor #RajkummarRao"
        )
    },
    {
        "slug": "kalki-2898-ad",
        "title": "Kalki 2898 AD",
        "hook": "Why Prabhas is Karna, Not Kalki: The Mind-Blowing Climax of Kalki 2898 AD!",
        "url": "https://cinematicbites.com/articles/kalki-2898-ad/",
        "story_url": "https://cinematicbites.com/stories/kalki-2898-ad/",
        "image": "https://image.tmdb.org/t/p/w1280/lPbFwNohpsCNeLXpzV8ZS3mnI0X.jpg",
        "whatsapp": (
            "🏹 *Kalki 2898 AD Climax Revelation!*\n\n"
            "Bhairava (Prabhas) Kalki nahi hai—wo Mahabharat ke Suryaputra KARNA ka reincarnation hai! Vijay Deverakonda ka Arjun cameo aur Supreme Yaskin ka Gandiva bow decoded:\n\n"
            "👉 https://cinematicbites.com/articles/kalki-2898-ad/\n\n"
            "⚡ Visual Web Story: https://cinematicbites.com/stories/kalki-2898-ad/"
        ),
        "pinterest": {
            "title": "Why Prabhas is Karna, Not Kalki: Kalki 2898 AD Climax Decoded",
            "desc": "The divine Vijaya bow, Ashwatthama's realization, and Supreme Yaskin's Gandiva bow. Everything you need to know about the epic Mahabharata connections in Kalki 2898 AD. #Kalki2898AD #Prabhas #AmitabhBachchan #DeepikaPadukone #EndingExplained",
            "link": "https://cinematicbites.com/articles/kalki-2898-ad/"
        },
        "reddit": {
            "subreddit": "r/tollywood, r/bollywood",
            "title": "Why the Karna reveal in Kalki 2898 AD was pure cinematic gold (and what it means for Part 2)",
            "body": (
                "When Bhairava lifts the Vijaya staff and his memories unlock, Ashwatthama bowing was the biggest theater moment of 2024. Nag Ashwin confirmed Part 2 will dive deep into the Kurukshetra war.\n\n"
                "Read the complete ending breakdown, Kamal Haasan's Gandiva bow, and Part 2 roadmap:\n"
                "https://cinematicbites.com/articles/kalki-2898-ad/\n\n"
                "Will Karna fight Kalki or become his protector?"
            )
        },
        "twitter": (
            "Prabhas isn't Kalki—he's Suryaputra KARNA reincarnated. 🏹🔥\n\n"
            "Ashwatthama's shock, the divine Vijaya staff, and Kamal Haasan's Gandiva bow in the epic #Kalki2898AD climax decoded:\n\n"
            "👉 https://cinematicbites.com/articles/kalki-2898-ad/\n\n"
            "#Kalki #Prabhas #AmitabhBachchan"
        )
    },
    {
        "slug": "pushpa-2-the-rule",
        "title": "Pushpa 2: The Rule",
        "hook": "The Japan Smuggling Route & Shekhawat's Trap: Pushpa 2 Climax Clues Decoded!",
        "url": "https://cinematicbites.com/articles/pushpa-2-the-rule/",
        "story_url": "https://cinematicbites.com/stories/pushpa-2-the-rule/",
        "image": "https://image.tmdb.org/t/p/w1280/lPbFwNohpsCNeLXpzV8ZS3mnI0X.jpg",
        "whatsapp": (
            "🪓 *Pushpa 2: The Rule Climax Breakdown!*\n\n"
            "Sindoori Jathara sequence, Japan syndicate connection, aur SP Bhanwar Singh Shekhawat ka revenge plan. Sukumar ka Part 3 roadmap dekho:\n\n"
            "👉 https://cinematicbites.com/articles/pushpa-2-the-rule/\n\n"
            "⚡ Visual Web Story: https://cinematicbites.com/stories/pushpa-2-the-rule/"
        ),
        "pinterest": {
            "title": "Pushpa 2 Climax & Japan Syndicate Connection Decoded: The Rule Explained",
            "desc": "Allu Arjun's Pushpa Raj expands his red sandalwood empire to global waters. Inside the Jathara sequence, Shekhawat's vendetta, and Pushpa 3 setup. #Pushpa2 #Pushpa2TheRule #AlluArjun #RashmikaMandanna #EndingExplained",
            "link": "https://cinematicbites.com/articles/pushpa-2-the-rule/"
        },
        "reddit": {
            "subreddit": "r/tollywood, r/bollywood",
            "title": "Pushpa 2: The Rule - Unpacking the Sindoori Jathara scene and the global syndicate expansion",
            "body": (
                "The shift from local Chittoor forests to international waters in Pushpa 2 raises the stakes massively for Bhanwar Singh Shekhawat's vendetta.\n\n"
                "Here is the full scene breakdown, Easter eggs, and Part 3 franchise clues:\n"
                "https://cinematicbites.com/articles/pushpa-2-the-rule/\n\n"
                "Will Pushpa survive the international syndicate?"
            )
        },
        "twitter": (
            "The Sindoori Jathara sequence in #Pushpa2TheRule is next level. 🪓🔥\n\n"
            "How Pushpa Raj outplays Shekhawat and establishes his international empire—full climax breakdown & Part 3 clues:\n\n"
            "👉 https://cinematicbites.com/articles/pushpa-2-the-rule/\n\n"
            "#Pushpa2 #AlluArjun"
        )
    }
]

def print_banner():
    print("=" * 70)
    print("🚀 CINESTORIES VIRAL SOCIAL PUSH TOOLKIT")
    print("   Ready-to-copy promotion templates to kickstart initial traffic!")
    print("=" * 70)

def display_promo(promo: Dict[str, Any]):
    print(f"\n🎬 {promo['title'].upper()} — VIRAL CAMPAIGN")
    print(f"URL: {promo['url']}")
    print("-" * 65)

    print("\n🟢 [WHATSAPP / TELEGRAM] — Copy & Send to Groups/Status:")
    print(promo["whatsapp"])

    print("\n📌 [PINTEREST] — Create Pin at https://pinterest.com/pin-creation-tool/:")
    print(f" • Title      : {promo['pinterest']['title']}")
    print(f" • Description: {promo['pinterest']['desc']}")
    print(f" • Link       : {promo['pinterest']['link']}")
    print(f" • Image URL  : {promo['image']}")

    print("\n👽 [REDDIT] — Post to Indian OTT / Bollywood communities:")
    print(f" • Subreddits : {promo['reddit']['subreddit']}")
    print(f" • Title      : {promo['reddit']['title']}")
    print(f" • Body Text  :\n{promo['reddit']['body']}")

    print("\n🐦 [TWITTER / X] — Post Tweet:")
    print(promo["twitter"])
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Generate viral social media posts for CineStories")
    parser.add_argument("--slug", help="Filter by specific slug (e.g. panchayat-season-3)")
    parser.add_argument("--all", action="store_true", default=True, help="Display all viral campaigns")
    args = parser.parse_args()

    print_banner()

    found = False
    for p in VIRAL_PROMOTIONS:
        if args.slug and p["slug"] != args.slug:
            continue
        display_promo(p)
        found = True

    if not found:
        print(f"No campaigns found matching slug: '{args.slug}'.")

    print("\n💡 IMMEDIATE TRAFFIC PUSH INSTRUCTIONS:")
    print("1. Go to Google Search Console (https://search.google.com/search-console)")
    print("2. Enter 'https://cinematicbites.com/sitemap.xml' in Sitemaps tab")
    print("3. Inspect and click 'Request Indexing' for the top 5 article URLs above.")
    print("4. Copy the WhatsApp templates above into 2-3 active movie/entertainment groups.")
    print("   This kicks off the initial user engagement signals that Google Discover looks for!\n")

if __name__ == "__main__":
    main()
