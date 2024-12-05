{
    "parser": "Google",
    "code_version": "1.113",
    "schema": {
        ################################################################
        # attributes for key
        #  - input, general parse해서 필요한 Key 만들기
        ################################################################
        # input
        "input": {"original_url": {"class": "string", "examples": ["https://www.google.com/search?q=addidas"]}},
        # general
        "general": {
            "basic_view": {"class": "boolean", "examples": [False, True]},
            "country": {"class": "string", "examples": ["Russia", "France", "United Kingdom"]},
            "country_code": {"class": "string", "examples": ["RU", "FR", "GB"]},
            "empty": {"class": "boolean", "comment": "there are no results found", "examples": [True]},
            "gl": {"class": "string", "examples": ["RU", "FR", "GB"]},
            "language": {"class": "string", "examples": ["en-RU", "en-EG", "en"]},
            "location": {"class": "string", "examples": ["Pyt-Yakh, Khanty-Mansi Autonomous Okrug", "London", "USA"]},
            "mobile": {"class": "boolean", "examples": [False, True]},
            "original_empty": {
                "class": "boolean",
                "comment": "there were no results before spelling auto-correction",
                "examples": [True],
            },
            "page_title": {
                "class": "string",
                "examples": [
                    "addidas - Google Search",
                    "γú1000 loan - Google Search",
                    "Zachary Quinto - Google Search",
                ],
            },
            "query": {"class": "string", "examples": ["addidas", "cabaretclub casino", "cafe nearby"]},
            "results_cnt": {"class": "number", "examples": [2740000000, 10900000, 59700]},
            "search_engine": {"class": "string", "examples": ["google"]},
            "search_time": {"class": "number", "examples": [0.51, 0.53, 0.36]},
            "search_type": {"class": "string", "examples": ["text", "news", "image_output"]},
            "timestamp": {"class": "string", "examples": ["2020-03-09T12:34:56.000Z"]},
        },
        ################################################################
        # attributes for value
        #  -
        ################################################################
        ## organic - list of dict
        "organic": [
            {
                "author": {
                    "class": "string",
                    "examples": ["Wall Street Journal", "Cocomelon - Nursery Rhymes", "Totoy kids"],
                },
                "cached_link": {
                    "class": "string",
                    "examples": ["https://webcache.googleusercontent.com/search?q=ca..."],
                },
                "date": {"class": "string", "examples": ["Sep 18, 2015", "21 thg 8, 2018", "26 thg 10, 2020"]},
                "description": {
                    "class": "string",
                    "examples": ["Welcome to adidas Shop for adidas shoes, clothing ..."],
                },
                "display_link": {"class": "string", "examples": ["https://www.adidas.com/us"]},
                "duration": {"class": "string", "examples": ["2:48", "0:30", "4:03"]},
                "duration_sec": {"class": "number", "examples": [168, 30, 243]},
                "extensions": [
                    {
                        "key": {"class": "string", "examples": ["Products", "Net income", "Industry"]},
                        "rank": {"class": "rank"},
                        "type": "fact",
                        "value": [
                            {
                                "link": {
                                    "class": "string",
                                    "examples": ["https://en.wikipedia.org/wiki/Frankfurt_Stock_Exch..."],
                                },
                                "text": {
                                    "class": "string",
                                    "examples": ["Footwear, sportswear, sports equip...", "BFA", "2000–present"],
                                },
                            }
                        ],
                    },
                    {
                        "link": {
                            "class": "string",
                            "examples": ["https://www.google.com/search?num=100&hl=ur&gl=fj&..."],
                        },
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["2013", "Law", "Francis Rose"]},
                        "type": "google_books",
                    },
                    {
                        "link": {
                            "class": "string",
                            "examples": ["https://scholar.google.com/scholar?hl=en&nfpr=1&gl..."],
                        },
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["Related articles", "by JS TURNER", "1937"]},
                        "type": "google_scholar",
                    },
                    {
                        "inline": {"class": "boolean", "examples": [True]},
                        "link": {
                            "class": "string",
                            "examples": ["https://support.google.com/webmasters/answer/74898..."],
                        },
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["Learn why"]},
                        "type": "google_support",
                    },
                    {
                        "inline": {"class": "boolean", "examples": [True]},
                        "link": {
                            "class": "string",
                            "examples": ["https://www.biologyonline.com/dictionary/anaerobic..."],
                        },
                        "rank": {"class": "rank"},
                        "text": {
                            "class": "string",
                            "examples": ["Yeast fermentation", "Products", "Formation of biofilms"],
                        },
                        "type": "jump_to",
                    },
                    {
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["List includes", "Switchドック(映像出力)"]},
                        "type": "list",
                        "value": [
                            {
                                "link": {
                                    "class": "string",
                                    "examples": ["https://www.tripadvisor.com/RestaurantsNear-g60763..."],
                                },
                                "text": {
                                    "class": "string",
                                    "examples": ["Shinka Ramen and Sake", "Sup Crab", "View full list"],
                                },
                            }
                        ],
                    },
                    {
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["(ian", "295693)", "envs"]},
                        "type": "missing",
                    },
                    {
                        "link": {
                            "class": "string",
                            "examples": ["https://www.google.com/search?hl=en&biw=1920&bih=8..."],
                        },
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["envs", "ian", "931"]},
                        "type": "must_include",
                    },
                    {
                        "details": {
                            "class": "string",
                            "examples": ["Nearby attractions include Langa Wine Tour (2.7 mi..."],
                        },
                        "link": {
                            "class": "string",
                            "examples": ["https://www.tripadvisor.com/Hotel_Review-g194664-d..."],
                        },
                        "rank": {"class": "rank"},
                        "text": {
                            "class": "string",
                            "examples": ["Which popular attractions are close to Agriturismo..."],
                        },
                        "type": "question",
                    },
                    {
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["9.5/10", "5.0", "8.5/10"]},
                        "type": "rating",
                    },
                    {
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["(819)", "(820)", "(127)"]},
                        "type": "reviews",
                    },
                    {
                        "description": {
                            "class": "string",
                            "examples": ["Get the latest BBC News: breaking news, features, ..."],
                        },
                        "details": {"class": "string", "examples": ["Top answer  0 votes", "0 votes", "Mon, Oct 5"]},
                        "extended": {"class": "boolean", "examples": [True]},
                        "inline": {"class": "boolean", "examples": [True]},
                        "link": {
                            "class": "string",
                            "examples": [
                                "https://www.adidas.com/us/originals",
                                "http://www.imdb.com/media/rm3337331712/nm0704270",
                            ],
                        },
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["Originals", "Men", "Adidas Nite Jogger Shoes"]},
                        "type": "site_link",
                        "value": [
                            {
                                "link": {
                                    "class": "string",
                                    "examples": [
                                        "https://www.adidas.com/us/women-shoes",
                                        "https://www.samsung.com/us/televisions-home-theate...",
                                    ],
                                },
                                "text": {"class": "string", "examples": ["All Women's Shoes", "Apparel", "Tops"]},
                            }
                        ],
                    },
                    {
                        "data": [
                            [
                                {
                                    "rank": {"class": "rank"},
                                    "text": {"class": "string", "examples": ["Images", "Lot #", "Year"]},
                                }
                            ]
                        ],
                        "rank": {"class": "rank"},
                        "type": "table",
                    },
                    {
                        "inline": {"class": "boolean", "examples": [True]},
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["1207 items", "Mar 25, 2019", "1240 items"]},
                        "type": "text",
                    },
                ],
                "global_rank": {"class": "rank"},
                "has_link": {"class": "boolean", "examples": [False]},
                "icon": {"class": "string", "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAA..."]},
                "image": {"class": "string", "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."]},
                "image_alt": {
                    "class": "string",
                    "examples": ["Media posted by adidas", "why like that from akikolingoland.com"],
                },
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                },
                "images": [
                    {
                        "details": {
                            "class": "string",
                            "examples": ["Twitter · 4 days ago", "Twitter · 5 days ago", "Twitter · Aug 6, 2021"],
                        },
                        "image": {
                            "class": "string",
                            "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                        },
                        "image_alt": {
                            "class": "string",
                            "examples": ["Image for related document", "yoshikei-dvlp.co.jp からのミールキット"],
                        },
                        "image_base64": {
                            "class": "string",
                            "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "link": {
                            "class": "string",
                            "examples": ["https://twitter.com/CandyCrushSaga/status/14487101..."],
                        },
                        "title": {
                            "class": "string",
                            "examples": ["We wanna know who's qualified! Drop us a comment b..."],
                        },
                    }
                ],
                "info_description": {
                    "class": "string",
                    "examples": ["Tripadvisor, Inc. is an American online travel com..."],
                },
                "info_link": {
                    "class": "string",
                    "examples": ["https://en.wikipedia.org/wiki/Tripadvisor", "https://en.wikipedia.org/wiki/YouTube"],
                },
                "info_logo": {
                    "class": "string",
                    "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAA..."],
                },
                "info_source": {"class": "string", "examples": ["Wikipedia"]},
                "link": {
                    "class": "string",
                    "examples": ["https://www.adidas.com/us", "https://www.broadwayworld.com/people/Zachary-Quint..."],
                },
                "moments": [
                    {
                        "image": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "link": {"class": "string", "examples": ["https://www.youtube.com/watch?v=oyh7S8H4r4Y&t=8"]},
                        "rank": {"class": "rank"},
                        "start": {"class": "string", "examples": ["00:08", "02:26", "05:26"]},
                        "start_sec": {"class": "number", "examples": [8, 146, 326]},
                        "title": {"class": "string", "examples": ["The Sick Song", "Info", "Comparison"]},
                    }
                ],
                "rank": {"class": "rank"},
                "similar_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/search?hl=en&q=related:http..."],
                },
                "source": {"class": "string", "examples": ["Tripadvisor", "Uber Eats", "Just Eat"]},
                "subresults": [
                    {
                        "cached_link": {
                            "class": "string",
                            "examples": ["https://webcache.googleusercontent.com/search?q=ca..."],
                        },
                        "description": {
                            "class": "string",
                            "examples": ["Find the best Cute Cafes near you on Yelp - see al..."],
                        },
                        "display_link": {
                            "class": "string",
                            "examples": ["https://www.yelp.com › nearme › cute-cafes"],
                        },
                        "extensions": [
                            {
                                "key": {"class": "string", "examples": ["Russia", "Greece", "South Africa"]},
                                "rank": {"class": "rank"},
                                "type": "fact",
                                "value": [{"text": {"class": "string", "examples": ["53,649", "12,452", "77,400"]}}],
                            },
                            {
                                "rank": {"class": "rank"},
                                "text": {"class": "string", "examples": ["Rating: 8/10"]},
                                "type": "rating",
                            },
                            {
                                "rank": {"class": "rank"},
                                "text": {"class": "string", "examples": ["Review by The Nudge"]},
                                "type": "reviews",
                            },
                            {
                                "inline": {"class": "boolean", "examples": [True]},
                                "rank": {"class": "rank"},
                                "text": {"class": "string", "examples": ["Price range: £££", "hace 2 días"]},
                                "type": "text",
                            },
                        ],
                        "global_rank": {"class": "rank"},
                        "image": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "image_alt": {
                            "class": "string",
                            "examples": [
                                "ac repair near me from www.acserviceinnyc.com",
                                "yoshikei-dvlp.co.jp からのミールキット",
                            ],
                        },
                        "image_base64": {
                            "class": "string",
                            "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "info_description": {
                            "class": "string",
                            "examples": ["Yelp, Inc. develops, hosts, and markets the Yelp.c..."],
                        },
                        "info_link": {
                            "class": "string",
                            "examples": [
                                "https://en.wikipedia.org/wiki/Yelp",
                                "https://en.wikipedia.org/wiki/Realtor.com",
                            ],
                        },
                        "info_logo": {
                            "class": "string",
                            "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAA..."],
                        },
                        "info_source": {"class": "string", "examples": ["Wikipedia"]},
                        "link": {"class": "string", "examples": ["https://www.yelp.com/nearme/cute-cafes"]},
                        "rank": {"class": "rank"},
                        "similar_link": {
                            "class": "string",
                            "examples": ["https://www.google.com/search?hl=en&gl=us&q=relate..."],
                        },
                        "title": {"class": "string", "examples": ["Best Cute Cafes Near Me - January 2022 - Yelp"]},
                        "translate_link": {
                            "class": "string",
                            "examples": ["https://translate.google.com/translate?hl=hi&sl=en..."],
                        },
                    }
                ],
                "thumbnail": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn3.gstatic.com/images?q=tbn:AN..."],
                },
                "title": {
                    "class": "string",
                    "examples": [
                        "adidas Official Website | adidas US",
                        "Zachary Quinto Theatre Credits, News, Bio and Phot...",
                    ],
                },
                "translate_link": {
                    "class": "string",
                    "examples": ["https://translate.google.com/translate?hl=en&sl=de..."],
                },
                "videos": [
                    {
                        "details": {"class": "string", "examples": ["2 Oct 2021", "27 Sept 2021", "5 days ago"]},
                        "duration": {"class": "string", "examples": ["0:31", "3:34", "3:42"]},
                        "duration_sec": {"class": "number", "examples": [31, 214, 222]},
                        "image": {
                            "class": "string",
                            "examples": ["https://i.ytimg.com/vi/nfiUEAyL2iI/mqdefault.jpg?s..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://i.ytimg.com/vi/nfiUEAyL2iI/mqdefault.jpg?s..."],
                        },
                        "link": {
                            "class": "string",
                            "examples": [
                                "https://www.youtube.com/watch?v=nfiUEAyL2iI",
                                "https://www.youtube.com/watch?v=Icbp5Q9jydE",
                            ],
                        },
                        "title": {
                            "class": "string",
                            "examples": ["Calling All Crushers! | America's First Candy Crus..."],
                        },
                    }
                ],
            }
        ],
        ## videos - list of dict
        "videos": [
            {
                "author": {"class": "string", "examples": ["MoneyBags73", "SEMrush", "Star Wars"]},
                "date": {"class": "string", "examples": ["Apr 27, 2018", "Mar 2, 2017", "Jun 2, 2018"]},
                "description": {
                    "class": "string",
                    "examples": ["Ciao ragazzi, oggi prepariamo insieme il Ciambello..."],
                },
                "duration": {"class": "string", "examples": ["3:23", "2:18", "6:53"]},
                "duration_sec": {"class": "number", "examples": [203, 138, 413]},
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_alt": {
                    "class": "string",
                    "examples": ["Video result for Angel Has Fallen", "Video result for Zachary Quinto"],
                },
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                },
                "likes": {"class": "number", "examples": [1744]},
                "link": {
                    "class": "string",
                    "examples": [
                        "https://www.youtube.com/watch?v=oZGYtZug-HU",
                        "https://www.youtube.com/watch?v=XfibOi4PlBw",
                    ],
                },
                "moments": [
                    {
                        "image": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "image_base64": {
                            "class": "string",
                            "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "link": {"class": "string", "examples": ["https://m.youtube.com/watch?v=0RaqwBFMGqA&t=76"]},
                        "rank": {"class": "rank"},
                        "start": {"class": "string", "examples": ["01:16", "01:54", "02:14"]},
                        "start_sec": {"class": "number", "examples": [76, 114, 134]},
                        "title": {
                            "class": "string",
                            "examples": ["Ergonomical Shape", "GREENLAND (2020)", "JURASSIC WORLD (2015)"],
                        },
                    }
                ],
                "original_image": {
                    "class": "string",
                    "examples": ["https://nmvxdvra2muiv2amejorzkvqgg.gcdn.anvato.net..."],
                },
                "rank": {"class": "rank"},
                "source": {"class": "string", "examples": ["YouTube", "Vimeo", "Home Depot"]},
                "title": {"class": "string", "examples": ["Mandela Effect Addidas or Adidas? Thumbs Up For Ad..."]},
                "views": {"class": "number", "examples": [70475, 182]},
            }
        ],
        ## images - list of dict
        "images": [
            {
                "display_link": {"class": "string", "examples": ["www.bathplanet.com/img/pages/bath-replacement.jpg"]},
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_alt": {
                    "class": "string",
                    "examples": [
                        "File:Albert Einstein Head.jpg - Wikimedia Commons",
                        "Image result for site:youtube.com led",
                    ],
                },
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                },
                "link": {"class": "string", "examples": ["https://commons.wikimedia.org/wiki/File:Albert_Ein..."]},
                "original_image": {
                    "class": "string",
                    "examples": ["https://q-cf.bstatic.com/images/hotel/max1024x768/..."],
                },
                "rank": {"class": "rank"},
                "recipe": {
                    "duration": {"class": "string", "examples": ["55 min", "1 h 5 min", "1 h"]},
                    "duration_sec": {"class": "number", "examples": [3300, 3900, 3600]},
                    "ingredients": [
                        {"class": "string", "examples": ["3 mele (renette, pink lady o quelle che preferite)"]}
                    ],
                    "rating": {"class": "number", "examples": [5, 4.4]},
                    "reviews_cnt": {"class": "number", "examples": [2, 51]},
                    "summary": {
                        "class": "string",
                        "examples": ["La Ciambella alle mele è dolce alla frutta facile ..."],
                    },
                    "title": {
                        "class": "string",
                        "examples": ["Ciambella alle mele alta e soffice, la Ricetta fac..."],
                    },
                    "volume": {
                        "class": "string",
                        "examples": [
                            "per uno stampo a ciambella alto 12 cm diametro 20 ...",
                            "10 persone",
                            "8 persone",
                        ],
                    },
                },
                "source": {"class": "string", "examples": ["commons.wikimedia.org", "twitter.com", "news18.com"]},
                "source_logo": {
                    "class": "string",
                    "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAA..."],
                },
                "tag": {"class": "string", "examples": ["3 days ago", "Product", "Takeout"]},
                "title": {"class": "string", "examples": ["File:Albert Einstein Head.jpg - Wikimedia Commons"]},
            }
        ],
        ## twitter - items & title
        "twitter": {
            "items": [
                {
                    "date": {"class": "string", "examples": ["1 day ago", "2 days ago", "19 mins ago"]},
                    "global_rank": {"class": "rank"},
                    "image": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_alt": {
                        "class": "string",
                        "examples": ["Media posted by BBC", "Media posted by CDC", "Media posted by Dell"],
                    },
                    "image_base64": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_url": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                    },
                    "link": {"class": "string", "examples": ["https://twitter.com/BBC/status/1381577845693050882..."]},
                    "rank": {"class": "rank"},
                    "source": {"class": "string", "examples": ["Twitter"]},
                    "text": {"class": "string", "examples": ["The moving moment @GretaThunberg and Sir David Att..."]},
                }
            ],
            "title": {"class": "string", "examples": ["BBC (@BBC) · Twitter"]},
        },
        ## featured_snippiets - list of dict
        "featured_snippets": [
            {
                "display_link": {
                    "class": "string",
                    "examples": ["link.springer.com › pdf", "https://www.glassdoor.com › Xometry-Reviews-E14015..."],
                },
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_alt": {
                    "class": "string",
                    "examples": ["Image result for data set example", "Image result for google serp answer box"],
                },
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "link": {"class": "string", "examples": ["https://link.springer.com/content/pdf/10.1007%2F97..."]},
                "link_title": {
                    "class": "string",
                    "examples": ["RESPIRATION", "Xometry Reviews: What Is It Like to Work At ... - ..."],
                },
                "rank": {"class": "rank"},
                "title": {
                    "class": "string",
                    "examples": ["No, HTTP does not define any limit. However most w...", "Tata Tiago"],
                },
                "type": "answer",
                "value": {
                    "text": {"class": "string", "examples": ["In anaerobic respiration yeast breaks down glucose..."]}
                },
            },
            {
                "display_link": {"class": "string", "examples": ["Montana State University › cs › green"]},
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "link": {"class": "string", "examples": ["https://www.cs.montana.edu/webworks/projects/steve..."]},
                "link_title": {
                    "class": "string",
                    "examples": ["A Brief Introduction to Biofilms - Montana State U..."],
                },
                "rank": {"class": "rank"},
                "type": "image",
            },
            {
                "display_link": {
                    "class": "string",
                    "examples": [
                        "www.huffpost.com › entry › steps-to-success_b_7263...",
                        "www.huffpost.com › entry › ste...",
                    ],
                },
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_alt": {"class": "string", "examples": ["Картинки по запросу steps to success"]},
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "items": [
                    {
                        "rank": {"class": "rank"},
                        "value": {
                            "class": "string",
                            "examples": [
                                "Step 1: Set Your Goal. Start by setting your goal....",
                                "Step 7: Have Enough.",
                            ],
                        },
                    }
                ],
                "link": {"class": "string", "examples": ["https://www.huffpost.com/entry/steps-to-success_b_..."]},
                "link_title": {"class": "string", "examples": ["7 Steps to Success | HuffPost Life"]},
                "rank": {"class": "rank"},
                "type": "ordered_list",
            },
            {
                "display_link": {
                    "class": "string",
                    "examples": ["en.m.wikipedia.org › wiki › Fastest_...", "https://www.mainecooncentral.com"],
                },
                "global_rank": {"class": "rank"},
                "items": [[{"text": {"class": "string", "examples": ["Rank", "Animal", "Maximum speed"]}}]],
                "link": {"class": "string", "examples": ["https://en.wikipedia.org/wiki/Fastest_animals"]},
                "link_title": {
                    "class": "string",
                    "examples": [
                        "Fastest animals - Wikipedia",
                        "What Is The Average Weight Of A Maine Coon Cat? – ...",
                    ],
                },
                "more_link": {"class": "string", "examples": ["https://en.wikipedia.org/wiki/Fastest_animals"]},
                "more_text": {"class": "string", "examples": ["17 more rows", "2 more rows", "Тағы 12 қатар"]},
                "rank": {"class": "rank"},
                "table_title": {"class": "string", "examples": ["TOP 10 MOST POPULOUS COUNTRIES (July 1, 2020)"]},
                "title": {
                    "class": "string",
                    "examples": [
                        "List of animals by speed",
                        "World Population",
                        "How Much Do Maine Coon Kittens Weigh?",
                    ],
                },
                "type": "table",
            },
            {
                "display_link": {"class": "string", "examples": ["GunBacker › best-1911-holsters"]},
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_alt": {"class": "string", "examples": ["Resultado de imagem para carros no rio de janeiro"]},
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "images": [
                    {
                        "image": {
                            "class": "string",
                            "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                        },
                        "image_alt": {
                            "class": "string",
                            "examples": [
                                "Image result for best 1911 holster owb",
                                "Kết quả hình ảnh cho son dưới 50k",
                            ],
                        },
                        "image_base64": {
                            "class": "string",
                            "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                    }
                ],
                "items": [
                    {
                        "rank": {"class": "rank"},
                        "value": {"class": "string", "examples": ["Galco Combat Master. Product. ..."]},
                    }
                ],
                "link": {"class": "string", "examples": ["https://www.gunbacker.com/best-1911-holsters/"]},
                "link_title": {
                    "class": "string",
                    "examples": ["Best 1911 Holsters: IWB & OWB Concealed Carry Hols..."],
                },
                "rank": {"class": "rank"},
                "title": {"class": "string", "examples": ["OWB holsters are easy to find, and often the most ..."]},
                "type": "unordered_list",
            },
            {
                "display_link": {"class": "string", "examples": ["www.youtube.com › watch"]},
                "global_rank": {"class": "rank"},
                "link": {"class": "string", "examples": ["https://www.youtube.com/watch?v=wo1Uv2vlMO8"]},
                "link_title": {
                    "class": "string",
                    "examples": ["Bathtub Replacement | How to Install a Bathtub | T..."],
                },
                "rank": {"class": "rank"},
                "type": "video",
            },
        ],
        ## popular_products - items & title
        "popular_products": {
            "items": [
                {
                    "features": [{"class": "string", "examples": ["597 page", "Paperback", "Fiction"]}],
                    "global_rank": {"class": "rank"},
                    "image": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_alt": {
                        "class": "string",
                        "examples": ["10 x 10 Custom Graphics Printed Pop Up Canopy Tent..."],
                    },
                    "image_base64": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_url": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn2.gstatic.com/shopping?q=tbn:..."],
                    },
                    "link": {"class": "string", "examples": ["https://www.google.com/search?q=10+x+10+Custom+Gra..."]},
                    "price": {"class": "string", "examples": ["$7+", "$4+", "$9+"]},
                    "rank": {"class": "rank"},
                    "rating": {"class": "number", "examples": [4.8, 4.5, 3.9]},
                    "reviews_cnt": {"class": "number", "examples": [4, 22, 6]},
                    "thumbnail": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "title": {
                        "class": "string",
                        "examples": ["10 x 10 Custom Graphics Printed Pop Up Canopy Tent..."],
                    },
                    "type": "popular",
                },
                {
                    "compare_link": {
                        "class": "string",
                        "examples": ["https://www.google.com/search?hl=en&gl=us&q=Apple+..."],
                    },
                    "compare_text": {"class": "string", "examples": ["Compare"]},
                    "features": [{"class": "string", "examples": ["6.7″", "iOS", "5G"]}],
                    "global_rank": {"class": "rank"},
                    "image": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn2.gstatic.com/images?q=tbn:AN..."],
                    },
                    "image_url": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn2.gstatic.com/images?q=tbn:AN..."],
                    },
                    "link": {"class": "string", "examples": ["https://www.google.com/search?hl=en&gl=us&q=Apple+..."]},
                    "price": {"class": "string", "examples": ["$1,000+", "$570+", "$700+"]},
                    "rank": {"class": "rank"},
                    "rating": {"class": "number", "examples": [4.6, 4.5, 4.7]},
                    "reviews_cnt": {"class": "number", "examples": [7800, 32000, 2600]},
                    "title": {
                        "class": "string",
                        "examples": ["Apple iPhone 12 Pro Max", "iPhone 11", "iPhone 12 Mini"],
                    },
                    "type": "related",
                },
            ],
            "title": {"class": "string", "examples": ["Popular products", "Top 16 Dell Laptops", "Related products"]},
        },
        ## recipes - items & title
        "recipes": {
            "items": [
                {
                    "cook_time": {"class": "string", "examples": ["15 min", "30 min", "28 min"]},
                    "global_rank": {"class": "rank"},
                    "image": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_base64": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_url": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                    },
                    "ingredients": [
                        {"class": "string", "examples": ["Pearl dust", "powdered gelatin", "Knox gelatin"]}
                    ],
                    "link": {"class": "string", "examples": ["https://sugargeekshow.com/recipe/edible-glitter-re..."]},
                    "rank": {"class": "rank"},
                    "rating": {"class": "number", "examples": [5, 4.5, 4.9]},
                    "reviews_cnt": {"class": "number", "examples": [9, 18, 25]},
                    "source": {"class": "string", "examples": ["Sugar Geek Show", "Avalon Cakes", "wikiHow"]},
                    "title": {
                        "class": "string",
                        "examples": ["Edible Glitter Recipe", "Pizza Dough", "Easy Homemade Pizza Dough"],
                    },
                }
            ],
            "title": {"class": "string", "examples": ["Recipes"]},
        },
        ## top_stories - items & title
        "top_stories": {
            "items": [
                {
                    "date": {"class": "string", "examples": ["6 hours ago", "12 hours ago", "1 day ago"]},
                    "global_rank": {"class": "rank"},
                    "image": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                    },
                    "image_base64": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_url": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                    },
                    "link": {"class": "string", "examples": ["https://sneakernews.com/2019/04/08/adidas-alphaboo..."]},
                    "rank": {"class": "rank"},
                    "source": {"class": "string", "examples": ["Sneaker News", "Elle", "Коммерсант"]},
                    "source_logo": {
                        "class": "string",
                        "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJ0A..."],
                    },
                    "title": {
                        "class": "string",
                        "examples": ["adidas Blends Two Cushioning Franchises With The A..."],
                    },
                }
            ],
            "title": {"class": "string", "examples": ["Top stories", "Videos", "Schlagzeilen"]},
        },
        ## shopping - list of dict
        "shopping": [
            {
                "best_match": {"class": "boolean", "examples": [False, True]},
                "compare_prices": {
                    "class": "string",
                    "examples": ["https://www.google.com/shopping/product/1155370994..."],
                },
                "description": {
                    "class": "string",
                    "examples": ["CPU upgrade to improve product performance The AS1..."],
                },
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["https://lh3.googleusercontent.com/spp/AARfHkwvKQ8x..."]},
                "image_alt": {"class": "string", "examples": ["NERF - N-Strike Elite PocketStrike"]},
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/webp;base64,UklGRjQpAABXRUJQVlA4ICgpAAD..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://lh3.googleusercontent.com/spp/AARfHkwvKQ8x..."],
                },
                "link": {"class": "string", "examples": ["https://www.google.com/shopping/product/r/GB/13122..."]},
                "price": {"class": "string", "examples": ["£249.97", "$15.95", "$23.99"]},
                "rank": {"class": "rank"},
                "rating": {"class": "number", "examples": [4.5, 5, 4.6]},
                "referral_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/aclk?sa=L&ai=DChcSEwix1MKEu..."],
                },
                "reviews_cnt": {"class": "number", "examples": [56, 3, 2]},
                "shipping": {"class": "string", "examples": ["£4.99 delivery", "Free delivery", "€10.00 delivery"]},
                "shop": {"class": "string", "examples": ["Laptops Direct", "Mercato.com", "Walmart"]},
                "shop_link": {
                    "class": "string",
                    "examples": ["https://www.laptopsdirect.co.uk/asustor-4-bay-512m..."],
                },
                "title": {
                    "class": "string",
                    "examples": [
                        "Asustor AS1004T V2 4-Bay NAS 512MB",
                        "Vera Wang Princess Eau de Toilette 100ml Princess ...",
                    ],
                },
                "trusted_store": {"class": "boolean", "examples": [False, True]},
            }
        ],
        ## product_offers - list of dict
        "product_offers": [
            {
                "details": [
                    {
                        "class": "string",
                        "examples": ["Gratis forsendelse", "€\xa09,95 verzendkosten", "Versand gratis"],
                    }
                ],
                "global_rank": {"class": "rank"},
                "link": {"class": "string", "examples": ["https://www.google.com/aclk?sa=l&ai=DChcSEwiztba7g..."]},
                "price_details": [
                    {
                        "currency": {"class": "string", "examples": ["DKK", "USD", "EUR"]},
                        "price": {"class": "number", "examples": [749.95, 0, 424.99]},
                        "type": {"class": "string", "examples": ["Varens pris", "Forsendelse", "Samlet pris"]},
                    }
                ],
                "rank": {"class": "rank"},
                "seller": {
                    "class": "string",
                    "examples": ["Pro-Outdoor.dk", "AmericanLifeguard.Net", "Survive Outdoors"],
                },
            }
        ],
        ## related - list of dict
        "related": [
            {
                "expanded": {"class": "boolean", "examples": [True, False]},
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."]},
                "image_alt": {
                    "class": "string",
                    "examples": ["Image of Teemu Pukki", "Image of Italy flag", "Image of Italy food"],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                },
                "items": [
                    {
                        "description": {
                            "class": "string",
                            "examples": ["Pizza Hut is an American restaurant chain and inte..."],
                        },
                        "image": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "image_alt": {"class": "string", "examples": ["Image of Toy Car big", "Busuu", "HelloTalk"]},
                        "image_url": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "link": {
                            "class": "string",
                            "examples": ["https://www.google.com/search?gl=US&hl=en&q=BBC+Sp..."],
                        },
                        "title": {"class": "string", "examples": ["BBC Sport", "Hamm Truck", "Lizzie"]},
                        "type": "card",
                    },
                    {
                        "author": {"class": "string", "examples": ["BBC News", "BBC", "CBC News"]},
                        "date": {"class": "string", "examples": ["1 week ago", "2 weeks ago", "1 month ago"]},
                        "duration": {"class": "string", "examples": ["2:57", "12:19", "2:20"]},
                        "duration_sec": {"class": "number", "examples": [177, 739, 140]},
                        "image": {
                            "class": "string",
                            "examples": ["https://i.ytimg.com/vi/kTaXh_u_Qq4/mqdefault.jpg?s..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://i.ytimg.com/vi/kTaXh_u_Qq4/mqdefault.jpg?s..."],
                        },
                        "link": {
                            "class": "string",
                            "examples": [
                                "https://www.youtube.com/watch?v=kTaXh_u_Qq4",
                                "https://www.youtube.com/watch?v=rqyru7no0gk",
                            ],
                        },
                        "source": {"class": "string", "examples": ["YouTube"]},
                        "title": {
                            "class": "string",
                            "examples": ["Have we become more forgetful in lockdown? - BBC N..."],
                        },
                        "type": "video",
                    },
                ],
                "link": {"class": "string", "examples": ["https://www.google.com/search?hl=en&q=adidas+us&sa..."]},
                "list_group": {"class": "boolean", "examples": [False, True]},
                "more_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/search?gl=US&hl=en&q=BBC+ne..."],
                },
                "more_text": {"class": "string", "examples": ["See more", "Switch Lite", "Irish celebrities"]},
                "rank": {"class": "rank"},
                "text": {"class": "string", "examples": ["adidas us", "adidas shoes", "adidas originals"]},
            }
        ],
        ## people_also_ask - list of dict
        ## [NOTE] answer_link, but link
        "people_also_ask": [
            {
                "answer_display_link": {
                    "class": "string",
                    "examples": ["https://www.amazon.com/ask/questions/Tx1QIWVSM753Z..."],
                },
                "answer_html": {
                    "class": "string",
                    "examples": ['<div class="mod" data-md="61" style="clear:none"><...'],
                },
                "answer_link": {
                    "class": "string",
                    "examples": ["https://www.amazon.com/ask/questions/Tx1QIWVSM753Z..."],
                },
                "answer_source": {"class": "string", "examples": ["Amazon.com: Customer Questions & Answers"]},
                "answers": [
                    {
                        "rank": {"class": "rank"},
                        "title": {
                            "class": "string",
                            "examples": ["Lots of people wear shoes too big for them and it ..."],
                        },
                        "type": "answer",
                        "value": {
                            "text": {
                                "class": "string",
                                "examples": ["Lots of people wear shoes too big for them and it ..."],
                            }
                        },
                    },
                    {
                        "rank": {"class": "rank"},
                        "title": {
                            "class": "string",
                            "examples": ["BBC", "78 years (8 September 1941)", "Mike Bloomberg"],
                        },
                        "type": "exact_answer",
                    },
                    {
                        "image": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                        },
                        "rank": {"class": "rank"},
                        "type": "image",
                    },
                    {
                        "items": [
                            {
                                "rank": {"class": "rank"},
                                "value": {
                                    "class": "string",
                                    "examples": [
                                        "Adidas.com. Surprisingly, Adidas.com is one of the...",
                                        "Plant a tree.",
                                    ],
                                },
                            }
                        ],
                        "link": {
                            "class": "string",
                            "examples": ["https://www.printoclock.com/blog/8-regles-a-suivre..."],
                        },
                        "rank": {"class": "rank"},
                        "title": {
                            "class": "string",
                            "examples": ["The 5 Best Places to Find Cheap Adidas Shoes and G..."],
                        },
                        "type": "ordered_list",
                    },
                    {
                        "items": [
                            {
                                "rank": {"class": "rank"},
                                "value": {"class": "string", "examples": ["Alpharetta", "Zip codes", "BBC Worldwide"]},
                            }
                        ],
                        "rank": {"class": "rank"},
                        "title": {
                            "class": "string",
                            "examples": ["Alpharetta/Zip codes", "Chris Pine/Nationality", "Maine Coon/Масса"],
                        },
                        "type": "path",
                    },
                    {
                        "items": [[{"text": {"class": "string", "examples": ["", "Aerobic", "Anaerobic"]}}]],
                        "link": {
                            "class": "string",
                            "examples": ["https://www.thijsschouten.com/diverse-artikelen/be..."],
                        },
                        "more_link": {
                            "class": "string",
                            "examples": ["https://www.thijsschouten.com/diverse-artikelen/be..."],
                        },
                        "more_text": {"class": "string", "examples": ["Nog 5 rijen", "16 more rows", "20 more rows"]},
                        "rank": {"class": "rank"},
                        "table_title": {"class": "string", "examples": ["Unit Cost", "Rey", "Krypto the Superdog"]},
                        "title": {
                            "class": "string",
                            "examples": ["Aerobic respiration vs anaerobic respiration", "List by president"],
                        },
                        "type": "table",
                    },
                    {
                        "items": [
                            {
                                "rank": {"class": "rank"},
                                "value": {
                                    "class": "string",
                                    "examples": [
                                        "During anaerobic respiration, the oxidation of glu...",
                                        "Anvyl.",
                                        "Daedalus.",
                                    ],
                                },
                            }
                        ],
                        "link": {
                            "class": "string",
                            "examples": ["https://www.bbc.co.uk/bitesize/guides/zwvx8mn/revi..."],
                        },
                        "rank": {"class": "rank"},
                        "title": {
                            "class": "string",
                            "examples": ["Anaerobic respiration", "Top 9 Xometry competitors"],
                        },
                        "type": "unordered_list",
                    },
                    {
                        "items": [
                            {
                                "link": {
                                    "class": "string",
                                    "examples": ["https://www.google.com/search?hl=en&gl=us&q=30004&..."],
                                },
                                "rank": {"class": "rank"},
                                "summary": {"class": "string", "examples": ["Midfielder", "Adult"]},
                                "text": {"class": "string", "examples": ["30004", "30005", "30009"]},
                            }
                        ],
                        "rank": {"class": "rank"},
                        "type": "values",
                    },
                    {
                        "link": {
                            "class": "string",
                            "examples": [
                                "https://www.youtube.com/watch?v=RoB3ziqk0oI",
                                "https://www.youtube.com/watch?v=WM1XcYXix0Y",
                            ],
                        },
                        "rank": {"class": "rank"},
                        "type": "video",
                    },
                ],
                "global_rank": {"class": "rank"},
                "has_answer_link": {"class": "boolean", "examples": [False]},
                "question": {
                    "class": "string",
                    "examples": ["Do adidas run big or small?", "Why is Zachary Quinto not in discovery?"],
                },
                "question_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/search?hl=en&q=Do+adidas+ru..."],
                },
                "rank": {"class": "rank"},
            }
        ],
        ## questions_and_answers - list of dict
        "questions_and_answers": [
            {
                "answer": {"class": "string", "examples": ["In GP for this question your first term is a= 9\n\na..."]},
                "global_rank": {"class": "rank"},
                "link": {"class": "string", "examples": ["https://www.quora.com/What-is-the-common-ratio-of-..."]},
                "question": {
                    "class": "string",
                    "examples": ["What is the common ratio of GP 9, 3, and 1?", "8th term of the GP 1-3-9- - -"],
                },
                "rank": {"class": "rank"},
                "source": {"class": "string", "examples": ["Quora", "Study.com", "Doubtnut"]},
                "source_logo": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn3.gstatic.com/faviconV2?url=h..."],
                },
                "votes": {"class": "number", "examples": [0, 51, 1]},
            }
        ],
        ## news - list of dict
        "news": [
            {
                "date": {"class": "string", "examples": ["Mar 24, 2018", "4 days ago", "3 weeks ago"]},
                "description": {
                    "class": "string",
                    "examples": ["CCI approves acquisition of 100% equity in Virtusa..."],
                },
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                },
                "link": {"class": "string", "examples": ["https://www.domain-b.com/management/m_a/index.htm"]},
                "rank": {"class": "rank"},
                "source": {"class": "string", "examples": ["domain-b.com", "AiThority.com", "Fibre2Fashion"]},
                "source_logo": {
                    "class": "string",
                    "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAA..."],
                },
                "title": {"class": "string", "examples": ["Indian business : management : M&A/restructuring :..."]},
            }
        ],
        ################################################################
        # attributes to ignore
        ################################################################
        "pagination": {
            "current_page": {"class": "number", "examples": [1, 3, 6]},
            "first_page_link": {
                "class": "string",
                "examples": ["https://www.google.com/search?q=addidas&hl=en&gbv=..."],
            },
            "next_page": {"class": "number", "examples": [2, 4, 7]},
            "next_page_link": {
                "class": "string",
                "examples": ["https://www.google.com/search?q=adidas&hl=en&ei=KS..."],
            },
            "next_page_start": {"class": "number", "examples": [10, 30, 100]},
            "pages": [
                {
                    "link": {"class": "string", "examples": ["https://www.google.com/search?q=adidas&hl=en&ei=KS..."]},
                    "page": {"class": "number", "examples": [2, 3, 4]},
                    "start": {"class": "number", "examples": [10, 20, 30]},
                }
            ],
            "prev_page": {"class": "number", "examples": [2, 5, 1]},
            "prev_page_link": {
                "class": "string",
                "examples": ["https://www.google.com/search?q=addidas&hl=en&gbv=..."],
            },
            "prev_page_start": {"class": "number", "examples": [10, 40, 0]},
        },
        "jobs": {
            "items": [
                {
                    "company": {"class": "string", "examples": ["IBT GROUP", "Fiberlux", "Emprego"]},
                    "description": {
                        "class": "string",
                        "examples": ["RESUMEN En la empresa Transnacional IBT GROUP nos ..."],
                    },
                    "global_rank": {"class": "rank"},
                    "image": {
                        "class": "string",
                        "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgA..."],
                    },
                    "image_base64": {
                        "class": "string",
                        "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgA..."],
                    },
                    "link": {"class": "string", "examples": ["https://www.laborum.pe/job/IBT-GROUP/Asistente-de-..."]},
                    "location": {"class": "string", "examples": ["Lima", "San Luis", "Carabayllo"]},
                    "logo": {"class": "string", "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."]},
                    "rank": {"class": "rank"},
                    "site": {
                        "class": "string",
                        "examples": ["http://www.ibtgroupllc.com/", "via Jobilize", "via Job\\Searcher"],
                    },
                    "source": {
                        "class": "string",
                        "examples": ["a través de Laborum", "via ZipRecruiter", "via Internships.com"],
                    },
                    "tags": [
                        {
                            "name": {"class": "string", "examples": ["Posted", "Salary", "Опубликовано"]},
                            "value": {
                                "class": "string",
                                "examples": ["hace 1 día", "Tiempo completo", "hace 22 horas"],
                            },
                        }
                    ],
                    "title": {"class": "string", "examples": ["Asistente de Formación"]},
                }
            ]
        },
        "apps": {
            "items": [
                {
                    "app_id": {"class": "string", "examples": ["id1130498044", "id1300146617", "id329541503"]},
                    "global_rank": {"class": "rank"},
                    "has_install_button": {"class": "boolean", "examples": [True]},
                    "image": {
                        "class": "string",
                        "examples": ["https://lh3.googleusercontent.com/P3RxaRB7fOuOaYty..."],
                    },
                    "image_alt": {
                        "class": "string",
                        "examples": ["Apple Support", "Minecraft", "My Stocks Portfolio & Widget"],
                    },
                    "image_base64": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_url": {
                        "class": "string",
                        "examples": ["https://lh3.googleusercontent.com/P3RxaRB7fOuOaYty..."],
                    },
                    "link": {"class": "string", "examples": ["https://apps.apple.com/us/app/apple-support/id1130..."]},
                    "price": {
                        "class": "string",
                        "examples": ["Free", "Puzzle · Match 3", "Puzzle · Match 3 · Casual"],
                    },
                    "rank": {"class": "rank"},
                    "rating": {"class": "string", "examples": ["3.7", "4.0", "4.7"]},
                    "reviews_cnt": {"class": "number", "examples": [35000, 1000000, 88000]},
                    "source": {
                        "class": "string",
                        "examples": ["Mojang", "Sony Home Entertainment & Sound Products Inc.", "Tinder"],
                    },
                    "title": {
                        "class": "string",
                        "examples": ["Apple Support", "Minecraft", "My Stocks Portfolio & Widget"],
                    },
                }
            ],
            "title": {"class": "string", "examples": ["Apps", "AppsMore apps", "(34K)"]},
        },
        "flights": {
            "date_from": {"class": "string", "examples": ["Mon, August 2", "Mon, Aug 2", "Fri, March 26"]},
            "date_to": {"class": "string", "examples": ["Sun, August 8", "Sun, Aug 8", "Sat, April 10"]},
            "from": {"class": "string", "examples": ["Moscow, Russia (all airports)", "Sydney, Australia"]},
            "items": [
                {
                    "global_rank": {"class": "rank"},
                    "link": {"class": "string", "examples": ["https://www.google.com/flights?gl=us&hl=en&source=..."]},
                    "logo": {"class": "string", "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAA..."]},
                    "price": {"class": "string", "examples": ["from $462", "from $539", "from $603"]},
                    "rank": {"class": "rank"},
                    "stops": {"class": "string", "examples": ["Connecting", "Nonstop"]},
                    "title": {"class": "string", "examples": ["Turkish Airlines", "Qatar Airways", "Air India"]},
                    "travel_time": {"class": "string", "examples": ["9h 55m+", "1d 6h+", "6h 30m"]},
                }
            ],
            "title": {
                "class": "string",
                "examples": ["Flights from Moscow, Russia (all airports) to New ...", "Flights to New York"],
            },
            "to": {
                "class": "string",
                "examples": ["New Delhi, India (DEL)", "New Delhi, India", "New York, NY (all airports)"],
            },
        },
        "top_knowledge_carousel": {
            "list": [
                {
                    "global_rank": {"class": "rank"},
                    "image": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                    },
                    "image_alt": {"class": "string", "examples": ["Lisa Loven Kongsli", "Doutzen Kroes", "Ann Wolfe"]},
                    "image_base64": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "image_url": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                    },
                    "link": {"class": "string", "examples": ["https://www.google.com/search?hl=en&gl=us&q=Lisa+L..."]},
                    "rank": {"class": "rank"},
                    "subtitle": {"class": "string", "examples": ["Menalippe", "Venelia", "Artemis of Bana-Mighdall"]},
                    "thumbnail": {
                        "class": "string",
                        "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                    },
                    "title": {"class": "string", "examples": ["Lisa Loven Kongsli", "Doutzen Kroes", "Ann Wolfe"]},
                }
            ],
            "more_text": {"class": "string", "examples": ["More shows & movies", "Тағы"]},
            "path": [
                {
                    "link": {"class": "string", "examples": ["https://www.google.com/search?hl=en&gl=us&q=wonder..."]},
                    "text": {"class": "string", "examples": ["Wonder Woman", "Cast", "Microsoft Corporation"]},
                }
            ],
            "predicate": {
                "class": "string",
                "examples": ["kc:/film/film:cast", "kc:/people/person:movies", "kc:/people/person:sideways"],
            },
        },
        "knowledge": {
            "address": {
                "class": "string",
                "examples": [
                    "Strada Scaparoni, 4, 12051 Alba CN, Italy",
                    "901 Technology Center Dr, Stoughton, MA 02072",
                ],
            },
            "booking_available": {"class": "string", "examples": ["unknown", False, True]},
            "category": {"class": "string", "examples": ["Hotel", "Магазин мебели", "Marketing agency"]},
            "description": {"class": "string", "examples": ["Adidas AG is a multinational corporation, founded ..."]},
            "description_link": {
                "class": "string",
                "examples": ["https://en.wikipedia.org/wiki/Adidas", "https://en.wikipedia.org/wiki/Zachary_Quinto"],
            },
            "description_source": {"class": "string", "examples": ["Wikipedia", "Wikipédia", "Google Books"]},
            "distance": {"class": "string", "examples": ["1,5 km"]},
            "events": [
                {
                    "day": {"class": "string", "examples": ["Fri, Jan 13", "Sat, Jan 14"]},
                    "hours": {"class": "string", "examples": ["6:00PM", "9:00PM", "1:30PM"]},
                    "link": {"class": "string", "examples": ["https://www.google.com/search?gl=us&hl=en&q=paul+s..."]},
                    "name": {"class": "string", "examples": ["Paul Smith", "DJ Ckastley", "Katie Stewart"]},
                }
            ],
            "facts": [
                {
                    "key": {"class": "string", "examples": ["Subsidiaries", "Founder", "Founded"]},
                    "key_link": {
                        "class": "string",
                        "examples": ["https://www.google.com/search?hl=en&q=adidas+subsi..."],
                    },
                    "predicate": {
                        "class": "string",
                        "examples": ["hw:/collection/organizations:subsidiaries", "kc:/people/person:education"],
                    },
                    "value": [
                        {
                            "link": {
                                "class": "string",
                                "examples": ["https://www.google.com/search?hl=en&q=Reebok&stick..."],
                            },
                            "text": {"class": "string", "examples": ["Reebok", "Five Ten Footwear", "Runtastic"]},
                        }
                    ],
                }
            ],
            "fid": {"class": "string", "examples": ["0x12d2b2cc308d745f:0x7959f1515aae5fd1"]},
            "future_open": {"class": "string", "examples": ["Abre el 16 abr."]},
            "hotel_amenities": [{"class": "string", "examples": ["Free Wi-Fi", "Free breakfast", "Accessible"]}],
            "hotel_description": {
                "class": "string",
                "examples": ["This polished hotel in an elegant 19th-century bui..."],
            },
            "hotel_rates": {
                "date_from": {"class": "string", "examples": ["Wed, Jan 15", "Sun, Jan 19", "Mon, Dec 6"]},
                "date_to": {"class": "string", "examples": ["Thu, Jan 16", "Mon, Jan 20", "Tue, Dec 7"]},
                "items": [
                    {
                        "extensions": [
                            {"class": "string", "examples": ["Read Real Guest ReviewsGet Instant Confirmation"]}
                        ],
                        "global_rank": {"class": "rank"},
                        "price": {"class": "string", "examples": ["RUB 4,970", "RUB 4,958", "$91"]},
                        "rank": {"class": "rank"},
                        "title": {"class": "string", "examples": ["Expedia.com", "Booking.com", "Hotels.com"]},
                    }
                ],
                "occupancy": {"class": "string", "examples": ["2"]},
            },
            "images": [
                {
                    "image": {
                        "class": "string",
                        "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsA..."],
                    },
                    "image_alt": {
                        "class": "string",
                        "examples": ["Image result for Angel Has Fallen", "Image result for Zachary Quinto"],
                    },
                    "image_base64": {
                        "class": "string",
                        "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsA..."],
                    },
                    "image_url": {
                        "class": "string",
                        "examples": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:AN..."],
                    },
                    "link": {"class": "string", "examples": ["https://www.google.com/search?q=Angel+Has+Fallen&g..."]},
                    "thumbnail": {
                        "class": "string",
                        "examples": ["data:image/webp;base64,UklGRp4IAABXRUJQVlA4IJIIAAC..."],
                    },
                }
            ],
            "latitude": {"class": "number", "examples": [27.7691744, 53.3815527, 49.8736558]},
            "lcl_akp_link": {"class": "string", "examples": ["https://www.google.com/async/lcl_akp?ei=JeBbXfCuFt..."]},
            "longitude": {"class": "number", "examples": [-82.636906, -1.4716948, 2.2782018]},
            "maps_link": {"class": "string", "examples": ["https://maps.google.com/maps/place//data=!4m2!3m1!..."]},
            "menu": {"class": "string", "examples": ["http://www.cubanatapasbar.co.uk/pdf/Cubana-Tapas-M..."]},
            "merchant_description": {
                "class": "string",
                "examples": ['"Sample our authentic Cuban surroundings, unique C...'],
            },
            "name": {"class": "string", "examples": ["Adidas", "Farm from Mom", "Angel Has Fallen"]},
            "open_hours": [
                {
                    "day": {"class": "string", "examples": ["Tuesday", "Wednesday", "Thursday"]},
                    "day_comment": {
                        "class": "string",
                        "examples": ["(Summer Bank Holiday)", "(Thanksgiving)", "(Black Friday)"],
                    },
                    "hours": {"class": "string", "examples": ["9am–8pm", "9am–6pm", "9am–5:30pm"]},
                    "hours_comment": {
                        "class": "string",
                        "examples": ["Hours might differ", "Les horaires peuvent être modifiés."],
                    },
                }
            ],
            "open_status": {"class": "string", "examples": ["Open", "permanently_closed"]},
            "phone": {"class": "string", "examples": ["800 915 904", "0370 010 0222", "0333 247 1247"]},
            "pid": {
                "class": "string",
                "examples": [
                    "ChIJX3SNMMyy0hIR0V-uWlHxWXk",
                    "ChIJQ4iTm2ZreUgRIdidQJt0nEU",
                    "ChIJqW4_ULyD5IkRcuMJW3k5x1E",
                ],
            },
            "price": {"class": "string", "examples": ["$$", "$$$"]},
            "rating": {"class": "number", "examples": [4.8, 4.2, 5]},
            "reservations": {"class": "string", "examples": ["http://cubanatapasbar.co.uk/request.php"]},
            "reservations_links": [{"class": "string", "examples": ["http://cubanatapasbar.co.uk/request.php"]}],
            "reviews": [
                {
                    "comment": {
                        "class": "string",
                        "examples": ["543214.33 件のレビュー543214.33 件のレビュー543215432155443322..."],
                    },
                    "link": {"class": "string", "examples": ["https://www.google.com/maps/contrib/10886972567153..."]},
                    "rating": {"class": "number", "examples": [4.3, 5, 4]},
                    "star_rating": {"class": "number", "examples": [4.3, 5, 4]},
                    "title": {"class": "string", "examples": ["543214.33 件のレビュー", "Rooms", "Location"]},
                }
            ],
            "reviews_cnt": {"class": "number", "examples": [202, 1079, 4]},
            "site": {
                "class": "string",
                "examples": ["https://www.adidas.com/us", "https://www.youtube.com/watch?v=PFVK2BR9Na4"],
            },
            "subtitle": {
                "class": "string",
                "examples": ["R 2019 ‧ Action/Thriller ‧ 2h 1m", "Animal", "Novel series"],
            },
            "summary": {"class": "string", "examples": ["3-star hotel", "Restaurant", "Peruvian restaurant"]},
            "view_more_rates_link": {
                "class": "string",
                "examples": ["https://www.google.com/travel/hotels/Agriturismo%2..."],
            },
            "widgets": [
                {
                    "global_rank": {"class": "rank"},
                    "items": [
                        {
                            "image": {
                                "class": "string",
                                "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEcA..."],
                            },
                            "image_alt": {"class": "string", "examples": ["Nike", "Reebok", "Puma"]},
                            "image_base64": {
                                "class": "string",
                                "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEcA..."],
                            },
                            "image_url": {
                                "class": "string",
                                "examples": ["https://lh5.googleusercontent.com/p/AF1QipO_QzLEIE..."],
                            },
                            "link": {
                                "class": "string",
                                "examples": ["https://www.google.com/search?hl=en&q=NIKE&stick=H..."],
                            },
                            "rank": {"class": "rank"},
                            "subtitle": {"class": "string", "examples": ["Mike Banning", "Dora Skirth", "2021"]},
                            "title": {"class": "string", "examples": ["Nike", "Reebok", "Puma"]},
                        }
                    ],
                    "key": {"class": "string", "examples": ["sideways", "cast", "related sets"]},
                    "key_link": {
                        "class": "string",
                        "examples": ["https://www.google.com/search?hl=en&q=ADIDAS&stick..."],
                    },
                    "predicate": {"class": "string", "examples": ["kc:/common:sideways"]},
                    "rank": {"class": "rank"},
                    "title": {"class": "string", "examples": ["People also search for", "Cast", "В ролях"]},
                    "type": "carousel",
                },
                {
                    "global_rank": {"class": "rank"},
                    "items": [
                        {
                            "author": {"class": "string", "examples": ["Ben Kenigsberg", "Neil Soans", "John Nugent"]},
                            "link": {
                                "class": "string",
                                "examples": ["https://www.sify.com/movies/angel-has-fallen-revie..."],
                            },
                            "rank": {"class": "rank"},
                            "source": {
                                "class": "string",
                                "examples": ["Sify Movies", "The NYTimes", "Times of India"],
                            },
                            "text": {
                                "class": "string",
                                "examples": ["Angel Has Fallen starring Gerard Butler and Morgan..."],
                            },
                        }
                    ],
                    "key": {"class": "string", "examples": ["critic_reviews"]},
                    "key_link": {
                        "class": "string",
                        "examples": ["https://www.google.com/search?gl=us&hl=en&q=angel+..."],
                    },
                    "predicate": {
                        "class": "string",
                        "examples": ["kc:/film/film:critic_reviews", "kc:/book/book:critic_reviews"],
                    },
                    "rank": {"class": "rank"},
                    "title": {"class": "string", "examples": ["Critic reviews"]},
                    "type": "critic_reviews",
                },
                {
                    "global_rank": {"class": "rank"},
                    "items": [
                        {
                            "link": {
                                "class": "string",
                                "examples": [
                                    "https://www.imdb.com/title/tt6189022/",
                                    "https://www.metacritic.com/movie/wonder-woman",
                                ],
                            },
                            "rank": {"class": "rank"},
                            "rating": {"class": "string", "examples": ["6.4/10", "38%", "45%"]},
                            "title": {"class": "string", "examples": ["IMDb", "Rotten Tomatoes", "Metacritic"]},
                        }
                    ],
                    "key": {"class": "string", "examples": ["reviews", "critic-ratings"]},
                    "predicate": {
                        "class": "string",
                        "examples": [
                            "kc:/film/film:reviews",
                            "kc:/book/book:reviews",
                            "kc:/shopping/gpc:critic-ratings",
                        ],
                    },
                    "rank": {"class": "rank"},
                    "type": "rate",
                },
                {
                    "global_rank": {"class": "rank"},
                    "items": [
                        {
                            "link": {"class": "string", "examples": ["http://instagram.com/adidas/"]},
                            "name": {"class": "string", "examples": ["Instagram", "Facebook", "Twitter"]},
                            "rank": {"class": "rank"},
                        }
                    ],
                    "key": {"class": "string", "examples": ["social media presence"]},
                    "predicate": {"class": "string", "examples": ["kc:/common/topic:social media presence"]},
                    "rank": {"class": "rank"},
                    "type": "social_media",
                },
                {
                    "global_rank": {"class": "rank"},
                    "key": {"class": "string", "examples": ["thumbs_up"]},
                    "predicate": {"class": "string", "examples": ["kc:/ugc:thumbs_up"]},
                    "rank": {"class": "rank"},
                    "type": "thumbs",
                    "value": {
                        "subtitle": {"class": "string", "examples": ["Google users"]},
                        "title": {
                            "class": "string",
                            "examples": ["87% liked this movie", "92% liked this book", "90% liked this book"],
                        },
                    },
                },
                {
                    "global_rank": {"class": "rank"},
                    "items": [
                        {
                            "rank": {"class": "rank"},
                            "rating": {"class": "number", "examples": [5, 4]},
                            "text": {
                                "class": "string",
                                "examples": ["This is hands down the best film in the trilogy an..."],
                            },
                            "user_pic": {
                                "class": "string",
                                "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                            },
                        }
                    ],
                    "key": {"class": "string", "examples": ["user_reviews"]},
                    "predicate": {"class": "string", "examples": ["kc:/ugc:user_reviews"]},
                    "rank": {"class": "rank"},
                    "summary": {
                        "rating": {"class": "string", "examples": ["4.3", "4.6", "4.4"]},
                        "ratings": [
                            {
                                "percentage": {"class": "number", "examples": [66, 15, 5]},
                                "rating": {"class": "number", "examples": [5, 4, 3]},
                            }
                        ],
                        "reviews_cnt": {"class": "number", "examples": [936, 376, 117]},
                    },
                    "type": "user_reviews",
                },
            ],
            "zoom": {"class": "number", "examples": [15]},
        },
        "hotels_selection": {
            "date_from": {"class": "string", "examples": ["Sat, Jan 18", "Tue, Jul 18", "शनि, 22 जुल॰"]},
            "date_to": {"class": "string", "examples": ["Sun, Jan 19", "Wed, Jul 19", "रवि, 23 जुल॰"]},
            "link": {"class": "string", "examples": ["https://www.google.com/travel/hotels/forest%20park..."]},
            "suggestions": [
                {
                    "global_rank": {"class": "rank"},
                    "link": {"class": "string", "examples": ["https://www.google.com/travel/hotels/forest%20park..."]},
                    "name": {
                        "class": "string",
                        "examples": [
                            "The Residences at Forest Park",
                            "Ouray Riverside Resort / Ouray RV Park & Cabins",
                        ],
                    },
                    "price": {"class": "string", "examples": ["$129", "$81", "$203"]},
                    "rank": {"class": "rank"},
                    "rating": {"class": "number", "examples": [4.1, 2.4, 4.2]},
                    "reviews_cnt": {"class": "number", "examples": [9, 467, 840]},
                    "tags": [{"class": "string", "examples": ["Free parking", "Free Wi-Fi", "Free breakfast"]}],
                }
            ],
            "title": {"class": "string", "examples": ["Near United States"]},
        },
        "snack_pack_map": {
            "altitude": {"class": "number", "examples": [3142, 4072, 36263]},
            "image": {"class": "string", "examples": ["https://www.google.com/maps/vt/data=o99fOkXrF5vDGD..."]},
            "image_alt": {
                "class": "string",
                "examples": ["Map of adidas", "Map of samsung phone", "Map of super dog"],
            },
            "image_base64": {"class": "string", "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAeAA..."]},
            "image_url": {"class": "string", "examples": ["https://www.google.com/maps/vt/data=o99fOkXrF5vDGD..."]},
            "latitude": {"class": "number", "examples": [61.25774, 53.583819, 37.985839]},
            "link": {"class": "string", "examples": ["https://www.google.com/search?hl=en&q=adidas&npsic..."]},
            "longitude": {"class": "number", "examples": [73.405605, 9.947835, -122.181323]},
        },
        "snack_pack": [
            {
                "address": {
                    "class": "string",
                    "examples": ["Nefteyuganskoye Shosse, 1", "39660 Lyndon B Johnson Fwy"],
                },
                "cid": {
                    "class": "string",
                    "examples": ["176167453568822596", "6886485132707460061", "7646379954526047805"],
                },
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://lh5.googleusercontent.com/p/AF1QipNrmJrE8I..."],
                },
                "images": [
                    {
                        "image": {
                            "class": "string",
                            "examples": ["https://lh5.googleusercontent.com/p/AF1QipPnuwpF8o..."],
                        },
                        "image_base64": {
                            "class": "string",
                            "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFQA..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://lh5.googleusercontent.com/p/AF1QipPnuwpF8o..."],
                        },
                    }
                ],
                "link": {"class": "string", "examples": ["https://www.google.com/search?hl=en&q=ADIDAS,+%D1%..."]},
                "maps_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/maps/dir//ADIDAS,+%D1%81%D0..."],
                },
                "name": {
                    "class": "string",
                    "examples": ["ADIDAS, сеть магазинов спортивных товаров", "LEA Networks", "Spend Matters"],
                },
                "phone": {
                    "class": "string",
                    "examples": ["8 (346) 231-00-93", "8 (346) 252-30-83", "8 (346) 231-00-94"],
                },
                "price": {"class": "string", "examples": ["$$", "$$$", "$"]},
                "rank": {"class": "rank"},
                "rating": {"class": "number", "examples": [3, 4.1, 1]},
                "reviews_cnt": {"class": "number", "examples": [2, 11, 1]},
                "site": {
                    "class": "string",
                    "examples": ["http://www.adidas.ru/", "http://southtoyotapm.com/?utm_source=google&utm_me..."],
                },
                "summary": {"class": "string", "examples": ["Their website mentions aeg"]},
                "tags": [{"class": "string", "examples": ["In-store shopping", "In-store pick-up", "Dine-in"]}],
                "type": {"class": "string", "examples": ["Handicraft", "Electronics repair shop", "Hardware store"]},
                "work_status": {"class": "string", "examples": ["Open", "Closed", "Opens soon"]},
                "work_status_details": {"class": "string", "examples": ["Closes 10PM", "Closes 9PM", "Opens 11AM"]},
            }
        ],
        "top_ads": [
            {
                "deal_link": {
                    "class": "string",
                    "examples": ["https://www.googleadservices.com/pagead/aclk?sa=L&..."],
                },
                "deal_text": {"class": "string", "examples": ["50% off Residential Plan"]},
                "description": {
                    "class": "string",
                    "examples": ["Фирменная одежда и обувь adidas®. Успей сделать за..."],
                },
                "display_link": {"class": "string", "examples": ["www.adidas.ru/", "www.comparethemarket.com/"]},
                "extensions": [
                    {
                        "description": {
                            "class": "string",
                            "examples": ["Terms From 1-7 Years", "Terms From 1-30 Years", "Single Monthly Repayment"],
                        },
                        "link": {
                            "class": "string",
                            "examples": ["https://www.googleadservices.com/pagead/aclk?sa=L&..."],
                        },
                        "price": {"class": "string", "examples": ["Up to £25K", "Up to £2M", "Up to £50K"]},
                        "rank": {"class": "rank"},
                        "text": {
                            "class": "string",
                            "examples": ["Personal Loans", "Secured Loans", "Debt Consolidation"],
                        },
                        "type": "price",
                    },
                    {
                        "description": {
                            "class": "string",
                            "examples": ["Создай свой неповторимы образ.\nСочетай как нравитс..."],
                        },
                        "extended": {"class": "boolean", "examples": [True]},
                        "is_phone": {"class": "boolean", "examples": [True]},
                        "link": {
                            "class": "string",
                            "examples": ["http://www.adidas.ru/zhenschiny?cm_mmc=AdieSEM_Goo..."],
                        },
                        "rank": {"class": "rank"},
                        "referral_link": {
                            "class": "string",
                            "examples": ["https://www.google.com.vn/aclk?sa=l&ai=DChcSEwj-1t..."],
                        },
                        "text": {
                            "class": "string",
                            "examples": ["adidas® для женщин", "Samsung Deals & Offers", "Samsung Offers & Deals"],
                        },
                        "type": "site_link",
                    },
                ],
                "global_rank": {"class": "rank"},
                "has_install_button": {"class": "boolean", "examples": [True]},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_alt": {
                    "class": "string",
                    "examples": ["Image from vistaprint.com", "makemytrip.com से मिली इमेज", "होटल की इमेज"],
                },
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "link": {"class": "string", "examples": ["https://www.adidas.ru/"]},
                "phone": {"class": "string", "examples": ["8 (800) 250-77-53", "(866) 735-2490", "(866) 973-5355"]},
                "rank": {"class": "rank"},
                "referral_link": {
                    "class": "string",
                    "examples": ["https://www.googleadservices.com/pagead/aclk?sa=L&..."],
                },
                "title": {"class": "string", "examples": ["Официальный магазин adidas® | Новая коллекция на с..."]},
            }
        ],
        "bottom_ads": [
            {
                "description": {
                    "class": "string",
                    "examples": ["Redesign Your Bath in Days. Hassle-Free, Guarantee..."],
                },
                "display_link": {
                    "class": "string",
                    "examples": ["www.remodelnation.com/", "www.believeloans.com/", "www.loan.co.uk/homeowner/loan"],
                },
                "extensions": [
                    {
                        "description": {
                            "class": "string",
                            "examples": ["Sizes 0-20", "Sizes 5-10", "Tested & Warrantied"],
                        },
                        "link": {
                            "class": "string",
                            "examples": ["https://www.google.co.uk/aclk?sa=l&ai=DChcSEwjuof7..."],
                        },
                        "price": {"class": "string", "examples": ["From $14.00", "From $7.00", "From $12.00"]},
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["Luxe Dresses", "Killer Tops", "On Point Rompers"]},
                        "type": "price",
                    },
                    {
                        "description": {
                            "class": "string",
                            "examples": [
                                "$6.12 - Color, Front and Back",
                                "￥3,000 - 2人用／5日分",
                                "￥4,500 - 3人用／5日分",
                            ],
                        },
                        "extended": {"class": "boolean", "examples": [True]},
                        "is_phone": {"class": "boolean", "examples": [True]},
                        "link": {
                            "class": "string",
                            "examples": [
                                "https://www.bizay.com/en-us/promo",
                                "https://www.googleadservices.com/pagead/aclk?sa=L&...",
                            ],
                        },
                        "rank": {"class": "rank"},
                        "text": {"class": "string", "examples": ["Special Offers", "Book Now", "Book for Tomorrow"]},
                        "type": "site_link",
                    },
                ],
                "global_rank": {"class": "rank"},
                "link": {
                    "class": "string",
                    "examples": [
                        "https://remodelnation.com/",
                        "https://www.believeloans.com/",
                        "https://www.loan.co.uk/loans-uk-1/",
                    ],
                },
                "phone": {"class": "string", "examples": ["(833) 750-0124", "(888) 229-2423", "+44 20 3666 1840"]},
                "rank": {"class": "rank"},
                "referral_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/aclk?sa=l&ai=DChcSEwink5_Q6..."],
                },
                "title": {"class": "string", "examples": ["Bathtub Replacement Experts - Clean & Serene Bath ..."]},
            }
        ],
        "top_pla": [
            {
                "description": {
                    "class": "string",
                    "examples": ["Nordstrom has all the hottest sneakers, from athle..."],
                },
                "display_link": {"class": "string", "examples": ["shop.nordstrom.com", "www.dsw.com", "www.lyst.com"]},
                "extensions": [{"class": "string", "examples": ["Free shipping", "Free delivery", "Was £25.97"]}],
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/webp;base64,UklGRnAXAABXRUJQVlA4IGQXAAD..."]},
                "image_alt": {
                    "class": "string",
                    "examples": ["Image of Samsung Galaxy A72 Smartphone, Display In..."],
                },
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/webp;base64,UklGRnAXAABXRUJQVlA4IGQXAAD..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn1.gstatic.com/shopping?q=tbn:..."],
                },
                "link": {"class": "string", "examples": ["https://www.google.com/search?tbm=shop&q=apple"]},
                "offers": [
                    {
                        "image": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/shopping?q=tbn:..."],
                        },
                        "image_alt": {
                            "class": "string",
                            "examples": ["Women's Nike Air Force 1 '07 Sneaker, Size 7.5 M -..."],
                        },
                        "image_url": {
                            "class": "string",
                            "examples": ["https://encrypted-tbn0.gstatic.com/shopping?q=tbn:..."],
                        },
                        "rating": {"class": "number", "examples": [4.7, 4.6, 4.2]},
                        "referral_link": {
                            "class": "string",
                            "examples": ["https://www.googleadservices.com/pagead/aclk?sa=L&..."],
                        },
                        "reviews_cnt": {"class": "number", "examples": [372, 417, 58]},
                        "title": {
                            "class": "string",
                            "examples": ["Women's Nike Air Force 1 '07 Sneaker, Size 7.5 M -..."],
                        },
                    }
                ],
                "old_price": {"class": "string", "examples": ["Was $35", "Was $22", "$830"]},
                "price": {"class": "string", "examples": ["€390.00", "€499.90", "€221.90"]},
                "rank": {"class": "rank"},
                "rating": {"class": "number", "examples": [4.7, 4.2, 4.5]},
                "referral_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/aclk?sa=L&ai=DChcSEwjy8O26o..."],
                },
                "return_policy": {
                    "class": "string",
                    "examples": ["For most items:90-day return policy", "For most items: 30-day return policy"],
                },
                "reviews_cnt": {"class": "number", "examples": [327, 711, 3]},
                "reviews_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/shopping/product/1298200703..."],
                },
                "shipping": {
                    "class": "string",
                    "examples": ["Free shipping", "Free shipping, no tax", "Kostenloser Versand"],
                },
                "shop": {"class": "string", "examples": ["Amazon.it", "Samsung Shop", "TrenDevice"]},
                "summary": {
                    "class": "string",
                    "examples": ["Free Shipping & Returns", "Shop UO Sneakers", "Shop Women's Footwear"],
                },
                "thumbnail": {
                    "class": "string",
                    "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIUA..."],
                },
                "title": {"class": "string", "examples": ["Samsung Galaxy A72 Smartphone, Display Infinity-O ..."]},
                "view_all": {"class": "boolean", "examples": [True]},
            }
        ],
        "bottom_pla": [
            {
                "extensions": [{"class": "string", "examples": ["Was $19.99", "Was $2,293.20", "Free shipping"]}],
                "global_rank": {"class": "rank"},
                "has_link": {"class": "boolean", "examples": [False]},
                "image": {"class": "string", "examples": ["https://encrypted-tbn3.gstatic.com/shopping?q=tbn:..."]},
                "image_alt": {
                    "class": "string",
                    "examples": ["Image of Dell Inspiron 14 Laptop w/ 11th gen Intel..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn3.gstatic.com/shopping?q=tbn:..."],
                },
                "link": {"class": "string", "examples": ["https://www.google.com/search?gl=us&q=Dell+Inspiro..."]},
                "price": {"class": "string", "examples": ["$11.99", "$826.20", "$6.99"]},
                "rank": {"class": "rank"},
                "rating": {"class": "number", "examples": [4, 3.9, 4.2]},
                "referral_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/aclk?sa=l&ai=DChcSEwjU4aDxr..."],
                },
                "reviews_cnt": {"class": "number", "examples": [354, 1000, 3000]},
                "shipping": {"class": "string", "examples": ["Free shipping"]},
                "shop": {
                    "class": "string",
                    "examples": ["360 Health Services", "WeShieldDirect.com", "Medicus Health"],
                },
                "thumbnail": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn0.gstatic.com/shopping?q=tbn:..."],
                },
                "title": {
                    "class": "string",
                    "examples": [
                        "iHealth Antigen Rapid Test",
                        "カジュアル 漫画 Tシャツ, L",
                        "もう洋服で悩まない! 服を着るならこんなふうに 実践編",
                    ],
                },
            }
        ],
        "jackpot_pla": [
            {
                "features": [
                    {
                        "class": "string",
                        "examples": ["Dell Inspiron 15 3000 Laptop - w/ 11th gen Intel C...", "Space Gray", "64 GB"],
                    }
                ],
                "global_rank": {"class": "rank"},
                "has_image": {"class": "boolean", "examples": [False]},
                "image": {"class": "string", "examples": ["https://encrypted-tbn2.gstatic.com/shopping?q=tbn:..."]},
                "image_alt": {"class": "string", "examples": ['Изображение товара "Сыр Bonfesto Кремчиз 70% 500г"']},
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHkA..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://encrypted-tbn2.gstatic.com/shopping?q=tbn:..."],
                },
                "link": {"class": "string", "examples": ["https://www.tsum.ru/catalog/kedy-4061/tekstilnye_k..."]},
                "offers": [{"class": "string", "examples": ["For 24 months", "Free shipping", "No tax"]}],
                "old_price": {"class": "string", "examples": ["17 €", "22 €", "$65"]},
                "price": {"class": "string", "examples": ["RUB 10,990", "RUB 19,768", "RUB 22,046"]},
                "rank": {"class": "rank"},
                "rating": {"class": "number", "examples": [4.8, 3.8]},
                "referral_link": {
                    "class": "string",
                    "examples": ["https://www.googleadservices.com/pagead/aclk?sa=L&..."],
                },
                "return_policy": {
                    "class": "string",
                    "examples": [
                        "30-day returns",
                        "For most items:30-day return policy",
                        "45-day returns (most items)",
                    ],
                },
                "reviews_cnt": {"class": "number", "examples": [88, 86, 195]},
                "reviews_link": {
                    "class": "string",
                    "examples": ["https://www.google.com/shopping/product/5255061832..."],
                },
                "shipping": {
                    "class": "string",
                    "examples": ["Free shipping", "Livraison gratuite", "+ 3,48 € de frais de port"],
                },
                "shop": {"class": "string", "examples": ["ЦУМ", "farfetch.com", "adidas.ru"]},
                "thumbnail": {
                    "class": "string",
                    "examples": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHkA..."],
                },
                "title": {"class": "string", "examples": ["Текстильные кроссовки NMD R1 adidas Originals Черн..."]},
                "unit_price": {"class": "string", "examples": ["0,02 €/1ct", "0,01 €/1ct", "0,13 €/1ct"]},
                "view_all": {"class": "boolean", "examples": [True]},
            }
        ],
        "spelling": {
            "auto_corrected_link": {
                "class": "string",
                "examples": ["https://www.google.com/search?hl=en&q=adidas&spell..."],
            },
            "auto_corrected_text": {
                "class": "string",
                "examples": ["adidas", "BJ's Wholesale club 02072", "why like that"],
            },
            "auto_included_link": {
                "class": "string",
                "examples": ["https://www.google.com/search?gl=us&hl=en&q=hello+..."],
            },
            "auto_included_text": {"class": "string", "examples": ["hello world", "http header maximum length"]},
            "ignored_words": {"class": "string", "examples": ['"AND"']},
            "original_empty": {"class": "boolean", "examples": [True]},
            "original_link": {
                "class": "string",
                "examples": ["https://www.google.com/search?hl=en&q=addidas&nfpr..."],
            },
            "original_text": {"class": "string", "examples": ["addidas", "helo world", "http header max length"]},
            "suggested_link": {
                "class": "string",
                "examples": ["https://www.google.com/search?newwindow=1&q=adidas..."],
            },
            "suggested_text": {
                "class": "string",
                "examples": [
                    "adidas",
                    '("It easily removes tough weeds and smooths out")',
                    "toyota tire replacement dallas",
                ],
            },
        },
        "navigation_tabs": [
            {
                "global_rank": {"class": "rank"},
                "is_active": {"class": "boolean", "examples": [True, False]},
                "is_primary": {"class": "boolean", "examples": [True, False]},
                "link": {"class": "string", "examples": ["https://www.google.com/#wptab=s:0-Un5dYlllUWgwAOiV..."]},
                "rank": {"class": "rank"},
                "title": {"class": "string", "examples": ["Overview", "Locations", "Products"]},
            }
        ],
        "local_services_ads": {
            "items": [
                {
                    "category": {"class": "string", "examples": ["real estate agent", "plumber", "electrician"]},
                    "extensions": [
                        {
                            "text": {
                                "class": "string",
                                "examples": ["11 years in business", "Open 24/7", "6 years in business"],
                            }
                        }
                    ],
                    "global_rank": {"class": "rank"},
                    "guaranteed_badge": {"class": "boolean", "examples": [True]},
                    "image": {
                        "class": "string",
                        "examples": ["https://lh3.googleusercontent.com/qR306n35C1UXCVMJ..."],
                    },
                    "image_alt": {"class": "string", "examples": ["provider-photo"]},
                    "image_url": {
                        "class": "string",
                        "examples": ["https://lh3.googleusercontent.com/qR306n35C1UXCVMJ..."],
                    },
                    "link": {"class": "string", "examples": ["https://www.google.com/search?gsas=1&q=alpharetta,..."]},
                    "phone": {"class": "string", "examples": ["(510) 455-5542", "(707) 203-8121", "(415) 888-4534"]},
                    "rank": {"class": "rank"},
                    "rating": {"class": "number", "examples": [5, 4.5, 3.5]},
                    "reviews_cnt": {"class": "number", "examples": [28, 2, 15]},
                    "title": {
                        "class": "string",
                        "examples": [
                            "The Justin Landis Group",
                            "Alberto Vasquez - AV Home Experts with Keller Will...",
                        ],
                    },
                }
            ],
            "screened_badge": {"class": "boolean", "examples": [True]},
            "title": {
                "class": "string",
                "examples": ["Real estate agents nearby", "Over 20 providers nearby", "See Real Estate Agents"],
            },
            "view_more_link": {
                "class": "string",
                "examples": ["https://www.google.com/search?q=alpharetta,+ga+rea..."],
            },
            "view_more_link_title": {"class": "string", "examples": ["More real estate agents"]},
        },
        "html": {"class": "string", "examples": ['<!DOCTYPE html><html itemscope="" itemtype="http:/...']},
        "hotel_ads": [
            {
                "global_rank": {"class": "rank"},
                "image": {"class": "string", "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."]},
                "image_alt": {"class": "string", "examples": ["होटल की इमेज"]},
                "image_base64": {
                    "class": "string",
                    "examples": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."],
                },
                "image_url": {
                    "class": "string",
                    "examples": ["https://lh6.googleusercontent.com/proxy/vgDDsSP3lu..."],
                },
                "link": {"class": "string", "examples": ["https://www.makemytrip.com/hotels/hotel-listing/?t..."]},
                "price": {"class": "string", "examples": ["₹5,017", "₹4,063", "₹1,596"]},
                "rank": {"class": "rank"},
                "rating": {"class": "number", "examples": [4.1, 4, 3.4]},
                "referral_link": {
                    "class": "string",
                    "examples": ["https://www.google.co.in/aclk?sa=l&ai=CB4RLRCa1ZMi..."],
                },
                "reviews_cnt": {"class": "number", "examples": [7600, 5800, 494]},
                "source": {"class": "string", "examples": ["MakeMyTrip.com", "FabHotels", "Clicktrip.com"]},
                "title": {"class": "string", "examples": ["लेमन ट्री होटल"]},
            }
        ],
        "navigation_filters": [
            {
                "global_rank": {"class": "rank"},
                "has_popup": {"class": "boolean", "examples": [False, True]},
                "is_active": {"class": "boolean", "examples": [False, True]},
                "popup_items": [
                    {
                        "is_active": {"class": "boolean", "examples": [False, True]},
                        "title": {"class": "string", "examples": ["Shows", "Movies", "Shows and movies"]},
                    }
                ],
                "rank": {"class": "rank"},
                "title": {"class": "string", "examples": ["Past 3 days", "Full-time", "Work from home"]},
            }
        ],
    },
}
