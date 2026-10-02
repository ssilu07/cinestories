"""
Curated, high-CTR storytelling slides for Hollywood's most viral Blockbusters,
TV Series, and Cult Franchises.
Strictly compliant with Google AMP Web Story guidelines (Word count < 40 words per slide).
"""

from typing import Dict, Any

CURATED_STORIES: Dict[str, Dict[str, Any]] = {
    # 1. Money Heist
    "money-heist": {
        "title": "Bella Ciao! 5 Insane Professor Masterstrokes You Missed 💰",
        "seo_description": "Uncover the genius tactics, hidden clues, and Berlin's sacrifices in Netflix's global phenomenon Money Heist (La Casa de Papel).",
        "slides": [
            {
                "id": "page-1",
                "badge": "🔥 GLOBAL PHENOMENON",
                "title": "The €2.4 Billion Heist",
                "text": "Armed with Salvador Dalí masks and red jumpsuits, eight robbers executed the most audacious heist in history. But nothing was left to chance.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🧠 MASTERMIND RULE",
                "title": "Rule #1: No Bloodshed",
                "text": "The Professor spent 20 years planning the Royal Mint operation. His golden rule? Win the public's hearts by printing money rather than stealing anyone's savings.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "⚡ SHOCKING TWIST",
                "title": "The Inspector's Coffee",
                "text": "The Professor brazenly befriended lead negotiator Raquel Murillo at a local café, monitoring police radio frequencies right under her nose.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎭 ICONIC ANTHEM",
                "title": "The Power of Bella Ciao",
                "text": "The Italian anti-fascist hymn 'Bella Ciao' turned into an international symbol of rebellion, streamed over 1 billion times worldwide.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "👑 BERLIN'S SACRIFICE",
                "title": "The Ultimate Stand",
                "text": "Berlin's terminal illness gave him nothing to lose. His heroic last stand holding off special forces cemented his status as TV's most loved antihero.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 BINGE NOW",
                "title": "Ready For The Next Heist?",
                "text": "Stream all 5 seasons of Money Heist and explore the spinoff universe of Berlin on Netflix today.",
                "backdrop_index": 1,
                "cta_text": "Explore Series & Cast Details",
                "cta_url": "https://www.themoviedb.org/tv/71446"
            }
        ]
    },

    # 2. Final Destination
    "final-destination": {
        "title": "Death's Plan: 5 Terrifying Accidental Kill Traps Ranked 💀",
        "seo_description": "Discover how Death stalks survivors through ingenious chain reactions in horror classic Final Destination.",
        "slides": [
            {
                "id": "page-1",
                "badge": "💀 CULT HORROR LEGEND",
                "title": "You Can't Cheat Death",
                "text": "When Alex Browning had a terrifying premonition of Flight 180 exploding, he saved his classmates. But cheating Death carries a horrifying price.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "✈️ FLIGHT 180",
                "title": "The Original Nightmare",
                "text": "Inspired by a real-life X-Files script, the airplane explosion remains one of the most stressful opening sequences in cinematic horror history.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🩸 FATAL CHAIN REACTION",
                "title": "Death's Rube Goldberg Traps",
                "text": "Unlike slashers with knives, Death weaponizes everyday household items: leaking water pipes, frayed wires, kitchen knives, and tea kettles.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "👁️ TONY TODD'S WARNING",
                "title": "The Mortician's Secret",
                "text": "Horror icon Tony Todd as mortician William Bludworth delivered the franchise's spine-chilling lore: 'In Death, there are no accidents.'",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🔮 REVERSE ORDER",
                "title": "The Fatal Pattern",
                "text": "Survivors die in the exact order they were originally destined to perish on the plane. Intervening only passes the curse to the next victim.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🎬 WATCH THE FRANCHISE",
                "title": "Bloodlines Return Soon",
                "text": "Relive every heart-stopping twist across the 5-film franchise as Final Destination: Bloodlines prepares to terrify theaters.",
                "backdrop_index": 1,
                "cta_text": "Check Franchise Details",
                "cta_url": "https://www.themoviedb.org/movie/9532"
            }
        ]
    },

    # 3. Stranger Things
    "stranger-things": {
        "title": "The Upside Down: 5 Dark Secrets Ahead Of Season 5 🚲⚡",
        "seo_description": "Explore the shadowy secrets of Hawkins, Eleven's psychokinetic powers, and Vecna's master plan in Stranger Things.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🚲 80S NOSTALGIA",
                "title": "Welcome to Hawkins",
                "text": "When Will Byers mysteriously disappeared into the dark woods of Hawkins, Indiana, a group of kids stumbled upon an eerie government conspiracy.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🧇 ELEVEN'S POWERS",
                "title": "Eggos & Telekinesis",
                "text": "Escaping Hawkins National Laboratory, Eleven weaponized psychokinesis to battle monstrous Demogorgons while discovering real friendship and eggo waffles.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🎧 RUNNING UP THAT HILL",
                "title": "Max's Masterpiece Escape",
                "text": "Kate Bush's 'Running Up That Hill' rocketed back to #1 globally after soundtracking Max Mayfield's pulse-pounding flight from Vecna's curse.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "⏳ TIME FROZEN",
                "title": "November 6, 1983",
                "text": "Nancy Wheeler discovered the chilling truth: the Upside Down is permanently frozen on the exact day Will Byers first vanished.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "⚡ THE FINAL BATTLE",
                "title": "Season 5 Apocalypse",
                "text": "With the 4 gates torn wide open across Hawkins, the final battle between Eleven and Vecna promises cinema-level runtime and heartbreak.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 STREAM ON NETFLIX",
                "title": "Prepare For The Series Finale",
                "text": "Catch up on every episode of Stranger Things before the Duffer Brothers conclude the epic saga.",
                "backdrop_index": 1,
                "cta_text": "View Series Cast & Episodes",
                "cta_url": "https://www.themoviedb.org/tv/66732"
            }
        ]
    },

    # 4. The Boys
    "the-boys": {
        "title": "Homelander Unhinged: 5 Sickest Twists In The Boys 🩸🦸‍♂️",
        "seo_description": "Inside the chaotic, bloody world of Vought, Compound V, and Butcher's war against Homelander.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🩸 DIABOLICAL SATIRE",
                "title": "Never Meet Your Heroes",
                "text": "In a world where superheroes are manufactured corporate celebrities, Billy Butcher and The Boys fight to expose Vought's darkest secrets.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🥛 HOMELANDER'S PSYCHOSIS",
                "title": "The God Complex",
                "text": "Antony Starr's chilling portrayal of Homelander turned him into modern television's most terrifying, unpredictable supervillain.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "💉 COMPOUND V",
                "title": "Superheroes Aren't Born",
                "text": "The greatest corporate cover-up: 'Supes' were never chosen by God. They were injected as babies with Vought's blue miracle drug, Compound V.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "⚔️ HEROGASM RECKONING",
                "title": "Soldier Boy's Revenge",
                "text": "Jensen Ackles joined the fray as Soldier Boy, leading to an epic, brutal showdown that almost stripped Homelander of his godlike reign.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🔥 FINAL SEASON WAR",
                "title": "Butcher's Last Stand",
                "text": "With deadly temp V rotting his brain and Homelander seizing government power, Butcher has nothing left to lose in the coming war.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 STREAM ON PRIME",
                "title": "Join The Anti-Hero Crusade",
                "text": "Catch every chaotic, unfiltered episode of The Boys on Prime Video and witness television history.",
                "backdrop_index": 1,
                "cta_text": "Explore The Boys Trivia",
                "cta_url": "https://www.themoviedb.org/tv/76479"
            }
        ]
    },

    # 5. Breaking Bad
    "breaking-bad": {
        "title": "I Am The Danger: How Walter White Became TV's Greatest Villain ⚗️",
        "seo_description": "From timid high school teacher to the legendary Heisenberg: how Vince Gilligan crafted television's greatest transformation.",
        "slides": [
            {
                "id": "page-1",
                "badge": "⚗️ PEAK TELEVISION",
                "title": "Mr. Chips to Scarface",
                "text": "Diagnosed with terminal lung cancer, modest chemistry teacher Walter White paired with slacker student Jesse Pinkman to brew blue crystal meth.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🎩 HEISENBERG RISES",
                "title": "This Is Not Meth",
                "text": "The moment Walt detonated Tuco Salamanca's hideout with fulminated mercury, Heisenberg was born—a ruthless ego that consumed Walter White.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🍗 LOS POLLOS HERMANOS",
                "title": "Gus Fring's Empire",
                "text": "Giancarlo Esposito's icy cold Gustavo Fring set the gold standard for television antagonists. His iconic final walking scene blew minds.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🚪 THE ONE WHO KNOCKS",
                "title": "I Am The Danger",
                "text": "'You clearly don't know who you're talking to. I am not in danger, Skyler. I AM the danger!' Bryan Cranston delivered TV's defining monologue.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🏆 OZYMANDIAS PERFECTION",
                "title": "A 10/10 Masterpiece",
                "text": "Episode 'Ozymandias' holds an unprecedented, perfect 10/10 score on IMDb with over 200,000 votes—widely crowned the greatest TV hour ever aired.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 REWATCH THE LEGEND",
                "title": "Stream Breaking Bad & BCS",
                "text": "Revisit Walter White and Saul Goodman's Albuquerque crime empire across Netflix and AMC.",
                "backdrop_index": 1,
                "cta_text": "Check Series Facts & Cast",
                "cta_url": "https://www.themoviedb.org/tv/1396"
            }
        ]
    },

    # 6. Wednesday
    "wednesday": {
        "title": "Wednesday Addams: 5 Goth Secrets That Broke Netflix Records 🖤🕷️",
        "seo_description": "Jenna Ortega's gothic charm, Thing's practical magic, and Tim Burton's Nevermore Academy secrets revealed.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🖤 GOTH RECORD-BREAKER",
                "title": "Nevermore's Dark Outcast",
                "text": "Smart, sarcastic, and a little dead inside, Wednesday Addams took Nevermore Academy by storm, amassing over 1 billion view hours in weeks.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "💃 VIRAL DANCE CRAZE",
                "title": "The Goo Goo Muck Dance",
                "text": "Jenna Ortega personally choreographed the iconic Rave'N Dance scene in just a few days, inspiring tens of millions of TikTok recreations.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "✋ THING WAS 100% REAL",
                "title": "Practical Hand Magic",
                "text": "Thing wasn't CGI! Magician Victor Dorobantu wore a full blue chroma-suit, hiding under tables and contorting his body to bring the disembodied hand to life.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎬 TIM BURTON'S TOUCH",
                "title": "No Blinking Allowed",
                "text": "Director Tim Burton instructed Jenna Ortega not to blink while on camera to give Wednesday an eerie, unnerving gothic presence.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🎻 CELLO VIRTUOSO",
                "title": "Paint It Black",
                "text": "Ortega learned how to play the cello specifically for the role, performing intense instrumental renditions of The Rolling Stones and Metallica.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 SEASON 2 AHEAD",
                "title": "More Darkness Incoming",
                "text": "Prepare for Wednesday Season 2 as Nevermore opens its gates to darker villains and more supernatural chaos.",
                "backdrop_index": 1,
                "cta_text": "Explore Wednesday Details",
                "cta_url": "https://www.themoviedb.org/tv/119051"
            }
        ]
    },

    # 7. Game of Thrones
    "game-of-thrones": {
        "title": "Winter Is Here: 5 Shocking Westeros Secrets Finally Unveiled 🐉⚔️",
        "seo_description": "Dragons, betrayal, and the iron throne: discover the epic lore and production feats behind Game of Thrones.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🐉 DRAGON FIRE",
                "title": "Win Or You Die",
                "text": "Nine noble houses fought ruthlessly for the Iron Throne, while an icy threat beyond the 700-foot Wall prepared to wipe out humanity.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🍷 THE RED WEDDING",
                "title": "The Rains of Castamere",
                "text": "The Red Wedding shocked millions of viewers into silence, breaking every fantasy TV convention and proving nobody in Westeros is ever safe.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "⚔️ BATTLE OF THE BASTARDS",
                "title": "Cinematic War Mastery",
                "text": "Jon Snow facing a charging cavalry alone was filmed with 500 extras, 70 real horses, and 25 days of brutal mud and steel stunt work.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "👑 MOTHER OF DRAGONS",
                "title": "Daenerys & Drogon",
                "text": "From an exiled Targaryen princess to breaker of chains, Daenerys commanded three colossal dragons that brought kingdoms to their knees.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "❄️ WINTER IS HERE",
                "title": "Night King's March",
                "text": "The long-awaited invasion of the Army of the Dead took 55 consecutive freezing night shoots in Northern Ireland to capture the Long Night.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 EXPLORE WESTEROS",
                "title": "House of the Dragon & GOT",
                "text": "Binge the complete 8 seasons of Game of Thrones and prequel House of the Dragon on Max today.",
                "backdrop_index": 1,
                "cta_text": "Discover GOT Lore & Cast",
                "cta_url": "https://www.themoviedb.org/tv/1399"
            }
        ]
    },

    # 8. Interstellar
    "interstellar": {
        "title": "Into The Black Hole: 5 Christopher Nolan Mindfucks In Interstellar 🚀⏳",
        "seo_description": "Time dilation on Miller's Planet, Gargantua's real physics, and the fifth dimension tesseract explained.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🚀 SCI-FI EPIC",
                "title": "Beyond Our Dying Earth",
                "text": "When Earth faced agricultural extinction, Cooper left his family behind to journey through a mysterious Saturn wormhole into the unknown.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🌊 MILLER'S PLANET",
                "title": "Every Hour Is 7 Years",
                "text": "Trapped in Gargantua's gravitational time dilation, every tick of Hans Zimmer's soundtrack represented 1 day passing on Earth. Cooper lost 23 years in minutes.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🌌 GARGANTUA PHYSICS",
                "title": "Nobel Prize Science",
                "text": "Astrophysicist Kip Thorne calculated the exact mathematical equations for Gargantua, rendering the most accurate black hole visual in human history.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🤖 TARS & PRACTICAL FX",
                "title": "No Green Screen Robots",
                "text": "TARS wasn't animated CGI! Puppeteer Bill Irwin physically pushed and operated an 86-kilogram hydraulic rig live on Icelandic glaciers.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "📚 THE TESSERACT",
                "title": "Love Transcends Dimensions",
                "text": "Trapped inside the 5-dimensional tesseract, Cooper discovered love was the one quantum force capable of bridging space, time, and gravity.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🍿 EXPERIENCE INTERSTELLAR",
                "title": "Christopher Nolan's Masterpiece",
                "text": "Experience Interstellar in IMAX 70mm or 4K Ultra HD for the ultimate cosmic emotional voyage.",
                "backdrop_index": 1,
                "cta_text": "View Interstellar Credits",
                "cta_url": "https://www.themoviedb.org/movie/157336"
            }
        ]
    },

    # 9. Inception
    "inception": {
        "title": "Did The Top Stop Spinning? 5 Mind-Bending Inception Secrets 🌀💤",
        "seo_description": "Dream layers, the rotating hallway fight, and the final spinning top debate in Christopher Nolan's Inception.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🌀 MIND HEIST",
                "title": "Your Mind Is The Crime Scene",
                "text": "Dom Cobb extracts secrets from corporate targets while they dream. But planting an original idea requires diving 3 layers deep into the subconscious.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "⏳ TIME EXPANSION",
                "title": "The Multi-Layer Kick",
                "text": "5 minutes in the real world equals 1 hour in dream 1, 12 hours in dream 2, and decades in Limbo. One wrong move leaves you in subconscious purgatory.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🥋 ROTATING HALLWAY",
                "title": "Zero CGI Gravity Fight",
                "text": "Joseph Gordon-Levitt trained for weeks to perform in a massive 100-foot rotating steel centrifuge, creating cinema's greatest gravity-defying brawl.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎺 THE HANS ZIMMER BRAAM",
                "title": "Edith Piaf Slowed 10x",
                "text": "The earth-shaking brass horn 'BRAAM' sound was created by slowing down Édith Piaf's song 'Non, je ne regrette rien' to match dream time dilation.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "💍 THE WEDDING RING",
                "title": "The Real Totem Revealed",
                "text": "The spinning top wasn't Cobb's totem—it was Mal's! Look closely: Cobb only wears his wedding ring inside dreams, but is bare-handed in the finale.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🎬 STREAM INCEPTION",
                "title": "Wake Up To Reality",
                "text": "Dive back into the dream architecture of Christopher Nolan's 4-time Oscar-winning sci-fi thriller.",
                "backdrop_index": 1,
                "cta_text": "Check Inception Details",
                "cta_url": "https://www.themoviedb.org/movie/27205"
            }
        ]
    },

    # 10. The Dark Knight
    "the-dark-knight": {
        "title": "Why So Serious? How Heath Ledger's Joker Made Movie History 🃏🦇",
        "seo_description": "Heath Ledger's diary, the hospital explosion, and the philosophical war for Gotham's soul in The Dark Knight.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🃏 AGENT OF CHAOS",
                "title": "Welcome To A World Without Rules",
                "text": "When the Joker unleashes psychological warfare on Gotham City, Batman must cross his moral lines to prevent total civic collapse.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🏨 HOSPITAL EXPLOSION",
                "title": "Heath's Unscripted Stunt",
                "text": "When the detonator misfired during the real hospital blast, Heath Ledger stayed in character, fiddling with the remote until it blew up behind him.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "📓 THE JOKER DIARY",
                "title": "Months In Isolation",
                "text": "Ledger locked himself in a London hotel room for 6 weeks, filling a notebook with hyena laughter, unsettling drawings, and manic handwriting.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🚛 REAL 18-WHEELER FLIP",
                "title": "No Computer Graphics",
                "text": "Nolan flipped an actual 18-wheel semi-truck vertically in downtown Chicago using a massive TNT piston under the trailer.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🦇 YOU COMPLETE ME",
                "title": "An Unstoppable Force",
                "text": "The interrogation scene redefined comic cinema: Batman and Joker aren't just foes; they are two sides of an eternal philosophical coin.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🏆 OSCAR TRIUMPH",
                "title": "Cinema's Greatest Villain",
                "text": "Heath Ledger won a posthumous Academy Award, forever etching The Dark Knight into film history.",
                "backdrop_index": 1,
                "cta_text": "Explore Dark Knight Trivia",
                "cta_url": "https://www.themoviedb.org/movie/155"
            }
        ]
    },

    # 11. John Wick: Chapter 4
    "john-wick-chapter-4": {
        "title": "Baba Yaga Returns: 442 Kills & Insane Stunt Secrets Revealed 🔫🥋",
        "seo_description": "The Dragon's Breath top-down shotgun sequence, Sacré-Cœur 222 steps, and Keanu Reeves' martial arts training in John Wick 4.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🥋 BABA YAGA IS BACK",
                "title": "One Way Out",
                "text": "With a multimillion-dollar bounty on his head, John Wick challenges the High Table to a duel to the death for his eternal freedom.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🔥 TOP-DOWN SHOTGUN",
                "title": "Dragon's Breath Spectacle",
                "text": "Filmed in a single continuous bird's-eye shot inspired by the video game 'Hong Kong Massacre', Wick clears an entire apartment with incendiary rounds.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "⛪ 222 STEPS STUNT",
                "title": "The Fall of Sacré-Cœur",
                "text": "Stuntman Vincent Bouillon tumbled down all 222 concrete steps of Sacré-Cœur multiple times to capture Wick's agonizing climb to dawn.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🦯 DONNIE YEN'S CAINE",
                "title": "The Blind Assassin",
                "text": "Martial arts master Donnie Yen brought lethal elegance as blind assassin Caine, using motion sensors and doorbell chimes to take down waves of killers.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🚗 ARC DE TRIOMPHE",
                "title": "Doorless Drift Shooting",
                "text": "Keanu Reeves spent months mastering reverse 180-degree car drifts while simultaneously reloading and firing a live pistol out the missing driver door.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🍿 STREAM JOHN WICK",
                "title": "Witness Action Perfection",
                "text": "Experience nearly 3 hours of adrenaline-pumping stunt choreography in John Wick: Chapter 4 on 4K Blu-ray and digital platforms.",
                "backdrop_index": 1,
                "cta_text": "Check John Wick 4 Stats",
                "cta_url": "https://www.themoviedb.org/movie/603692"
            }
        ]
    },

    # 12. Deadpool & Wolverine
    "deadpool-and-wolverine": {
        "title": "Maximum Effort! 5 Mindblowing Marvel Cameos & Secrets ⚔️🍿",
        "seo_description": "Hugh Jackman's comic-accurate yellow suit, shocking multiverse cameos, and box office records in Deadpool & Wolverine.",
        "slides": [
            {
                "id": "page-1",
                "badge": "⚔️ MAXIMUM EFFORT",
                "title": "The Marvel Jesus",
                "text": "Wade Wilson's civilian life is shattered when the TVA threatens his entire timeline, forcing him to track down a reluctant, battle-scarred Wolverine.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🟡 THE YELLOW SUIT",
                "title": "24 Years In The Making",
                "text": "After 24 years playing Wolverine in black leather, Hugh Jackman finally suited up in the iconic comic-accurate yellow and blue spandex suit.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🃏 BLADE & GAMBIT RETURN",
                "title": "The Void Resistance",
                "text": "Wesley Snipes shattered Guinness records returning as Blade 26 years later, while Channing Tatum finally realized his dream playing Gambit.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🐕 DOGPOOL CELEBRITY",
                "title": "Britain's Ugliest Dog",
                "text": "Peggy, a real-life pug-Chinese crested mix crowned Britain's ugliest dog, stole hearts worldwide as Wade's beloved Mary Puppins (Dogpool).",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "💰 $1.3 BILLION RECORD",
                "title": "Highest Grossing R-Rated Film",
                "text": "Deadpool & Wolverine conquered the global box office with $1.33 billion, becoming the highest-grossing R-rated movie in cinematic history.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🍿 STREAM ON DISNEY+",
                "title": "Watch The Dynamic Duo",
                "text": "Stream Deadpool & Wolverine in IMAX Enhanced on Disney+ with exclusive behind-the-scenes gag reels.",
                "backdrop_index": 1,
                "cta_text": "Explore Cameos & Cast",
                "cta_url": "https://www.themoviedb.org/movie/533535"
            }
        ]
    },

    # 13. Dune: Part Two
    "dune-part-two": {
        "title": "Shai-Hulud Unleashed: 5 Epic Dune 2 Secrets You Missed 🏜️🔥",
        "seo_description": "Riding the giant sandworms, Austin Butler's terrifying Feyd-Rautha, and the battle for Arrakis in Dune 2.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🏜️ SCI-FI MASTERPIECE",
                "title": "The Prophet of Arrakis",
                "text": "Paul Atreides unites with Chani and the Fremen to wage holy war against House Harkonnen, fulfilling ancient spice prophecies.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🪱 RIDING SHAI-HULUD",
                "title": "Filming The Sandworm",
                "text": "Director Denis Villeneuve created a separate 'worm unit' that spent 3 months in Jordan's desert filming Timothée Chalamet on a mechanical shaking rig.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "⚫ GIEDI PRIME IN INFRARED",
                "title": "Feyd-Rautha's Arena",
                "text": "The monochrome Harkonnen gladiator sequence was filmed using specialized infrared cameras to simulate the planet's black sun illumination.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "⚔️ KNIFE FIGHT DYNAMICS",
                "title": "Paul vs. Feyd-Rautha",
                "text": "Austin Butler and Timothée Chalamet trained for months to execute the brutal final knife duel without stunt doubles, relying on practical choreography.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "👁️ WATER OF LIFE",
                "title": "The Golden Path",
                "text": "Drinking the lethal Water of Life, Paul awakens the memories of all his ancestors, foreseeing billions dying across the galaxy in his name.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🍿 EXPERIENCE DUNE 2",
                "title": "Prepare For Dune Messiah",
                "text": "Experience Dune: Part Two on 4K Ultra HD and stream the epic saga ahead of Denis Villeneuve's Dune Messiah.",
                "backdrop_index": 1,
                "cta_text": "Check Dune 2 Details",
                "cta_url": "https://www.themoviedb.org/movie/693134"
            }
        ]
    },

    # 14. Gladiator II
    "gladiator-ii": {
        "title": "Echoes In Eternity: Inside Ridley Scott's Epic Colosseum War 🏛️⚔️",
        "seo_description": "Paul Mescal as Lucius, naval Colosseum battles, and Denzel Washington's mastermind in Gladiator II.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🏛️ RETURN TO ROME",
                "title": "Echoes In Eternity",
                "text": "Years after Maximus gave his life for Rome, his son Lucius is dragged into the Colosseum as a gladiator to challenge tyrannical co-emperors.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🦈 NAVAL COLOSSEUM WAR",
                "title": "Flooding The Arena",
                "text": "Ridley Scott recreated ancient Rome's naumachia, flooding the Colosseum arena with water, warships, and man-eating sharks.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "👑 MACRINUS MASTERMIND",
                "title": "Denzel's Puppet Show",
                "text": "Denzel Washington steals the show as Macrinus, a ruthless arms dealer who uses gladiators and political scheming to seize the imperial throne.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🦏 WAR RHINO STUNT",
                "title": "Beasts of the Arena",
                "text": "Lucius faces savage gladiatorial challenges including rabid baboons and a colossal war rhino controlled with jaw-dropping practical animatronics.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "⚔️ HONORING MAXIMUS",
                "title": "A Father's Armor",
                "text": "When Lucius dons the breastplate of Maximus Decimus Meridius, Rome witnesses the resurrection of the dream of a free Republic.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🍿 THEATRICAL EVENT",
                "title": "Witness Gladiator II",
                "text": "Experience the blood and glory of Ridley Scott's Gladiator II on the biggest cinema screens worldwide.",
                "backdrop_index": 1,
                "cta_text": "Explore Gladiator II Cast",
                "cta_url": "https://www.themoviedb.org/movie/558449"
            }
        ]
    }
}
