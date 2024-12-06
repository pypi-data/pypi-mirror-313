million = 1e6  # 10^6
billion = 1e9  # 10^9
trillion = 1e12  # 10^12
quadrillion = 1e15  # 10^15
quintillion = 1e18  # 10^18
sextillion = 1e21  # 10^21
septillion = 1e24  # 10^24
octillion = 1e27  # 10^27
nonillion = 1e30  # 10^30

atomic = {
    0: 'нул',
    1: 'сад',
    2: 'кьвед',
    3: 'пуд',
    4: 'кьуд',
    5: 'вад',
    6: 'ругуд',
    7: 'ирид',
    8: 'муьжуьд',
    9: 'кIуьд',
    10: 'цIуд',
    20: 'къад',
    40: 'яхцIур',
    100: 'виш',         # 10^2
    1000: 'агъзур',     # 10^3
    million: 'миллион',  # 10^6
    billion: 'миллиард',  # 10^9
    trillion: 'триллион',  # 10^12
    quadrillion: 'квадриллион',  # 10^15
    quintillion: 'квинтиллион',  # 10^18
    sextillion: 'секстиллион',  # 10^21
    septillion: 'септиллион',  # 10^24
    octillion: 'октиллион',  # 10^27
    nonillion: 'нониллион',  # 10^30
}

MINUS = 'минус'

allowedFromHundred = {'minStr': 'виш', 'min': 100, 'max': float('inf')}
allowedFromThousand = {'minStr': 'агъзур', 'min': 1000, 'max': float('inf')}

numerals = {
    'нул': {'value': 0, 'requiresNext': False},
    'сад': {'value': 1, 'requiresNext': False},
    'кьвед': {'value': 2, 'requiresNext': False},
    'кьве': {'value': 2, 'requiresNext': True, 'allowedNext': allowedFromHundred},
    'пуд': {'value': 3, 'requiresNext': False, 'allowedNext': allowedFromHundred},
    'кьуд': {'value': 4, 'requiresNext': False, 'allowedNext': allowedFromHundred},
    'вад': {'value': 5, 'requiresNext': False, 'allowedNext': allowedFromHundred},
    'ругуд': {'value': 6, 'requiresNext': False, 'allowedNext': allowedFromHundred},
    'ирид': {'value': 7, 'requiresNext': False, 'allowedNext': allowedFromHundred},
    'муьжуьд': {'value': 8, 'requiresNext': False, 'allowedNext': allowedFromHundred},
    'кIуьд': {'value': 9, 'requiresNext': False, 'allowedNext': allowedFromHundred},
    'цIуд': {'value': 10, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIусад': {'value': 11, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIикьвед': {'value': 12, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIипуд': {'value': 13, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIикьуд': {'value': 14, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIувад': {'value': 15, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIуругуд': {'value': 16, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIерид': {'value': 17, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIемуьжуьд': {'value': 18, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'цIекIуьд': {'value': 19, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'къад': {'value': 20, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'къанни': {
        'value': 20,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': 19}
    },
    'яхцIур': {'value': 40, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'яхцIурни': {
        'value': 40,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': 19}
    },
    'пудкъад': {'value': 60, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'пудкъанни': {
        'value': 60,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': 19}
    },
    'кьудкъад': {'value': 80, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'кьудкъанни': {
        'value': 80,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': 19}
    },
    'виш': {'value': 100, 'requiresNext': False, 'allowedNext': allowedFromThousand},
    'вишни': {
        'value': 100,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': 99}
    },
    'агъзур': {'value': 1000, 'requiresNext': False},
    'агъзурни': {
        'value': 1000,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': 1000}
    },
    'миллион': {'value': million, 'requiresNext': False},
    'миллионни': {
        'value': million,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': million}
    },
    'миллиард': {'value': billion, 'requiresNext': False},
    'миллиардни': {
        'value': billion,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': billion}
    },
    'триллион': {'value': trillion, 'requiresNext': False},
    'триллионни': {
        'value': trillion,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': trillion}
    },
    'квадриллион': {'value': quadrillion, 'requiresNext': False},
    'квадриллионни': {
        'value': quadrillion,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': quadrillion}
    },
    'квинтиллион': {'value': quintillion, 'requiresNext': False},
    'квинтиллионни': {
        'value': quintillion,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': quintillion}
    },
    'секстиллион': {'value': sextillion, 'requiresNext': False},
    'секстиллионни': {
        'value': sextillion,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': sextillion}
    },
    'септиллион': {'value': septillion, 'requiresNext': False},
    'септиллионни': {
        'value': septillion,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': septillion}
    },
    'октиллион': {'value': octillion, 'requiresNext': False},
    'октиллионни': {
        'value': octillion,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': octillion}
    },
    'нониллион': {'value': nonillion, 'requiresNext': False},
    'нониллионни': {
        'value': nonillion,
        'requiresNext': True,
        'allowedNext': {'minStr': 'сад', 'min': 1, 'max': nonillion}
    },
}
