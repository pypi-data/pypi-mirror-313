lib: python_pkgs:
python_pkgs.more-itertools.overridePythonAttrs (
  _: rec {
    version = "8.14.0";
    src = lib.fetchPypi {
      pname = "more-itertools";
      inherit version;
      hash = "sha256-wJRDzT1UOLja/M2GemvBywiUOJ6Qy1PSJ0VrCwvMt1A=";
    };
  }
)
