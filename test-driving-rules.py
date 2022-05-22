import unittest
from driving_rules import *
from nltk import pos_tag


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_get_subject_phrase(self):
        sample = 'If you are stopped at a traffic light'
        tags = pos_tag(sample.split(" "))
        test = get_noun_phrase(tags)
        self.assertEqual(test, [('traffic', 'NN'), ('light', 'NN')])

        sample2 = "If your vehicle has antilock brakes"
        tags2 = pos_tag(sample2.split(" "))
        test2 = get_noun_phrase(tags2)
        self.assertEqual(test2, None)


    def test_make_subject_phrase(self):
        sample = [('traffic', 'NN'), ('light', 'NN')]
        test = make_noun_phrase(sample)
        self.assertEqual('traffic light', test)


    def test_make_triple(self):
        if_sample = 'If you are stopped at a traffic light that turns green'
        test = make_triples_from_phrase(if_sample)
        goal = 'AND((self, at, traffic light), (traffic light, isA green)'
        # print(test)

        multiple = "your traffic signal is red or if it is red and yellow"
        test = make_triples_from_phrase(multiple)
        print(test)


    def test_if_clause(self):
        tough = 'You must yield to pedestrians if your traffic signal is red or if it is red and yellow'
        result = set_if_clause([tough])
        self.assertEqual(result, ('your traffic signal is red or it is red and yellow',
                                  'You must yield to pedestrians'))


    def test_extract_rule(self):
        # TODO: make a keyword for safety belt
        sample = "If your car drives into water: Unfasten your safety belt and escape through a window"
        test = extract_rule(sample)
        self.assertEqual('IF (car, into, water), THEN AND((self, Unfasten, safety belt), (escape, through, window))',
                         test)

        sample2 = "If your vehicle  has antilock  brakes, never pump the brakes"
        test1= extract_rule(sample2)
        self.assertEqual(test1, 'IF (vehicle, hasA, brakes), THEN NOT(self, pump, brakes)')

        sample3 = "If a tailgater is behind you, move to another lane or pull to the side of the road to let the \
        tailgater pass"
        test3 = extract_rule(sample3)
        self.assertEqual(test3, 'IF (tailgater, behind, you), THEN OR(NOT(move, isA, None), (pull, of, road))')

        sample4 = "If you are stopped at a traffic light that turns green, you must yield to pedestrians already in the crosswalk"
        test4 = extract_rule(sample4)
        print(test4)
        # self.assertEqual()

        sample5 = "Submit to a breathalyzer or blood test to calculate your BAC, if you have been arrested"

        sample6 = "If you are in another drivers blind spot, safely drive through the blind spot as quickly as you can"
        test6 = extract_rule(sample6)
        print("Blind spot: %s"%test6)

        sample7 = "You must yield to pedestrians if your traffic signal is red or if it is red and yellow"
        test7 = extract_rule(sample7)
        # self.assertEqual(test7, 'IF AND((traffic, isA, red), (yellow, isA, None)), THEN (self, yield, pedestrians) AND((self, isA, traffic), (turns, isA, None))')
        print(test7)


if __name__ == '__main__':
    unittest.main()
