import logging


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)

rock_genres = {
    'Post-Hardcore': {
        'Future Palace': {
            'Decarabia': 'https://t.me/RockReplay/6'
        },
        'Our Promise': {
            'FiftyFive': 'https://t.me/RockReplay/16'
        },
        'DeadRabbits': {
            'Oxygen': 'https://t.me/RockReplay/92'
        },
        'Memphis May Fire': {
            'Necessary Evil': 'https://t.me/RockReplay/106',
            'Shapeshifter': 'https://t.me/RockReplay/339'
        },
        'Annisokay': {
            'Get Your Sh!t Together': 'https://t.me/RockReplay/107',
            'feat. Antitype - The Devil And The Saint': 'https://t.me/RockReplay/300'
        },
        'Our Mirage': {
            'Right Now': 'https://t.me/RockReplay/144'
        },
        'Wildways': {
            'Сакура': 'https://t.me/RockReplay/193'
        },
        'Sleep Theory': {
            'Paralyzed': 'https://t.me/RockReplay/223'
        },
        'Antitype': {
            'feat. Annisokay - The Devil And The Saint': 'https://t.me/RockReplay/223'
        },
        'Sludge Mother': {
            'No Temple': 'https://t.me/RockReplay/327'
        },
        'Indecent Behavior': {
            'Chaos': 'https://t.me/RockReplay/351'
        },
        'The Hara': {
            'The System': 'https://t.me/RockReplay/354'
        }
    },
    'Melodic Death Metal': {
        'The Black Dahlia Murder': {
            "Mammoth's Hand": 'https://t.me/RockReplay/17'
        },
        'I Am Your God': {
            'Til Death Do Us Part': 'https://t.me/RockReplay/8'
        },
        'Rising Insane': {
            'Monster': 'https://t.me/RockReplay/37'
        },
        'Equilibrium': {
            'Gnosis': 'https://t.me/RockReplay/71'
        },
        'Dark Tranquillity': {
            'Wayward Eyes': 'https://t.me/RockReplay/94'
        },
        'The Crown': {
            'Churchburner': 'https://t.me/RockReplay/121'
        },
        'Amaranthe': {
            'Interference': 'https://t.me/RockReplay/151',
            'Burn With Me': 'https://t.me/RockReplay/317'
        },
        'Arch Enemy': {
            'Liars & Thieves': 'https://t.me/RockReplay/168'
        },
        'The Halo Effect': {
            'Detonate': 'https://t.me/RockReplay/207',
            'March Of The Unheard': 'https://t.me/RockReplay/274'
        },
        'Cabal': {
            'Still Cursed': 'https://t.me/RockReplay/216'
        },
        'League Of Distortion': {
            'Crucify Me': 'https://t.me/RockReplay/228'
        },
        'As I Lay Dying': {
            'Whitewashed Tomb': 'https://t.me/RockReplay/174',
            'Parallels': 'https://t.me/RockReplay/272'
        },
        'Lankester Merrin': {
            'High Plains Drifter': 'https://t.me/RockReplay/326'
        }

    },
    'Alternative Rock': {
        'Blacktoothed': {
            'Get Me Down': 'https://t.me/RockReplay/39',
            'Antidote': 'https://t.me/RockReplay/373'
        },
        'Ekoh': {
            'The Sound Of Falling': 'https://t.me/RockReplay/41',
            'Drag Me From Hell': 'https://t.me/RockReplay/150',
            'Save Me (feat. Zero 9:36)': 'https://t.me/RockReplay/161'
        },
        'Bad Omens x POPPY': {
            'V.A.N.': 'https://t.me/RockReplay/57'
        },
        'Skillet': {
            'Unpopular': 'https://t.me/RockReplay/57',
            'Ash In The Wind': 'https://t.me/RockReplay/162',
            'Hero': 'https://t.me/RockReplay/342'
        },
        'Live': {
            'Lady Bhang (She Got Me Rollin ) ft. Dean DeLeo': 'https://t.me/RockReplay/86'
        },
        'Нуки': {
            'Спичка': 'https://t.me/RockReplay/108'
        },
        'Storm Orchestra': {
            'Drummer': 'https://t.me/RockReplay/132'
        },
        'Chaosbay': {
            'Eye For An Eye': 'https://t.me/RockReplay/148'
        },
        'Anberlin': {
            'High Stakes': 'https://t.me/RockReplay/156'
        },
        'Nothing,nowhere.': {
            'The heart mechanic': 'https://t.me/RockReplay/182'
        },
        'Wake Up Hate': {
            'Spite': 'https://t.me/RockReplay/206'
        },
        'Hollywood Undead': {
            'Hollywood Forever': 'https://t.me/RockReplay/220'
        },
        'Rock Privet': {
            'Король и Шут / Skillet - Кукла Колдуна': 'https://t.me/RockReplay/221'
        },
        'Prime Circle': {
            'What We Got': 'https://t.me/RockReplay/270'
        },
        'Неил Шери': {
            'По Кусочкам': 'https://t.me/RockReplay/277'
        },
        'The Cure': {
            'I Can Never Say Goodbye': 'https://t.me/RockReplay/299'
        },
        'Hinder': {
            'Everything Is A Cult': 'https://t.me/RockReplay/357'
        },
        'The Haunt': {
            'Going Under': 'https://t.me/RockReplay/374'
        }
    },
    'Hard Rock': {
        'Malvada': {
            'Down The Walls': 'https://t.me/RockReplay/7'
        },
        'Fate': {
            'Around the Sun': 'https://t.me/RockReplay/9'
        },
        'Radioactive': {
            'Sentimental': 'https://t.me/RockReplay/18'
        },
        'Cortez': {
            'Gimme Danger': 'https://t.me/RockReplay/70'
        },
        'Blue Heron': {
            'We Breathe Darkness': 'https://t.me/RockReplay/74'
        },
        'Daughtry': {
            'The Dam': 'https://t.me/RockReplay/186'
        },
        'Massive Wagon': {
            'Sleep Forever': 'https://t.me/RockReplay/217'
        },
        'Queen': {
            'We Will Rock You': 'https://t.me/RockReplay/232',
            'Keep Yourself Alive': 'https://t.me/RockReplay/252'
        },
        'Mr. Big': {
            'Shine': 'https://t.me/RockReplay/237'
        },
        'The Who': {
            'Who Are You': 'https://t.me/RockReplay/238'
        },
        "Guns N'Roses": {
            'You Could Be Mine': 'https://t.me/RockReplay/243'
        },
        'Dominum': {
            'One Of Us': 'https://t.me/RockReplay/303'
        },
        'Thundermother': {
            'Dead Or Alive': 'https://t.me/RockReplay/336'
        },
        'Electric Temple': {
            'Big Black Hole': 'https://t.me/RockReplay/341'
        }
    },
    'Trash Metal': {
        'Flotsam And Jetsam': {
            'A New Kind Of Hero': 'https://t.me/RockReplay/10'
        },
        'Demiser': {
            'Hell is Full of Fire': 'https://t.me/RockReplay/59'
        },
        'Tortured Demon': {
            'Nothing Left To Say': 'https://t.me/RockReplay/236'
        },
        'Dread': {
            'Hide': 'https://t.me/RockReplay/269'
        },
        'Exodus': {
            'Beating Around The Bush': 'https://t.me/RockReplay/287'
        }
    },
    'Progressive Metal': {
        'Gojira': {
            'Ah! Ça Ira': 'https://t.me/RockReplay/13'
        },
        'Oceans Ate Alaska': {
            'Onsra': 'https://t.me/RockReplay/23'
        },
        'Accvsed': {
            'Avoider': 'https://t.me/RockReplay/28',
            'Never Enough': 'https://t.me/RockReplay/165'
        },
        'Unprocessed': {
            'Dark, Silent and Complete': 'https://t.me/RockReplay/191'
        },
        'Vola': {
            'Bleed Out': 'https://t.me/RockReplay/268'
        },
        'Queensrÿche': {
            'Fallout': 'https://t.me/RockReplay/284'
        },
        'Vanitas': {
            'Wait & See': 'https://t.me/RockReplay/337'
        },
        'Pathogenic': {
            'Mass Grave Memory': 'https://t.me/RockReplay/348'
        },
        'Arimea': {
            'Orchid Street': 'https://t.me/RockReplay/368'
        },
        'Beriedir': {
            'Neon': 'https://t.me/RockReplay/369'
        },
        'Connections': {
            'Facade': 'https://t.me/RockReplay/379'
        }
    },
    'Industrial Metal': {
        'Turmion Kätilöt': {
            'Yksi Jumalista': 'https://t.me/RockReplay/98'
        },
        'OOMPH!': {
            'Soll das Liebe sein?': 'https://t.me/RockReplay/146'
        },
        'Anoxia': {
            'Relinquish The Quiet': 'https://t.me/RockReplay/257'
        },
        'Eisbrecher': {
            'Everything is wunderbar': 'https://t.me/RockReplay/370'
        }
    },
    'Heavy Metal': {
        'Serious Black': {
            'Silent Angel': 'https://t.me/RockReplay/40'
        },
        'Arctis': {
            "I'll Give You Hell": 'https://t.me/RockReplay/97'
        },
        'Dance with the Dead': {
            'Neon Cross': 'https://t.me/RockReplay/197',
            'Wolf Pack': 'https://t.me/RockReplay/224'
        },
        'Motörhead': {
            'Enter Sandman': 'https://t.me/RockReplay/231',
            'Ace Of Spades': 'https://t.me/RockReplay/293'
        },
        'Saltatio Mortis vs. Eskimo Callboy': {
            'Hypa Hypa': 'https://t.me/RockReplay/241'
        },
        'Helloween': {
            'Are You Metal': 'https://t.me/RockReplay/244'
        },
        'Firewind': {
            'Fallen Angel': 'https://t.me/RockReplay/251'
        },
        'Deathless Legacy': {
            'Absolution': 'https://t.me/RockReplay/259'
        },
        'Nightmare': {
            'Saviours of the Damned': 'https://t.me/RockReplay/262'
        },
        'Bagira': {
            'Пришел. Увидел. Победил': 'https://t.me/RockReplay/263'
        },
        'Burning Witches': {
            'The Spell Of The Skull': 'https://t.me/RockReplay/288'
        },
        'Crown Magnetar': {
            'Decapitation Ritual': 'https://t.me/RockReplay/290'
        },
        'Marty Friedman': {
            'Song for an Eternal Child': 'https://t.me/RockReplay/292'
        },
        'TEЯRATOMORF': {
            'Игра в прятки': 'https://t.me/RockReplay/295'
        },
        'Воля и Разум': {
            'Грешник или Святой': 'https://t.me/RockReplay/305'
        },
        'Ignitor': {
            'Shattered Crosses': 'https://t.me/RockReplay/331'
        },
        'All For Metal': {
            'All For Metal Is Coming To Town': 'https://t.me/RockReplay/364'
        },
        'Ozzy Osbourne': {
            'Dreamer': 'https://t.me/RockReplay/378'
        }
    },
    'Shoegaze': {
        'Amira Elfeky': {
            'Save Yourself': 'https://t.me/RockReplay/20'
        },
        'Zetra': {
            'Suffer Eternally': 'https://t.me/RockReplay/47'
        }
    },
    'Grindcore': {
        'Nails': {
            'Every Bridge Burning': 'https://t.me/RockReplay/22'
        },
    },
    'Metalcore': {
        'Villian of the Story': {
            'My Own Way': 'https://t.me/RockReplay/24',
            'Face It': 'https://t.me/RockReplay/355'
        },
        'Oceans': {
            'Parasite': 'https://t.me/RockReplay/25'
        },
        'Bleeding Through': {
            'Our Brand Is Chaos': 'https://t.me/RockReplay/69',
            'Path Of Our Disease': 'https://t.me/RockReplay/376'
        },
        'Set for Tomorrow': {
            'Doom + Gloom': 'https://t.me/RockReplay/76'
        },
        'Falling in Reverse': {
            'Prequel': 'https://t.me/RockReplay/87'
        },
        'Alleviate': {
            'DMNS': 'https://t.me/RockReplay/105'
        },
        'Attack Attack!': {
            'We All Meet Up In The End': 'https://t.me/RockReplay/115'
        },
        'ten56.': {
            'ICU': 'https://t.me/RockReplay/126'
        },
        'Resolve': {
            'Molotov': 'https://t.me/RockReplay/127'
        },
        'Haste The Day': {
            'Burn': 'https://t.me/RockReplay/163'
        },
        'Make Them Suffer': {
            'Mana God': 'https://t.me/RockReplay/175'
        },
        'Underoath': {
            'Survivors Guilt': 'https://t.me/RockReplay/178'
        },
        'Beartooth': {
            '_ATTN._ ': 'https://t.me/RockReplay/199'
        },
        'Further Within': {
            'Static': 'https://t.me/RockReplay/214'
        },
        'Balance Breach': {
            'Come Undone': 'https://t.me/RockReplay/218'
        },
        'The Dark': {
            'Slip Away': 'https://t.me/RockReplay/279'
        },
        'All That Remains': {
            'Forever Cold': 'https://t.me/RockReplay/297'
        },
        'Мегамозг': {
            'Радиация': 'https://t.me/RockReplay/298'
        },
        'If Not For Me': {
            'Say It To My Face': 'https://t.me/RockReplay/307'
        },
        'Butcher Babies': {
            'Sincerity': 'https://t.me/RockReplay/325'
        },
        'Killswitch Engage': {
            'Forever Aligned': 'https://t.me/RockReplay/340'
        },
        'Space Of Variations': {
            'Lies': 'https://t.me/RockReplay/343'
        }
    },
    'Nu Metal': {
        'Vended': {
            'Serenity': 'https://t.me/RockReplay/85'
        },
        'Cane Hill': {
            'Permanence in Sleep': 'https://t.me/RockReplay/122'
        },
        'Chaoseum': {
            'Freakin\' Head': 'https://t.me/RockReplay/141'
        },
        'A Killer\'s Confession': {
            'Voices': 'https://t.me/RockReplay/147'
        },
        'Nathan James': {
            'Misanthrope': 'https://t.me/RockReplay/180'
        },
        'Linkin Park': {
            'One step closer': 'https://t.me/RockReplay/195',
            'Over Each Other': 'https://t.me/RockReplay/317',
            'Two Faced': 'https://t.me/RockReplay/320'
        },
        'Ocean Grove': {
            'SOWHAT1999': 'https://t.me/RockReplay/362'
        },
        'Tori Aster': {
            'Океан наших слез': 'https://t.me/RockReplay/363'
        }
    },
    'Power Metal': {
        'Dragony': {
            'Beyond The Rainbow Bridge': 'https://t.me/RockReplay/32'
        },
        'PowerWolf': {
            "We Don't Wanna Be No Saints": 'https://t.me/RockReplay/35'
        },
        'Dynazty': {
            'Devilry of Ecstasy': 'https://t.me/RockReplay/46',
            'Game of Faces': 'https://t.me/RockReplay/367'
        },
        "Sinner's Blood": {
            'Enemy': 'https://t.me/RockReplay/61'
        },
        'Iotunn': {
            'I Feel the Night': 'https://t.me/RockReplay/114'
        },
        'Aries Descendant': {
            'Aflame the Cold': 'https://t.me/RockReplay/138'
        },
        'Brothers Of Metal': {
            'Fimbulvinter': 'https://t.me/RockReplay/152'
        },
        'Alterium': {
            'Of War and Flames': 'https://t.me/RockReplay/250'
        },
        'Dragonspell': {
            'Феникс': 'https://t.me/RockReplay/261'
        }
    },
    'AOR': {
        'Find Me': {
            'Never Be Alone': 'https://t.me/RockReplay/38'
        },
        'The Night Flight Orchestra': {
            'Shooting Velvet': 'https://t.me/RockReplay/242'
        }
    },
    'Nu Metalcore': {
        'Vicious Rain': {
            'Shadow Dancer': 'https://t.me/RockReplay/42'
        }
    },
    'Alternative Metal': {
        'Defences': {
            'Perish': 'https://t.me/RockReplay/56',
            'Breathe It In': 'https://t.me/RockReplay/171'
        },
        'Phrenia': {
            'You Are Your Own Worst Enemy': 'https://t.me/RockReplay/12'
        },
        'Eyes Like Midnight': {
            'Quicksand': 'https://t.me/RockReplay/14'
        },
        'Emil Bulls': {
            'Warrior of Love feat. Doro': 'https://t.me/RockReplay/30'
        },
        'Tremonti': {
            'Just Too Much': 'https://t.me/RockReplay/19',
            'One More Time': 'https://t.me/RockReplay/239'
        },
        'СЛОТ': {
            'С.М.Г.О': 'https://t.me/RockReplay/26'
        },
        'Serj Tankian': {
            'Justice Will Shine On': 'https://t.me/RockReplay/31'
        },
        'Radio Tapok': {
            'Императрица': 'https://t.me/RockReplay/67',
            'Фрау Чёрная Смерть': 'https://t.me/RockReplay/321'
        },
        'Phoenix Lake': {
            'Serenity': 'https://t.me/RockReplay/96'
        },
        'In This Moment': {
            'Sanctify Me': 'https://t.me/RockReplay/111'
        },
        'InYourFace': {
            'Dale Don Dale feat. Vanity Vercetti': 'https://t.me/RockReplay/145'
        },
        'Amatory': {
            'IXODUS': 'https://t.me/RockReplay/167'
        },
        'Dream State': {
            'Bloom': 'https://t.me/RockReplay/169'
        },
        'No Resolve': {
            'CrossFire': 'https://t.me/RockReplay/157'
        },
        'Islander': {
            'Die Dreaming': 'https://t.me/RockReplay/170'
        },
        'ТЕППО, Drummatix': {
            'Сон Нереид': 'https://t.me/RockReplay/172'
        },
        'Pop Evil': {
            'What Remains': 'https://t.me/RockReplay/176',
            'Death Walk': 'https://t.me/RockReplay/345'
        },
        'Sick Puppies': {
            'Going Places': 'https://t.me/RockReplay/203'
        },
        "Devil's Cut": {
            'Dangerous': 'https://t.me/RockReplay/209'
        },
        'Devilskin': {
            'Unborn': 'https://t.me/RockReplay/291'
        },
        'Loudblood': {
            'Brave Monsters': 'https://t.me/RockReplay/301'
        },
        'Нерыдай!': {
            'Иллюзии': 'https://t.me/RockReplay/304'
        },
        'Bullet For My Valentine': {
            'All These Things I Hate': 'https://t.me/RockReplay/317'
        },
        'Spiritbox': {
            'Perfect Soul': 'https://t.me/RockReplay/335'
        },
        'Three Days Grace': {
            'Mayday': 'https://t.me/RockReplay/347'
        },
        'Smash Into Pieces': {
            'Maze of Fools': 'https://t.me/RockReplay/353'
        },
        'Blackbriar': {
            'Floriography': 'https://t.me/RockReplay/356'
        }
    },
    'Progressive Deathcore': {
        'Distant': {
            'The Undying': 'https://t.me/RockReplay/58'
        }
    },
    'Black Metal': {
        'Primordial': {
            'Nothing New Under the Sun': 'https://t.me/RockReplay/60'
        },
        'SCOUR': {
            'Infusorium': 'https://t.me/RockReplay/334'
        }
    },
    'RapCore': {
        'Fever 333': {
            'Higher Power': 'https://t.me/RockReplay/66',
            'No Hostages': 'https://t.me/RockReplay/82'
        },
        'Eralise': {
            'Enough?': 'https://t.me/RockReplay/225'
        },
        'Twiztid': {
            'dance on my grave': 'https://t.me/RockReplay/338'
        }
    },
    'Black Death Metal': {
        'Burn Down Eden': {
            'Epistrophy': 'https://t.me/RockReplay/75'
        }
    },
    'Industrial Rock': {
        'Marilyn Manson': {
            'Raise The Red Flag': 'https://t.me/RockReplay/95',
            'OAUG': 'https://t.me/RockReplay/346'
        },
        'Love Ghost x Skold': {
            'Nightshade and Cocaine': 'https://t.me/RockReplay/137'
        }
    },
    'Symphonic Metal': {
        'Ad Infinitum': {
            'Surrender': 'https://t.me/RockReplay/131',
            'Follow Me Down': 'https://t.me/RockReplay/173'
        },
        'Cradle of Filth': {
            'Malignant Perfection': 'https://t.me/RockReplay/189'
        },
        'Eleine': {
            'Never Forget': 'https://t.me/RockReplay/190'
        },
        'Epica': {
            'The Ghost In Me': 'https://t.me/RockReplay/226',
            'Arcana': 'https://t.me/RockReplay/312'
        },
        "Leaves' Eyes": {
            'Realm of Dark Waves': 'https://t.me/RockReplay/253'
        },
        "Visions Of Atlantis": {
            'Monsters': 'https://t.me/RockReplay/264'
        },
        'Delain': {
            'The Reaping': 'https://t.me/RockReplay/286'
        },
        'Revengin': {
            'Circle Of Mistakes': 'https://t.me/RockReplay/309'
        },
        "Valkyrie's Fire": {
            'Ride of the Valkyrie': 'https://t.me/RockReplay/311'
        },
        'Aeon Gods': {
            'King Of Gods': 'https://t.me/RockReplay/314'
        },
        'Hamadría': {
            'Valió la pena': 'https://t.me/RockReplay/328'
        },
        'Арктида': {
            'Поезда': 'https://t.me/RockReplay/352'
        }
    },
    'Melodic HardCore': {
        'Eclipse': {
            'All I Want': 'https://t.me/RockReplay/153'
        },
        'The Big Deal': {
            'Like A Fire': 'https://t.me/RockReplay/359'
        }
    },
    'Folk Metal': {
        'Bloodywood': {
            'Nu Delhi': 'https://t.me/RockReplay/184',
            'Machi Bhasad': 'https://t.me/RockReplay/210',
            'Dana Dan': 'https://t.me/RockReplay/210',
            'Gaddaar': 'https://t.me/RockReplay/210',
            'Aaj': 'https://t.me/RockReplay/210'
        },
        'КняZZ': {
            'Сталкер': 'https://t.me/RockReplay/240'
        },
        'Subway To Sally': {
            'Post Mortem': 'https://t.me/RockReplay/294',
            'feat. Warkings - Stahl auf Stahl': 'https://t.me/RockReplay/365'
        },
        'Korpiklaani': {
            'Sauna': 'https://t.me/RockReplay/302'
        },
        'Feuerschwanz': {
            'feat.Lord Of The Lost-Lords Of Fyre': 'https://t.me/RockReplay/313'
        },
        'Lord Of The Lost': {
            'feat.Feuerschwanz-Lords Of Fyre': 'https://t.me/RockReplay/313'
        }
    },
    'Electronic Rock': {
        'The Browning': {
            'Soul Drift': 'https://t.me/RockReplay/204'
        },
        'The Birthday Massacre': {
            'Blue': 'https://t.me/RockReplay/375'
        },
        'Phantom Elite': {
            'Sangre Mala': 'https://t.me/RockReplay/377'
        }
    },
    'Modern Metal': {
        'The Fear': {
            'White Noise': 'https://t.me/RockReplay/227'
        },
        'About Monsters': {
            'Crash and Burn': 'https://t.me/RockReplay/260'
        },
        'Metheora': {
            'Черный снег': 'https://t.me/RockReplay/323'
        },
        'Enemy Inside': {
            'ft. Zak Tell - Fck That Party': 'https://t.me/RockReplay/344'
        },
        'Полина Полякова': {
            'Нас нет': 'https://t.me/RockReplay/360'
        }
    },
    'DeathCore': {
        'Fit For An Autopsy': {
            'Red Horizon': 'https://t.me/RockReplay/229'
        },
        'Molotov Solution': {
            'Devour The Children': 'https://t.me/RockReplay/258',
            'Mortis Imperium': 'https://t.me/RockReplay/350'
        }
    },
    'Punk Rock': {
        'Операция пластелин': {
            'Танцпол ждет своих героев': 'https://t.me/RockReplay/248'
        }
    },
    'Gothic Metal': {
        'Lacrimosa': {
            'Avalon': 'https://t.me/RockReplay/275'
        },
        'Lacrimonia': {
            'Never surrender': 'https://t.me/RockReplay/358'
        }
    },
    'Melodic Heavy Metal': {
        'Matt Guillory': {
            'Middlefield': 'https://t.me/RockReplay/322'
        },
        'The Ferrymen': {
            'Iron Will': 'https://t.me/RockReplay/366'
        }
    }
}


