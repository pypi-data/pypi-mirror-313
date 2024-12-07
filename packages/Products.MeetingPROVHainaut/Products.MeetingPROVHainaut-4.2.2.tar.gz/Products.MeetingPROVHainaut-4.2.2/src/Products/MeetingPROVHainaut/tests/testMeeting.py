# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.testMeeting import testMeetingType as mctmt
from Products.MeetingPROVHainaut.tests.MeetingPROVHainautTestCase import MeetingPROVHainautTestCase


class testMeetingType(MeetingPROVHainautTestCase, mctmt):
    """Tests the Meeting class methods."""


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingType, prefix='test_pm_'))
    return suite
