# CHANGELOG

## 0.3.3 (2024-12-03)

- [Feature] During deployment, file size is verified before uploading the project to make sure it doesn't exceed the maximum amount.
- [Fix] Updated PostHog API key

## 0.3.2 (2024-11-11)

- [Feature] New Warning if an environment variable matches a secret with a different casing (lower/upper)
- [Feature] New Warning if environment variables used in the previous deployment are missing

## 0.3.1 (2024-11-05)

- [Feature] Add `ploomber-cloud start --project-id PROJECT_ID` to start a stopped app
- [Feature] Add `ploomber-cloud stop --project-id PROJECT_ID` to stop an app

## 0.3.0 (2024-10-07)

- [API Change] `ploomber-cloud init --from-existing` now downloads the project in ./project_id/. Use `ploomber-cloud init --from-existing --only-config` for previous behavior  (only downloading the ploomber-cloud.json config file)

## 0.2.20 (2024-09-30)

- [Fix] `ploomber-cloud auth --add --feature={feature}` will throw an error for features not allowed for the user.

## 0.2.19 (2024-09-24)

- [Feature] `ploomber-cloud auth --add --feature={feature}` will add authentication to features that support it
- [Feature] `ploomber-cloud auth --remove --feature={feature}` will remove authentication to features that support it

## 0.2.18 (2024-08-12)

- [Fix] Fixes outdated pricing spec

## 0.2.17 (2024-08-05)

- [Feature] `ploomber-cloud labels --sync` will update the local config with the latest labels from the UI

## 0.2.16 (2024-07-29)

- [Feature] Add support for `ignore` field in `ploomber-cloud.json`
- [Fix] Removes importlib_resources

## 0.2.15 (2024-06-25)

- [Feature] Add ploomber-cloud logs command

## 0.2.14 (2024-06-20)

- [Fix] Minor improvements to Auth0 template workflow
- [Fix] Improvements to `examples` command

## 0.2.13 (2024-06-07)

- [Fix] Updating Auth0 template due to new env variable requirement

## 0.2.12 (2024-06-04)

- [Fix] Upgrades vLLM template

## 0.2.11 (2024-05-29)

- [Feature] Better confirmation message when deleting all projects

## 0.2.10 (2024-05-26)

- [Feature] Add native support for Chainlit applications

## 0.2.9 (2024-05-21)

- [Feature] show custom ID when using `--from-existing`.

## 0.2.8 (2024-05-15)

- [Feature] Add support for Flask applications

## 0.2.7 (2024-05-08)

- [Feature] Add `--clear-cache` option to `ploomber-cloud examples`.

## 0.2.6 (2024-05-03)

- [Feature] Allow switching the config file to use via `--config/-c` in `init`, `deploy`, `templates`, `resources`, and `labels` subcommands

## 0.2.5 (2024-05-02)

- [Feature] Add `--watch-incremental` option to `ploomber-cloud deploy`.

## 0.2.4 (2024-05-02)

- [Feature] Allow deploying secrets using `secret-keys` in `ploomber-cloud.json`

## 0.2.3 (2024-04-26)

- [Feature] Add `ploomber-cloud labels` for adding or deleting labels of the project.

## 0.2.2 (2024-04-26)

- [Feature] Better validation when running `ploomber-cloud templates auth0`
- [Feature] Automatically generated `AUTH_SCRET` when using `ploomber-cloud templates auth0`

## 0.2.1 (2024-04-25)

- [Feature] Handles 500 errors
- [Feature] Add `ploomber-cloud templates auth0`

## 0.2.0 (2024-04-22)

- [Feature] Add `ploomber-cloud resources` to enable custom resources

## 0.1.29 (2024-04-17)

- [Fix] Improve output message for the delete command

## 0.1.28 (2024-04-16)

- [Fix] Clearer error message when missing API key

## 0.1.27 (2024-04-15)

- [Feature] Better message for using `--force` with `--from-existing`

## 0.1.26 (2024-04-12)

- [Feature] Add `gpu` key to `ploomber-cloud.json`
- [Feature] Add `ploomber-cloud templates vllm`

## 0.1.25 (2024-04-11)

- [Feature] Add watch as a separate command

## 0.1.24 (2024-04-08)

- [Feature] Delete: add project_id optional argument and --all option

## 0.1.23 (2024-04-04)

