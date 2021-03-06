#
# This command builds a set of search URLs to use for stress testing the full
# stack.  Invoke with a base URL and number of search URLs to generate.
#
# An example using `palb` as a benchmarker with this management command.  This
# will run a benchmark with 10 concurrent users making 1000 requests, each to a
# distinct random but valid search URL, so as to miss the cache often:
#
#   python manage.py search_benchmark http://example.com 1000 | xargs palb -c 10 -n 1000
#
import sys
import urllib
import random
from django.db.models.fields import TextField
from django.core.management.base import BaseCommand
import haystack

from afg.models import DiaryEntry
from afg.search_indexes import DiaryEntryIndex

class Command(BaseCommand):
    args = '<base url> <number of urls>'
    help = """Construct a list of random URLs to use for benchmarking the server."""

    def handle(self, *args, **kwargs):
        try:
            base_url = args[0]
            number_of_urls = int(args[1])
        except IndexError:
            print self.args
            print self.help
            sys.exit()

        options = {}

        for facet in DiaryEntryIndex.search_facet_display:
            field = DiaryEntryIndex.fields[facet]
            name = field.index_fieldname.rstrip('_')
            if name == 'total_casualties':
                #XXX domain specific....
                nums = range(0, 191)
                options[name + '__lte'] = nums
                options[name + '__gte'] = nums
            elif isinstance(field, haystack.fields.DateTimeField):
                dates = list(d.strftime("%Y-%m-%d") for d in DiaryEntry.objects.all().dates(name, 'day'))
                options[name + '__lte'] = dates
                options[name + '__gte'] = dates
            elif isinstance(field, haystack.fields.IntegerField):
                ints = range(DiaryEntry.objects.order_by(name).values(name)[0][name],
                             DiaryEntry.objects.order_by('-' + name).values(name)[0][name])
                options[name + '__lte'] = ints
                options[name + '__gte'] = ints
            elif isinstance(field, haystack.fields.CharField):
                if not isinstance(DiaryEntry._meta.get_field(name), TextField):
                    options[name] = [a[name] for a in DiaryEntry.objects.all().values(name).distinct()]
            else:
                pass

        #XXX domain specific,  phrase search
        in_db_phrases = []
        texts = [a['summary'] for a in DiaryEntry.objects.all().order_by('?').values('summary')[0:number_of_urls]]
        for text in texts:
            in_db_phrases += text.split()
        options['q'] = random.sample(RANDOM_WORDS, min(len(RANDOM_WORDS), number_of_urls))
        options['q'] += random.sample(in_db_phrases, number_of_urls)

        urls = []
        for i in range(number_of_urls):
            # Choose a number of facets to search on.
            num_facets = max(1, int(random.expovariate(1)))
            facets = []
            # 50% of the time, search for text.
            if random.random() > 0.5:
                facets.append('q')
            facets += random.sample(options.keys(), num_facets - len(facets))
            params = dict((facet, random.choice(options[facet])) for facet in facets)
            urls.append(base_url + '?' + urllib.urlencode(params))
        for url in urls:
            print url


