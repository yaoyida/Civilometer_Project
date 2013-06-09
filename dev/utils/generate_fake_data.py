import json, datetime, random, time
from bson.objectid import ObjectId
from pymongo.errors import InvalidId

class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def random_date():
    dt = datetime.datetime(
        random.choice(range(2000,2012)),
        random.choice(range(1,13)),
        random.choice(range(1,29)),
        random.choice(range(1,25)),
        random.choice(range(1,61)),
        random.choice(range(1,61))
    )

    return dt
    return {"$date" : long(time.mktime(dt.timetuple()))}

urls = ["adisgruntledrepublican.com", "americablog.com", "americanthinker.com", "nlt.ashbrook.org", "barkbarkwoofwoof.com", "batr.org", "baumbach.org", "biased-bbc.blogspot.com", "biopsychiatry.com", "sabbah.biz", "blacks4barack.com", "consul-at-arms2.blogspot.com", "jailhouselawyersblog.blogspot.com", "wolfhowling.blogspot.com", "biased-bbc.blogspot.com", "smalltalkwitht.blogspot.com", "socraticgadfly.blogspot.com", "kennethdfranks.blogspot.com", "afrikaner-genocide-achives.blogspot.com", "grayee.blogspot.com", "traditional-catholic-prayers.blogspot.com", "daisysdeadair.blogspot.com", "saberpoint.blogspot.com", "shimronletters.blogspot.com", "blogfromonhigh.blogspot.com", "historyscoper-islamwatch.blogspot.com", "metaphysicalperegrine.blogspot.com", "bookerrising.net", "bookninja.com", "bradblog.com", "pithy.butnowyouknow.net", "cagle.com", "cahsrblog.com", "cato.org", "pjmedia.com", "wn.com", "whitehouse12.com", "likethedew.com", "ansionnachfionn.com", "townhall.com", "fullmetalpatriotblog.com", "wattsupwiththat.com", "biggovernment.com", "dailycaller.com", "pajamasmedia.com", "nofrakkingconsensus.com", "michellemalkin.com", "order-order.com", "donklephant.com", "scaredmonkeys.com", "politicalbyline.com", "organizationsandmarkets.com", "veracityvoice.com", "ethicsforadversaries.com", "frontpagemag.com", "offthekuff.com", "majorityinms.com", "definingthenarrative.com", "reflectionsofarationalrepublican.com", "noplaceforsheep.com", "endtimestoday.com", "superfrenchie.com", "21stcenturywire.com", "thedisorderofthings.com", "catholiclane.com", "twawki.com", "footnotes2plato.com", "vox-nova.com", "cifwatch.com", "underthemountainbunker.com", "lettingfreedomring.com", "howtheuniversityworks.com", "indiancountrytodaymedianetwork.com", "volokh.com", "crimefilenews.com", "topics.dailycaller.com", "dailykos.com", "dumpbachmann.com", "economist.com", "eureferendum.blogspot.com", "everydaycitizen.com", "feministlawprofessors.com", "firstthings.com", "foreignpolicy.com", "gaypatriot.net", "gnxp.com", "healingcombattrauma.com", "blog.heritage.org", "hoover.org", "humanevents.com", "irishhistorypodcast.ie", "williambowles.info", "infowars.com", "intellectualconservative.com", "israeli-occupation.org", "jihadwatch.org", "jpost.com", "kennethdurden.com", "blog.kentforliberty.com", "mars2earth.blogspot.com", "usconstitution.meetup.com", "politics.meetup.com", "liberty.meetup.com", "freedom.meetup.com", "localpolitics.meetup.com", "tea-party.meetup.com", "conservative.meetup.com", "libertarian.meetup.com", "mypetjawa.mu.nu", "ace.mu.nu", "nationaljournal.com", "global.nationalreview.com", "nationalreview.com", "alternativenewsreport.net", "dprogram.net", "butnowyouknow.net", "photonicportal.net", "nzclimatescience.net", "nannystateliberationfront.net", "andrewroman.net", "yourdaddy.net", "chicagoboyz.net", "video.nytimes.com", "opednews.com", "constitutionclub.org", "thecampofthesaints.org", "thinkprogress.org", "politicalvelcraft.org", "jonathanturley.org", "platypus1917.org", "intelnews.org", "bellacaledonia.org.uk", "kafila.org", "stephaniemcmillan.org", "rmiglobal.org", "ansnuclearcafe.org", "spectator.org", "orlytaitzesq.com", "patheos.com", "peter-ould.net", "politico.com", "politicususa.com", "politikditto.com", "powerlineblog.com", "prolifeblogs.com", "qando.net", "rawstory.com", "realclearpolitics.com", "realzionistnews.com", "redstate.com", "riehlworldview.com", "ronpaul.com", "rumormillnews.com", "saberpoint.blogspot.com", "sajaforum.org", "salon.com", "samefacts.com", "sarah-palin-2012.blogspot.com", "singularity2050.com", "slate.com", "socialistparty.org.uk", "state.gov", "stoptheaclu.com", "store.tcpress.com", "blogs.telegraph.co.uk", "theatlantic.com", "theblaze.com", "thecenterlane.com", "andrewsullivan.thedailybeast.com", "thedissidentfrogman.com", "thegatewaypundit.com", "thejidf.org", "thelibertypapers.org", "themaritimesentry.com", "thenation.com", "theodoresworld.net", "theotherrussia.org", "think-israel.org", "thinking-catholic-strategic-center.com", "thunderrun.us", "rodonline.typepad.com", "atlasshrugs2000.typepad.com", "marcmasferrer.typepad.com", "weaselzippers.us", "vanguardnewsnetwork.com", "washingtonmonthly.com", "washingtontimes.com", "weeklystandard.com", "whitehouse.gov", "wolfhowling.blogspot.com", "maboulette.wordpress.com", "sadbastards.wordpress.com", "thisblksistaspage.wordpress.com", "danieljmitchell.wordpress.com", "loveandgarbage.wordpress.com", "robertlindsay.wordpress.com", "openparachute.wordpress.com", "elmsprogressivemedia.wordpress.com", "msrb.wordpress.com", "thedaleygator.wordpress.com", "fma7.wordpress.com", "sentient.wordsof.org"]

codebooks = ['facts, sources, and evidence', 'objective tone', 'public import', 'infotainment', 'emotional reactions', 'divisiveness', 'respect for others', 'emotional appeals', 'divisiveness', 'respect for others']

fixture_file = '../../cvm_project/fixtures/test-1/cvm_document.json'

J = json.load(file(fixture_file, 'r'))
for j in J:
    j["metadata"]["timestamp"] = random_date()
    j["metadata"]["source"] = random.choice(urls)
    
    j["civility_labels"] = dict([ (c, {"score": random.choice(range(10))}) for c in codebooks])
    #print j["civility_labels"]

file('cvm_document.json', 'w').write(json.dumps(J, indent=2, cls=MongoEncoder))
