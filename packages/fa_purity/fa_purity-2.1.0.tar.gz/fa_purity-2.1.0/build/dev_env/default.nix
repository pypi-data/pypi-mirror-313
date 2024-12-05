{
  nixpkgs,
  dev_env,
}:
nixpkgs.mkShell {
  inherit dev_env;
  auto_conf = ./vs_settings.py;
  conf_python = nixpkgs.python311;
  packages = [dev_env];
  shellHook = ./hook.sh;
}
