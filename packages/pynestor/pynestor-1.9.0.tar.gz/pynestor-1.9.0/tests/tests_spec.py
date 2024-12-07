import unittest
from dataclasses import dataclass
from typing import List, Union
from unittest import mock
from unittest.mock import patch

from pynestor.preview_odoo_nestor import (
    EnvironementConfig,
    PreviewUpScript,
    PreviewUtils,
)
from pynestor.pynestor import NestorDescSet, NestorInstance, NestorOpt


def _create_all_spec_sources(project_path):
    return NestorDescSet([NestorOpt("sources.branch", "test_branch")])


@dataclass
class MockInstance:
    name: str = "test"
    url: str = "test"
    existing: bool = True
    password: str = "test"
    verbose: bool = False
    filestore = None
    db = None
    spec = {}
    update_return_value = 0

    def exist(self):
        return self.existing

    def version(self, values):
        return 15.0

    def install(self, modules: str):
        pass

    def update(self, module_names: Union[str, List[str]]) -> int:
        return self.update_return_value

    def delete_and_exit_if_failed(self, return_code: int):
        pass

    def exit_if_failed(self, return_code: int):
        pass

    def wait(self, up: bool = True, postgres: bool = True, timeout=0):
        return 0

    def start(self):
        return 0

    def direct_call(self, cde=""):
        pass

    def create(self, odoo_version: str = None, values_set: NestorDescSet = None):
        return type(self)()

    def set_memory_worker(self, workers: int = None, memory_hard: int = None, memory_soft: int = None):
        pass

    @staticmethod
    def list():
        pass

    def edit(self, values_set: NestorDescSet = None):
        pass

    def db_restore_from_s3(
        self,
        dump_path: str,
        alt_dump_path: str = None,
        s3_secret: str = None,
        bucket: str = None,
        set_password_to_all: bool = False,
        no_reset_password: bool = False,
        verbose: bool = False,
    ):
        pass


