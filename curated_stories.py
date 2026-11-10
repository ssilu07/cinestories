"""
Curated, high-CTR storytelling slides for Hollywood's most viral Blockbusters,
TV Series, and Cult Franchises.
Strictly compliant with Google AMP Web Story guidelines (Word count < 40 words per slide).
"""

from typing import Dict, Any

CURATED_STORIES: Dict[str, Dict[str, Any]] = {

    # 1. Panchayat Season 3
    "panchayat-season-3": {
        "title": "Did Pradhan Ji Stage His Own Shooting? Panchayat S3 Ending Decoded",
        "seo_description": "Unpack the 3 crucial clues behind the shocking bus stand shooting of Pradhan Ji in Panchayat Season 3.",
        "slides": [
            {
                "id": "page-1",
                "badge": "⚡ CLIFFHANGER CLIMAX",
                "title": "The Phulera Bloodshed",
                "text": "Two masked motorbike assassins pulled triggers at the Phulera bus stand. Pradhan Ji was shot in the shoulder. But who ordered the hit?",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "❓ THE BURNING MYSTERY",
                "title": "Did Vidhayak Really Do It?",
                "text": "Local MLA Vidhayak Ji has violent motives, but shooting Pradhan Ji days before the election guarantees an overwhelming sympathy wave for Phulera's camp.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🔍 CLUE #1: SHOULDER SHOT",
                "title": "A Non-Fatal Wound",
                "text": "The assassins had point-blank range, yet chose the shoulder rather than a fatal chest shot. Professional hit or a staged political drama?",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🕵️ CLUE #2: BHUSHAN'S CALL",
                "title": "The Informer's Alibi",
                "text": "Banrakas Bhushan was standing near the market when the shooting occurred. His frantic reaction proved even the opposition camp was caught completely off guard.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "💡 THE DECODED TRUTH",
                "title": "The Sympathy Wave Strategy",
                "text": "With Manju Devi trailing in initial village opinion, a near-fatal shooting completely turned public sentiment. Pradhan Ji secured the election in blood.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🚜 VILLAGE POLITICS",
                "title": "Real UP Panchayat Elections",
                "text": "Director Deepak Kumar Mishra confirmed Season 4 focuses heavily on the police investigation and the fallout of the bus stand brawl.",
                "backdrop_index": 1
            },
            {
                "id": "page-7",
                "badge": "📺 SEASON 4 ROADMAP",
                "title": "Sachiv Ji's Transfer Blocked",
                "text": "Abhishek's transfer is officially suspended due to the criminal FIR. Season 4 will premiere on Amazon Prime Video in late 2025.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "What Do You Believe?",
                "text": "Cast your vote below on who really pulled the strings behind the Phulera assassination attempt.",
                "backdrop_index": 1,
                "poll": {
                    "id": "poll-panchayat-s3",
                    "type": "binary",
                    "prompt": "Did Pradhan Ji stage the shooting?",
                    "option1": "Yes, 100% staged",
                    "option2": "No, Vidhayak did it"
                },
                "cta_text": "Read Full Season 3 Breakdown",
                "cta_url": None
            }
        ]
    },

    # 2. Mirzapur Season 3
    "mirzapur-season-3": {
        "title": "Why Kaleen Bhaiya Killed Sharad Shukla: The Hidden Deal in Mirzapur 3!",
        "seo_description": "Unravel the shocking climax betrayal, Madhuri's hidden pact, and Maqbool's return in Mirzapur Season 3.",
        "slides": [
            {
                "id": "page-1",
                "badge": "👑 THRONE BETRAYAL",
                "title": "The 10-Second Reign",
                "text": "Sharad Shukla touched the throne of Mirzapur for barely ten seconds before a bullet ended his life. But who pulled the strings?",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🤝 THE SECRET PACT",
                "title": "Madhuri's Hidden Deal",
                "text": "Chief Minister Madhuri Yadav promised Kaleen Bhaiya absolute immunity and Purvanchal control on one chilling condition: eliminate Sharad Shukla.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🩸 GUDDU'S MADNESS",
                "title": "The Fall of Guddu Pandit",
                "text": "Addicted to power and drugs, Guddu Pandit lost control of the streets, paving the way for Akhandanand Tripathi's calculated return.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎭 ROBIN'S FATE",
                "title": "A Tragic Murder",
                "text": "Guddu crushing Robin's throat in a fit of rage shattered his alliance with Dimpy, isolating himself completely before his arrest.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🎬 POST-CREDITS STINGER",
                "title": "Maqbool Returns",
                "text": "In the final post-credits scene, Beena Tripathi secretly contacts exiled enforcer Maqbool Khan, setting up an explosive vengeance arc.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "⚔️ JAIL ESCAPE SETUP",
                "title": "Guddu Behind Bars",
                "text": "With Golu orchestrating his rescue from prison, Guddu prepares for an all-out war across Uttar Pradesh in Season 4.",
                "backdrop_index": 1
            },
            {
                "id": "page-7",
                "badge": "📺 SEASON 4 RELEASE",
                "title": "The Ultimate Finale",
                "text": "Mirzapur Season 4 has officially entered pre-production, aiming for a late 2025 release on Amazon Prime Video.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "Who Rules Mirzapur?",
                "text": "Vote on who deserves to sit on the blood-soaked throne of Mirzapur in Season 4.",
                "backdrop_index": 1,
                "poll": {
                    "id": "poll-mirzapur-s3",
                    "type": "binary",
                    "prompt": "Who will conquer Mirzapur in S4?",
                    "option1": "Kaleen Bhaiya",
                    "option2": "Guddu Pandit"
                },
                "cta_text": "Read Full Mirzapur 3 Breakdown",
                "cta_url": None
            }
        ]
    },

    # 3. Stree 2
    "stree-2": {
        "title": "Is Akshay Kumar the 'Thanos' of Maddock Universe? Stree 2 Post-Credits Decoded!",
        "seo_description": "Decode the shocking Sarkata post-credits scene, Akshay Kumar's supervillain role, and Shraddha's parentage in Stree 2.",
        "slides": [
            {
                "id": "page-1",
                "badge": "👻 CHANDERI UNIVERSE",
                "title": "The Headless Menace",
                "text": "The headless demon Sarkata terrified the women of Chanderi, forcing the town to unite with the spirit of Stree.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🔥 POST-CREDITS SHOCK",
                "title": "Akshay Kumar Revealed",
                "text": "Locked inside an asylum, Akshay Kumar plays Sarkata's descendant who inhales the demon's ashes to become the universe's ultimate supervillain.",
                "backdrop_index": 0
            },
            {
                "id": "page-3",
                "badge": "🩸 SHRADDHA'S SECRET",
                "title": "Daughter of Stree",
                "text": "Shraddha Kapoor's mysterious character was finally revealed as the biological daughter of the original Stree spirit from 1824.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🐺 BHEDIYA CROSSOVER",
                "title": "Varun Dhawan's Entry",
                "text": "Bhaskar transforms into Bhediya to battle Sarkata alongside Vicky, officially cementing the interconnected Maddock Supernatural Universe.",
                "backdrop_index": 0
            },
            {
                "id": "page-5",
                "badge": "🧠 THE THANOS PARALLEL",
                "title": "Maddock's Master Villain",
                "text": "Director Amar Kaushik confirmed Akshay Kumar's character will serve as the overarching villain across Stree 3, Bhediya 2, and Thama.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "💰 600 CRORE RECORD",
                "title": "Box Office History",
                "text": "Stree 2 shattered all records to become the highest-grossing Hindi film in domestic box office history, crossing 600 crore net.",
                "backdrop_index": 0
            },
            {
                "id": "page-7",
                "badge": "🔮 WHAT'S NEXT",
                "title": "Roadmap to Stree 3",
                "text": "Ayushmann Khurrana enters next in Thama as a vampire, leading directly into the massive ensemble showdown of Stree 3.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "Ultimate Showdown Vote",
                "text": "Who will defeat Akshay Kumar's supervillain in the Maddock Universe finale?",
                "backdrop_index": 0,
                "poll": {
                    "id": "poll-stree-2",
                    "type": "binary",
                    "prompt": "Who defeats Sarkata's heir?",
                    "option1": "Stree & Shraddha",
                    "option2": "Bhediya & Vicky"
                },
                "cta_text": "Read Stree 2 Universe Guide",
                "cta_url": None
            }
        ]
    },

    # 4. Kalki 2898 AD
    "kalki-2898-ad": {
        "title": "Why Prabhas is Karna, Not Kalki: The Mind-Blowing Climax of Kalki 2898 AD!",
        "seo_description": "Unpack the epic Mahabharata connections, Bhairava's Karna awakening, and Supreme Yaskin's Gandiva bow in Kalki 2898 AD.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🏹 MAHABHARAT PROPHECY",
                "title": "Divine Reincarnation",
                "text": "In the dystopian wasteland of Kasi, bounty hunter Bhairava unwittingly unlocks cosmic power when he touches the divine staff Vijaya.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "⚡ THE KARNA REVEAL",
                "title": "Not Kalki, But Karna!",
                "text": "As the sun rises, memories of the Kurukshetra war ignite. Bhairava is revealed to be the reincarnation of Suryaputra Karna.",
                "backdrop_index": 0
            },
            {
                "id": "page-3",
                "badge": "🛡️ ASHWATTHAMA'S BOW",
                "title": "The Immortal Recognizes Him",
                "text": "Amitabh Bachchan's towering Ashwatthama stops his attack in awe, recognizing his fallen comrade's unmatched archery stance.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "👑 SUPREME YASKIN",
                "title": "Kamal Haasan's Threat",
                "text": "Supreme Yaskin absorbs the divine serum from Sumathi's unborn child and lifts Arjuna's legendary bow Gandiva.",
                "backdrop_index": 0
            },
            {
                "id": "page-5",
                "badge": "🌟 THE ACTUAL KALKI",
                "title": "Sumathi's Unborn Child",
                "text": "Director Nag Ashwin clarified that Deepika Padukone's unborn child is the true 10th avatar of Vishnu, not Bhairava.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "⚔️ PART 2 CONFLICT",
                "title": "Karna vs Arjuna's Bow",
                "text": "Kalki Part 2 will feature an epic mythological collision: Karna's reincarnation defending Kalki against Yaskin wielding Gandiva.",
                "backdrop_index": 0
            },
            {
                "id": "page-7",
                "badge": "🎬 CINEMATIC SCALE",
                "title": "Global Box Office Giant",
                "text": "Grossing over 1,000 crores worldwide, Kalki 2898 AD revolutionized Indian sci-fi filmmaking on a grand scale.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "Mythological Clash Vote",
                "text": "Who will triumph in the climactic battlefield of Kalki 2898 AD Part 2?",
                "backdrop_index": 0,
                "poll": {
                    "id": "poll-kalki-2898",
                    "type": "binary",
                    "prompt": "Who wins the Part 2 duel?",
                    "option1": "Bhairava (Karna)",
                    "option2": "Supreme Yaskin"
                },
                "cta_text": "Read Kalki Climax Decoded",
                "cta_url": None
            }
        ]
    },

    # 5. Sector 36
    "sector-36": {
        "title": "The Horrific Real Story Behind Sector 36: Nithari Reality vs Netflix!",
        "seo_description": "Explore the chilling true crime origins, Vikrant Massey's interrogation scene, and police files behind Sector 36.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🔪 DARK CRIME THRILLER",
                "title": "The House of Horrors",
                "text": "A dilapidated bungalow in Sector 36 hides a sadistic butcher preying on slum children while local authorities look the other way.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🩸 VIKRANT'S MONSTER",
                "title": "Prem Singh's Confession",
                "text": "Vikrant Massey delivers a chilling performance as Prem, casually eating fried fish while describing his gruesome crimes without emotion.",
                "backdrop_index": 0
            },
            {
                "id": "page-3",
                "badge": "⚖️ THE NITHARI REALITY",
                "title": "True 2006 Police Files",
                "text": "Sector 36 is inspired by the infamous 2006 Nithari serial killings in Noida, where skulls and bones were unearthed from drainage ditches.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🕵️ THE TRAGIC COP",
                "title": "Inspector Pandey's Awakening",
                "text": "Deepak Dobriyal's Inspector Ram Charan Pandey transforms from a bribed cop to an obsessed father after his own daughter is targeted.",
                "backdrop_index": 0
            },
            {
                "id": "page-5",
                "badge": "🏛️ SYSTEMIC COLLAPSE",
                "title": "Why the Rich Escape",
                "text": "The film boldly illustrates how political influence shielded wealthy mastermind Bassi, mirroring the real-world Nithari court acquittals.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "⚠️ THE GRIM FINALE",
                "title": "No Triumphant Justice",
                "text": "Instead of a Bollywood heroic victory, Pandey is ruthlessly executed, leaving the corrupt hierarchy completely intact.",
                "backdrop_index": 0
            },
            {
                "id": "page-7",
                "badge": "📺 NETFLIX RECEPTION",
                "title": "Critically Acclaimed Hit",
                "text": "Directed by Aditya Nimbalkar, Sector 36 ranked among Netflix's top non-English films worldwide within 48 hours.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "True Crime Impact Vote",
                "text": "Did Sector 36 portray the systemic failure of the justice system accurately?",
                "backdrop_index": 0,
                "poll": {
                    "id": "poll-sector-36",
                    "type": "binary",
                    "prompt": "Did Sector 36 capture real Nithari?",
                    "option1": "Yes, chillingly accurate",
                    "option2": "Fictionalized too much"
                },
                "cta_text": "Read Sector 36 True Story",
                "cta_url": None
            }
        ]
    },

    # 6. Do Patti
    "do-patti": {
        "title": "Did Dhruv Really Try to Kill Saumya? The Shocking Twist Ending of Do Patti Decoded!",
        "seo_description": "Decode the twin sister paraglider conspiracy, Kriti Sanon's double role, and Kajol's moral dilemma in Do Patti.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🎭 IDENTICAL TWINS",
                "title": "The Misty Hills Mystery",
                "text": "In the picturesque town of Devigarh, identical twin sisters Saumya and Shailee play a lethal psychological game of deception.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🪂 SABOTAGED PARAGLIDER",
                "title": "The Attempted Murder",
                "text": "Saumya plunges from the sky in a sabotaged paraglider crash. All evidence points directly to her abusive husband Dhruv Sood.",
                "backdrop_index": 0
            },
            {
                "id": "page-3",
                "badge": "💡 THE TWIST ENDING",
                "title": "The Mastermind Plan",
                "text": "The paraglider harness was intentionally tampered with by the sisters themselves to send Dhruv to prison for attempted murder.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "📜 SECTION 498A",
                "title": "Legal Loopholes Exposed",
                "text": "Unable to secure justice against domestic abuse under weak laws, Saumya engineered an attempted murder charge to guarantee Dhruv's conviction.",
                "backdrop_index": 0
            },
            {
                "id": "page-5",
                "badge": "⚖️ KAJOL'S DILEMMA",
                "title": "Inspector Vidya's Choice",
                "text": "Kajol's Inspector Vidya uncovers the truth, but tears up the evidence in court, choosing moral justice over corrupt legality.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🌟 KRITI'S DOUBLE ROLE",
                "title": "Career-Best Performance",
                "text": "Kriti Sanon delivered contrasting shades of vulnerability and venom as producer and lead in her first double role.",
                "backdrop_index": 0
            },
            {
                "id": "page-7",
                "badge": "📊 CHART-TOPPING RUN",
                "title": "Global Netflix Success",
                "text": "Do Patti reached the Global Top 10 on Netflix across 25 countries, generating viral social debates on domestic abuse laws.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "Moral Dilemma Vote",
                "text": "Was Inspector Vidya right to tear up the evidence and let the twins walk free?",
                "backdrop_index": 0,
                "poll": {
                    "id": "poll-do-patti",
                    "type": "binary",
                    "prompt": "Did Kajol do the right thing?",
                    "option1": "Yes, moral justice won",
                    "option2": "No, breaking law is wrong"
                },
                "cta_text": "Read Do Patti Twist Decoded",
                "cta_url": None
            }
        ]
    },

    # 7. Devara: Part 1
    "devara-part-1": {
        "title": "The Next 'Katappa' Mystery: Why Did Vara Murder His Own Father Devara?",
        "seo_description": "Unpack the shocking patricide climax, the Red Sea shark battle, and Devara Part 2 setup in Jr NTR's action epic.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🌊 COASTAL CARNAGE",
                "title": "The Smuggling Clans",
                "text": "Four coastal villages fight over illegal sea smuggling until Devara demands an immediate end to blood-soaked piracy.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🦈 UNDERWATER TERROR",
                "title": "The Shark Sequence",
                "text": "Jr NTR delivers a legendary sea battle, riding and butchering a ferocious shark while retrieving contraband from the ocean deep.",
                "backdrop_index": 0
            },
            {
                "id": "page-3",
                "badge": "⚔️ THE GHOST ON WATER",
                "title": "Fear Governs the Sea",
                "text": "When Devara vanishes, his legendary weapons continue appearing on the shore, keeping the treacherous Bhaira terrified of the dark water.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🩸 THE PATRICIDE SHOCK",
                "title": "Vara Killed Devara!",
                "text": "The climax unleashes the biggest twist: mild-mannered son Vara stabbed his own father Devara in cold blood years ago.",
                "backdrop_index": 0
            },
            {
                "id": "page-5",
                "badge": "❓ WHY DID VARA KILL HIM?",
                "title": "The Katappa Secret",
                "text": "Did Devara order his son to sacrifice him to become an immortal symbol of fear, or did Vara have a sinister betrayal motive?",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "👑 JR NTR'S DUAL ROLE",
                "title": "Fierce vs Mild-Mannered",
                "text": "Jr NTR's masterful physical transformation between the commanding father Devara and the cowardly son Vara stunned audiences.",
                "backdrop_index": 0
            },
            {
                "id": "page-7",
                "badge": "🎬 PART 2 ROADMAP",
                "title": "The War of the Seas",
                "text": "Devara Part 2 will unravel the true reason behind the patricide and pit Vara against Saif Ali Khan's vengeful Bhaira.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "The Big Mystery Vote",
                "text": "Why did Vara murder his own father Devara?",
                "backdrop_index": 0,
                "poll": {
                    "id": "poll-devara",
                    "type": "binary",
                    "prompt": "Why did Vara kill Devara?",
                    "option1": "Devara ordered him to",
                    "option2": "Vara secretly betrayed him"
                },
                "cta_text": "Read Devara Climax Breakdown",
                "cta_url": None
            }
        ]
    },

    # 8. Pushpa 2: The Rule
    "pushpa-2-the-rule": {
        "title": "Pushpa 2 Ending Decoded: What That Shocking Wedding Blast Means for Pushpa 3!",
        "seo_description": "Decode the high-octane Jaathara fight, Shekawat's revenge, and the Pushpa 3: The Rampage cliffhanger stinger.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🪓 THE SYNDICATE KING",
                "title": "Pushpa Raj Rules",
                "text": "Pushpa Raj establishes undisputed dominion over red sandalwood smuggling, challenging the entire state machinery.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🔥 JAATHARA SPECTACLE",
                "title": "The Saree Fight",
                "text": "Allu Arjun's breathtaking Jaathara dance sequence in blue silk saree and ghungroos set internet records with 100M views.",
                "backdrop_index": 0
            },
            {
                "id": "page-3",
                "badge": "👮 SHEKAWAT'S VENGEANCE",
                "title": "The Climax Standoff",
                "text": "Fahadh Faasil's humiliated SP Bhanwar Singh Shekawat unleashes an unhinged, scorched-earth strategy to execute Pushpa.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "💥 WEDDING CLIFFHANGER",
                "title": "The Blast That Shook Fans",
                "text": "An explosive ambush during a high-profile wedding leaves characters fighting for survival and pushes Pushpa into exile.",
                "backdrop_index": 0
            },
            {
                "id": "page-5",
                "badge": "🌍 INTERNATIONAL SCALE",
                "title": "Red Sandalwood Empire",
                "text": "Director Sukumar expands the battlefield beyond Seshachalam into ports in Japan, Malaysia, and the Middle East.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "⚡ PUSHPA 3 STINGER",
                "title": "The Rampage Begins",
                "text": "The post-credits title card officially confirms Pushpa 3: The Rampage, setting up an international syndicate war.",
                "backdrop_index": 0
            },
            {
                "id": "page-7",
                "badge": "💰 1,500 CRORE TARGET",
                "title": "Box Office Juggernaut",
                "text": "Pushpa 2 shattered advance booking records worldwide, cementing Allu Arjun as a pan-Indian box office powerhouse.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "Sequel Hype Vote",
                "text": "Will Pushpa 3: The Rampage cross the 2,000 crore mark globally?",
                "backdrop_index": 0,
                "poll": {
                    "id": "poll-pushpa-2",
                    "type": "binary",
                    "prompt": "Will Pushpa 3 beat Pushpa 2?",
                    "option1": "Yes, 2,000 Cr+ beast",
                    "option2": "No, Part 2 was peak"
                },
                "cta_text": "Read Pushpa 2 Ending Decoded",
                "cta_url": None
            }
        ]
    },

    # 9. Squid Game Season 2
    "squid-game-season-2": {
        "title": "The Brutal Betrayal: Why Gi-hun’s Armed Coup Failed in Squid Game Season 2!",
        "seo_description": "Unpack the failed dormitory rebellion, the Front Man's psychological war, and new deadly games in Squid Game S2.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🦑 RETURN TO THE ARENA",
                "title": "Player 456 is Back",
                "text": "Three years after winning billions, Seong Gi-hun returns to the deadly island with crimson hair and a vow to dismantle the games.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🔫 THE ARMED REBELLION",
                "title": "Undercover Infiltration",
                "text": "Gi-hun coordinates an armed insurrection inside the dormitories, teaming up with unexpected allies to target the pink guards.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "💔 THE BRUTAL BETRAYAL",
                "title": "Why the Coup Failed",
                "text": "When given the choice between freedom and a growing piggy bank of 45.6 billion won, the players vote 'O' to keep playing.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎭 THE FRONT MAN'S GAME",
                "title": "Lee Byung-hun's Trap",
                "text": "The Front Man anticipated Gi-hun's rebellion, proving that human greed is the games' greatest weapon against reform.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "☠️ DEADLY NEW TRIALS",
                "title": "Nostalgic Nightmares",
                "text": "Season 2 introduces sadistic twists on traditional Korean childhood schoolyard games, eliminating contestants in seconds.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 GLOBAL NETFLIX TITAN",
                "title": "Record-Breaking Debut",
                "text": "Squid Game Season 2 shattered Netflix premiere records across 90 countries on December 26, 2024.",
                "backdrop_index": 1
            },
            {
                "id": "page-7",
                "badge": "🔮 SEASON 3 FINALE",
                "title": "The Final War in 2025",
                "text": "Director Hwang Dong-hyuk shot Season 2 and Season 3 back-to-back. The series finale arrives on Netflix in mid-2025.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "Gi-hun's Fate Vote",
                "text": "Can Seong Gi-hun ever truly destroy the Squid Game organization?",
                "backdrop_index": 1,
                "poll": {
                    "id": "poll-squid-game-s2",
                    "type": "binary",
                    "prompt": "Can Gi-hun end the game?",
                    "option1": "Yes, Front Man dies",
                    "option2": "No, the system wins"
                },
                "cta_text": "Read Squid Game 2 Climax",
                "cta_url": None
            }
        ]
    },

    # 10. Singham Again
    "singham-again": {
        "title": "Chulbul Pandey Joins Singham: The Post-Credits Crossover That Broke the Internet!",
        "seo_description": "Decode the epic Salman Khan Chulbul Pandey post-credits crossover, Ramayana allegory, and Cop Universe future in Singham Again.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🦁 THE COP UNIVERSE",
                "title": "Mission in Sri Lanka",
                "text": "Bajirao Singham launches a cross-border rescue mission to save Avni from dangerous international terrorist Danger Lanka.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "📖 RAMAYANA ALLEGORY",
                "title": "Mythological Parallels",
                "text": "Rohit Shetty structured the narrative around the Ramayana: Singham as Rama, Avni as Sita, Simmba as Hanuman, and Sooryavanshi as Lakshmana.",
                "backdrop_index": 0
            },
            {
                "id": "page-3",
                "badge": "🔥 CHULBUL PANDEY CAMEO",
                "title": "The Stinger That Blew Up",
                "text": "Salman Khan swaggered onto screen in the post-credits scene, putting on his aviators to officially join the Cop Universe.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🤝 SHETTY X DABANGG",
                "title": "Mission Chulbul Singham",
                "text": "Rohit Shetty and Salman Khan confirmed a standalone crossover film featuring Chulbul Pandey alongside Ajay Devgn's Singham.",
                "backdrop_index": 0
            },
            {
                "id": "page-5",
                "badge": "⚡ LADY SINGHAM",
                "title": "Deepika's Shakti Shetty",
                "text": "Deepika Padukone debuted as SP Shakti Shetty, bringing ruthless martial arts combat and cracking comedy into the squad.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "💥 DIWALI BOX OFFICE",
                "title": "350 Crore Blockbuster",
                "text": "Clashing against Bhool Bhulaiyaa 3, Singham Again delivered colossal Diwali collections backed by immense star power.",
                "backdrop_index": 0
            },
            {
                "id": "page-7",
                "badge": "🔮 WHAT'S NEXT",
                "title": "Future of the Universe",
                "text": "With Dabangg, Singham, Sooryavanshi, and Simmba under one banner, Bollywood's biggest franchise prepares for Mission 2026.",
                "backdrop_index": 0
            },
            {
                "id": "page-8",
                "badge": "🗳️ FAN VERDICT POLL",
                "title": "Universe Ranking Vote",
                "text": "Who is your favorite cop in Rohit Shetty's expanded Cop Universe?",
                "backdrop_index": 0,
                "poll": {
                    "id": "poll-singham-again",
                    "type": "binary",
                    "prompt": "Who is the top cop?",
                    "option1": "Bajirao Singham",
                    "option2": "Chulbul Pandey"
                },
                "cta_text": "Read Singham Again Post-Credits",
                "cta_url": None
            }
        ]
    }
