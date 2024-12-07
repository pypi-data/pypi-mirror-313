import enum
import os
import re
import subprocess
import sys
from functools import cached_property
from typing import List, Optional, Set, Union

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


######################################
# Python wrapping nestor
######################################


class Utils:
    @staticmethod
    def flat_map(f, xs):
        return [y for ys in xs for y in f(ys)]

    @staticmethod
    def quote_if_needed(value):
        if isinstance(value, str):
            try:
                float(value)
                value = "'%s'" % value
            except ValueError:
                pass
        return value

    @staticmethod
    def flat_dico(parent_keys, dico):
        result = []
        for key, value in dico.items():
            new_key = (*parent_keys, key)
            if isinstance(value, dict):
                result += Utils.flat_dico(parent_keys=new_key, dico=value)
            else:
                result.append((new_key, value))
        return result


class NestorDesc:
    def to_set_opt(self) -> "NestorDescSet":
        """Return a list of valid parameters for the --set arg for the 'nestor new' command"""
        raise NotImplementedError()

    def _key_hash(self):
        raise NotImplementedError()

    def __hash__(self):
        return hash(self._key_hash())

    def __eq__(self, other):
        if isinstance(other, NestorDesc):
            return self._key_hash() == other._key_hash()
        return False

    def __str__(self):
        return str(self.to_set_opt())

    def __ge__(self, other):
        if isinstance(other, NestorDesc):
            return self._key_hash().__ge__(other._key_hash())
        raise TypeError

    def __le__(self, other):
        if isinstance(other, NestorDesc):
            return self._key_hash().__le__(other._key_hash())
        raise TypeError

    def __lt__(self, other):
        if isinstance(other, NestorDesc):
            return self._key_hash().__lt__(other._key_hash())
        raise TypeError

    def __gt__(self, other):
        if isinstance(other, NestorDesc):
            return self._key_hash().__gt__(other._key_hash())
        raise TypeError


class NestorOpt(NestorDesc):
    _prefix = "spec."

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_set_opt(self):
        """Return a list of valid parameters for the --set arg for the 'nestor new' command"""
        return NestorDescSet([self])

    def _key_hash(self):
        name = self.name
        if not name.startswith(NestorOpt._prefix):
            name = NestorOpt._prefix + name
        return name

    def __str__(self):
        name = self.name
        if not name.startswith(NestorOpt._prefix):
            name = NestorOpt._prefix + name
        return "%s=%s" % (name, Utils.quote_if_needed(self.value))

    def __repr__(self):
        return '%s("%s", %s)' % (
            type(self).__name__,
            self.name,
            Utils.quote_if_needed(self.value),
        )


