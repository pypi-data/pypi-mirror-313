let
  commit = "9b7cd3a20a181ccceb75c25ee91825b0e0de3103";
  sha256 = "sha256:1wiv8fp581x5jllf4a6z3rsazqhbg0zsn9gpj4n5i3za2v2mqwlh";
in {
  makesSrc = builtins.fetchTarball {
    inherit sha256;
    url = "https://api.github.com/repos/fluidattacks/makes/tarball/${commit}";
  };
}
