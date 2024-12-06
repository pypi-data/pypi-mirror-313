from .constants import MINUS, numerals

def lezgiToNum(lezgiNum: str) -> int:
    if not isinstance(lezgiNum, str):
        raise TypeError('Provided value is not a string')
    isNegative = lezgiNum.startswith(MINUS)
    if isNegative:
        lezgiNum = lezgiNum.replace(MINUS, '', 1).strip()
    else:
        lezgiNum = lezgiNum.strip()
    lezgiNumeralArray = lezgiNum.split(' ')
    
    if len(lezgiNumeralArray) == 1:
        # Handle simple mapped numbers e.g. 'виш', 'кьвед' etc.
        numeral = lezgiNumeralArray[0]
        if numeral in numerals:
            numeral_data = numerals[numeral]
            if numeral_data.get('requiresNext', False):
                allowed_next = numeral_data.get('allowedNext', {})
                min_str = allowed_next.get('minStr', 'сад')
                raise ValueError(
                    f"Provided value '{numeral}' requires a next value e.g. '{min_str}'"
                )
            value = numeral_data['value']
            return -value if isNegative else value
        else:
            raise ValueError(f"Provided value is not a valid Lezgi numeral: '{numeral}'")
    else:
        # Handle multi-numeral numbers e.g. 'вишни кьвед', 'кьве миллионни сад' etc.
        mappedNumeralArray = []
        for numeral in lezgiNumeralArray:
            if numeral in numerals:
                mappedNumeralArray.append(numerals[numeral])
            else:
                raise ValueError(f"Provided value is not a valid Lezgi numeral: '{numeral}'")
        
        mappedNumeralsChunks = [mappedNumeralArray[0]['value']]
        if len(mappedNumeralArray) > 1:
            for i in range(1, len(mappedNumeralArray)):
                previous = mappedNumeralArray[i - 1]
                curr = mappedNumeralArray[i]
                prev_numeral = lezgiNumeralArray[i - 1]
                curr_numeral = lezgiNumeralArray[i]

                if 'allowedNext' in previous:
                    allowed_next = previous['allowedNext']
                    if not (allowed_next['min'] <= curr['value'] <= allowed_next['max']):
                        raise ValueError(
                            f"In the provided value '{lezgiNum}' should be a number between "
                            f"'{allowed_next['min']}' and '{allowed_next['max']}' after "
                            f"'{prev_numeral}', but '{curr_numeral}' was provided which equals "
                            f"to '{curr['value']}'"
                        )
                if curr.get('requiresNext', False) and i == len(mappedNumeralArray) - 1:
                    raise ValueError(
                        f"Provided value '{lezgiNum}' requires a next value, but none was provided"
                    )
                if previous['value'] > curr['value']:
                    if mappedNumeralsChunks[-1] < 1000:
                        # Combine values less than 1000
                        mappedNumeralsChunks[-1] += curr['value']
                    else:
                        # Do not combine for values >= 1000
                        mappedNumeralsChunks.append(curr['value'])
                elif previous['value'] < curr['value']:
                    # Multiply when the current value is greater
                    mappedNumeralsChunks[-1] *= curr['value']
                else:
                    # Equal values (unlikely but included for completeness)
                    mappedNumeralsChunks.append(curr['value'])
        result = sum(mappedNumeralsChunks)
        return -result if isNegative else result

# Example usage:
# print(lezgiToNum('кьве агъзурни къанни кьуд'))  # Output: 2024

# Test cases:
# print(lezgiToNum('кьве'))  # Raises ValueError
# print(lezgiToNum('кьве сад'))  # Raises ValueError
# print(lezgiToNum('агъзурни миллион'))  # Raises ValueError
