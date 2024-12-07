# Changelog

## [0.15.1](https://github.com/uptick/gitops/compare/server-v0.15.0...server-v0.15.1) (2024-12-06)


### Bug Fixes

* deploy new gitops fix ([4994131](https://github.com/uptick/gitops/commit/49941316d85f320a77a3abf9f08970871f2fd3dc))

## [0.15.0](https://github.com/uptick/gitops/compare/server-v0.14.0...server-v0.15.0) (2024-12-06)


### Features

* **server:** add an updating emoji during deployments ([002d160](https://github.com/uptick/gitops/commit/002d160daa4a90ebf158cd3e0fc224cb3854baba))

## [0.14.0](https://github.com/uptick/gitops/compare/server-v0.13.0...server-v0.14.0) (2024-11-26)


### Features

* **server:** update deploy failed messages to point to grafana ([b6a90b8](https://github.com/uptick/gitops/commit/b6a90b8e4845982a71c49b3203103f55e8332e24))

## [0.13.0](https://github.com/uptick/gitops/compare/server-v0.12.1...server-v0.13.0) (2024-11-15)


### Features

* Add slack user name shaming to slack hook ([0561e29](https://github.com/uptick/gitops/commit/0561e29addb532c32d8fc9bcc623b189542c311e))
* Adds sentry alerting to gitops_server ([3416398](https://github.com/uptick/gitops/commit/34163988e24bc8b679f1561bbdc8a32a82624677))
* Continue even if sha is not found ([c450eae](https://github.com/uptick/gitops/commit/c450eaebc438ffd7028aff6ced683060e54d19a6))
* Fix startup for python 3.10 ([938f8a4](https://github.com/uptick/gitops/commit/938f8a413cd350258bb893bf4356f193447bad6e))
* **gitops_server:** Update github deployment status ([fbe8811](https://github.com/uptick/gitops/commit/fbe88119814ffd49b7713487dddb85b99e63f94e))
* **gitops-0.10.5:** add --create-namespace during install/upgrades ([c97b386](https://github.com/uptick/gitops/commit/c97b3868a67df40b2a6b312aae80d9361257ae1b))
* **healthcheck:** Add health check endpoint which doesn't show up in logs ([07335f0](https://github.com/uptick/gitops/commit/07335f01ac9b2d3df75ebf5f4ff7dbc5ce39cb40))
* Limit helm history to 3 ([5d2856c](https://github.com/uptick/gitops/commit/5d2856c7af35b0ce5a66f26a5ad44e5b0b2d3a95))
* **logs:** Add timestamps to logs ([0f3f09d](https://github.com/uptick/gitops/commit/0f3f09dddd4d6287d2ed8ddcbea316c0cbe92bc7))
* **server:** Deploy servers into specific namespaces ([1fed618](https://github.com/uptick/gitops/commit/1fed6186a1d47a19faf93ba8848a52a000c7e1a6))
* **slack:** use external tickforge slack api to find slack user if provided ([862de0f](https://github.com/uptick/gitops/commit/862de0fcd0ab881d5c8154c530584e2c7fc5f2aa))
* **status-updater:** catch the exception around self.process_work... ([726cc05](https://github.com/uptick/gitops/commit/726cc05160b6cb1eb1cb36bb5e4555ba6bb0589f))
* Use helm-secrets for extra decryption ([025fcc7](https://github.com/uptick/gitops/commit/025fcc7996ac1f01aededf1a721cb6297b89872e))


### Bug Fixes

* **0.9.1:** Fix slack token injection ([bd1e270](https://github.com/uptick/gitops/commit/bd1e27093a2346cae648bcb1ced492ed102e9a63))
* async run should not default to exit code of 1 ([3495a72](https://github.com/uptick/gitops/commit/3495a7214c39f948bcef1b9577fbfb03a15ae887))
* correctly use NetworkingV1Api ([fc76338](https://github.com/uptick/gitops/commit/fc76338a94d349eacecc07d2d8ca543929e6d966))
* **deploy:** Fix httpx post request ([ba34cf4](https://github.com/uptick/gitops/commit/ba34cf4076b32f8246445cc58b4335d40a03ea60))
* fix broken semaphore env parsing ([cad0239](https://github.com/uptick/gitops/commit/cad0239128fb4867e0567783df868ad0bf86e091))
* **gitop-server:** Use json patch to update deployment status ([df69596](https://github.com/uptick/gitops/commit/df695968a1327da77e70cda0330364e08889fa25))
* gitops ingress update for eks 1.22+ ([d23dc35](https://github.com/uptick/gitops/commit/d23dc35bad0ab6b1d6faa93f97e3a18f1c2db973))
* **gitops_server:** Fix uninstall not removing apps ([f30e90e](https://github.com/uptick/gitops/commit/f30e90e961386d4f46257ac572ced6eacae5883c))
* **gitops_server:** treat suspended servers as removed ([743abaa](https://github.com/uptick/gitops/commit/743abaa231817de2903ec7a6e7c03be68a0ddfea))
* **gitops-server:** Don't raise exception if deployment doesn't exist ([91f11b8](https://github.com/uptick/gitops/commit/91f11b859e67074c8066470e3ab9b981f5816f00))
* **server:** fix checking out branch refs for charts ([35c0fb4](https://github.com/uptick/gitops/commit/35c0fb448480306dad153f6c7dd1c889469241b9))
* **slack:** forgot to await slack user ([f9b923f](https://github.com/uptick/gitops/commit/f9b923f3a8716e5523d8fb3654bcee8e1b21d515))


### Dependencies

* Bumped uvicorn and mypy ([be74598](https://github.com/uptick/gitops/commit/be74598a5c34c67d006613ae033910e763522be3))
