from random import choice, shuffle

chart_types = ['Bar chart', 'Single line graph', 'Multiple line graph', 'Dot plot', 'Pie chart', 'Word cloud'] 
civility_scales = ["public import", "neutral voice", "shouting", "humor", "respect for others", "divisiveness", "appeals to anger and fear", "information gathering", "sources and evidence"]
keywords = ['abortion', 'Barack Obama', 'climate change', 'Democrats', 'education', 'federal debt', 'government spending', 'health care', 'inflation', 'jobs', 'karate', 'Mitt Romney']
time_frames = ['in the last year', 'in the last nine months', 'in the last 60 days', 'in the last 30 days', 'since 2000', 'since 2004', 'since 2008', 'since 2010', 'since January', 'between July 2008 and November 2008', 'since the midterm elections']

media_types = ['blogs', 'newspaper articles', 'newspaper editorials', 'talk radio', 'TV news', 'news magazines', 'campaign ads', 'campaign emails']

categories = ['political party', 'state', 'media type', 'issue area']

###############################################################################

generators = []

def generator(function):
    generators.append(function)
    return function

@generator
@generator
def scale_about_keywords_over_time():
    return 'Line graph (single) : Trends in ' + choice(civility_scales) + ' about ' + choice(keywords) + ' ' + choice(time_frames)

@generator
@generator
def scales_about_keyword_over_time():
    shuffle(civility_scales)
    return 'Line graph (multiple) : Trends in ' + civility_scales[0] + ', ' + civility_scales[1] + ', and ' + civility_scales[2] + ' about ' + choice(keywords) + ' ' + choice(time_frames)

@generator
def scale_by_category():
    return 'Bar graph : Use of ' + choice(civility_scales) + ' by ' + choice(categories)

@generator
def scale_in_media_type_about_keyword():
    return 'Bar graph : Use of ' + choice(civility_scales) + ' in ' + choice(media_types) + ' about ' + choice(keywords)

@generator
def word_cloud():
    return 'Word cloud : Words associated (and disassociated) with ' + choice(civility_scales)

@generator
@generator
def word_cloud_about_topic():
    return 'Word cloud : Words associated (and disassociated) with ' + choice(civility_scales) + ' about ' + choice(keywords)


###############################################################################
def generate_graph_titles(n=100):
    for i in range(n):
        print choice(generators)()

generate_graph_titles()
