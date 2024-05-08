{ pkgs, lib, config, inputs, ... }:

{
  # See full reference at https://devenv.sh/reference/options/

  packages = [
    pkgs.go-task
  ];

  languages.python = {
      enable = true;
      version = "3.12.2";
      venv = {
        enable = true;
        requirements = ./requirements.txt;
      };
  };
}
