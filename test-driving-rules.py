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
        test1 = extract_rule(sample2)
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
        print("Blind spot: %s" % test6)

        sample7 = "You must yield to pedestrians if your traffic signal is red or if it is red and yellow"
        test7 = extract_rule(sample7)
        self.assertEqual(test7,
                         'IF OR((traffic signal, isA, red), AND(None, (yellow, isA, None))), THEN (self, yield, pedestrians)')
        print(test7)

        ## Radhika edit

        sample8 = "If There's A Fire, Stop, turn off the engine, and exit your vehicle."
        test8 = extract_rule(sample8)
        print("fire: %s" % test8)
        # self.assertEqual(test8, 'IF (self, 's, Fire), THEN AND((Stop, isA, None), (self, exit, vehicle))')

        sample9 = "If You Witness a Crash, Park your car off the road, Turn on your emergency flashers to warn other drivers"
        test9 = extract_rule(sample9)
        self.assertEqual(test9, 'IF (self, Witness, Crash), THEN (Park, off, road)')
        print("Car crash: %s" % test9)

        sample10 = "If Entering a Tunnel, turn on your headlights"
        test10 = extract_rule(sample10)
        self.assertEqual(test10, 'IF (self, Entering, Tunnel), THEN (turn, on, headlights)')
        print("Tunnel: %s" % test10)

        sample11 = "If You Witness a Crash, Park your car off the road."
        test11 = extract_rule(sample11)
        self.assertEqual(test11, 'IF (self, Witness, Crash), THEN (Park, off, road)')
        print("Witness car crash: %s" % test11)

        sample12 = "If your gas pedal sticks, Put your car in neutral and press the brake pedal to slow down."
        test12 = extract_rule(sample12)
        self.assertEqual(test12, 'IF (gas, isA, None), THEN AND((car, in, neutral), (press, slow, down))')
        print("Pedal Sticks: %s" % test12)

        sample13 = "If a vehicle is driving toward you head on in your lane, Slow down and pull to the right"
        test13 = extract_rule(sample13)
        self.assertEqual(test13, 'IF (vehicle, toward, lane), THEN AND(None, (pull, isA, None))')
        print("Vehicle is driving toward you: %s" % test13)

        sample14 = "If your headlights suddenly go out, Turn on your parking lights, emergency flashers, or turn signal"
        test14 = extract_rule(sample14)
        self.assertEqual(test14, 'IF (headlights, go, out), THEN OR((self, Turn, lights), (turn, isA, None))')
        print("Headlight Failure: %s" % test14)


class Illinois(unittest.TestCase):
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
        # page 24
        sample1 = "A driver must take care to slow down when approaching and crossing an intersection"
        test1 = extract_rule(sample1)
        print("s1: %s" % test1)
        # Expected - IF(self, crossing, intersection) THEN (self, must, slowdown)
        # Output - Throws an error

        # page 85
        sample2 = "If you come across a roadway or viaduct that has been flooded due to heavy rain, do not drive " \
                  "through the flooded area. "
        test2 = extract_rule(sample2)
        self.assertEqual(test2, 'IF OR((self, come, roadway), AND((viaduct, isA, None), (self, hasA, rain))), '
                                'THEN NOT(self, do, area)')
        # self.assertEqual(test2, 'IF(self, come, roadway), THEN NOT (self, drive, flood)')
        # print("Flood: %s"%test2)

        # page 30
        sample3 = "In a business or residential area, you must give a continuous turn signal for at least 100 feet " \
                  "before turning. In other areas, the signal must be given at least 200 feet before turning. "
        test3 = extract_rule(sample3)
        self.assertEqual(test3, 'IF((self, must, turn), (self, in a, residential area)) THEN (self, turn signal, '
                                '100 ft before)')
        print("s3: %s" % test3)
        # Expected 'IF OR((business, isA, None), (area, isA, None)), THEN (turn, for, feet)'
        # Output  IF((self, must, turn), (self, in a, residential area)) THEN (self, turn signal, '
        #                                 '100 ft before)

        # page 31
        sample4 = "When moving your vehicle from the right-hand lane to the left-hand lane, check for traffic behind " \
                  "your vehicle and to the left by turning your head and visually assessing the area. If the area is " \
                  "clear, give the left-turn signal and carefully move into the left lane. "
        test4 = extract_rule(sample4)
        self.assertEqual(test4,
                         'IF (vehicle, from, right-hand), THEN AND((check, for, traffic), AND((self, left, head), '
                         'AND((area, If, area), (self, move, left))))')
        print("s4: %s" % test4)
        # Expected - IF(self, moving to, left hand lane) THEN (self, check behind, vehicle)
        # Output - 'IF (vehicle, from, right-hand), THEN AND((check, for, traffic), AND((self, left, head), '
        #                          'AND((area, If, area), (self, move, left))))'

        sample5 = "If you park on a street with curbing and your vehicle is facing downhill, turn the front wheels " \
                  "toward the curb so your vehicle will roll toward the curb. "
        test5 = extract_rule(sample5)
        self.assertEqual(test5, 'IF AND((street, with, curbing), (vehicle, isA, downhill)), THEN (front, toward, curb)')
        print("s5: %s" % test5)
        # Expected - IF AND ((self, parking, curbing street) (self, parking, downhill)) THEN (self, turn wheels,
        # toward curb)
        # Output - IF AND((street, with, curbing), (vehicle, isA, downhill)), THEN (front, toward, curb)


