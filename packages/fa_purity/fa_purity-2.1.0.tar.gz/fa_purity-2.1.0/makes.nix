# https://github.com/fluidattacks/makes
{
  cache = {
    readNixos = true;
    extra = {
      fa-foss = {
        enable = true;
        pubKey = "fa-foss.cachix.org-1:RoFAjJdHUUFrNAfbaLFqvFQVfmNmyMMAorl7j2VqV9M=";
        type = "cachix";
        token = "CACHIX_AUTH_TOKEN";
        url = "https://fa-foss.cachix.org";
        write = true;
      };
    };
  };
  formatBash = {
    enable = true;
    targets = ["/"];
  };
  formatNix = {
    enable = true;
    targets = ["/"];
  };
  formatPython = {
    default = {
      targets = ["/"];
    };
  };
  lintBash = {
    enable = true;
    targets = ["/"];
  };
  lintNix = {
    enable = true;
    targets = ["/"];
  };
}
