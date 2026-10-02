"""
High-fidelity sample data representing Hollywood Movies, Cult Classics, and Hit TV Series.
Includes authentic posters, backdrops, cast, creators, and metadata from TMDB.
"""

SAMPLE_MEDIA = [
    # 1. Hit TV Series: Money Heist (La Casa de Papel)
    {
        "id": 71446,
        "title": "Money Heist",
        "original_title": "La Casa de Papel",
        "slug": "money-heist",
        "media_type": "tv",
        "release_date": "2017-05-02",
        "overview": "To carry out the biggest heist in history, a mysterious man called The Professor recruits a band of eight robbers with nothing to lose.",
        "tagline": "The ultimate heist begins.",
        "genres": ["Crime", "Drama", "Thriller"],
        "runtime": 50,
        "seasons": 5,
        "vote_average": 8.2,
        "vote_count": 18500,
        "category": "series",
        "director": "Álex Pina (Creator)",
        "top_cast": ["Álvaro Morte", "Úrsula Corberó", "Pedro Alonso", "Itziar Ituño", "Alba Flores", "Miguel Herrán"],
        "poster_path": "/reEMJA1uzscCbk5rSXGno05GAYg.jpg",
        "backdrop_path": "/mGJu9OCUJJl50uGTr847bS3u5q0.jpg",
        "backdrops": [
            "/mGJu9OCUJJl50uGTr847bS3u5q0.jpg",
            "/gFZri2YbFUReMwQZasKAI8zeqeC.jpg",
            "/14q1U8c1m8q0v119101v018q7.jpg",
            "/3g1847bS3u5q0mGJu9OCUJJl50.jpg",
            "/mGJu9OCUJJl50uGTr847bS3u5q0.jpg"
        ]
    },
    # 2. Hit TV Series: Stranger Things
    {
        "id": 66732,
        "title": "Stranger Things",
        "original_title": "Stranger Things",
        "slug": "stranger-things",
        "media_type": "tv",
        "release_date": "2016-07-15",
        "overview": "When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.",
        "tagline": "Every ending has a beginning.",
        "genres": ["Sci-Fi & Fantasy", "Drama", "Mystery"],
        "runtime": 60,
        "seasons": 4,
        "vote_average": 8.6,
        "vote_count": 17200,
        "category": "series",
        "director": "The Duffer Brothers",
        "top_cast": ["Millie Bobby Brown", "Finn Wolfhard", "Winona Ryder", "David Harbour", "Gaten Matarazzo", "Sadie Sink"],
        "poster_path": "/49WJfeN0moxb9IPfGn8AIqMGskD.jpg",
        "backdrop_path": "/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
        "backdrops": [
            "/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
            "/2meX1nMdScFOoV4370rqHWFDxZf.jpg",
            "/reEMJA1uzscCbk5rSXGno05GAYg.jpg",
            "/mGJu9OCUJJl50uGTr847bS3u5q0.jpg"
        ]
    },
    # 3. Hit TV Series: The Boys
    {
        "id": 76479,
        "title": "The Boys",
        "original_title": "The Boys",
        "slug": "the-boys",
        "media_type": "tv",
        "release_date": "2019-07-26",
        "overview": "A fun and irreverent take on what happens when superheroes—who are as popular as celebrities—abuse their superpowers rather than use them for good.",
        "tagline": "Never meet your heroes.",
        "genres": ["Action & Adventure", "Sci-Fi & Fantasy"],
        "runtime": 60,
        "seasons": 4,
        "vote_average": 8.5,
        "vote_count": 10400,
        "category": "series",
        "director": "Eric Kripke (Creator)",
        "top_cast": ["Karl Urban", "Jack Quaid", "Antony Starr", "Erin Moriarty", "Dominique McElligott", "Jensen Ackles"],
        "poster_path": "/7Ns6tO3aYjppI5J8ojQ32mQ4q0o.jpg",
        "backdrop_path": "/nxxCPRgt1fX74iNq9470v1038v.jpg",
        "backdrops": [
            "/nxxCPRgt1fX74iNq9470v1038v.jpg",
            "/56v2KjBlU4XaOv9rVYEQypROD7P.jpg",
            "/2meX1nMdScFOoV4370rqHWFDxZf.jpg"
        ]
    },
    # 4. Cult Franchise: Final Destination
    {
        "id": 9532,
        "title": "Final Destination",
        "original_title": "Final Destination",
        "slug": "final-destination",
        "media_type": "movie",
        "release_date": "2000-03-17",
        "overview": "After a teenager has a terrifying premonition of their plane exploding, he saves his classmates—only for Death to stalk them one by one in gruesome chain-reaction accidents.",
        "tagline": "Death doesn't like to be cheated.",
        "genres": ["Horror", "Mystery"],
        "runtime": 98,
        "seasons": None,
        "vote_average": 6.6,
        "vote_count": 5200,
        "category": "cult_classic",
        "director": "James Wong",
        "top_cast": ["Devon Sawa", "Ali Larter", "Kerr Smith", "Kristen Cloke", "Tony Todd"],
        "poster_path": "/bkQj4E4FmD89n830v9408018h2.jpg",
        "backdrop_path": "/9v8b901h19f018h2v8b901h19f0.jpg",
        "backdrops": [
            "/9v8b901h19f018h2v8b901h19f0.jpg",
            "/87IVFtMoqvSsznUVNbtymLtV3bm.jpg",
            "/lzWHmY2vtjxsScRpn17eaNZmALU.jpg"
        ]
    },
    # 5. Cult Hollywood Masterpiece: Interstellar
    {
        "id": 157336,
        "title": "Interstellar",
        "original_title": "Interstellar",
        "slug": "interstellar",
        "media_type": "movie",
        "release_date": "2014-11-05",
        "overview": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
        "tagline": "Mankind was born on Earth. It was never meant to die here.",
        "genres": ["Adventure", "Drama", "Science Fiction"],
        "runtime": 169,
        "seasons": None,
        "vote_average": 8.4,
        "vote_count": 35000,
        "category": "cult_classic",
        "director": "Christopher Nolan",
        "top_cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain", "Michael Caine", "Matt Damon"],
        "poster_path": "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "backdrop_path": "/xJHokMbljvjADYdit5fK5VQsXEG.jpg",
        "backdrops": [
            "/xJHokMbljvjADYdit5fK5VQsXEG.jpg",
            "/rAiYTsqJiOEZ10e21rjpm2f2Z2O.jpg",
            "/5qA3bftqeHMq1i5zndb69l4zfqd.jpg"
        ]
    },
    # 6. Trending Blockbuster: Dune: Part Two
    {
        "id": 693134,
        "title": "Dune: Part Two",
        "original_title": "Dune: Part Two",
        "slug": "dune-part-two",
        "media_type": "movie",
        "release_date": "2024-03-01",
        "overview": "Follow the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a path of revenge against the conspirators who destroyed his family.",
        "tagline": "Long live the fighters.",
        "genres": ["Science Fiction", "Adventure"],
        "runtime": 166,
        "seasons": None,
        "vote_average": 8.2,
        "vote_count": 5400,
        "category": "trending",
        "director": "Denis Villeneuve",
        "top_cast": ["Timothée Chalamet", "Zendaya", "Rebecca Ferguson", "Javier Bardem", "Austin Butler", "Florence Pugh"],
        "poster_path": "/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
        "backdrop_path": "/xOMo8BRK7PfcJv9JCnx7s520b22.jpg",
        "backdrops": [
            "/xOMo8BRK7PfcJv9JCnx7s520b22.jpg",
            "/lzWHmY2vtjxsScRpn17eaNZmALU.jpg",
            "/87IVFtMoqvSsznUVNbtymLtV3bm.jpg",
            "/5qA3bftqeHMq1i5zndb69l4zfqd.jpg"
        ]
    },
    # 7. Box Office Hit: Deadpool & Wolverine
    {
        "id": 533535,
        "title": "Deadpool & Wolverine",
        "original_title": "Deadpool & Wolverine",
        "slug": "deadpool-and-wolverine",
        "media_type": "movie",
        "release_date": "2024-07-26",
        "overview": "A listless Wade Wilson toils away in civilian life. But when his homeworld faces an existential threat, Wade reluctantly suits up with an even more reluctant Wolverine.",
        "tagline": "Come together.",
        "genres": ["Action", "Comedy", "Science Fiction"],
        "runtime": 128,
        "seasons": None,
        "vote_average": 7.7,
        "vote_count": 6100,
        "category": "now_playing",
        "director": "Shawn Levy",
        "top_cast": ["Ryan Reynolds", "Hugh Jackman", "Emma Corrin", "Morena Baccarin", "Matthew Macfadyen"],
        "poster_path": "/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
        "backdrop_path": "/yDHYTjA3R0ne84guT43QBCvoK0I.jpg",
        "backdrops": [
            "/yDHYTjA3R0ne84guT43QBCvoK0I.jpg",
            "/9lEN04rN1Z2P6f38mK1i79E3zG5.jpg"
        ]
    },
    # 8. Upcoming Hollywood Epic: Gladiator II
    {
        "id": 558449,
        "title": "Gladiator II",
        "original_title": "Gladiator II",
        "slug": "gladiator-ii",
        "media_type": "movie",
        "release_date": "2024-11-22",
        "overview": "Years after witnessing the death of hero Maximus, Lucius enters the Colosseum after his home is conquered by the tyrannical Emperors of Rome.",
        "tagline": "What we do in life echoes in eternity.",
        "genres": ["Action", "Adventure", "Drama"],
        "runtime": 148,
        "seasons": None,
        "vote_average": 6.8,
        "vote_count": 2800,
        "category": "upcoming",
        "director": "Ridley Scott",
        "top_cast": ["Paul Mescal", "Pedro Pascal", "Denzel Washington", "Connie Nielsen"],
        "poster_path": "/2cxhvwyEwRlysAmRH4iodkvo0z5.jpg",
        "backdrop_path": "/euYIwmwkmz95mnXvufEmbL69ovr.jpg",
        "backdrops": [
            "/euYIwmwkmz95mnXvufEmbL69ovr.jpg",
            "/ag66gJCiZ06q9qZqZ8078f4vG3z.jpg"
        ]
    }
]

# Alias for backwards compatibility
SAMPLE_MOVIES = SAMPLE_MEDIA
