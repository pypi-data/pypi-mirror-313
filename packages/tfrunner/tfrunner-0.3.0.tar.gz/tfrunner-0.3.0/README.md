# Tfrunner

Welcome to `tfrunner`, a `cli` tool to run terraform commands with the following facilities:
- Multi-project support
- Automation support
- Remote backend
- GitLab secrets pulling


## Installation

Since `tfrunner` is a `cli` tool, the recommended installation is using `pipx`.

Please ensure you have a compatible `python >= 3.12` version.

Install with: `pipx install tfrunner`


## Usage

To use it to manage multiple projects, create a `yaml` file configuring each.

Here is an example file, let's name it `tfrunner.yaml`:
```yaml
awesome-project:
  kind: gitlab # For terraform remote state backend integration
  path: ./infra/awesome-project/terraform # path relative to this config file's parent folder
  spec:
    url: "https://gitlab.com" # Your gitlab url
    state_name: awesome-state # Name of your remote terraform state
    project_id: 123456        # Identifier of the GitLab project to push state to and to load CI variables from
    token_var: GITLAB_TOKEN   # Environment variable containing gitlab token. Will be used to auto-load CI variables as ENV variables.

great-project:
  kind: gitlab
  path: ./infra/awesome-project/terraform
  spec:
    url: "https://gitlab.com"
    state_name: awesome-state
    project_id: 123456
    token_var: GITLAB_TOKEN
```

Now you can run `tfrunner` as you would run any regular `terraform` command (options are also included). You need only to be wary of two additional arguments that are needed:
- `--config_path`: path to your configuration file.
- `--project`: name of your project, as specified in your config file.

As examples, for the `great-project` in our example `tfrunner.yaml` file, you could run:
```bash
tfrunner init --config_path tfrunner.yaml --project great-project
tfrunner fmt --config_path tfrunner.yaml --project great-project
tfrunner validate --config_path tfrunner.yaml --project great-project
tfrunner plan --config_path tfrunner.yaml --project great-project
tfrunner apply --config_path tfrunner.yaml --project great-project
tfrunner destroy --config_path tfrunner.yaml --project great-project
```
