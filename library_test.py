import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEqual(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)
    
    # Fourth unit test; prove that if we look for a date, we find one in the given text.
    def test_date(self):
        self.assert_extract("I was born on 2015-07-25.", library.dates_iso8601, '2015-07-25')

    # Fifth unit test; prove that invalid date should not be found.
    def test_invalid_date(self):
        self.assert_extract("I was born on 2015-07-35.", library.dates_iso8601)
    
    # Sixth unit test; prove that date of type 20 Jan 2018 are handled.
    def test_date_with_month_names(self):
        self.assert_extract("I was born on 20 Mar 2017.", library.dates_with_month_names,"20 Mar 2017")
    
    def test_date_with_month_names_with_hyphen(self):
        self.assert_extract("I was born on 20-Mar-2017.", library.dates_with_month_names,"20-Mar-2017")

    def test_date_with_month_names_with_fslash(self):
        self.assert_extract("I was born on 20/Mar/2017.", library.dates_with_month_names,"20/Mar/2017")

    def test_date_with_month_names_with_colon(self):
        self.assert_extract("I was born on 20:Mar:2017.", library.dates_with_month_names,"20:Mar:2017")

    def test_date_with_full_month_names(self):
        self.assert_extract("I was born on 20:March:2017.", library.dates_with_month_names,"20:March:2017")

    def test_date_with_full_month_names_space(self):
        self.assert_extract("I was born on 20 March 2017.", library.dates_with_month_names,"20 March 2017")

    def test_date_RFC(self):
        self.assert_extract("I was born on Mon, 17 Apr 2006 21:22:48 GMT.", library.dates_iso8601, 'Mon, 17 Apr 2006 21:22:48 GMT')

    def test_date_UTC(self):
        self.assert_extract("I was born on 2006-04-17T21:22:48.2698750Z", library.dates_iso8601, '2006-04-17T21:22:48.2698750Z')

    def test_date_UTC_UNDEFINED(self):
        self.assert_extract("I was born on 2000-03-20T13:02:03.0000000", library.dates_iso8601, '2000-03-20T13:02:03.0000000')

    def test_date_SORTABLE(self):
        self.assert_extract("I was born on 2006-04-17T14:22:48", library.dates_iso8601, '2006-04-17T14:22:48')

    def test_date_UNIV(self):
        self.assert_extract("I was born on 2006-04-17 21:22:48Z", library.dates_iso8601, '2006-04-17 21:22:48Z')



if __name__ == '__main__':
    unittest.main()