class NestorDescSet:
    """Représente un ensemble de NestorOpt (qui sont des paires clef / valeur)"""

    def __init__(self, init: List["NestorDesc"] = None):
        self.values: Set[NestorOpt] = set()
        self.add(init or [])

    def add(self, other: Union[List["NestorDescSet"], "NestorDescSet", "NestorDesc", List["NestorDesc"]]) -> None:
        if not isinstance(other, list):
            other = [other]
        for vo in other:
            if isinstance(vo, NestorOpt):
                values = [vo]
            elif isinstance(vo, NestorDesc):
                values = vo.to_set_opt().values
            elif isinstance(vo, NestorDescSet):
                values = vo.values
            else:
                raise ValueError("Can't add type %s" % type(vo))
            for v in values:
                if v in self.values:
                    self.values.remove(v)
                self.values.add(v)

    def merge(self, other: Union["NestorDescSet", List["NestorDescSet"]]):
        if not isinstance(other, list):
            other = [other]
        for vo in other:
            if not isinstance(vo, NestorDescSet):
                raise ValueError("Can't add type %s" % type(vo))
            self.values |= vo.values
        return self

    def __getitem__(self, item: Union[str, "NestorDesc"]) -> Optional[NestorOpt]:
        to_find = item
        if isinstance(to_find, str):
            # __hash__ only on the key not on the value, TODO replace with custom lib internal class
            to_find = NestorOpt(item, 0)

        for el in self.values:
            if el == to_find:
                return el
        return None

    def get(self, item, default=None):
        res = self.__getitem__(item)
        if not res:
            if callable(default):
                return default()
            return default
        return res

    def has_sub_key(self, key: str) -> bool:
        """
        True if the set has a key which is a sub key (for example spec.sources.repositories
        is a subset of spec.sources
        """
        return any(k.name.startswith(key) for k in self.values)

    def __repr__(self):
        return self.values.__repr__()

    def __str__(self):
        return self.values.__str__()

    @staticmethod
    def parse_nestor_cfg(path_nestor_cfg, section):
        nestor_values = NestorDescSet()
        stream = open(path_nestor_cfg)
        data = load(stream, Loader=Loader)
        print("Parsing section [%s] of %s" % (section, path_nestor_cfg))
        for key, value in Utils.flat_dico((), data.get(section, {})):
            try:
                nestor_values.add(NestorOpt(".".join(key), value))
            except TypeError as e:
                print(key, value)
                print(e, flush=True)
                raise e
        return nestor_values

    def to_str(self, pretty=False):
        prefix = pretty and "\n" or ","
        return prefix.join(
            sorted(
                map(
                    lambda it: str(it),
                    self.values,
                )
            )
        )


class NestorGitDesc(NestorDesc):
    """Python class to handle the yml part of the Odoo operator
    branch: ""
          method: ssh
          path: odoo-addons/community-addons
          secret: ""
          server: ""
    """

    _tmpl = "spec.sources.repositories.DEPOT_GIT%(idx)s.%(key)s"

    def __init__(self, idx, path, branch=None, method=None, secret=None, server=None):
        self.idx = idx
        self.path = path
        self.branch = branch
        self.method = method
        self.secret = secret
        self.server = server

    def get_dict_set_opt(self, key):
        return {"idx": self.idx or "", "key": key}

    def to_set_opt(self):
        values = NestorDescSet([NestorOpt(self._tmpl % self.get_dict_set_opt("path"), self.path)])
        if self.branch:
            values.add(
                NestorOpt(
                    self._tmpl % self.get_dict_set_opt("branch"),
                    Utils.quote_if_needed(str(self.branch)),
                )
            )
        if self.method:
            values.add(NestorOpt(self._tmpl % self.get_dict_set_opt("method"), self.method))
        if self.secret:
            values.add(NestorOpt(self._tmpl % self.get_dict_set_opt("secret"), self.secret))
        if self.server:
            values.add(NestorOpt(self._tmpl % self.get_dict_set_opt("server"), self.server))
        return values

    def _key_hash(self):
        return tuple(self.path)


class NestorPersistenceDesc(NestorDesc):
    def __init__(self, s3_secret: str = None, s3_bucket: str = None, enable_s3: bool = True):
        self.s3_secret = s3_secret
        self.s3_bucket = s3_bucket
        self.enable_s3 = enable_s3

    def to_set_opt(self) -> NestorDescSet:
        values = NestorDescSet()
        values.add(NestorOpt("persistence.disabled", self.enable_s3))
        if self.s3_secret:
            values.add(NestorOpt("persistence.s3.secret", self.s3_secret))
        if self.s3_bucket:
            values.add(NestorOpt("persistence.s3.bucket", self.s3_bucket))
        if self.s3_secret and self.s3_bucket:
            values.add(NestorOpt("persistence.s3.allowWrite", True))
            values.add(NestorOpt("persistence.s3.enabled", self.enable_s3))
        return values


class NestorCommand:
    def __init__(self, instance, names, *args, **kwargs):
        if isinstance(names, str):
            names = [names]
        self._n_cmd = ["nestor"] + names + [instance.name]
        self.args = list(args)
        self.kwargs = kwargs

    def call(self) -> int:
        print(self, flush=True)
        return subprocess.call(str(self), shell=True)

    def getoutput(self) -> str:
        print(self, flush=True)
        return subprocess.getoutput(str(self))

    def __str__(self):
        return " ".join([str(i) for i in (self._n_cmd + self.args)])


