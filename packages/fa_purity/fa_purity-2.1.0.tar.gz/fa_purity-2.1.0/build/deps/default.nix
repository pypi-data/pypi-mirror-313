{
  nixpkgs,
  python_version,
  makesLib,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    inherit (nixpkgs."${python_version}".pkgs) buildPythonPackage;
    inherit (nixpkgs.python3Packages) fetchPypi;
  };

  utils = makesLib.pythonOverrideUtils;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;

  layer_1 = python_pkgs:
    python_pkgs
    // {
      arch-lint = let
        result = import ./arch_lint.nix {
          inherit lib nixpkgs python_pkgs python_version;
          makes_inputs = makesLib;
        };
      in result."v4.0.0".pkg;
      more-itertools = import ./more-itertools.nix lib python_pkgs;
      types-deprecated = import ./deprecated/stubs.nix lib;
      types-simplejson = import ./simplejson/stubs.nix lib;
    };
  python_pkgs = utils.compose [layer_1] nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
