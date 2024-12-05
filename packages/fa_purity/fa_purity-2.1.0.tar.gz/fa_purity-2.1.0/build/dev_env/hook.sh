# shellcheck shell=bash

mkdir -p ./.vscode \
  && "${conf_python}/bin/python" "${auto_conf}" ./.vscode/settings.json "${dev_env}"
