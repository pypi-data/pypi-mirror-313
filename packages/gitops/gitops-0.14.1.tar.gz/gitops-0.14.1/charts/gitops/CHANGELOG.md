# Changelog

## [0.13.2](https://github.com/uptick/gitops/compare/helm-v0.13.1...helm-v0.13.2) (2024-12-06)


### Bug Fixes

* change charts directory for helm ci ([105357a](https://github.com/uptick/gitops/commit/105357a831f9efdf4f743fc5abc7937aa0d266f0))
* revert our helm chart publisher action ([3f558d8](https://github.com/uptick/gitops/commit/3f558d85d631e3384a2417a20fd32f25a94fc13e))

## [0.13.1](https://github.com/uptick/gitops/compare/helm-v0.13.0...helm-v0.13.1) (2024-12-06)


### Bug Fixes

* add more memory to gitops ([3ca722f](https://github.com/uptick/gitops/commit/3ca722f1f1e03131979a4de66e17f23052a14c24))

## [0.13.0](https://github.com/uptick/gitops/compare/helm-v0.12.1...helm-v0.13.0) (2024-11-15)


### Features

* Adds sentry alerting to gitops_server ([3416398](https://github.com/uptick/gitops/commit/34163988e24bc8b679f1561bbdc8a32a82624677))
* Bump version number to 0.8.7 ([dad4a3b](https://github.com/uptick/gitops/commit/dad4a3baee106bb82801de596c4de70e5a06f3cf))
* **cli:** Added --cpu and --memory to bash/command/shell_plus to specify container resources ([93ae33c](https://github.com/uptick/gitops/commit/93ae33ccb0c2b3b4a356d55efb6a01ddd081d05e))
* **gitops_server:** Update github deployment status ([fbe8811](https://github.com/uptick/gitops/commit/fbe88119814ffd49b7713487dddb85b99e63f94e))
* **gitops-0.10.5:** add --create-namespace during install/upgrades ([c97b386](https://github.com/uptick/gitops/commit/c97b3868a67df40b2a6b312aae80d9361257ae1b))
* **helm:** Add liveness probe to helm chart ([4cec510](https://github.com/uptick/gitops/commit/4cec5100a3549c5b2562ccfc5ce09decb45c95e2))
* **helm:** Add service account to helm chart ([86d5361](https://github.com/uptick/gitops/commit/86d5361e5cd908be486dcfe238a2f8f8282e3a86))
* **helm:** Added sample values to values.yaml ([ab05d17](https://github.com/uptick/gitops/commit/ab05d1720143884db11701048217a25046c41002))
* **helm:** Modified chart to allow specifying subdomain ([63ed12e](https://github.com/uptick/gitops/commit/63ed12eeb389be9bbdb230f0586b2f4340402c8e))
* release version 0.9.20 ([9793aea](https://github.com/uptick/gitops/commit/9793aea22877ecac49a9aee1815dc0b9923fad40))
* **slack:** use external tickforge slack api to find slack user if provided ([862de0f](https://github.com/uptick/gitops/commit/862de0fcd0ab881d5c8154c530584e2c7fc5f2aa))
* **status-updater:** catch the exception around self.process_work... ([726cc05](https://github.com/uptick/gitops/commit/726cc05160b6cb1eb1cb36bb5e4555ba6bb0589f))
* swap project to uv ([91e5530](https://github.com/uptick/gitops/commit/91e5530240a344018bfa42749fe0ac8235799609))


### Bug Fixes

* :bug: Fix ingrss spec ([d585a3c](https://github.com/uptick/gitops/commit/d585a3c4783eb3a9dd4285682a2839d81f3bc531))
* **0.9.1:** Fix slack token injection ([bd1e270](https://github.com/uptick/gitops/commit/bd1e27093a2346cae648bcb1ced492ed102e9a63))
* **cli:** Fixed mcommand not working ([565ccb2](https://github.com/uptick/gitops/commit/565ccb2c7a72268a98b95594885146221a30a92b))
* correctly use NetworkingV1Api ([fc76338](https://github.com/uptick/gitops/commit/fc76338a94d349eacecc07d2d8ca543929e6d966))
* **gitops-cli:** Fixed bump to select the correct image tag ([0c93664](https://github.com/uptick/gitops/commit/0c93664f8978d58f4179f770aedfeb2e3ece15c6))
* **gitops-cli:** prevent bumping to non-existent image prefix ([5c27edf](https://github.com/uptick/gitops/commit/5c27edfdce86d1da61ed0a99ce6c3b5f86eab6ff))