RANDOM_WORDS = ["sever",
"fillet",
"Conodonta",
"H2NC6H4COOC2H5",
"pina colada",
"large order",
"Front door",
"pruritic",
"in straitened circumstances",
"cash out",
"Smelting",
"fireproof",
"chittagong",
"why",
"Rural deanery",
"girondin",
"genus Callorhinus",
"bouncier",
"Cock",
"Betelgeux",
"clipping",
"dissatisfy",
"tendril",
"Mezquita",
"Aloft",
"Oligarchic",
"load factor",
"derby",
"Broch'e",
"psychotic",
"Death bell",
"hejaz, el",
"prospect",
"legislation",
"one-man",
"foiling",
"Cobaea scandens",
"tokology",
"white mullein",
"Phyodactylus gecko",
"Paragnath",
"To clear for action",
"sekt",
"goddamn",
"Sulphanilic",
"naturist",
"Agaricaceae",
"Boundaries",
"reflexivity",
"big-bang theory",
"Fillet",
"dry fly",
"Listera cordata",
"violence",
"whelm",
"Reata",
"Clematis tangutica",
"turgescence",
"souslik",
"Indian banyan",
"recapitalize",
"Lubrical",
"sharif",
"persiflage",
"symphonic",
"Eolipile",
"thackeray, william makepeace",
"viral infection",
"gordin",
"Bewetted",
"entropy",
"Superstratum",
"Mohammedan calendar",
"Pyrotechnian",
"happy medium",
"combinative vs noncombinative",
"Dammara",
"Atrabiliary capsule",
"autoharp",
"sikhs",
"3f7",
"group practice",
"distributor",
"Mouthpiece",
"dovishness",
"Sulkies",
"Telharmony",
"self-enrichment",
"anointer",
"assignat",
"Astoned",
"obstinately",
"presuppose",
"mo08",
"Kingdom of Norway",
"unsown",
"Satirist",
"barn owl",
"Trajan",
"cloud seeder",
"willy-nilly",
"yard goods",
"Interreceive",
"Eleocharis acicularis",
"wasp waist",
"give suck",
"Frobisher",
"gouda",
"Mart",
"Charcot",
"vent",
"herba impia",
"cohort",
"Parental",
"invisible",
"stressful",
"barathea",
"capital of Kazakhstan",
"iconoclast",
"bound",
"Drawled",
"proboscis monkey",
"sabre",
"snafu",
"arabicize",
"ghiberti, lorenzo",
"buzzer",
"cayenne pepper",
"out to lunch",
"parenthetical",
"Belgian franc",
"party liner",
"Toxication",
"thermonuclear",
"verst",
"tore",
"antiperspirant",
"procurable",
"nephron",
"Snow partridge",
"reprocess",
"Carriage horse",
"seeable",
"mach number",
"Labrador tea",
"backcountry",
"door-to-door",
"misapprehension",
"weather strip",
"hammond",
"billionth",
"gulp",
"crazed",
"bmx",
"loony bin",
"dry-bulb thermometer",
"Helminthologic",
"lindsay",
"family Struthionidae",
"Brazenly",
"nonrapid eye movement",
"Enlink",
"untenanted",
"wizard of the north",
"nibelung",
"Mad",
"Queensland tulipwood",
"large-print",
"antianxiety agent",
"mioses",
"shmegegge",
"spencer",
"solid-state physics",
"addison, joseph",
"nonflammable",
"currently",
"formlessness",
"Upupa",
"hunted",
"coffin",
"Seethe",
"respiratory acidosis",
"hagfishes",
"demonetization",
"Mullus surmulletus",
"Gloved",
"Ostia",
"syndic",
"Flitter",
"hair dye",
"monometer",
"anatomise",
"i16",
"augustus",
"pectoralis major",
"whit leather",
"Prudential",
"Carbuncular",
"6mi1",
"Hobble-skirted",
"Spicated",
"Venture",
"soft-soaper",
"paton, john gibson",
"large-leaved cucumber tree",
"sleaze",
"meteoroidal",
"Aristarchus",
"Mekong River",
"6az7",
"Mustelus",
"deadeye",
"Underpossessor",
"Curtain lecture",
"echinococcosis",
"lithiate",
"quizzical",
"Convalescing",
"Lieutenancy",
"ought",
"family Tetraodontidae",
"Branchial clefts",
"geochemistry",
"act of God",
"zulu",
"carl",
"erlenmeyer",
"5nd0",
"soapbox",
"welted thistle",
"Chaldaic",
"hermeneutic",
"Ventriculite",
"muezzin",
"Animal",
"anglo-catholic",
"bonesetter",
"Safety touchdown",
"improvement",
"rhizome",
"pollyannaish",
"unease",
"unbidden",
"Witlessness",
"think-tank",
"Halaka",
"doorstep",
"aden",
"constructor",
"uvulae",
"lying",
"Fire bug",
"high-concept",
"metabolic acidosis",
"roseola",
"gunite",
"alkali poisoning",
"Spent",
"lotos",
"kerb",
"germano-",
"capsize",
"sketchy",
"negation",
"cowling",
"newsletter",
"Tur",
"corrosive sublimate",
"million instructions per second",
"Congolese",
"handclasp",
"blida",
"Biggest",
"sheath knife",
"cinnabar chanterelle",
"iodinated protein",
"heretical",
"Taurus",
"inscrutable",
"pigeon-breasted",
"Cassia javonica",
"52nd",
"walking ticket",
"Essence",
"vih",
"4al4",
"Helmless",
"7ii3",
"jokester",
"well-lighted",
"underwood",
"non-acceptance",
"mythicize",
"daphnia",
"sexual",
"equilibristic",
"stratford de redcliffe, sir stafford canning, first viscount",
"crevice",
"30",
"caesarean section",
"Complementary",
"bowery",
"Levied",
"Lamblike",
"pemmican",
"robot",
"Waste",
"pentameter",
"precentor",
"forcible",
"underproduction",
"trellis",
"flt. sgt.",
"Entune",
"43ne",
"clickety-clack",
"Piston rod",
"Blue ruin",
"Etropus rimosus",
"To sit at meat",
"Mickey Finn",
"self-willed",
"malacca cane",
"7pn5",
"rock hyrax",
"mimeograph",
"quaere",
"Asilus",
"butter stamp",
"narcissistic personality",
"drinking chocolate",
"laxity",
"initiator",
"dew",
"optimal",
"sigmoid colon",
"droshky",
"Walling wax",
"Bewhore",
"curcuma",
"postpositive",
"Coachdog",
"Romanian",
"Glover's stitch",
"superiority complex",
"unpropitious",
"Demersion",
"buttonlike",
"expense",
"Towy",
"Mebles",
"Yerba mansa",
"54ny",
"skillet fish",
"Curtail dog",
"decapitate",
"wiggle nail",
"muscarine",
"waviness",
"driftwood",
"Opportunely",
"new albany",
"down-at-the-heel",
"Abacus harmonicus",
"run out",
"Tribonyx Mortierii",
"Predeterminable",
"Nuphar",
"creusot, le",
"Pyroscope",
"place aux dames",
"oilier",
"earthstar",
"Prink",
"spenser, edmund",
"Malled",
"-way",
"vaguely",
"walloons",
"Parus ater",
"desdemona",
"azote",
"Vagous",
"cuttlefish",
"saturable",
"beholden",
"nimbus",
"stand watch",
"3z1",
"scamp",
"Retreating",
"g-spot",
"pious",
"Biblical Latin",
"Saintliness",
"tillamook bay",
"5ok8",
"goer",
"sum total",
"Mercilessly",
"Jumpweld",
"extinguish",
"Poterium Sanguisorba",
"Barong",
"aver`ro&euml;s",
"haggiss",
"On",
"outstripped",
"0ne3",
"blackwell, alexander",
"amazedly",
"radio",
"d'urfey, tom",
"To make up",
"predisposition",
"squirreltail grass",
"basset",
"Policed",
"Dissembling",
"finsen",
"Uncorrigible",
"Approbate",
"outside clinch",
"zanu",
"Doff",
"adiz",
"Labdanum",
"shipper",
"Mesohippus",
"A atricapillus",
"Whanghee",
"grindal, edmund",
"Pineal",
"Radiatiform",
"Jean Francois Champollion",
"beta iron",
"unquestioningly",
"Vitrificate",
"rushee",
"informant",
"Cote",
"senior citizen",
"order Actinomyxidia",
"nylghau",
"ambient",
"viva",
"topcoat",
"Tilt roof",
"subaudition",
"Piano",
"Staminode",
"subvocalise",
"station break",
"recalcitrance",
"Fiber optics",
"cinderella",
"unoxygenated",
"Triangular compasses",
"anxiousness",
"Verbatim et literatim",
"Diabolism",
"Cauterization",
"Podia",
"Deposited",
"84ts",
"countryman",
"Coltish",
"lcc",
"anticipate",
"taciturn",
"substandard",
"tarn",
"uncinate",
"prosthesis",
"longboard",
"American cheese",
"Muss",
"Lorelei",
"diphtheroid",
"m",
"invincibly",
"Symbol",
"Horned horse",
"Slovenian",
"Guevina avellana",
"Indian file",
"quetzal",
"Cycloidal engine",
"Charles Wesley",
"boxing glove",
"Peise",
"blue streak",
"read/write memory",
"Nelumbo nucifera",
"fragonard, jean honore",
]
