{ lib, makes_inputs, nixpkgs, python_pkgs, python_version, }:
let
  make_bundle = commit: sha256:
    let
      raw_src = builtins.fetchTarball {
        inherit sha256;
        url =
          "https://gitlab.com/dmurciaatfluid/arch_lint/-/archive/${commit}/arch_lint-${commit}.tar";
      };
      src = import "${raw_src}/build/filter.nix" nixpkgs.nix-filter raw_src;
    in import "${raw_src}/build" {
      makesLib = makes_inputs;
      inherit nixpkgs python_version src;
    };
in {
  "v4.0.0" = make_bundle "ae3f276eb43062e1c8841a24f277bafc082e7f78"
    "0p93qazadx72gfcgaisf5n2x9dr905mwp5rsqppzqiis2afkika9";
}