CHANNEL_USERNAME = "@RockReplay"

async def check_subscription(user_id, context):
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        return False

async def send_main_menu(update: Update, image_url: str = None):
    keyboard = [
        [InlineKeyboardButton("Алфавит", callback_data="alphabet")],
        [InlineKeyboardButton("Поджанры", callback_data="genres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if image_url:
        await update.message.reply_photo(photo=image_url, caption='🎶 Привет, рок-энтузиаст! Готов отправиться в увлекательное музыкальное '
            'путешествие? Выбери способ поиска любимых клипов: По алфавиту – если ты знаешь, '
            'с какой буквы начинается твой любимый коллектив! По поджанрам – для тех, '
            'кто хочет исследовать разнообразие рок-музыки! Выбери вариант ниже:', reply_markup=reply_markup)
    else:
        await update.message.reply_text(
            '🎶 Привет, рок-энтузиаст! Готов отправиться в увлекательное музыкальное '
            'путешествие? Выбери способ поиска любимых клипов: По алфавиту – если ты знаешь, '
            'с какой буквы начинается твой любимый коллектив! По поджанрам – для тех, '
            'кто хочет исследовать разнообразие рок-музыки! Выбери вариант ниже:',
            reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    image_url = 'https://logodix.com/logo/580915.png' 
    await send_main_menu(update, image_url=image_url)

async def send_search_options(update: Update):
    keyboard = [
        [InlineKeyboardButton("Алфавит", callback_data="alphabet")],
        [InlineKeyboardButton("Поджанры", callback_data="genres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        'Выбери способ поиска любимых клипов: По алфавиту или по поджанрам.',
        reply_markup=reply_markup)

async def check_subscription_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context)

    query = update.callback_query
    await query.answer()

    if is_subscribed:
        # Кнопка для перехода к поиску
        keyboard = [[InlineKeyboardButton("Перейти к поиску", callback_data="go_to_search")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text="Подписка проверена! Вы можете продолжать.", reply_markup=reply_markup)
    else:
        # Заменяем сообщение о вариантах поиска на сообщение о необходимости подписки
        keyboard = [
            [InlineKeyboardButton("Подписаться", url=f"t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text='Подписка не активна. Пожалуйста, подпишитесь на канал.',
            reply_markup=reply_markup
        )

async def go_to_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_search_options(update)
async def alphabet_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await verify_subscription_and_proceed(update, context, "alphabet")

async def genre_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await verify_subscription_and_proceed(update, context, "genres")

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    image_url = 'https://logodix.com/logo/580915.png' 
    keyboard = [
        [InlineKeyboardButton("Алфавит", callback_data="alphabet")],
        [InlineKeyboardButton("Поджанры", callback_data="genres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_photo(
        photo=image_url,
        caption='🎶 Привет, рок-энтузиаст! Готов отправиться в увлекательное музыкальное '
                'путешествие? \nВыбери способ поиска любимых клипов: По алфавиту – если ты знаешь, '
                'с какой буквы начинается твой любимый коллектив! По поджанрам – для тех, '
                'кто хочет исследовать разнообразие рок-музыки!',
        reply_markup=reply_markup
    )

    await query.message.delete()

async def send_alphabet_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Русский", callback_data="ru_alphabet")],
        [InlineKeyboardButton("Английский", callback_data="en_alphabet")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(
            text='Выберите алфавит:',
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Ошибка при редактировании сообщения: {e}")
        await query.message.reply_text(
            text='Выберите алфавит:',
            reply_markup=reply_markup
        )

async def verify_subscription_and_proceed(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context)
    query = update.callback_query
    try:
        # Попытка ответить на callback_query
        await query.answer()

        if is_subscribed:
            if callback_data == "alphabet":
                await send_alphabet_selection(update, context)
            elif callback_data == "genres":
                await send_genre_selection(update, context)
        else:
            keyboard = [
                [InlineKeyboardButton("Подписаться", url=f"t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            try:
                # Используем edit_message_text для редактирования сообщения вместо повторного ответа на query
                await query.message.edit_text(
                    text='Пожалуйста, подпишитесь на канал и затем нажмите "Проверить подписку".',
                    reply_markup=reply_markup
                )
            except Exception as e:
                logging.error(f"Ошибка при редактировании сообщения: {e}")
                await query.message.reply_text(
                    text='Пожалуйста, подпишитесь на канал и затем нажмите "Проверить подписку".',
                    reply_markup=reply_markup
                )
    except Exception as e:
        logging.error(f"Ошибка при обработке callback_query: {e}")
        # В случае ошибки можно отправить сообщение обратно, например:
        await query.message.reply_text('Произошла ошибка при обработке запроса. Попробуйте снова.')

async def send_genre_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    genres = list(rock_genres.keys())
    keyboard = []
    buttons_per_row = 3 
    for i in range(0, len(genres), buttons_per_row):
        row = [InlineKeyboardButton(genre, callback_data=f"genre_{genre}") for genre in genres[i:i + buttons_per_row]]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(
            text='Выберите поджанр:',
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Ошибка при редактировании сообщения: {e}")
        await query.message.reply_text(
            text='Выберите поджанр:',
            reply_markup=reply_markup
        )

async def russian_alphabet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    letters = 'А В К М Н О П С Т'.split()
    keyboard = []

    for i in range(0, len(letters), 4):
        keyboard.append([InlineKeyboardButton(letter, callback_data=f"ru_{letter}") for letter in letters[i:i + 4]])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text='Выбирай букву, на которую начинается твой любимый коллектив:', reply_markup=reply_markup)

async def english_alphabet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    letters = 'A B C D E F G H I K L M N O P Q R S T U V W'.split()
    keyboard = []

    for i in range(0, len(letters), 4):
        keyboard.append([InlineKeyboardButton(letter, callback_data=f"en_{letter}") for letter in letters[i:i + 4]])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text='Выбирай букву, на которую начинается твой любимый коллектив:', reply_markup=reply_markup)
async def handle_alphabet_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "ru_alphabet":
        await russian_alphabet(update, context) 
    elif query.data == "en_alphabet":
        await english_alphabet(update, context)

async def handle_letter_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    letter = query.data.split('_')[1]
    # Фильтруем группы по первой букве
    bands = [band for genre in rock_genres.values() for band in genre.keys() if band.startswith(letter)]

    if bands:
        keyboard = []
        buttons_per_row = 2
        for i in range(0, len(bands), buttons_per_row):
            row = [InlineKeyboardButton(band, callback_data=band) for band in bands[i:i + buttons_per_row]]
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f'В этом списке – группы, начинающиеся на букву {letter}:\nВыбери свою '
                                           f'любимую команду и давай продолжим наше путешествие!',
                                       reply_markup=reply_markup)
    else:
        keyboard = [[InlineKeyboardButton("Назад", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f'К сожалению, на выбранную букву {letter} пока не добавлено коллективов, но скоро они появятся.',
            reply_markup=reply_markup)

async def band_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    band = query.data
    genre = next(gen for gen in rock_genres if band in rock_genres[gen])
    tracks = rock_genres[genre][band]
    keyboard = []
    buttons_per_row = 3 
    track_items = list(tracks.items())
    for i in range(0, len(track_items), buttons_per_row):
        row = [InlineKeyboardButton(track, url=url) for track, url in track_items[i:i + buttons_per_row]]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    new_text = (f'🎵 Встречай творения группы {band}\nВот список их хитовых видеоклипов, которые '
                 f'точно заставят твое сердце биться в ритме рока. Выбирай трек и погружайся в '
                 f'мир невероятной музыки!')
    if query.message.text != new_text or query.message.reply_markup != reply_markup:
        try:
            await query.edit_message_text(text=new_text, reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Ошибка при редактировании сообщения: {e}")
            await query.message.reply_text(new_text, reply_markup=reply_markup)

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await back_to_menu(update, context)

async def select_genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    genre = query.data.split('_')[1]
    bands = list(rock_genres[genre].keys())

    buttons_per_row = 3
    keyboard = []

    for i in range(0, len(bands), buttons_per_row):
        row = [InlineKeyboardButton(band, callback_data=band) for band in bands[i:i + buttons_per_row]]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Назад к меню выбора вариантов поиска", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=f'🎸 Вот кто готов закрутить тебе голову звуками рока в поджанре {genre}:\n'
                                       f'Выбери свою любимую команду и давай продолжим наше путешествие!',
                                  reply_markup=reply_markup)

def main() -> None:
    app = ApplicationBuilder().token().build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_back, pattern='^back$'))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern='^back$'))
    app.add_handler(CallbackQueryHandler(alphabet_selection, pattern='^alphabet$'))
    app.add_handler(CallbackQueryHandler(genre_selection, pattern='^genres$'))
    app.add_handler(CallbackQueryHandler(check_subscription_handler, pattern='^check_subscription$'))
    app.add_handler(CallbackQueryHandler(select_genre, pattern='^genre_.*$'))
    app.add_handler(CallbackQueryHandler(handle_alphabet_choice, pattern='^(ru_alphabet|en_alphabet)$'))
    app.add_handler(CallbackQueryHandler(band_selection, pattern='|'.join(
        band for bands in rock_genres.values() for band in bands.keys())))
    app.add_handler(CallbackQueryHandler(go_to_search, pattern='^go_to_search$'))
    app.add_handler(CallbackQueryHandler(handle_letter_selection, pattern='^ru_[А-Я]$'))
    app.add_handler(CallbackQueryHandler(handle_letter_selection, pattern='^en_[A-Z]$'))

    app.run_polling()

if __name__ == '__main__':
    main()
