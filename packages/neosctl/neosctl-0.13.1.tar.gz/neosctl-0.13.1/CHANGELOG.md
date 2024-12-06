# Changelog

## v0.13.1 (released 2024-12-03)

### Miscellaneous

- Remove deprecated registry, auth and profile commands. [[57b54f0](https://github.com/NEOS-Critical/neos-platform-cli/commit/57b54f0c346fdb0586e4f17f877f6a7b5ea4c6d7)]

## v0.13.0 (released 2024-12-03)

### Miscellaneous

- Remove backwards compatibility work arounds. [[fdc4656](https://github.com/NEOS-Critical/neos-platform-cli/commit/fdc46560caaf5351f0a3b35a25c1c010cc247e25)]

## v0.12.31 (released 2024-11-28)

### Bug fixes

- Support new publish request format in gateway. [[a44e615](https://github.com/NEOS-Critical/neos-platform-cli/commit/a44e6151dd0ec23b491d15a91780fb623b35b7fb)]
- Typo fix [[d9d4ec8](https://github.com/NEOS-Critical/neos-platform-cli/commit/d9d4ec856b071b3d0d8350d997d984f3ecf315cf)]

## v0.12.30 (released 2024-09-12)

### Bug fixes

- Fix env `whoami` command description [[f4fd248](https://github.com/NEOS-Critical/neos-platform-cli/commit/f4fd248122c6c28f03cf1ccc24fcce605b966b04)]

### Miscellaneous

- Migrate from poetry to uv for dependency and build management [[021f381](https://github.com/NEOS-Critical/neos-platform-cli/commit/021f3813dd8b24805d0c9e35cf5d68d399a636a1)]
- Update aws4 lib [[e15ba58](https://github.com/NEOS-Critical/neos-platform-cli/commit/e15ba587248563f28857f6c0c3573202f85c1c5e)]

## v0.12.29 (released 2024-07-30)

### Miscellaneous

- Update aws4 with bugfix. [[4e98473](https://github.com/NEOS-Critical/neos-platform-cli/commit/4e9847391f5215b2aef468930cd63dbe1cfba255)]

## v0.12.28 (released 2024-07-30)

### Miscellaneous

- Use auth-aws4 [[64c2b5d](https://github.com/NEOS-Critical/neos-platform-cli/commit/64c2b5ddd09aa38d11136ad88baeacdc61dc502a)]

## v0.12.27 (released 2024-07-19)

### Bug fixes

- Use correct syntax for python3.9 [[e7dcfb0](https://github.com/NEOS-Critical/neos-platform-cli/commit/e7dcfb06b0891c7ab0a233abadd82659e06cb61b)]

## v0.12.26 (released 2024-07-17)

### Miscellaneous

- Update changelog tool [[5c8e5cd](https://github.com/NEOS-Critical/neos-platform-cli/commit/5c8e5cd8cdf3c90e6c15663d38c8e26ec1c763e7)]

## v0.12.25 (released 2024-07-11)

### Features and Improvements

- Add support for proxy configuration for requests. [[d6d6907](https://github.com/NEOS-Critical/neos-platform-cli/commit/d6d690726e0277dfd6baa873580b158e863654bf)]

## v0.12.24 (released 2024-04-26)

### Bug fixes

- Extract nested entities in gateway requests [[7afb620](https://github.com/NEOS-Critical/neos-platform-cli/commit/7afb620d3a052509a02e4192f51445ee3f436d9e)]

## v0.12.23 (released 2024-04-26)

### Features and Improvements

- Add fields filter to all commands that have an output. [[9f021e7](https://github.com/NEOS-Critical/neos-platform-cli/commit/9f021e7b459fe49b89ba9151ea437f7651b62915)]

## v0.12.22 (released 2024-04-26)

### Bug fixes

- Update info commands to use __neos endpoints. [[82e3762](https://github.com/NEOS-Critical/neos-platform-cli/commit/82e376223f49b19abb88ff39d3d5a74ae501958e)]

## v0.12.21 (released 2024-04-19)

### Features and Improvements

- Add `neosctl info` subcommand with version, permission and error-cores [[0cbbc4c](https://github.com/NEOS-Critical/neos-platform-cli/commit/0cbbc4ca2be66eddfca440a3c2d1692584ab0e81)]

## v0.12.20 (released 2024-04-18)

### Bug fixes

- Drop neos_common dependency, implement http and signer locally. [[7a0eec6](https://github.com/NEOS-Critical/neos-platform-cli/commit/7a0eec6ad03e4980f173c1b8ee44c44fd04adffc)]

## v0.12.19 (released 2024-04-17)

### Features and Improvements

- Add output format option to all service commands. [[10c8860](https://github.com/NEOS-Critical/neos-platform-cli/commit/10c886053529abd203e8a4f6d57e066ba806a8d7)]

## v0.12.18 (released 2024-04-17)

### Documentation

- Update README with environment commands. [[850b868](https://github.com/NEOS-Critical/neos-platform-cli/commit/850b868d9d837bca368ca10c75f5b1369ad391b4)]

## v0.12.17 (released 2024-04-16)

### Bug fixes

- Remove need for sign/no-sign on whoami [[d48ddad](https://github.com/NEOS-Critical/neos-platform-cli/commit/d48ddad7015eba102869535374c6bb5ac754b436)]
- Neaten up iam and registry modules. [[69a79f2](https://github.com/NEOS-Critical/neos-platform-cli/commit/69a79f2309dae38e906d1aee15f47cb2c424eb3e)]
- Raise on env override if not found. [[380e55c](https://github.com/NEOS-Critical/neos-platform-cli/commit/380e55c7e34c41fd15d0693840c01d1c54416922)]
- Add env override flag for quick toggle [[2a023a2](https://github.com/NEOS-Critical/neos-platform-cli/commit/2a023a2bef11ffc56d39fa28338d6f5adc438a68)]
- Allow fetching current user information. [[cfe81e2](https://github.com/NEOS-Critical/neos-platform-cli/commit/cfe81e23e1cd956533311d7f226bc48c29d164da)]

## v0.12.13 (released 2024-04-15)

### Bug fixes

- Pin to simpler neos-common with optional extras. [[deee0a5](https://github.com/NEOS-Critical/neos-platform-cli/commit/deee0a5495838c79e37718ca247a9ae3855a018a)]

## v0.12.12 (released 2024-04-12)

### Bug fixes

- Drop unused kafka dependency from neos-common [[e2f8d95](https://github.com/NEOS-Critical/neos-platform-cli/commit/e2f8d9585b5a2ff1f4d34db8b04d8a10ec931f07)]

## v0.12.11 (released 2024-04-12)

### Bug fixes

- Issue where a default profile was required when an env was activated. [[3808ed1](https://github.com/NEOS-Critical/neos-platform-cli/commit/3808ed13c6303ef56048e1320bdef81b87227a78)]

## v0.12.10 (released 2024-04-12)

### Bug fixes

- Pull all configuration from active_env if available. [[6279600](https://github.com/NEOS-Critical/neos-platform-cli/commit/62796007bba030786526d2e1bf916017706ea744)]

## v0.12.9 (released 2024-04-12)

### Features and Improvements

- Cache environment cores on activation, support per call override of active core. [#NEOS-6810](https://neom.atlassian.net/browse/NEOS-6810) [d3f78d0](https://github.com/NEOS-Critical/neos-platform-cli/commit/d3f78d0c8115aba75ac438952da529cb46d5e497)

## v0.12.8 (released 2024-04-11)

### Bug fixes

- Add rich to requirements [8f322da](https://github.com/NEOS-Critical/neos-platform-cli/commit/8f322da5c8336b68ec4e40646822d66accf1ec8a)
- Deprecate top level registry commands in favour of nested commands. [97c7878](https://github.com/NEOS-Critical/neos-platform-cli/commit/97c78783fabc9ebe12083bfbcf84f19cc786d466)

## v0.12.7 (released 2024-04-11)

### Features and Improvements

- Simplify configuration with environments rather than per core profiles. [#NEOS-6806](https://neom.atlassian.net/browse/NEOS-6806) [9200893](https://github.com/NEOS-Critical/neos-platform-cli/commit/92008933e8c21e2cc6cdaecaf5332fc75e85d70d)

## v0.12.6 (released 2024-04-10)

### Bug fixes

- Extract response data from storage before closing the connection. [b9338d2](https://github.com/NEOS-Critical/neos-platform-cli/commit/b9338d2b27634e251c8a2968f3f30a5022df7eb4)

## v0.12.5 (released 2024-04-05)

### Bug fixes

- Add in verbosity flag for all commands [4f6111b](https://github.com/NEOS-Critical/neos-platform-cli/commit/4f6111b307e54eca7b337cce4d479dce612751b2)

## v0.12.4 (released 2024-04-05)

### Miscellaneous

- Update neos-common and keycloak library [a392cbc](https://github.com/NEOS-Critical/neos-platform-cli/commit/a392cbc0004efb330e06c6856dd71fb2198b40cb)
- Update common library with timeout handling. [41d6688](https://github.com/NEOS-Critical/neos-platform-cli/commit/41d66885fa93c3eed34cdc7a1543374f2164da96)

## v0.12.3 (released 2024-03-20)

### Bug fixes

- Update package description [3a28783](https://github.com/NEOS-Critical/neos-platform-cli/commit/3a28783137daed3352bcfd348cedf394b6b242ec)

## v0.12.2 (released 2024-03-20)

## v0.12.1 (released 2024-03-11)]

### Bug fixes

- Handle updated error response formats [[6bbf26d](https://github.com/NEOS-Critical/neos-platform-cli/commit/6bbf26d6b82a6a6cf1730fd8057db8fe4c7de471)]

## v0.12.0 (released 2024-03-11)]

### Bug fixes

- **Breaking:** Wire in changelog gen, minimum python version bumped to 3.9 [[2483b96](https://github.com/NEOS-Critical/neos-platform-cli/commit/2483b9617d7edbd52b45aea2bedfbd2fe66f7c29)]
- Update neos common library [[389e166](https://github.com/NEOS-Critical/neos-platform-cli/commit/389e16619042eb8162ee8d5b627b4b6143859462)]
