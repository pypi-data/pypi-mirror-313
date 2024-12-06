# Changelog

## v0.14.12 (released 2024-12-04)

### Features and Improvements

- add devsecops jobs NEOSDEV-163 [[71509c4](https://github.com/NEOS-Critical/neos-platform-common/commit/71509c4e9eb5380af3d18e01b21825b56a2bae09)]

### Bug fixes

- Restore support for NEOS4-HMAC algorithm validation in SignatureValidator. [[84f9ba3](https://github.com/NEOS-Critical/neos-platform-common/commit/84f9ba3eea5848265b78efdd05aa57444ea895ba)]
- dependency [[050d963](https://github.com/NEOS-Critical/neos-platform-common/commit/050d96370d3f0253d5b454ee0dbf455314d44b94)]

## v0.14.11 (released 2024-11-25)

### Bug fixes

- Allow libs to skip import errors for documentation generation [[7c8be50](https://github.com/NEOS-Critical/neos-platform-common/commit/7c8be50026b012412fff52348701910c170dad4f)]

## v0.14.10 (released 2024-11-23)

### Miscellaneous

- migrate pdoc to a package dependency [[b81efe2](https://github.com/NEOS-Critical/neos-platform-common/commit/b81efe22ac1e88170861ae4106136607746f7ef2)]

## v0.14.9 (released 2024-11-23)

### Miscellaneous

- Add hook to support generating api docs on release. [[bafb2f5](https://github.com/NEOS-Critical/neos-platform-common/commit/bafb2f55bf5bcd0a3056f5c9d8207ab8aa0b5bc3)]

## v0.14.8 (released 2024-11-18)

### Bug fixes

- Allow a larger range of jinja2 installs, pytorch doesnt support the previous version. [[9e0526d](https://github.com/NEOS-Critical/neos-platform-common/commit/9e0526d4e589c2fa8d3a6729948606e80b36dfc0)]

## v0.14.7 (released 2024-11-13)

### Features and Improvements

- Add SMTP email handler without templating. [[604936a](https://github.com/NEOS-Critical/neos-platform-common/commit/604936a73ee64f463f5f689c187c1894be141a48)]
- Add support for email contents templating with jinja2 [[423b997](https://github.com/NEOS-Critical/neos-platform-common/commit/423b997d4a1450fc699c28cf43b0215de37aca10)]

## v0.14.6 (released 2024-11-12)

### Features and Improvements

- Added contract params to update hub client request. [[9e8b4cc](https://github.com/NEOS-Critical/neos-platform-common/commit/9e8b4cc45d24e7ad2200d7b5e25d3fe714104153)]

## v0.14.5 (released 2024-10-29)

### Features and Improvements

- Create drone pipeliene [[f3cf5a9](https://github.com/NEOS-Critical/neos-platform-common/commit/f3cf5a9b7b6eb6831f553cd25e4cdfbb6b57c0ae)]
- Support session id in event emitters. [[b0e7d72](https://github.com/NEOS-Critical/neos-platform-common/commit/b0e7d72a34bb08a6995c077cafdc3f1aa62d40b8)]

### Bug fixes

- try host network in drone steps to resolve connectivity issues [[d2b0212](https://github.com/NEOS-Critical/neos-platform-common/commit/d2b0212d53d4ab865e928c655c3e2e01b2f2f7e5)]

## v0.14.4 (released 2024-09-10)

### Miscellaneous

- Use uv for build tooling. [[d22644d](https://github.com/NEOS-Critical/neos-platform-common/commit/d22644ddab49ed32c0510bce28683ac38eaf837c)]

## v0.14.3 (released 2024-08-08)

### Features and Improvements

- Pull trace id from header for timing logs, or generate one if not supplied. [[0f17119](https://github.com/NEOS-Critical/neos-platform-registry/commit/0f171199352871f122448483b9b500dbfc13af87)]

## v0.14.2 (released 2024-08-08)

### Bug fixes

- Remove assertion and replace with a robust error check in timing middleware. [[af18548](https://github.com/NEOS-Critical/neos-platform-registry/commit/af18548453c21854108b8115b201a4454c3075d1)]

## v0.14.1 (released 2024-08-08)

### Features and Improvements

- Add start logs to timing middleware [[5c2e2bb](https://github.com/NEOS-Critical/neos-platform-registry/commit/5c2e2bb14fad29324ca8aa39a16947508bbb54ae)]

### Bug fixes

- Pass through client problem responses as problem errors. [[5c6bfbe](https://github.com/NEOS-Critical/neos-platform-registry/commit/5c6bfbeb68115d18195b327f69d36249dfd385ff)]

### Miscellaneous

- Update auth-aws4 client and remove custom KeyPair class [[a49a34d](https://github.com/NEOS-Critical/neos-platform-registry/commit/a49a34d77b25d1c48a8d4958cbdd0ad2cbc215c3)]
- Upgrade changelog-gen [[74baffd](https://github.com/NEOS-Critical/neos-platform-registry/commit/74baffd07bc66425fb0eb7b6a24f002f86e60c16)]

## v0.14.0 (released 2024-06-11)

### Features and Improvements

- **Breaking:** Drop python3.9 support. [[3186ade](https://github.com/NEOS-Critical/neos-platform-registry/commit/3186ade2b4132cef42e49c1f872ab2897a61eddc)]

### Bug fixes

- Drop fastapi problem from dependencies [[58bd481](https://github.com/NEOS-Critical/neos-platform-registry/commit/58bd4817813b247c2fdd914c8b328285e7eb09a4)]

### Miscellaneous

- Add typing_extensions to dependencies for python39. [[dbb0eaf](https://github.com/NEOS-Critical/neos-platform-registry/commit/dbb0eafa0ce63becbd5332096702ef31ab244991)]

## v0.13.1 (released 2024-05-01)

### Bug fixes

- Decouple fastapi_problem from unrelated modules [[4b1fe7e](https://github.com/NEOS-Critical/neos-platform-registry/commit/4b1fe7ee06ab7d61beabb62b013f89d56968a2db)]
- Decouple fastapi_problem from unrelated modules [[a884754](https://github.com/NEOS-Critical/neos-platform-registry/commit/a884754d54f814cee61c0e51002f16607e292067)]

## v0.13.0 (released 2024-05-01)

### Miscellaneous

- **Breaking:** Migrate to fastapi-problem, the new version of web-error [[eda581d](https://github.com/NEOS-Critical/neos-platform-registry/commit/eda581d610b4cac3999b4cfeeb17e3122f71ba8b)]

## v0.12.6 (released 2024-04-19)

### Bug fixes

- Handle websocket routes in get_routes util. [[35e2b2d](https://github.com/NEOS-Critical/neos-platform-registry/commit/35e2b2dd7486d4cce842b0db9a5a46d89ce89b24)]

## v0.12.5 (released 2024-04-19)

### Bug fixes

- Dont render logic operator when no permissions are set. [[6d36b7a](https://github.com/NEOS-Critical/neos-platform-registry/commit/6d36b7a879a6e303c2d1ddcbef3f39b383e4d421)]

## v0.12.4 (released 2024-04-19)

### Features and Improvements

- Add support for extracting permissions from a FastAPI route in a view. [[9086b67](https://github.com/NEOS-Critical/neos-platform-registry/commit/9086b67ba7bb8ff288558005ec3bdaa57e30eded)]

## v0.12.3 (released 2024-04-17)

### Features and Improvements

- Extract IAM only code into iam service. [[2b02906](https://github.com/NEOS-Critical/neos-platform-registry/commit/2b0290674d8e1f04280e5f4be2025d40a601cd34)]

## v0.12.2 (released 2024-04-15)

### Features and Improvements

- Add `self` Action type. [[15efb6b](https://github.com/NEOS-Critical/neos-platform-registry/commit/15efb6b90c1657fbc1fd76f917ba7f627f8cdd01)]

## v0.12.1 (released 2024-04-15)

### Bug fixes

- Move additional dependencies to optional. [[8dafefc](https://github.com/NEOS-Critical/neos-platform-registry/commit/8dafefcd07756d8583fdecf109074b4233098b96)]

## v0.12.0 (released 2024-04-12)

### Bug fixes

- **Breaking:** Move kafka and pydantic-settings into optional extra installs. [[9c4fe16](https://github.com/NEOS-Critical/neos-platform-registry/commit/9c4fe166aab432e27b46a55605804b388ccf9ad9)]

## v0.11.7 (released 2024-04-12)

### Features and Improvements

- Support OR operations for permissions checks. [[#NEOS-6809](https://neom.atlassian.net/browse/NEOS-6809)] [[eab96ba](https://github.com/NEOS-Critical/neos-platform-registry/commit/eab96ba453a388e77f7d935b4bd70da4f3dc21ab)]

## v0.11.6 (released 2024-04-05)

### Miscellaneous

- Update keycloak library [[b4a0936](https://github.com/NEOS-Critical/neos-platform-registry/commit/b4a0936f44f46b0507e00455caf42b32ff278b5c)]

## v0.11.5 (released 2024-04-03)

### Bug fixes

- Clean up type hints for baseclass Config [[a894f62](https://github.com/NEOS-Critical/neos-platform-registry/commit/a894f625da1c1e596a0d59284bac29c26f6e46ab)]

## v0.11.4 (released 2024-04-03)

### Bug fixes

- Handle timeout errors in HttpClient and simplify configuration setup. [[#NEOS-6805](https://neom.atlassian.net/browse/NEOS-6805)] [[4f7dbb8](https://github.com/NEOS-Critical/neos-platform-registry/commit/4f7dbb817834c35edd83b30ee2a1771f746189ba)]

## v0.11.3 (released 2024-03-11)]

### Bug fixes

- Drop yoyo migrations dependency [[1a17784](https://github.com/NEOS-Critical/neos-platform-registry/commit/1a17784bb5826fb0d6aacc4299adbe1e3a00c506)]

## v0.11.2 (released 2024-03-11)]

### Bug fixes

- Clean up some additional error code mappings [[80f41de](https://github.com/NEOS-Critical/neos-platform-registry/commit/80f41def60f33bf39856f78763911c854b653b10)]

## v0.11.1 (released 2024-03-11)]

### Bug fixes

- Update web-error library [[a4c6026](https://github.com/NEOS-Critical/neos-platform-registry/commit/a4c60267958c3c3a03124a7fd6310051eff95c3d)]

## v0.11.0 (released 2024-03-11)]

### Bug fixes

- **Breaking:** Wire in changelog gen tooling, bump python version to 3.9 [[31a663d](https://github.com/NEOS-Critical/neos-platform-registry/commit/31a663dd28da317d1834a399b35b986384b21acc)]
