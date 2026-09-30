#!/usr/bin/env python
"""Locale-safe launcher for ansible-core CLI on Windows (cp1252 default codepage).

Ansible's initialize_locale() calls locale.setlocale(LC_ALL, ''), which on this
machine resolves to English_United States.1252. Ansible requires UTF-8.
This wrapper redirects the *default* locale request to a UTF-8 variant before
Ansible is imported. All other arguments are passed through unchanged.

Usage:
    python ansiblew.py playbook <args>   -> ansible-playbook <args>
    python ansiblew.py adhoc <args>      -> ansible <args>
"""
import sys
import locale

_ORIG_SETLOCALE = locale.setlocale


def _patched_setlocale(category, value):
    if value == "":
        value = "English_United States.UTF8"
    return _ORIG_SETLOCALE(category, value)


locale.setlocale = _patched_setlocale

from ansible.cli.playbook import PlaybookCLI  # noqa: E402
from ansible.cli.adhoc import AdhocCLI  # noqa: E402


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: ansiblew.py {playbook|adhoc} [ansible args...]", file=sys.stderr)
        return 2
    command, rest = args[0], args[1:]
    if command == "playbook":
        cli = PlaybookCLI(rest)
    elif command == "adhoc":
        cli = AdhocCLI(rest)
    else:
        print(f"unknown subcommand: {command}", file=sys.stderr)
        return 2
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
