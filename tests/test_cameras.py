import unittest

from fujifilm_converter.cameras import get_camera, list_presets


class CameraPresetTests(unittest.TestCase):
    def test_unsupported_profile_presets_are_not_listed(self):
        self.assertNotIn("hasselblad", list_presets())
        self.assertNotIn("leica", list_presets())

    def test_unsupported_profile_aliases_are_rejected(self):
        for name in ("hasselblad", "hassel", "hassy", "哈苏", "leica", "徕卡"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    get_camera(preset=name)


if __name__ == "__main__":
    unittest.main()
