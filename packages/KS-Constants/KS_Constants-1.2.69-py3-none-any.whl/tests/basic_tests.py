import unittest

from ks_constants.devs import Developer
from ks_constants.regions import Region
from ks_constants.maps import Map
from ks_constants.ranks import Rank
from ks_constants.roles import Role, RoleType, Team
from ks_constants.locale import Language

class TestStringMethods(unittest.TestCase):

    def test_maps(self):
        self.assertEqual(Map.Aiur_Fountains.original_author(), Developer.Luminous)
        self.assertEqual(Map.Ruins_Of_Imladoon.original_author(), Developer.Fatline)
        self.assertEqual(Map.Ruins_Of_Imladoon.current_author(), Developer.Templar)
        self.assertFalse(Map.Vintage_Shores.is_disliked())
        self.assertEqual(Map.Classic.get_name(Language.English), Map.Classic.get_english_name())
        self.assertEqual(Map.from_index(0), Map.Classic)

    def test_roles(self):
        self.assertEqual(Role.Ares.get_current_author(), Role.Aewyn.get_current_author())
        self.assertEqual(Role.Ascendant.get_role_type(), RoleType.Builder)
        self.assertEqual(Role.Dark_Templar.get_role_type(), RoleType.Support)
        self.assertEqual(Role.Brakk.get_role_type(), RoleType.Hunter)
        self.assertEqual(Role.from_index(5), Role.Ares)
        self.assertEqual(Role.Brakk.get_team(), Team.Kerrigan)
        self.assertEqual(Role.Team_Nova.get_english_name(), Role.Team_Nova.get_name(Language.English))
        self.assertEqual(Role["Scientist"], Role.from_index(1))
        self.assertEqual(Role.Scientist, Role.from_index(1))
        self.assertEqual(Role.from_name("Scientist"), Role.Scientist)
        self.assertEqual(Role.from_name("Team_Nova"), Role.Team_Nova)
        self.assertIsNone(Role.from_name("oisjdfw"))

    def test_teams(self):
        self.assertEqual(Team.Kerrigan.to_int(), 1)

    def test_ranks(self):
        self.assertGreater(Rank.Bronze.upper_percentile(), 0)

    def test_regions(self):
        self.assertEqual(Region.from_index(1), Region.North_America)

if __name__ == '__main__':
    unittest.main()
