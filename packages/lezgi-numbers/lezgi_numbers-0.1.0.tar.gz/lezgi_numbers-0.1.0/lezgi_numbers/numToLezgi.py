from .constants import (
    atomic,
    million,
    billion,
    trillion,
    quadrillion,
    quintillion,
    sextillion,
    septillion,
    octillion,
    nonillion,
    MINUS,
)

def separateNumberIntoUnits(n: int) -> list:
    if n == 0:
        return [0]
    arr = []
    i = 1
    while n > 0:
        arr.insert(0, (n % 10) * i)
        n = n // 10
        i *= 10
    result = groupNumberUnitsToLezgiRange(arr)
    return result

ranges = [
    {'start': nonillion, 'end': octillion},   # nonillion to octillion
    {'start': octillion, 'end': septillion},   # octillion to septillion
    {'start': septillion, 'end': sextillion},  # septillion to sextillion
    {'start': sextillion, 'end': quintillion}, # sextillion to quintillion
    {'start': quadrillion, 'end': quintillion},# quadrillion to quintillion
    {'start': trillion, 'end': quadrillion},   # trillion to quadrillion
    {'start': billion, 'end': trillion},       # billion to trillion
    {'start': million, 'end': billion},        # million to billion
    {'start': 1000, 'end': million},           # thousand to million
]

def groupNumberUnitsToLezgiRange(arr: list) -> list:
    result = []
    for range_ in ranges:
        sum_ = sum(num for num in arr if num >= range_['start'] and num < range_['end'])
        if sum_ != 0:
            result.append(sum_)
        # Filter out the numbers that were added to sum
        arr = [num for num in arr if num < range_['start'] or num >= range_['end']]
    # Concatenate the remaining numbers to the result
    result.extend(arr)
    return result

def getTenPlusBase(num: int) -> list:
    if num < 10 or num >= 20:
        raise ValueError('Invalid number')
    if num == 10:
        return [atomic[10]]
    base10 = atomic[10][:-2]
    if num in (11, 15, 16):
        return [base10 + 'у']
    elif num < 15:
        return [base10 + 'и']
    return [base10 + 'е']

def getTwentyPlusBase(num: int) -> list:
    return [atomic[20]] if num == 20 else ['къанни']

def getThirtyPlusBase(num: int) -> list:
    return getTwentyPlusBase(num) + getTenPlusBase(num - 20)

def getFourtyPlusBase(num: int) -> list:
    return [atomic[40]] if num == 40 else [atomic[40], 'ни']

def getFiftyPlusBase(num: int) -> list:
    return getFourtyPlusBase(num) + getTenPlusBase(num - 40)

def getSixtyPlusBase(num: int) -> list:
    return [atomic[3], atomic[20]] if num == 60 else [atomic[3]] + getTwentyPlusBase(num)

def getSeventyPlusBase(num: int) -> list:
    return getSixtyPlusBase(61) + getTenPlusBase(num - 60)

def getEightyPlusBase(num: int) -> list:
    return [atomic[4], atomic[20]] if num == 80 else [atomic[4]] + getTwentyPlusBase(num)

def getNinetyPlusBase(num: int) -> list:
    return getEightyPlusBase(81) + getTenPlusBase(num - 80)

def getHundredPlusBase(num: int) -> list:
    return [atomic[100]] if num % 100 == 0 else [atomic[100], 'ни']

def getHundredPlusNumCount(numCount: int) -> list:
    if numCount in atomic:
        return [atomic[numCount][:-1]] if numCount == 2 else [atomic[numCount]]
    return None

def getBetweenHundredAndThousand(num: int, followUpNumber: int) -> list:
    hundredsCount = num // 100
    hundredsCountInLezgi = getHundredPlusNumCount(hundredsCount)
    return hundredsCountInLezgi + [' '] + getHundredPlusBase(num + followUpNumber)

def getThousandPlusBase(num: int) -> list:
    return [atomic[1000]] if num % 1000 == 0 else [atomic[1000], 'ни']

def getBetweenThousandAndMillion(num: int, followUpNumber: int) -> list:
    thousandsCount = num // 1000
    thousandsCountInLezgi = getHundredPlusNumCount(thousandsCount) or getCompound(thousandsCount)
    return thousandsCountInLezgi + [' '] + getThousandPlusBase(num + followUpNumber)

