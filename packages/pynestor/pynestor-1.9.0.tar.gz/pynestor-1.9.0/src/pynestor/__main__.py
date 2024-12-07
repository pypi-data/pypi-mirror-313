import argparse
import sys

from pynestor import preview_odoo_nestor
from pynestor.pynestor import NestorInstance


def launch_preview_script(args):
    if args.interactive:
        word = "Démarage" if args.up else "Arret"
        preview_odoo_nestor.log(word + " d'une preview en mode interactif")
        script_config = preview_odoo_nestor.InteractiveConfig()
    else:
        script_config = preview_odoo_nestor.EnvironementConfig()

    script_config.apply_default()
    preview_odoo_nestor.log("====Config====")
    preview_odoo_nestor.log(script_config)
    preview_odoo_nestor.log("==============")

    if args.interactive:
        preview_odoo_nestor.log("Voulez vous continuer avec la configuration si dessus ?")
        rep = input("[y/N] =>")
        if rep.upper() != "y".upper():
            preview_odoo_nestor.log("Exit")
            return 0
    script = preview_odoo_nestor.ScriptNestor(script_config)
    if args.up:
        script = preview_odoo_nestor.PreviewUpScript(script_config)
    if args.down:
        script = preview_odoo_nestor.PreviewDownScript(script_config)
    preview_odoo_nestor.log(args)
    return script.run_script()


def main():
    parsr = argparse.ArgumentParser()
    parsr.add_argument(dest="command", help="Command à utiliser")
    args, other = parsr.parse_known_args()
    print(args, other)
    if args.command == "preview":
        preview_parser = argparse.ArgumentParser()
        preview_parser.add_argument("--down", dest="down", action="store_true")
        preview_parser.add_argument("--up", dest="up", action="store_true")
        preview_parser.add_argument("--interactive", "-i", dest="interactive", action="store_true")
        sys.exit(launch_preview_script(preview_parser.parse_args(other)))
    if args.command == "wait":
        wait_parser = argparse.ArgumentParser()
        wait_parser.add_argument(dest="name", help="Command à utiliser")
        wait_parser.add_argument("--down", dest="down", action="store_false")
        wait_parser.add_argument("--db", dest="db", action="store_true")
        wait_parser.add_argument("--timeout", dest="timeout", type=int, default=None)
        args = wait_parser.parse_args(other)
        print(args)
        inst = NestorInstance(args.name)
        inst.wait(args.down, args.db, timeout=args.timeout)
    if args.command == "exist":
        exist_parser = argparse.ArgumentParser()
        exist_parser.add_argument(dest="name", help="Command à utiliser")
        args = exist_parser.parse_args(other)
        print(args)
        inst = NestorInstance(args.name)
        inst.exist()


if __name__ == "__main__":
    main()
