import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from ovos_PHAL_plugin_alsa import AlsaControl


class TestPlugin(unittest.TestCase):
    @unittest.skip
    def test_alsa_control(self):
        a = AlsaControl()
        a.set_volume(100)
        self.assertFalse(a.is_muted())

        a.mute()
        self.assertTrue(a.is_muted())

        a.unmute()
        self.assertFalse(a.is_muted())
        self.assertEqual(a.get_volume(), 100)

        a.set_volume(50)
        self.assertEqual(a.get_volume(), 50)

        a.set_volume(70)
        self.assertEqual(a.get_volume(), 70)


if __name__ == "__main__":
    unittest.main()