- [Feature] Pinning `cloudpickle==3.0.0`
- [Feature] Increase default timeout to 5 minutes
- [Feature] Adds `pdf_scanned_to_text`

## 0.1.22 (2024-04-04)

- [Feature] Updates API calls to `[@functions](https://github.com/functions).serverless`

## 0.1.21 (2024-04-04)

- [Feature] Fixed issue when calling the `pdf_to_text` function

## 0.1.20 (2024-04-02)

- [Feature] Add `[@functions](https://github.com/functions).serverless`

## 0.1.19 (2024-03-29)

- [Fix] Rename `env_variables` to `secrets` ([#64](https://github.com/ploomber/ploomber-cloud/issues/64))

## 0.1.18 (2024-03-26)

- [Feature] Add `functions.{pdf_to_text, image_to_text, get_result}`

## 0.1.17 (2024-03-20)

- [Feature] Add `delete` to delete a project ([#41](https://github.com/ploomber/ploomber-cloud/issues/41))
- [Feature] Allow deploying examples from docker ([#61](https://github.com/ploomber/ploomber-cloud/issues/61))

## 0.1.16 (2024-03-11)

- [Feature] Add `pc` as a CLI shortcut for `ploomber-cloud`

## 0.1.15 (2024-03-11)

- [Feature] Deploy `--watch` shows logs ([#38](https://github.com/ploomber/ploomber-cloud/issues/38))

## 0.1.14 (2024-03-07)

- [Feature] Add support for Dash applications ([#58](https://github.com/ploomber/ploomber-cloud/issues/58))
- [Fix] More informative error messages for Ploomber Cloud exceptions ([#55](https://github.com/ploomber/ploomber-cloud/issues/55))
- [Fix] Add smarter project detection for Docker types with informative message ([#47](https://github.com/ploomber/ploomber-cloud/issues/47))

## 0.1.13 (2024-03-04)

- [Feature] Add `ploomber-cloud examples` for downloading example apps ([#36](https://github.com/ploomber/ploomber-cloud/issues/36))

## 0.1.12 (2024-03-04)

- [Feature] Add support for Voila applications ([#50](https://github.com/ploomber/ploomber-cloud/issues/50))

## 0.1.11 (2024-02-27)

- [Feature] Add support for Shiny-R applications ([#51](https://github.com/ploomber/ploomber-cloud/issues/51))

## 0.1.10 (2024-02-16)

- [Feature] Adds anonymous telemetry
- [Feature] Add smarter project detection ([#40](https://github.com/ploomber/ploomber-cloud/issues/40))

## 0.1.9 (2024-02-01)

- [Feature] Add support for Solara applications ([#31](https://github.com/ploomber/ploomber-cloud/issues/31))

## 0.1.8 (2024-01-31)

- [Feature] Add support for secrets via `.env` file ([#26](https://github.com/ploomber/ploomber-cloud/issues/26))
- [Fix] Shorter error when trying to deploy a project that hasn't been initialized
- [Fix] Changed deployment link from `dashboards` to `applications` ([#34](https://github.com/ploomber/ploomber-cloud/issues/34))

## 0.1.7 (2024-01-24)

- [Fix] Checking HTTP code (404) to decide which error message to display

## 0.1.6 (2024-01-23)

- [Feature] Add `github` for creating or updating the GitHub actions file `.github/workflows/ploomber-cloud.yaml` in repository.

## 0.1.5 (2024-01-09)

- [Fix] Fix issue when using `--watch` ([#20](https://github.com/ploomber/ploomber-cloud/issues/20))

## 0.1.4 (2023-12-20)

- [Feature] Add `--force` option to init to re-initialize a project and override the existing `ploomber-cloud.json` file
- [Feature] Add `--version`
- [Fix] Updates API header from `access_token` to `api_key`

## 0.1.3 (2023-12-14)

- [Feature] Add `ploomber-cloud deploy --watch` to watch deploy status from CLI ([#11](https://github.com/ploomber/ploomber-cloud/issues/11))

## 0.1.2 (2023-12-11)

- [Feature] Allow `init` to initialize an existing project

## 0.1.1 (2023-11-17)

- [Feature] Read key from `PLOOMBER_CLOUD_KEY` environment variable, if set

## 0.1.0 (2023-11-17)

- [Feature] Add `ploomber-cloud key` command to set key
- [Feature] Add `ploomber-cloud init` to configure a project
- [Feature] Add `ploomber-cloud deploy` to deploy a project
