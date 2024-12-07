# Changelog

## [0.14.1](https://github.com/uptick/gitops/compare/cli-v0.14.0...cli-v0.14.1) (2024-12-06)


### Bug Fixes

* change charts directory for helm ci ([105357a](https://github.com/uptick/gitops/commit/105357a831f9efdf4f743fc5abc7937aa0d266f0))
* revert our helm chart publisher action ([3f558d8](https://github.com/uptick/gitops/commit/3f558d85d631e3384a2417a20fd32f25a94fc13e))

## [0.14.0](https://github.com/uptick/gitops/compare/cli-v0.13.2...cli-v0.14.0) (2024-12-06)


### Features

* **server:** add an updating emoji during deployments ([002d160](https://github.com/uptick/gitops/commit/002d160daa4a90ebf158cd3e0fc224cb3854baba))

## [0.13.2](https://github.com/uptick/gitops/compare/cli-v0.13.1...cli-v0.13.2) (2024-12-05)


### Bug Fixes

* fix release-please pipeline for cli ([823eed7](https://github.com/uptick/gitops/commit/823eed79a8654f91f0bf521f70a63ae31d09e228))

## [0.13.1](https://github.com/uptick/gitops/compare/cli-v0.13.0...cli-v0.13.1) (2024-12-05)


### Bug Fixes

* fix gitops bump for cross account ([d3394e3](https://github.com/uptick/gitops/commit/d3394e3214d104c323fb397d885c118a36075b5b))

## [0.13.0](https://github.com/uptick/gitops/compare/cli-v0.12.1...cli-v0.13.0) (2024-11-15)


### Features

* **0.8.1:** ADded gitops db.wipe-db to delete a tenant db ([d585cf3](https://github.com/uptick/gitops/commit/d585cf357818007d27cd9e7284ba7677404cc200))
* **0.8.5:** Added a confirmation to gitops bash/sp when run against production environment ([f65057e](https://github.com/uptick/gitops/commit/f65057ef337a6fe34f3510c889c2284c1fdb7218))
* **0.9.7:** Bump other repos ([45bc035](https://github.com/uptick/gitops/commit/45bc0359d090897e2c99b7dbb650392d37069086))
* Add ability to gitops bash with a serviceAccount ([c305e03](https://github.com/uptick/gitops/commit/c305e03a253786cc9eed12b116af4f844e7161bc))
* Add gitops.db-pgcli as a command ([665bcae](https://github.com/uptick/gitops/commit/665bcae9a2018d2c7c108d14a9958501040d23af))
* Adds sentry alerting to gitops_server ([3416398](https://github.com/uptick/gitops/commit/34163988e24bc8b679f1561bbdc8a32a82624677))
* allow gitops db.proxy to work with RDS IAM Access ([0e91586](https://github.com/uptick/gitops/commit/0e9158690f0299bd9171648486d6ce3152c411cc))
* Be able to bump other repos ([3b8a79e](https://github.com/uptick/gitops/commit/3b8a79e138609361b6d1b8af6b4b1e2154ad2ca1))
* Bump the version to 0.9.8 in the __init__.py file ([f0a91de](https://github.com/uptick/gitops/commit/f0a91decb6776c2b64d42855ef5e9c0cf6d96633))
* Bump version number to 0.8.7 ([dad4a3b](https://github.com/uptick/gitops/commit/dad4a3baee106bb82801de596c4de70e5a06f3cf))
* **bump:** When bumping --push, pull first ([5df0ee0](https://github.com/uptick/gitops/commit/5df0ee03ecd9ba67e97d09a16fcee7d18eea4ad6))
* **cli:** Added --cpu and --memory to bash/command/shell_plus to specify container resources ([93ae33c](https://github.com/uptick/gitops/commit/93ae33ccb0c2b3b4a356d55efb6a01ddd081d05e))
* **cli:** efficiently find latest image using prefix search for latest image tag ([a6d8be1](https://github.com/uptick/gitops/commit/a6d8be1eb5db2dcae2527b8e07cc71e993d8c7ec))
* **cli:** Enforce namespace as a required param for App ([28ee089](https://github.com/uptick/gitops/commit/28ee0891ae864faf907038c0a8052d96f16371b3))
* **cli:** Update commands to use the apps namespace ([38cecf7](https://github.com/uptick/gitops/commit/38cecf7a4ff6be270a6fa37e920bcf3df73d84e8))
* **db:** Add gb.rds-logs to fetch rds logs ([604aa73](https://github.com/uptick/gitops/commit/604aa73a5d176badd07d4a2146aa81a261cc304c))
* Gitops bump works for repos without a prefix ([d417e61](https://github.com/uptick/gitops/commit/d417e61fd165276991bd8f28dd5b070f357296a2))
* **gitops_server:** Update github deployment status ([fbe8811](https://github.com/uptick/gitops/commit/fbe88119814ffd49b7713487dddb85b99e63f94e))
* **gitops-0.10.5:** add --create-namespace during install/upgrades ([c97b386](https://github.com/uptick/gitops/commit/c97b3868a67df40b2a6b312aae80d9361257ae1b))
* **gitops-cli:** Add a minimum gitops version check ([5cff7ae](https://github.com/uptick/gitops/commit/5cff7aeb60edcc6a2413361ac6c7b5dd46c8de79))
* **gitops:** expose App, get_app_details, get_apps as top level interfaces ([626466a](https://github.com/uptick/gitops/commit/626466a5034c532995e41b0cf476f182bb3679f0))
* **gitops:** makes gitops db.pgcli more robust ([fb4fbcb](https://github.com/uptick/gitops/commit/fb4fbcb38166bdef1d119c2ecbebf61592f4f79d))
* **helm:** Add service account to helm chart ([86d5361](https://github.com/uptick/gitops/commit/86d5361e5cd908be486dcfe238a2f8f8282e3a86))
* **helm:** Modified chart to allow specifying subdomain ([63ed12e](https://github.com/uptick/gitops/commit/63ed12eeb389be9bbdb230f0586b2f4340402c8e))
* release version 0.9.20 ([9793aea](https://github.com/uptick/gitops/commit/9793aea22877ecac49a9aee1815dc0b9923fad40))
* **slack:** use external tickforge slack api to find slack user if provided ([862de0f](https://github.com/uptick/gitops/commit/862de0fcd0ab881d5c8154c530584e2c7fc5f2aa))
* **status-updater:** catch the exception around self.process_work... ([726cc05](https://github.com/uptick/gitops/commit/726cc05160b6cb1eb1cb36bb5e4555ba6bb0589f))
* swap project to uv ([91e5530](https://github.com/uptick/gitops/commit/91e5530240a344018bfa42749fe0ac8235799609))
* Use helm-secrets for extra decryption ([025fcc7](https://github.com/uptick/gitops/commit/025fcc7996ac1f01aededf1a721cb6297b89872e))
* Use release-please ([0324a14](https://github.com/uptick/gitops/commit/0324a148d3b7c1df47cadf8345dd42dd20906914))


### Bug Fixes

* :art: Fix linting ([e31ae69](https://github.com/uptick/gitops/commit/e31ae693687871a00959463586ff1e6924897b77))
* :bug: Fix issue [#64](https://github.com/uptick/gitops/issues/64) ([e1f3b45](https://github.com/uptick/gitops/commit/e1f3b45d0b82ab71f009eea5f9da6c8ad34adbc5))
* **0.9.1:** Fix slack token injection ([bd1e270](https://github.com/uptick/gitops/commit/bd1e27093a2346cae648bcb1ced492ed102e9a63))
* async run should not default to exit code of 1 ([3495a72](https://github.com/uptick/gitops/commit/3495a7214c39f948bcef1b9577fbfb03a15ae887))
* **bump:** exclude only if the image tag ends with -latest ([742ccd3](https://github.com/uptick/gitops/commit/742ccd349fc8c0cb1812c41b374aa1ceda4cb8cd))
* **cli:** Fixed bump --push command being broken ([2d264d7](https://github.com/uptick/gitops/commit/2d264d7e082261cf3ce6a08593e53ceeb4149c65))
* **cli:** Fixed mcommand not working ([565ccb2](https://github.com/uptick/gitops/commit/565ccb2c7a72268a98b95594885146221a30a92b))
* **cli:** Rename gitops db.rds-logs to gitops db.logs ([4104059](https://github.com/uptick/gitops/commit/4104059a8b1a90a394d0a218581bd7474c91f95b))
* correctly inject the availability zone for db commands ([db4610d](https://github.com/uptick/gitops/commit/db4610d75df1cb6520add97d43a946957b808495))
* correctly use NetworkingV1Api ([fc76338](https://github.com/uptick/gitops/commit/fc76338a94d349eacecc07d2d8ca543929e6d966))
* **db-proxy:** Db proxy fixed for database urls without ports ([fb20f96](https://github.com/uptick/gitops/commit/fb20f9691acbfd68abff653af532d1b86fd9baf7))
* **deploy:** Fix httpx post request ([ba34cf4](https://github.com/uptick/gitops/commit/ba34cf4076b32f8246445cc58b4335d40a03ea60))
* fix unsetenv to tolerate `environment: null` ([cb21e26](https://github.com/uptick/gitops/commit/cb21e268d1a80d47bdb62c439be558c9f39fbe3d))
* **gitop-server:** Use json patch to update deployment status ([df69596](https://github.com/uptick/gitops/commit/df695968a1327da77e70cda0330364e08889fa25))
* **gitops_cli:** Removed more usages of App as a dict ([ffa6529](https://github.com/uptick/gitops/commit/ffa65293edae9d33100aceb4c6fa6b1fc011d801))
* **gitops-cli:** Fixed bump to select the correct image tag ([0c93664](https://github.com/uptick/gitops/commit/0c93664f8978d58f4179f770aedfeb2e3ece15c6))
* **gitops-cli:** make error message more useful ([41b3777](https://github.com/uptick/gitops/commit/41b37770dae923b577dc226f22e49daf97a49957))
* **gitops-cli:** Output warning message to stderr ([f09e588](https://github.com/uptick/gitops/commit/f09e588af2ca5f9c853ed7301b9b9ece83722ac1))
* **gitops-cli:** prevent bumping to non-existent image prefix ([5c27edf](https://github.com/uptick/gitops/commit/5c27edfdce86d1da61ed0a99ce6c3b5f86eab6ff))
* **gitops-server:** Don't raise exception if deployment doesn't exist ([91f11b8](https://github.com/uptick/gitops/commit/91f11b859e67074c8066470e3ab9b981f5816f00))
* **server:** fix checking out branch refs for charts ([35c0fb4](https://github.com/uptick/gitops/commit/35c0fb448480306dad153f6c7dd1c889469241b9))


### Dependencies

* Added black and updated lockfile ([62367fa](https://github.com/uptick/gitops/commit/62367fab35f502a3205bccf7fcc1c565d9a51613))
* Bumped uvicorn and mypy ([be74598](https://github.com/uptick/gitops/commit/be74598a5c34c67d006613ae033910e763522be3))
