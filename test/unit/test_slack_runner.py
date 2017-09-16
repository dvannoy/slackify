import json
import unittest
import slack_runner
from datetime import datetime
import arrow

class TestSlackRunner(unittest.TestCase):
    def setUp(self):
        self.rec = ['2017-05-01',
               'Welcome to the first week of the new Slacker Devotional!',
               '4 Love is patient, love is kind. It does not envy, it does not boast, it is not proud. 5 It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs. 6 Love does not delight in evil but rejoices with the truth. 7 It always protects, always trusts, always hopes, always perseveres. - 1 Corinthians 13:4-7',
               '6 Love does not delight in evil but rejoices with the truth. 7 It always protects, always trusts, always hopes, always perseveres. - 1 Corinthians 13:6-7',
               'Where in chapter 13 does Paul speak to the people of the Corinthians? Where does he speak to you?',
               'Which action of love is the most difficult for you to achieve? ',
               'Choose to do one of the attributes of love with someone whom you are struggling with.',
               'Prayer for the PB&J Connect Group', 'Please Lord help me to have a loving heart.  Teach me to choose compassion over self.',
               'I find my joy of living in the fierce and ruthless battles of life, and my pleasure comes from learning something new. - August Strindberg'
               ]

        channels = {1: "tst-meditation-monday", 2: "tst-takeaway-tuesday", 3: "tst-wisdom-wednesday",
                         4: "tst-throwdown-thurs", 5: "tst-tgif-friday"}

    def test_monday(self):
        #test_date = datetime.strptime('2017-08-07', '%Y-%m-%d')
        test_date = arrow.get('2017-08-07', 'YYYY-MM-DD')
        payload = slack_runner.get_payload(test_date, self.rec)
        expected_results = {'username': 'SlacKing', 'channel': 'tst-meditation-monday', 'mrkdwn_in': True, 'attachments': [{'pretext': '*Week of August 7, 2017*\nWelcome to the first week of the new Slacker Devotional!', 'text': '4 Love is patient, love is kind. It does not envy, it does not boast, it is not proud. 5 It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs. 6 Love does not delight in evil but rejoices with the truth. 7 It always protects, always trusts, always hopes, always perseveres. - 1 Corinthians 13:4-7', 'mrkdwn_in': ['text', 'pretext'], 'title': 'Scripture of the Week'}]}
        self.assertEquals(expected_results, payload)


    def test_tuesday(self):
        # test_date = datetime.strptime('2017-08-07', '%Y-%m-%d')
        test_date = arrow.get('2017-08-08', 'YYYY-MM-DD')
        payload = slack_runner.get_payload(test_date, self.rec)
        expected_results = {'username': 'SlacKing', 'channel': 'tst-takeaway-tuesday', 'mrkdwn_in': True, 'attachments': [
            {'text': '6 Love does not delight in evil but rejoices with the truth. 7 It always protects, always trusts, always hopes, always perseveres. - 1 Corinthians 13:6-7',
             'mrkdwn_in': ['text', 'pretext'], 'title': 'Memory Verse'}]}
        self.assertEquals(expected_results, payload)


    def test_wednesday(self):
        # test_date = datetime.strptime('2017-08-07', '%Y-%m-%d')
        test_date = arrow.get('2017-08-09', 'YYYY-MM-DD')
        payload = slack_runner.get_payload(test_date, self.rec)
        print payload
        expected_results = {'username': 'SlacKing', 'channel': 'tst-wisdom-wednesday', 'mrkdwn_in': True,
                                'attachments': [
                                  {'pretext': 'Here are this weeks question.  Please respond and discuss in this channel:',
                                   'text': '1. Where in chapter 13 does Paul speak to the people of the Corinthians? Where does he speak to you?\n2. Which action of love is the most difficult for you to achieve? ',
                                   'mrkdwn_in': ['text', 'pretext'],
                                   'title': 'Questions'}
                                ]
                            }
        self.assertEquals(expected_results, payload)

    # def test_it_posts_to_slack(self):
    #     self.assertEquals(1,1)