def getMillionPlusBase(num: int) -> list:
    return [atomic[million]] if num % million == 0 else [atomic[million], 'ни']

def getBetweenMillionAndBillion(num: int, followUpNumber: int) -> list:
    millionsCount = num // million
    millionsCountInLezgi = getHundredPlusNumCount(millionsCount) or getCompound(millionsCount)
    return millionsCountInLezgi + [' '] + getMillionPlusBase(num + followUpNumber)

def getBillionPlusBase(num: int) -> list:
    return [atomic[billion]] if num % billion == 0 else [atomic[billion], 'ни']

def getBetweenBillionAndTrillion(num: int, followUpNumber: int) -> list:
    billionsCount = num // billion
    billionsCountInLezgi = getHundredPlusNumCount(billionsCount) or getCompound(billionsCount)
    return billionsCountInLezgi + [' '] + getBillionPlusBase(num + followUpNumber)

def getTrillionPlusBase(num: int) -> list:
    return [atomic[trillion]] if num % trillion == 0 else [atomic[trillion], 'ни']

def getBetweenTrillionAndQuadrillion(num: int, followUpNumber: int) -> list:
    trillionsCount = num // trillion
    trillionsCountInLezgi = getHundredPlusNumCount(trillionsCount) or getCompound(trillionsCount)
    return trillionsCountInLezgi + [' '] + getTrillionPlusBase(num + followUpNumber)

def getQuadrillionPlusBase(num: int) -> list:
    return [atomic[quadrillion]] if num % quadrillion == 0 else [atomic[quadrillion], 'ни']

def getBetweenQuadrillionAndQuintillion(num: int, followUpNumber: int) -> list:
    quadrillionsCount = num // quadrillion
    quadrillionsCountInLezgi = getHundredPlusNumCount(quadrillionsCount) or getCompound(quadrillionsCount)
    return quadrillionsCountInLezgi + [' '] + getQuadrillionPlusBase(num + followUpNumber)

def getQuintillionPlusBase(num: int) -> list:
    return [atomic[quintillion]] if num % quintillion == 0 else [atomic[quintillion], 'ни']

def getBetweenQuintillionAndSextillion(num: int, followUpNumber: int) -> list:
    quintillionsCount = num // quintillion
    quintillionsCountInLezgi = getHundredPlusNumCount(quintillionsCount) or getCompound(quintillionsCount)
    return quintillionsCountInLezgi + [' '] + getQuintillionPlusBase(num + followUpNumber)

def getSextillionPlusBase(num: int) -> list:
    return [atomic[sextillion]] if num % sextillion == 0 else [atomic[sextillion], 'ни']

def getBetweenSextillionAndSeptillion(num: int, followUpNumber: int) -> list:
    sextillionsCount = num // sextillion
    sextillionsCountInLezgi = getHundredPlusNumCount(sextillionsCount) or getCompound(sextillionsCount)
    return sextillionsCountInLezgi + [' '] + getSextillionPlusBase(num + followUpNumber)

def getSeptillionPlusBase(num: int) -> list:
    return [atomic[septillion]] if num % septillion == 0 else [atomic[septillion], 'ни']

def getBetweenSeptillionAndOctillion(num: int, followUpNumber: int) -> list:
    septillionsCount = num // septillion
    septillionsCountInLezgi = getHundredPlusNumCount(septillionsCount) or getCompound(septillionsCount)
    return septillionsCountInLezgi + [' '] + getSeptillionPlusBase(num + followUpNumber)

def getOctillionPlusBase(num: int) -> list:
    return [atomic[octillion]] if num % octillion == 0 else [atomic[octillion], 'ни']

def getBetweenOctillionAndNonillion(num: int, followUpNumber: int) -> list:
    octillionsCount = num // octillion
    octillionsCountInLezgi = getHundredPlusNumCount(octillionsCount) or getCompound(octillionsCount)
    return octillionsCountInLezgi + [' '] + getOctillionPlusBase(num + followUpNumber)

def getNonillionPlusBase(num: int) -> list:
    return [atomic[nonillion]] if num % nonillion == 0 else [atomic[nonillion], 'ни']