,

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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
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
                "cta_url": None
            }
        ]
    },

    # 15. Weekly Top 10 Streaming Hits (US/UK) - Netflix / HBO / Prime
    "streaming-weekly-top-10-us-uk": {
        "title": "Top 10 Streaming Hits This Week in the US & UK 🍿📊",
        "seo_description": "Discover which shows are dominating Netflix, HBO Max, and Prime Video this week across the US and UK.",
        "slides": [
            {
                "id": "page-1",
                "badge": "📊 WEEKLY LEADERBOARD",
                "title": "The Streaming Race",
                "text": "Millions of viewers across the US and UK tuned in this week, crowning new viral champions across Netflix, HBO Max, and Amazon Prime Video.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🔴 NETFLIX #1 SENSATION",
                "title": "Global Record Breakers",
                "text": "International thrillers and true-crime docuseries dominated Netflix charts, accumulating over 250 million viewing hours in their debut week alone.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🟣 HBO SUNDAY DOMINANCE",
                "title": "Prestige TV Reigns Supreme",
                "text": "Sunday night appointment viewing is alive. Epic fantasy and dark criminal dramas held the top spot on HBO Max across the United States.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🔵 PRIME VIDEO HIT",
                "title": "Wasteland & Superheroes",
                "text": "Prime Video saw record surges with action-packed franchise adaptations and razor-sharp satire conquering both US and UK living rooms.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🇬🇧 UK VS 🇺🇸 US TRENDS",
                "title": "What Country Streams What?",
                "text": "While US viewers binged high-octane sci-fi, UK audiences catapulted gritty British crime procedurals and witty comedy into their top 5.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 WEEKEND WATCHLIST",
                "title": "Ready For Your Next Binge?",
                "text": "Plan your weekend watchlist now with our complete weekly breakdown of top 10 movies and series on streaming.",
                "backdrop_index": 1,
                "cta_text": "Explore Top 10 Streaming Charts",
                "cta_url": None
            }
        ]
    },

    # 16. Fallout (Prime Video Weekly Sensation)
    "fallout-prime-video": {
        "title": "Fallout: 5 Mind-Blowing Vault Secrets That Broke Prime Video ☢️ Vault 33",
        "seo_description": "Inside Vault 33 and the nuclear wasteland. 5 shocking secrets and Easter eggs from Prime Video's Fallout.",
        "slides": [
            {
                "id": "page-1",
                "badge": "☢️ VAULT-TEC EMPIRE",
                "title": "Welcome To Vault 33",
                "text": "When Lucy MacLean left the sanitized comfort of Vault 33, she stepped into a radioactive Californian wasteland full of ghouls and secrets.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🤠 THE GHOUL REVEAL",
                "title": "Walton Goggins As Cooper",
                "text": "Cooper Howard survived 200 years of nuclear hellfire. His transformation from Hollywood star to ruthless gunslinger Ghoul stole the entire series.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🤫 CONSPIRACY UNMASKED",
                "title": "Vault-Tec Dropped The Bomb",
                "text": "In a boardroom meeting of corporate titans, Vault-Tec executives revealed their sinister plot to ensure total monopoly by detonating the bombs themselves.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎮 GAME FIDELITY",
                "title": "100% Canon To Games",
                "text": "Todd Howard confirmed every event in Prime Video's series is officially canon to Bethesda's legendary Fallout video game timeline.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🎰 NEW VEGAS TEASE",
                "title": "Season 2 Destination",
                "text": "The jaw-dropping season finale camera pan over the Strip revealed New Vegas, setting the stage for an explosive Season 2 clash.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 STREAM ON PRIME",
                "title": "Binge Season 1 Today",
                "text": "Stream all 8 episodes of Fallout Season 1 in 4K HDR exclusively on Amazon Prime Video.",
                "backdrop_index": 1,
                "cta_text": "Explore Fallout Cast & Season 2",
                "cta_url": None
            }
        ]
    },

    # 17. House of the Dragon (HBO Max Weekly Chart-Topper)
    "house-of-the-dragon": {
        "title": "Dance of the Dragons: 5 Brutal Westeros Clashes On HBO Max 🐉🔥",
        "seo_description": "Inside the Targaryen civil war: dragon battles, Blood and Cheese, and Iron Throne betrayals on HBO Max.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🐉 FIRE AND BLOOD",
                "title": "A Dynasty Divided",
                "text": "The Greens versus the Blacks. When King Viserys died, brother fought sister and nephew fought uncle in Westeros' deadliest civil war.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "⚔️ ROOK'S REST CARNAGE",
                "title": "Dragon Vs. Dragon Battle",
                "text": "The battle at Rook's Rest delivered the most terrifying aerial dragon duel in television history as Vhagar, Sunfyre, and Meleys collided in flame.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🩸 BLOOD AND CHEESE",
                "title": "The Darkest Retaliation",
                "text": "Daemon Targaryen's ruthless decree 'A son for a son' plunged the Red Keep into irreversible psychological horror and tragedy.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "👑 RHAENYRA'S ARMY",
                "title": "The Dragonseeds Rise",
                "text": "To overcome Vhagar's immense size, Queen Rhaenyra found lowborn Targaryen bastards to claim unclaimed wild dragons Vermithor and Silverwing.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🔥 AEMOND'S REIGN",
                "title": "One Eye, No Mercy",
                "text": "Aemond Targaryen's betrayal of his brother Aegon II proved that in the game for the Iron Throne, family means nothing.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 WATCH ON HBO MAX",
                "title": "Stream Every Epic Episode",
                "text": "Experience both seasons of House of the Dragon streaming now on HBO Max.",
                "backdrop_index": 1,
                "cta_text": "Explore House of the Dragon",
                "cta_url": None
            }
        ]
    },

    # 18. Marvel Multiverse: Post-Credit Theories
    "marvel-post-credit-theories": {
        "title": "Marvel Post-Credits: 6 Insane Easter Eggs & Secret Wars Theories 🦸‍♂️⚡",
        "seo_description": "From Anchor Beings and Doctor Doom to Gambit's return—unpacking the biggest Marvel post-credit clues leading to Secret Wars.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🦸‍♂️ MARVEL DECODED",
                "title": "The End Credits Secret",
                "text": "Marvel revolutionized cinema by turning end credits into universe-altering teasers. Now, Phase 6 clues point directly toward catastrophic Multiversal War.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "⚓ ANCHOR BEINGS EXPLAINED",
                "title": "The Multiverse Anchor",
                "text": "Deadpool revealed that each universe relies on an Anchor Being. If that hero dies, their timeline decays into complete cosmic annihilation.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "👑 DOCTOR DOOM'S ARRIVAL",
                "title": "Robert Downey Jr. Returns",
                "text": "RDJ returning as Victor Von Doom isn't an Iron Man variant—comic theories suggest Doom will steal the Beyonder's powers to forge Battleworld.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🃏 GAMBIT & THE VOID",
                "title": "Did Gambit Escape?",
                "text": "Channing Tatum's post-credit TVA monitor screen proved Gambit survived Cassandra Nova's Void massacre through a magical sling-ring portal.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "😭 THOR WEEPING FOR WADE",
                "title": "The Battleworld Prophecy",
                "text": "Why was Thor crying over a dying Deadpool? Insiders theorize it takes place in the climactic final battle of Avengers: Doomsday.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🍿 PHASE 6 WATCHLIST",
                "title": "Prepare For Battleworld",
                "text": "Track upcoming Marvel release dates, comic connections, and post-credit breakdowns on CineStories.",
                "backdrop_index": 1,
                "cta_text": "Explore Marvel Multiverse Guide",
                "cta_url": None
            }
        ]
    },

    # 19. DC Universe: Easter Eggs & Multiverse Theories
    "dc-easter-eggs-theories": {
        "title": "DC Universe Secrets: 5 Dark Easter Eggs & Multiverse Theories 🦇🃏",
        "seo_description": "Arkham riddles, Joker ciphers, and James Gunn's DCU roadmap: uncover the darkest hidden clues in Batman & DC.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🦇 GOTHAM SHADOWS",
                "title": "Unmasking Gotham's Clues",
                "text": "From Matt Reeves' gritty detective saga to James Gunn's reborn DCU, hidden symbols in Gotham tell a sinister story ordinary viewers missed.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🃏 THE ARKHAM CIPHER",
                "title": "Barry Keoghan's Joker",
                "text": "The deleted Arkham conversation between Batman and Joker teased a congenital laughing disorder, setting up a terrifying alliance with Paul Dano's Riddler.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🦉 COURT OF OWLS HIDDEN",
                "title": "Gotham's True Masters",
                "text": "Owl motifs embedded in Wayne Tower and Mayor Mitchell's home strongly indicate Gotham's legendary Court of Owls will strike in The Batman Part II.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🐧 OZ COBB'S MONOPOLY",
                "title": "The Penguin's Rise",
                "text": "With Carmine Falcone gone, Oz Cobb eliminated rival mob families and seized Gotham's illicit drug trade, cementing himself as the new kingpin.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "⚡ GODS AND MONSTERS",
                "title": "James Gunn's DCU Era",
                "text": "Superman, Creature Commandos, and Peacemaker Season 2 are linking a cohesive tapestry of comic-accurate superheroes and antiheroes.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🎬 ENTER THE DC UNIVERSE",
                "title": "Explore Dark Detective Lore",
                "text": "Dive deeper into DC movie timelines, comic easter eggs, and casting updates today.",
                "backdrop_index": 1,
                "cta_text": "Explore DC Universe Cast & News",
                "cta_url": None
            }
        ]
    },

    # 20. Spider-Man & Venom: Post-Credit Clues
    "spiderman-venom-post-credits": {
        "title": "Spider-Man & Venom: 5 Post-Credit Clues Connecting The Multiverse 🕷️🖤",
        "seo_description": "The alien symbiote left behind in the MCU, Peter Parker's isolation, and Spider-Man 4 theories explained.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🕷️ THE SYMBIOTE DROPLET",
                "title": "Left Behind In The MCU",
                "text": "When Doctor Strange sent Eddie Brock back to his universe, a tiny living droplet of Venom stayed on the bar counter. The alien is now officially in the MCU.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🕸️ PETER'S TOTAL ISOLATION",
                "title": "Forgotten By Everyone",
                "text": "With Ned, MJ, and the Avengers completely forgetting Peter Parker existed, Spider-Man is back to his gritty, street-level comic roots.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🖤 BLACK SUIT SAGA NEXT?",
                "title": "A Darker Spider-Man",
                "text": "Vulnerable and grieving Aunt May, Peter is the perfect host for the alien symbiote, setting up Marvel's live-action Black Suit comic storyline.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "⚡ MILES MORALES LIVE-ACTION",
                "title": "The Brooklyn Spider",
                "text": "Electro's iconic quote 'There's gotta be a Black Spider-Man out there somewhere' teased the inevitable introduction of Miles Morales into the MCU.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🏙️ DAREDEVIL & KINGPIN ALLIANCE",
                "title": "New York Street War",
                "text": "With Matt Murdock defending Peter and Kingpin ruling New York, Spider-Man 4 is primed for a brutal grounded gangland war.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 STREAM NO WAY HOME",
                "title": "Relive The Multiverse Epic",
                "text": "Stream Spider-Man: No Way Home and explore full easter egg breakdowns on CineStories.",
                "backdrop_index": 1,
                "cta_text": "Explore Spider-Man 4 Details",
                "cta_url": None
            }
        ]
    },

    # 21. Friends: Where Are They Now?
    "friends-where-are-they-now": {
        "title": "Friends: Where Are The Central Perk Stars Today? ☕✨",
        "seo_description": "Thirty years later: where are Jennifer Aniston, Matt LeBlanc, Courteney Cox, David Schwimmer, Lisa Kudrow, and Matthew Perry's legacy?",
        "slides": [
            {
                "id": "page-1",
                "badge": "☕ 30 YEARS OF FRIENDS",
                "title": "The Central Perk Legacy",
                "text": "Premiering in 1994, Friends became the greatest sitcom in television history. Three decades later, what happened to the 6 beloved stars?",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "👑 JENNIFER ANISTON",
                "title": "Hollywood's Top Powerhouse",
                "text": "Jennifer Aniston evolved from Rachel Green into a global producer, award-winning star of Apple TV's The Morning Show, and successful beauty entrepreneur.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🎬 COURTENEY & LISA",
                "title": "Scream Queens & Producers",
                "text": "Courteney Cox leads the multi-million dollar Scream franchise, while Lisa Kudrow produces acclaimed comedies and stars in prestige shows like Time Bandits.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎭 MATT & DAVID",
                "title": "Stage, Speed & Passions",
                "text": "Matt LeBlanc conquered hosting on Top Gear and Man with a Plan, while David Schwimmer directed films and triumphed on London and Broadway stages.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🕊️ MATTHEW PERRY (1969-2023)",
                "title": "Chandler Bing Forever",
                "text": "Matthew Perry gave us television's most brilliant sarcastic wit. His best-selling memoir and addiction recovery advocacy continue saving lives worldwide.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 STREAM ALL 10 SEASONS",
                "title": "I'll Be There For You",
                "text": "Celebrate 30 years of laughter by streaming all 236 episodes of Friends and the HBO Reunion Special today.",
                "backdrop_index": 1,
                "cta_text": "Explore Friends Cast Retrospective",
                "cta_url": None
            }
        ]
    },

    # 22. The Office: Where Are They Now?
    "the-office-where-are-they-now": {
        "title": "The Office: Where Is The Dunder Mifflin Cast In 2026? 📄📎",
        "seo_description": "From Scranton paper salesmen to Oscar nominees and blockbuster directors: see where The Office stars are today.",
        "slides": [
            {
                "id": "page-1",
                "badge": "📄 SCRANTON LEGENDS",
                "title": "Life Beyond Dunder Mifflin",
                "text": "Nine seasons of mockumentary perfection made The Office the most-streamed comedy in history. Here is how its stars conquered Hollywood.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🏆 STEVE CARELL",
                "title": "The World's Best Boss",
                "text": "Steve Carell transformed from Michael Scott into an Oscar-nominated dramatic actor in Foxcatcher, The Big Short, and Broadway hit Uncle Vanya.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🎬 JOHN KRASINSKI",
                "title": "The Blockbuster Filmmaker",
                "text": "Jim Halpert became a major Hollywood auteur, creating the billion-dollar A Quiet Place franchise and headlining Tom Clancy's Jack Ryan.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🌱 RAINN WILSON",
                "title": "Dwight's Soulful Second Act",
                "text": "Rainn Wilson traded beets for bestselling books, founding media company SoulPancake and traveling the globe as a passionate climate change advocate.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🎙️ FISCHER & KINSEY",
                "title": "The Office Ladies Empire",
                "text": "Jenna Fischer and Angela Kinsey created the wildly popular Office Ladies podcast, winning Podcast of the Year and publishing bestselling backstage memoirs.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "☕ REVISIT SCRANTON",
                "title": "That's What She Said!",
                "text": "Stream all 9 seasons and exclusive Superfan episodes of The Office on Peacock and streaming platforms worldwide.",
                "backdrop_index": 1,
                "cta_text": "Explore The Office Cast & Trivia",
                "cta_url": None
            }
        ]
    },

    # 23. Popular 90s/2000s Sitcom Stars: Where Are They Now?
    "sitcom-stars-where-are-they-now": {
        "title": "Where Are They Now? 5 Popular 90s/2000s Sitcom Stars 📺✨",
        "seo_description": "Frankie Muniz, Alfonso Ribeiro, Angus T. Jones, and Jaleel White: where did Hollywood's biggest sitcom icons vanish to?",
        "slides": [
            {
                "id": "page-1",
                "badge": "📺 SITCOM RETROSPECTIVE",
                "title": "The Stars Who Grew Up",
                "text": "They made millions laugh every single week. But after the cameras stopped rolling, several beloved sitcom stars chose wildly unexpected paths in life.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🏎️ FRANKIE MUNIZ",
                "title": "Malcolm Is A NASCAR Driver",
                "text": "The Emmy-nominated star of Malcolm in the Middle left acting behind to become a full-time professional NASCAR stock car racing driver.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🕺 ALFONSO RIBEIRO",
                "title": "The Carlton Dance King",
                "text": "Fresh Prince's Carlton Banks turned his comedic charisma into an incredible hosting career, leading Dancing with the Stars and America's Funniest Home Videos.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🙏 ANGUS T. JONES",
                "title": "Half Men Star's New Calling",
                "text": "Once the highest-paid child actor on TV as Jake Harper in Two and a Half Men, Angus walked away from Hollywood to dedicate himself to faith and music production.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🤓 JALEEL WHITE",
                "title": "Did I Do That? Beyond Urkel",
                "text": "Family Matters genius Jaleel White authored a candid bestselling memoir, launched his 'ItsPurpl' lifestyle brand, and returned to star in Star Wars: Skeleton Crew.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "✨ NOSTALGIA REWIND",
                "title": "Relive The Sitcom Golden Age",
                "text": "Explore more then-and-now retrospectives of your favorite 90s and 2000s childhood comedy legends on CineStories.",
                "backdrop_index": 1,
                "cta_text": "Explore 90s Sitcom Retrospectives",
                "cta_url": None
            }
        ]
    },
    # 24. Fifty Shades of Grey
    "fifty-shades-of-grey": {
        "title": "Fifty Shades: 5 Untold Secrets Behind Christian Grey's Empire 🖤🔥",
        "seo_description": "Uncover the $570M box office phenomenon, Dakota Johnson's casting, and behind-the-scenes secrets of Fifty Shades of Grey.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🔥 $570M PHENOMENON",
                "title": "The Global Romance Shockwave",
                "text": "Adapted from E.L. James's bestselling novels, Fifty Shades of Grey shattered box office records, grossing over $570 million worldwide on Valentine's Day weekend.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🎬 DAKOTA'S AUDITION",
                "title": "Ana Steele's Casting Victory",
                "text": "Dakota Johnson beat dozens of Hollywood stars for Anastasia Steele by reading a dramatic scene from Ingmar Bergman's Persona, captivating director Sam Taylor-Johnson.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "👔 MR. GREY'S WORLD",
                "title": "Building The Seattle Empire",
                "text": "Jamie Dornan trained rigorously to embody Christian Grey's billionaire intensity, practicing ballroom dancing, piano pieces, and bespoke wardrobe styling.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎵 GRAMMY SOUNDTRACK",
                "title": "The Weeknd & Beyoncé Hits",
                "text": "The platinum-selling soundtrack produced global smash hits including The Weeknd's Oscar-nominated 'Earned It' and Ellie Goulding's record-shattering 'Love Me Like You Do'.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "💥 CULTURAL LEGACY",
                "title": "A Modern Pop Culture Shift",
                "text": "The trilogy sparked worldwide conversations around modern romance, dominating book clubs, streaming platforms, and pop culture debates for an entire generation.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "📺 STREAM THE SAGA",
                "title": "Relive The Romance Trilogy",
                "text": "Stream all three chapters of Fifty Shades on premium VOD platforms and explore full cast trivia today.",
                "backdrop_index": 1,
                "cta_text": "Explore Fifty Shades Details",
                "cta_url": None
            }
        ]
    },
    # 25. 365 Days
    "365-days": {
        "title": "365 Days: Why Netflix's Bold Sensation Broke Global Records 🔥💥",
        "seo_description": "Discover why 365 Days became a worldwide Netflix streaming phenomenon across 90+ countries and Michele Morrone's overnight rise.",
        "slides": [
            {
                "id": "page-1",
                "badge": "📊 GLOBAL STREAMING HIT",
                "title": "#1 in Over 90 Countries",
                "text": "Premiering on Netflix in 2020, 365 Days became one of the platform's most-watched foreign titles in history, topping daily Top 10 lists worldwide.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🕶️ MICHELE MORRONE",
                "title": "Overnight International Stardom",
                "text": "Italian actor and musician Michele Morrone went from obscurity to millions of followers overnight, singing lead vocal tracks on the film's chart-topping soundtrack.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🌊 SICILIAN SPECTACLE",
                "title": "Lavish Mediterranean Backdrops",
                "text": "Filmed across breathtaking Italian coastline villas, Warsaw luxury hotels, and sun-soaked yachts, the cinematography created an escapist dreamscape.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "⚡ VIRAL TIKTOK FRENZY",
                "title": "Billions of Social Impressions",
                "text": "Catchy dialogue lines like 'Are you lost baby girl?' sparked billions of TikTok views, propelling the film into a viral internet phenomenon.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🎬 TRILOGY EXPANSION",
                "title": "The Blockbuster Sequel Era",
                "text": "Massive international viewership prompted Netflix to greenlight two back-to-back sequels, cementing 365 Days as one of Europe's biggest commercial franchises.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🍿 BINGE THE TRILOGY",
                "title": "Watch All 3 Installments",
                "text": "Explore the full 365 Days movie universe, soundtrack, and cast profiles on CineStories today.",
                "backdrop_index": 1,
                "cta_text": "View 365 Days Details",
                "cta_url": None
            }
        ]
    },
    # 26. Basic Instinct
    "basic-instinct": {
        "title": "Basic Instinct: 5 Mind-Games That Defined The Erotic Thriller 🧊⚡",
        "seo_description": "Relive Paul Verhoeven's boundary-pushing masterpiece Basic Instinct, Sharon Stone's iconic performance, and the white ice-pick mystery.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🧊 CULT MASTERPIECE",
                "title": "The $350M Thriller Legend",
                "text": "Paul Verhoeven's 1992 neo-noir shattered box offices worldwide, raking in $352 million and revolutionizing the psychological erotic thriller genre.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "👑 SHARON STONE",
                "title": "The Interrogation Scene",
                "text": "Sharon Stone's electrifying portrayal of brilliant novelist Catherine Tramell cemented her status as cinema's ultimate, unshakeable femme fatale.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "🕵️ MICHAEL DOUGLAS",
                "title": "Nick Curran's Dark Descent",
                "text": "Michael Douglas delivered one of his most intense performances as a flawed homicide detective hopelessly ensnared in Catherine's deadly psychological web.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎼 JERRY GOLDSMITH",
                "title": "The Oscar-Nominated Score",
                "text": "Composer Jerry Goldsmith crafted a haunting, suspense-drenched orchestral masterpiece that elevated every tense confrontation into pure cinematic art.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "❓ UNANSWERED ENIGMA",
                "title": "Who Held The Ice Pick?",
                "text": "Decades later, cinephiles still passionately debate the final ambiguous bedroom camera reveal: was Catherine truly the killer, or the ultimate puppeteer?",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "🎬 CINEMA HISTORY",
                "title": "Stream The 4K Restored Classic",
                "text": "Experience Paul Verhoeven's uncut masterpiece in 4K UHD and explore retrospective cast interviews on CineStories.",
                "backdrop_index": 1,
                "cta_text": "Explore Basic Instinct Details",
                "cta_url": None
            }
        ]
    },
    # 27. Saltburn
    "saltburn": {
        "title": "Saltburn: 5 Twisted Mind Games & Shocking Estate Secrets 🏰🍷",
        "seo_description": "Explore Emerald Fennell's Saltburn: Barry Keoghan's masterclass, Jacob Elordi's charm, and the shocking secrets of the Catton estate.",
        "slides": [
            {
                "id": "page-1",
                "badge": "🏰 ARISTOCRATIC OBSESSION",
                "title": "Welcome To Saltburn Estate",
                "text": "Oscar winner Emerald Fennell delivers a gothic, deliciously wicked satire of English high society, obsession, and Machiavellian deceit.",
                "backdrop_index": 0
            },
            {
                "id": "page-2",
                "badge": "🎭 BARRY KEOGHAN",
                "title": "Oliver's Chilling Transformation",
                "text": "Barry Keoghan gives a fearless, career-defining performance as Oxford outsider Oliver Quick, who systematically ingratiates himself with the wealthy Cattons.",
                "backdrop_index": 1
            },
            {
                "id": "page-3",
                "badge": "✨ JACOB ELORDI",
                "title": "The Irresistible Felix Catton",
                "text": "Jacob Elordi shines as the charismatic golden boy heir, whose magnetic hospitality conceals the shallow cruelty of his aristocratic lineage.",
                "backdrop_index": 0
            },
            {
                "id": "page-4",
                "badge": "🎶 MURDER ON DANCEFLOOR",
                "title": "Sophie Ellis-Bextor's Revival",
                "text": "The unforgettable final dance sequence propelled Sophie Ellis-Bextor's 2001 classic 'Murder on the Dancefloor' back to the top of global music charts.",
                "backdrop_index": 1
            },
            {
                "id": "page-5",
                "badge": "🍷 SHOCKING TWISTS",
                "title": "The Master Manipulator",
                "text": "The third-act graveyard and estate revelations shocked audiences, cementing Saltburn as one of the most talked-about social thrillers of the decade.",
                "backdrop_index": 0
            },
            {
                "id": "page-6",
                "badge": "⚡ STREAM ON PRIME",
                "title": "Enter The World of Saltburn",
                "text": "Watch Saltburn on Prime Video and uncover behind-the-scenes cinematography details on CineStories.",
                "backdrop_index": 1,
                "cta_text": "Explore Saltburn Details",
                "cta_url": None
            }
        ]
    }
}


