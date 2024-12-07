import unittest
from unittest.mock import PropertyMock, patch

from pynestor.pynestor import NestorInstance


class TestNestorInstance(unittest.TestCase):
    def test01_version_14(self):
        correct_string = ["15", "15.0", "build-15.0-ba5d8624"]
        for version_string in correct_string:
            with self.subTest(version_string=version_string):
                with patch.object(NestorInstance, "_call", return_value=0):
                    # en surchargeant call, exist() va retourner None
                    with patch.object(NestorInstance, "spec", new_callable=PropertyMock) as mock_spec:
                        mock_spec.return_value = {"version": version_string}
                        inst = NestorInstance(name="dummy")
                        self.assertEqual(inst.version(), 15)