def getCompound(num: int) -> list:
    units = separateNumberIntoUnits(num)
    result = []
    for i, unit in enumerate(units):
        followUpNumber = sum(units[i + 1:])
        if unit == 0 and len(units) > 1:
            continue
        if i > 0 and unit == 7 and units[i - 1] in [10, 30, 50, 70, 90]:
            result.append(atomic[7][1:])
            continue
        if unit == 10:
            result.extend(getTenPlusBase(unit + followUpNumber))
        elif unit == 20:
            result.extend(getTwentyPlusBase(unit + followUpNumber))
        elif unit == 30:
            result.extend(getThirtyPlusBase(unit + followUpNumber))
        elif unit == 40:
            result.extend(getFourtyPlusBase(unit + followUpNumber))
        elif unit == 50:
            result.extend(getFiftyPlusBase(unit + followUpNumber))
        elif unit == 60:
            result.extend(getSixtyPlusBase(unit + followUpNumber))
        elif unit == 70:
            result.extend(getSeventyPlusBase(unit + followUpNumber))
        elif unit == 80:
            result.extend(getEightyPlusBase(unit + followUpNumber))
        elif unit == 90:
            result.extend(getNinetyPlusBase(unit + followUpNumber))
        elif unit == 100:
            result.extend(getHundredPlusBase(unit + followUpNumber))
        elif 100 < unit < 1000:
            result.extend(getBetweenHundredAndThousand(unit, followUpNumber))
        elif unit == 1000:
            result.extend(getThousandPlusBase(unit + followUpNumber))
        elif 1000 < unit < million:
            result.extend(getBetweenThousandAndMillion(unit, followUpNumber))
        elif unit == million:
            result.extend(getMillionPlusBase(unit + followUpNumber))
        elif million < unit < billion:
            result.extend(getBetweenMillionAndBillion(unit, followUpNumber))
        elif unit == billion:
            result.extend(getBillionPlusBase(unit + followUpNumber))
        elif billion < unit < trillion:
            result.extend(getBetweenBillionAndTrillion(unit, followUpNumber))
        elif unit == trillion:
            result.extend(getTrillionPlusBase(unit + followUpNumber))
        elif trillion < unit < quadrillion:
            result.extend(getBetweenTrillionAndQuadrillion(unit, followUpNumber))
        elif unit == quadrillion:
            result.extend(getQuadrillionPlusBase(unit + followUpNumber))
        elif quadrillion < unit < quintillion:
            result.extend(getBetweenQuadrillionAndQuintillion(unit, followUpNumber))
        elif unit == quintillion:
            result.extend(getQuintillionPlusBase(unit + followUpNumber))
        elif quintillion < unit < sextillion:
            result.extend(getBetweenQuintillionAndSextillion(unit, followUpNumber))
        elif unit == sextillion:
            result.extend(getSextillionPlusBase(unit + followUpNumber))
        elif sextillion < unit < septillion:
            result.extend(getBetweenSextillionAndSeptillion(unit, followUpNumber))
        elif unit == septillion:
            result.extend(getSeptillionPlusBase(unit + followUpNumber))
        elif septillion < unit < octillion:
            result.extend(getBetweenSeptillionAndOctillion(unit, followUpNumber))
        elif unit == octillion:
            result.extend(getOctillionPlusBase(unit + followUpNumber))
        elif octillion < unit < nonillion:
            result.extend(getBetweenOctillionAndNonillion(unit, followUpNumber))
        elif unit == nonillion:
            result.extend(getNonillionPlusBase(unit + followUpNumber))
        else:
            result.append(atomic.get(unit, str(unit)))
    return result

def getAtomicOrCompound(num: int) -> list:
    if num in atomic:
        return [atomic[num]]
    else:
        return getCompound(num)

def numToLezgiArray(num: int) -> list:
    if not isinstance(num, int):
        raise ValueError('Provided number is not an integer. Currently only integers are supported!')
    isNegative = num < 0
    num = abs(num)
    result = getAtomicOrCompound(num)
    result = [word for word in result if word != '']
    temp = []
    for word in result:
        if word.endswith('ни'):
            temp.extend([word, ' '])
        else:
            temp.append(word)
    result = temp
    if isNegative:
        return [MINUS, ' '] + result
    else:
        return result

def numToLezgi(num: int) -> str:
    resultArray = numToLezgiArray(num)
    return ''.join(resultArray).replace('  ', ' ').strip()


# print(numToLezgi(1986))  # Output: 'агъзурни кIуьд вишни кьудкъанни ругуд'