@mock.patch("time.sleep")
class TestEnvironment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env_dict = {
            "ENABLE_QUEUE_JOB": "True",
            "NESTOR_NAME": "test",
            "CI_PROJECT_DIR": "../src",
            "CI_BUILD_DIR": "./",
            "CI_PROJECT_PATH": "odoo/",
            "GITLAB_TOKEN": "test_token",
            "ODOO_VERSION": "15.0",
            "CI_COMMIT_REF_NAME": "test_mr",
        }

    def prepare_script(self, env_dict):
        config = EnvironementConfig(env_dict)
        config.apply_default()
        script = PreviewUpScript(config)
        return script

    def test_default_env(self, *mocks):
        env_dict = self.env_dict.copy()
        script = self.prepare_script(env_dict)
        with patch.object(PreviewUtils, "_create_all_spec_sources") as mock_method:
            mock_method.return_value = NestorDescSet([NestorOpt("sources.branch", "test_branch")])
            values = script.get_spec_values(stage="restore")
        script.log_spec(values)
        self.assertTrue(values["options.queueJobs.enabled"].value)
        # values contient des NestorOpt; NestorOpt.value retourne la chaine
        self.assertEqual(values["options.queueJobs.channels"].value, "root:1")

    def test_no_demo_data(self, *mocks):
        env_dict = self.env_dict.copy()
        env_dict.update({"NO_DB_DUMP": "True", "MODULES_WITHOUT_DEMO": "ALL"})
        script = self.prepare_script(env_dict)
        with patch.object(PreviewUtils, "_create_all_spec_sources") as mock_method:
            mock_method.return_value = NestorDescSet([NestorOpt("sources.branch", "test_branch")])
            values = script.get_spec_values(stage="restore")
        script.log_spec(values)
        self.assertEqual(values["options.withoutDemo"].value, True)
        # values contient des NestorOpt; NestorOpt.value retourne la chaine

    def test_always_restore(self, *mocks):
        env_dict = self.env_dict.copy()
        env_dict.update({"ALWAYS_RESTORE": "True"})
        script = self.prepare_script(env_dict)
        script.inst = MockInstance()
        with patch.object(PreviewUtils, "_create_all_spec_sources") as mock_method:
            mock_method.return_value = NestorDescSet([NestorOpt("sources.branch", "test_branch")])
            with patch.object(type(script), "restore_db") as mock_restore_db:
                with patch.object(type(script), "stop"):
                    with patch.object(type(script), "edit_with_values"):
                        script.run_script()
                        mock_restore_db.assert_called_with()

    def test_always_restore_false(self, *mocks):
        env_dict = self.env_dict.copy()
        env_dict.update({"ALWAYS_RESTORE": "false"})
        script = self.prepare_script(env_dict)
        script.inst = MockInstance()
        with patch.object(PreviewUtils, "_create_all_spec_sources") as mock_method:
            mock_method.return_value = NestorDescSet([NestorOpt("sources.branch", "test_branch")])
            with patch.object(type(script), "restore_db") as mock_restore_db:
                with patch.object(type(script), "stop"):
                    with patch.object(type(script), "edit_with_values"):
                        script.run_script()
                        mock_restore_db.assert_not_called()

    @mock.patch("subprocess.call")
    @mock.patch("sys.exit")
    def test_never_delete_on_fail(self, *mocks):
        env_dict = self.env_dict.copy()
        env_dict.update({"NEVER_DELETE_ON_FAIL": "True"})
        script = self.prepare_script(env_dict)
        with patch.object(PreviewUtils, "_create_all_spec_sources") as mock_method:
            mock_method.return_value = NestorDescSet([NestorOpt("sources.branch", "test_branch")])
            with patch.object(script.inst, "delete") as mock_delete:
                script.run_script()
                self.assertFalse(script.inst.allowed_to_delete)
                mock_delete.assert_not_called()

    @mock.patch("subprocess.call")
    @mock.patch("sys.exit")
    def test_never_delete_on_fail_false(self, *mocks):
        env_dict = self.env_dict.copy()
        env_dict.update({"NEVER_DELETE_ON_FAIL": "FALSE"})
        script = self.prepare_script(env_dict)
        with patch.object(PreviewUtils, "_create_all_spec_sources") as mock_method:
            mock_method.return_value = NestorDescSet([NestorOpt("sources.branch", "test_branch")])
            with patch.object(script.inst, "delete") as mock_delete:
                script.run_script()
                self.assertTrue(script.inst.allowed_to_delete)
                mock_delete.assert_called()

    @mock.patch("subprocess.call")
    def test_no_reset_password_is_set(self, mock_call, *args):
        env_dict = self.env_dict.copy()
        env_dict.update({"NO_RESET_PASSWORDS": "true", "ALWAYS_RESTORE": "true"})
        script = self.prepare_script(env_dict)
        script.inst = MockInstance()
        with patch.object(PreviewUtils, "_create_all_spec_sources") as mock_method:
            mock_method.return_value = NestorDescSet([NestorOpt("sources.branch", "test_branch")])
            with patch.object(type(script), "stop"):
                with patch.object(type(script), "edit_with_values"):
                    with patch.object(script.inst, "db_restore_from_s3", NestorInstance("test").db_restore_from_s3):
                        script.run_script()
                        self.assertTrue(any("--no-reset-passwords" in str(param) for param in mock_call.call_args_list))

    @mock.patch("subprocess.call")
    def test_no_reset_password_is_not_set(self, mock_call, *mocks):
        env_dict = self.env_dict.copy()
        env_dict.update({"ALWAYS_RESTORE": "true"})
        script = self.prepare_script(env_dict)
        script.inst = MockInstance()
        with patch.object(PreviewUtils, "_create_all_spec_sources") as mock_method:
            mock_method.return_value = NestorDescSet([NestorOpt("sources.branch", "test_branch")])
            with patch.object(type(script), "stop"):
                with patch.object(type(script), "edit_with_values"):
                    with patch.object(script.inst, "db_restore_from_s3", NestorInstance("test").db_restore_from_s3):
                        script.run_script()
                        self.assertFalse(any("no-reset-passwords" in str(param) for param in mock_call.call_args_list))