class NestorInstance:
    def __init__(self, name: str, verbose=False):
        self.name = name
        self.verbose = verbose
        self.filestore = NestorFileStoreCommand(self)
        self.db = NestorDatabaseCmd(self)

    def __repr__(self):
        return "nestor[%s]" % self.name

    def version(self, values: Optional[NestorDescSet] = None) -> int:
        if self.exist():
            value = self.spec["version"]
        elif values:
            value = values["version"] and values["version"].value
        else:
            raise ValueError("Version can't be found")
        # la version peut être 14, 14.0 ou build-14.0-ba5d8624 dans le cas d'une image pas encore déployée
        numeric_part = value.split("-")[-2:][0]  # on extrait la partie après le - s'il y en a un
        return int(float(numeric_part))

    def save_spec(self, values: NestorDescSet, path_dir: str):
        full_path = path_dir
        if os.path.splitext(path_dir)[1] != "spec":
            full_path = os.path.join(path_dir, self.name + ".spec")
        with open(os.path.expanduser(full_path), "w+") as spec_file:
            spec_file.write(values.to_str(True))
        return full_path

    @staticmethod
    def new_from_yaml(path_spec, name=None):
        ext = os.path.splitext(path_spec)[1]
        if ext not in ["yaml", "yml"]:
            raise ValueError(f"Le format [{ext}] du fichier {path_spec} n'est pas supporté")
        name = name or os.path.splitext(os.path.basename(path_spec))[0]
        inst = NestorInstance(name)
        inst.direct_call(f"cat {path_spec} | nestor new {name} -")
        return inst

    def exist(self):
        return not bool(self.wait(postgres=True, timeout=2))

    def create(self, odoo_version: str = None, values_set: NestorDescSet = None):
        opt = []
        if odoo_version:
            opt.append("--odoo-version")
            opt.append(str(odoo_version))
        if values_set:
            opt.append("--set")
            opt.append('"%s"' % values_set.to_str())
        self._call("new", *opt)
        return self

    def set_memory_worker(self, workers: int = None, memory_hard: int = None, memory_soft: int = None):
        workers = workers or 2
        memory_soft = memory_soft or 450_000_000  # 450Mo
        memory_hard = memory_hard or 1_000_000_000  # 1000Mo
        self.edit(
            NestorDescSet(
                [
                    NestorOpt("options.limitMemoryHard", memory_hard),
                    NestorOpt("options.limitMemorySoft", memory_soft),
                    NestorOpt("workers", workers),
                ]
            )
        )

    @staticmethod
    def list():
        r = subprocess.getoutput("nestor list -f name")
        return [NestorInstance(s.strip()) for s in r.splitlines()[1:]]

    def edit(self, values_set: NestorDescSet = None) -> int:
        return self._edit(values_set)

    def _edit(self, values_set: NestorDescSet = None) -> int:
        self._clear_cache()
        if self.verbose:
            print(values_set.to_str(pretty=True), flush=True)
        opt = []
        if values_set:
            opt.append("--set")
            opt.append('"%s"' % values_set.to_str())
        return self._call("edit", *opt)

    def filestore_s3_dump(self, s3_secret: str = None, bucket: str = None, verbose: bool = False):
        self._call(["filestore", "dump"], "s3", ".", "--progress", "--bucket", bucket or self.name, "--s3", s3_secret)

    def db_restore_from_s3(
        self,
        dump_path: str,
        alt_dump_path: str = None,
        s3_secret: str = None,
        bucket: str = None,
        set_password_to_all: bool = False,
        no_reset_password: bool = False,
        verbose: bool = False,
    ) -> int:
        if self.db.restore(
            NestorDatabaseCmd.DBCmdTarget.S3,
            dump_path,
            s3_secret,
            bucket,
            set_password_to_all,
            no_reset_password,
            verbose,
        ):
            print(f"{dump_path} not found, defaulting to {alt_dump_path}")
            return self.db.restore(
                NestorDatabaseCmd.DBCmdTarget.S3,
                alt_dump_path,
                s3_secret,
                bucket,
                set_password_to_all,
                no_reset_password,
                verbose,
            )
        return 0

    def wait(self, up: bool = True, postgres: bool = False, timeout: int = None) -> int:
        opt = []
        if up:
            opt.append("up")
        else:
            opt.append("down")
        if postgres:
            opt.append("--postgresql")
        if timeout:
            opt.append("--timeout")
            opt.append(str(timeout))
        return self._call("wait", *opt)

    def stop(self) -> int:
        return self._call("stop")

    def start(self) -> int:
        return self._call("start")

    def restart(self) -> int:
        return self._call("restart")

    def delete(self) -> int:
        print('echo "o" | nestor delete %s' % self.name, flush=True)
        return self.direct_call('echo "o" | nestor delete %(NESTOR_NAME)s')

    def update(self, module_names: Union[str, List[str]]) -> int:
        opt = []
        if isinstance(module_names, str):
            opt.append(module_names)
        else:
            opt.append(",".join(module_names))
        return self._call("update", *opt)

    def install(self, module_names: Union[str, List[str]]) -> int:
        opt = []
        if isinstance(module_names, str):
            opt.append(module_names)
        else:
            opt.append(",".join(module_names))
        return self._call("install", *opt)

    def delete_if_failed(self, result: int) -> bool:
        """delete when the result code is not zero (meaning that previous operation has failed)"""
        print("Delete ?", bool(result), flush=True)
        if result:
            return bool(self.delete())
        return False

    def show(self, output: str = "text"):
        opt = []
        if output:
            opt.append("-o")
            opt.append(output)
        return self._getoutput("show", *opt)

    def _clear_cache(self):
        cache = self.__dict__
        if cache.get("spec"):
            del self.spec
        if cache.get("spec_text"):
            del self.spec_text

    def _call(self, cmd_name: Union[str, List[str]], *opt) -> int:
        return NestorCommand(self, cmd_name, *opt).call()

    def _getoutput(self, cmd_name: str, *opt) -> str:
        return NestorCommand(self, cmd_name, *opt).getoutput()

    def direct_call(self, cmd):
        return subprocess.call(cmd % {"NESTOR_NAME": self.name}, shell=True)

    @cached_property
    def spec(self) -> dict:
        return load(self.show("yaml"), Loader)["spec"]

    @cached_property
    def spec_values(self) -> NestorDescSet:
        desc = NestorDescSet()
        specs = self.show("spec").split(",spec")
        key, value = specs[0].split("=")
        desc.add(NestorOpt(key, value))
        for opt in specs[1:]:
            key, value = opt.split("=")
            desc.add(NestorOpt("spec" + key, value))
        return desc

    @cached_property
    def spec_text(self):
        return self.show("text")

    @property
    def password(self):
        m = re.search(r"Odoo admin \/ DB Manager password: (.*?)\n", self.spec_text)
        if m:
            return m.group(1)
        return None

    @property
    def url(self):
        m = re.search(r"URL: (.*?)\n", self.spec_text)
        if m:
            return m.group(1)
        return None


