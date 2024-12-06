import unittest
from lezgi_numbers import lezgiToNum

class TestLezgiToNum(unittest.TestCase):
    def test_correct_values(self):
        correct_values = [
            ('агъзурни кIуьд вишни кьудкъанни ругуд', 1986),
            ('агъзурни кIуьд вишни цIерид', 1917),
            ('агъзурни кIуьд вишни къанни цIерид', 1937),
            ('кьуд миллиардни вишни цIипуд миллионни кьве вишни пудкъанни ирид агъзурни вад вишни яхцIурни цIерид', 4113267557),
            ('кьве агъзурни къанни кьуд', 2024),
            ('виш агъзур', 100000),
            ('кьве миллион', 2000000),
            ('кьве миллионни сад', 2000001),
            ('ирид виш', 700),
            ('агъзурни сад', 1001),
            ('вишни кьвед', 102),
            ('вишни яхцIурни цIерид агъзур', 157000),
            ('кIуьд квадриллионни ирид триллионни вишни кьудкъанни цIекIуьд миллиардни кьве вишни яхцIурни цIикьуд миллионни ирид вишни яхцIур агъзурни кIуьд вишни кьудкъанни цIусад', 9007199254740991),
            ('минус вишни кьвед', -102),
            ('минус кIуьд квадриллионни ирид триллионни вишни кьудкъанни цIекIуьд миллиардни кьве вишни яхцIурни цIикьуд миллионни ирид вишни яхцIур агъзурни кIуьд вишни кьудкъанни цIусад', -9007199254740991),
            ('цIуд агъзурни вишни къанни сад', 10121),
            ('кьве вишни къанни сад', 221),
        ]

        for input_str, expected in correct_values:
            with self.subTest(input_str=input_str):
                result = lezgiToNum(input_str)
                self.assertEqual(result, expected)

    def test_missing_next_value(self):
        missing_next_values = [
            ('кьве', "Provided value 'кьве' requires a next value e.g. 'виш'"),
            ('вишни', "Provided value 'вишни' requires a next value e.g. 'сад'"),
        ]

        for input_str, expected_error in missing_next_values:
            with self.subTest(input_str=input_str):
                with self.assertRaises(ValueError) as context:
                    lezgiToNum(input_str)
                self.assertEqual(str(context.exception), expected_error)

    def test_incorrect_next_value(self):
        incorrect_next_values = [
            (
                'кьве сад',
                "In the provided value 'кьве сад' should be a number between '100' and 'inf' after 'кьве', but 'сад' was provided which equals to '1'",
            ),
            (
                'агъзурни миллион',
                "In the provided value 'агъзурни миллион' should be a number between '1' and '1000' after 'агъзурни', but 'миллион' was provided which equals to '1000000.0'",
            ),
        ]

        for input_str, expected_error in incorrect_next_values:
            with self.subTest(input_str=input_str):
                with self.assertRaises(ValueError) as context:
                    lezgiToNum(input_str)
                self.assertEqual(str(context.exception), expected_error)

if __name__ == '__main__':
    unittest.main()