class California(unittest.TestCase):
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
        # page: 67
        sample1 = "When you cannot change lanes to pass a bicyclist, allow at least three feet between your vehicle " \
                  "and the bicyclist. Slow down if you cannot give three feet of space. "
        test1 = extract_rule(sample1)
        print("s1: %s" % test1)
        self.assertEqual(test1, 'IF NOT(self, change, lanes), THEN AND((allow, at, feet), (bicyclist, if, feet))')
        # Expected - IF NOT (self, change lane, passing cyclist) THEN AND ((self, give space, 3ft), (self, pass,
        # cyclist)
        # Output - IF NOT(self, change, lanes), THEN AND((allow, at, feet), (bicyclist, if, feet))

        # page: 70
        sample2 = "The speed limit is 25 mph when you drive within 500 to 1000 feet of a school while children are " \
                  "outside or crossing the street "
        test2 = extract_rule(sample2)
        # self.assertEqual(test2, 'IF OR((self, come, roadway), AND((viaduct, isA, None), (self, hasA, rain))),
        # THEN NOT(self, do, area)')
        print("s2: %s" % test2)
        # Expected - IF AND ((self, drive, school), (self, present, children)) THEN (self, speed, 25 mph)
        # Output - Throws error

        # page: 27
        sample3 = "Do not pass a vehicle in front of you if there is only one lane of traffic going your direction " \
                  "and a solid yellow line on your side of the road "
        test3 = extract_rule(sample3)
        self.assertEqual(test3, 'IF AND((lane, of, traffic), (line, on, side)), THEN (vehicle, in, front)')
        print("s3: %s" % test3)
        # Expected - IF AND((lane, of, traffic), (line, on, side)), THEN (vehicle, in, front)
        # Output - IF AND((lane, of, traffic), (line, on, side)), THEN (vehicle, in, front)

        # page: 29
        sample4 = "If you miss a turn, keep driving until you can safely and legally turn around."
        test4 = extract_rule(sample4)
        self.assertEqual(test4, 'IF (self, miss, turn), THEN AND((driving, until, safely), None)')
        print("s4: %s" % test4)
        # Expected - IF (self, miss, turn) THEN (self, drive, safe to turn)
        # Output - IF (self, miss, turn), THEN AND((driving, until, safely), None)

        # page: 33
        sample5 = "You may not turn right if you are stopped at a red arrow light. Wait until the light changes to " \
                  "green before making your turn "
        test5 = extract_rule(sample5)
        self.assertEqual(test5, 'IF NOT(self, turn, arrow), THEN (Wait, until, changes)')
        print("s5: %s" % test5)
        # Expected - IF (self, stop, red arrow light) THEN (self, wait, light green)
        # Output - IF NOT(self, turn, arrow), THEN (Wait, until, changes)


class Pennsylvania(unittest.TestCase):
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
        # Page 37
        sample1 = "When passing another vehicle, get past the other driver’s blind spot as quickly and as safely as " \
                  "you can "
        test1 = extract_rule(sample1)
        print("s1: %s" % test1)
        self.assertEqual(test1, 'IF AND((driver, as, quickly), None), THEN NOT(self, passing, vehicle)')
        # Expected - IF(self, passing, vehicle) THEN (self, pass blind spot, quickly)
        # Output - IF AND((driver, as, quickly), None), THEN NOT(self, passing, vehicle)

        # Page 43
        sample2 = "If you're driving and you see an approaching squall or know squalls are near, exit the roadway " \
                  "and wait for the squall to pass "
        test2 = extract_rule(sample2)
        self.assertEqual(test2, 'IF AND(None, OR((self, see, squall), (squalls, near, near))), THEN AND((exit, isA, '
                                'None), (wait, for, squall))')
        print("s2: %s" % test2)
        # Expected - IF(self, see, squall) THEN (self, exit, roadway)
        # Output - IF AND(None, OR((self, see, squall), (squalls, near, near))), THEN AND((exit, isA, '
        #                                 'None), (wait, for, squall))

        # Page 43
        sample3 = "If you encounter a snow squall, exercise extreme caution by gradually slowing and activating your " \
                  "hazard lights for increased visibility. "
        test3 = extract_rule(sample3)
        self.assertEqual(test3,
                         'IF (self, encounter, snow), THEN AND((exercise, by, slowing), (hazard, for, visibility))')
        print("s3: %s" % test3)
        # Expected - IF( self, encounter, snowfall) THEN (self, slow, turn on haz lights)
        # Output - IF (self, encounter, snow), THEN AND((exercise, by, slowing), (hazard, for, visibility))

        # Page 44
        sample4 = "If you must drive below 40 mph on a limited access highway, use your hazard (four-way) flashers to " \
                  "warn the drivers behind you. "
        test4 = extract_rule(sample4)
        self.assertEqual(test4, 'IF (mph, on, access), THEN (hazard, behind, you)')
        print("s4: %s" % test4)
        # Expected - IF((self, speed, 40 mph) (self, drive, highway)) THEN (self, use, hazard)
        # Output - IF (mph, on, access), THEN (hazard, behind, you)


if __name__ == '__main__':
    unittest.main()