class NestorDatabaseCmd:
    def __init__(self, inst: NestorInstance):
        self._inst = inst

    class DBCmdTarget(enum.Enum):
        LOCAL = "local"
        S3 = "s3"

    def restore(
        self,
        type: Union[str, DBCmdTarget],
        dump_path: str,
        s3_secret: str = None,
        bucket: str = None,
        set_password_to_all: bool = False,
        no_reset_password: bool = False,
        verbose: bool = False,
    ) -> int:
        if isinstance(type, NestorDatabaseCmd.DBCmdTarget):
            type = type.value
        opt = [type, dump_path]
        if s3_secret:
            opt.append("--s3")
            opt.append(s3_secret)
        if bucket:
            opt.append("--bucket")
            opt.append(bucket)
        if set_password_to_all:
            opt.append("--set-password-to-all")
        if no_reset_password:
            opt.append("--no-reset-passwords")
        if verbose:
            opt.append("--verbose")
        return NestorCommand(self._inst, ["database", "restore"], *opt).call()

    def dump(
        self,
        type: Union[str, DBCmdTarget],
        dump_path: str,
        s3_secret: str = None,
        bucket: str = None,
        verbose: bool = False,
    ):
        if isinstance(type, NestorDatabaseCmd.DBCmdTarget):
            type = type.value
        opt = [str(type), dump_path]
        if s3_secret:
            opt.append("--s3")
            opt.append(s3_secret)
        if bucket:
            opt.append("--bucket")
            opt.append(bucket)
        if verbose:
            opt.append("--verbose")
        return NestorCommand(self._inst, ["database", "dump"], *opt).call()

    def secret(self):
        raise NotImplementedError

    def port(self):
        raise NotImplementedError


