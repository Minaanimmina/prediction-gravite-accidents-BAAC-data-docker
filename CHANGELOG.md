# CHANGELOG


## v0.2.0 (2026-02-22)

### Features

- Add deliverables documentation and remove .vscode
  ([#17](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/17),
  [`375d9c5`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/375d9c56f007022a94e7b5d360d3faa41bd6c20a))

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>


## v0.1.0 (2026-02-21)

### Bug Fixes

- Fix formatting and add docstrings to backend and frontend
  ([`7c5126e`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/7c5126e9438e8fc24ddc7aafcef3fe9a8eff9d42))

- Improve Docker config with healthchecks, labels and env security
  ([#10](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/10),
  [`49c164a`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/49c164a5a905a18b926ce08bacb21ef8bc51dbd5))

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>

- Resolve merge conflicts with master
  ([`e8430ac`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/e8430ac0af6443b44addb2490756f2bcece7097e))

- Restore deleted files and correct backend imports after MVC refactor
  ([`fb9110a`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/fb9110ab61b7c48472834b0dd938ec882226bc83))

This commit fixes runtime errors introduced during the MVC refactor.

Changes include: - Restored accidentally deleted files - Fixed backend import paths - Updated
  configuration and project files to ensure the API starts correctly - Updated comment sections in
  .gitignore and .dockerignore files

The backend and frontend now run successfully in local development.

- Update Dockerfiles to use uv and fix database connection
  ([#8](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/8),
  [`e1c58e2`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/e1c58e261251a27b8922339ef89a7f1ac7686783))

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>

- Update semantic release config for master branch
  ([`90d2729`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/90d27297a6290311b8b9dd7053eb9608958b15e5))

### Code Style

- Linting corrected
  ([`9f02690`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/9f02690d81483dfe156c2ea64744763e59abd9b7))

- Remove unused import and class PredictionCreate
  ([#4](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/4),
  [`aca5f12`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/aca5f12366915bc09f2fecfd6249af92a41da709))

### Continuous Integration

- Add CI pipeline and first API tests
  ([#5](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/5),
  [`7665f2f`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/7665f2fc63e7770682da9ac2f12ccde0bc1ca2f2))

* ci: add CI pipeline and first API tests

* style: fix import sorting and formatting

* fix: resolve mypy everywhere and ruff import errors in prediction.py

* fix: resolve formatting and mypy path issues

* fix: resolve mypy import resolution for backend module

* fix: mark hardcoded bind as safe for Docker usage

* fix: configure build system for CI test imports

* fix: add missing dot in editable install command

* fix: use PYTHONPATH for test imports in CI

* fix: set PYTHONPATH inline for pytest in CI

* fix: restore build-system for editable install in CI

* ci: install package before running tests

* ci: use venv pytest directly to fix import resolution

* ci: add debug step for import resolution

* fix: stop ignoring backend/models directory and add missing files

* fix: stop ignoring ML model to fix to allow CI to load ML model

* fix: forced git to push ML model

* fix: fix formatting

---------

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>

- Add GHCR build and push workflow
  ([#9](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/9),
  [`cf5b1f6`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/cf5b1f66f51bf76e8f0b8dc30dee00a388fdbd2a))

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>

- Add manual trigger to semantic release workflow
  ([`af48885`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/af48885895afe2e3a361d0db030e361ae5aca882))

- Add master branch to all workflow triggers
  ([`1edb5e9`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/1edb5e922bd19a524c1578dfd6604bde57df05a2))

- Add semantic release config and workflow
  ([#12](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/12),
  [`e49dba0`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/e49dba0b3dc6a16c95cd996641583a870d2c750a))

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>

- Fix semantic release trigger condition
  ([`fd5e6f5`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/fd5e6f5ae12b309e43c45a87159dd8976d297f76))

### Documentation

- Update README
  ([`6d9467e`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/6d9467ef8a96d4b212d786448b1dab0106cfa0ec))

### Features

- Rewrite README with updated documentation
  ([#13](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/13),
  [`f7f3fea`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/f7f3fea3f47c1302206ed3c7aa5256333d170e82))

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>

- Rewrite README with updated documentation
  ([#14](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/14),
  [`3c8ed70`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/3c8ed70e392ddcf25f6b0eec9dad798f8b5c9609))

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>

### Refactoring

- Reorganize project into MVC structure
  ([`99e44db`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/99e44db35f7b4490e0a47b8f0356c248e57f6a5a))

### Testing

- Add API tests for default values, partial features and errors
  ([#6](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/pull/6),
  [`7a2b717`](https://github.com/Minaanimmina/prediction-gravite-accidents-BAAC-data-docker/commit/7a2b71799095b21e02295008c2ad880352dbe283))

* test: add API tests for default values, partial features and errors

* style: fix linting errors

---------

Co-authored-by: Mina Guinchard <mguinchard@afi-sa.fr>