class NestorFileStoreCommand:
    def __init__(self, instance: NestorInstance):
        self.inst = instance

    def enable_on_s3_spec(self, s3_secret: str, s3_bucket: str = None, values: NestorDescSet = None):
        assert s3_secret, "A s3 secret is required"
        assert self.inst.version(values) <= 15, "V15 not supported yet"

        s3_bucket = s3_bucket or self.inst.name
        specs = NestorPersistenceDesc(s3_secret, s3_bucket, enable_s3=True).to_set_opt()
        loads = (values["options.load"] or NestorOpt("options.load", "")).value.split(",")

        branch_name = str(float(self.inst.version(values)))
        if self.inst.version(values) >= 14:
            path = "odoo/cloud-modules"  # New repo only for 14.0 for now
            if "odoo_filestore_s3" not in loads:
                loads.append("odoo_filestore_s3")
            if self.inst.version(values) == 15:
                branch_name = "1.2.3"
        else:
            path = "kubernetes/odoo-modules"
            if "odoo_s3" not in loads:
                loads.append("odoo_s3")
        for idx in list(range(2, 20)):
            opt = "sources.repositories.DEPOT_GIT%s.path" % idx
            if not values[opt]:
                specs.add(NestorGitDesc(idx, path, branch_name).to_set_opt())
                break
        else:
            raise ValueError("Trop de DEPOT_GIT: superieur a 20")
        if self.inst.version(values) <= 12:
            specs.add(NestorOpt("options.load", ",".join(loads)))
        else:
            # les options sont separees par des espaces pour eviter le probleme de --set de nestor qui splitte sur
            # les virgules
            specs.add(NestorOpt("options.load", " ".join(loads)))

        return specs

    def dump_on_s3(self, s3_secret: str, s3_bucket: str = None):
        assert s3_secret, "A s3 secret is required"
        s3_bucket = s3_bucket or self.inst.name

        self.inst._call(
            ["filestore", "dump"], "s3", ".", "--progress", "--bucket", s3_bucket or self.inst.name, "--s3", s3_secret
        )

    def restore_from_s3(self, s3_secret, s3_bucket):
        self.inst._call(
            ["filestore", "restore"],
            "s3",
            ".",
            "--progress",
            "--bucket",
            s3_bucket or self.inst.name,
            "--s3",
            s3_secret,
        )


class ScriptNestorInstance(NestorInstance):
    def __init__(self, name, verbose=False, allowed_to_delete: bool = True):
        super(ScriptNestorInstance, self).__init__(name, verbose)
        self.allowed_to_delete = allowed_to_delete

    @staticmethod
    def from_inst(nestor_inst: NestorInstance):
        return ScriptNestorInstance(nestor_inst.name, nestor_inst.verbose)

    def delete_and_exit_if_failed(self, result: int):
        if self.allowed_to_delete:
            self.delete_if_failed(result)
        self.exit_if_failed(result)

    def exit_if_failed(self, result: int):
        if result:
            sys.exit(result)
