# Workflows for GitHub Actions

## Caching With UV

Our actions have a special setup because we use self-hosted runners which are persistent
across jobs. This requires some attention on how caching and environments are set up.

References:

- https://docs.astral.sh/uv/concepts/cache/#caching
- https://docs.astral.sh/uv/configuration/environment/
- https://github.com/astral-sh/setup-uv?tab=readme-ov-file#usage

### Environment Variables

- `VIRTUAL_ENV`
  - This variable sets the path to the virtual environment. This is not a variable by uv
    but is respected by it.
  - We set this to `${{ github.workspace }}/.venv` which corresponds to the `.venv`
    directory in the repository root.
  - Virtual environments are not persistent across jobs as GitHub Actions creates a new
    `${{ github.workspace }}` for every job.
  - We still want to use a virtual environment and not install into the system Python
    environment with `UV_SYSTEM_PYTHON=1` because the system Python environment is
    persistent across jobs due to the self-hosted runner setup.
  - Uv automatically uses `VIRTUAL_ENV` for its commands (you don't have to call
    `source .venv/bin/activate` before). But not all other tools respect it.
    For example, pytest still requires the environment to be activated. We activate the
    environment by adding it to the `GITHUB_PATH` variable instead of calling
    `source .venv/bin/activate`. This is required because GitHub Actions requires that
    `source .venv/bin/activate` is called in every step as environment variables are not
    persisted across steps. By adding the environment to `GITHUB_PATH`, we can skip the
    activation in every step.
- `UV_CACHE_DIR`
  - This variable determines where uv creates its cache.
  - It is set by the `cache-local-path` setting in the `astral-sh/setup-uv` action.
  - Must be set to a directory that is persistent across jobs. We set it to
    `/tmp/setup-uv-cache` which means that the cache is persistent as long as the
    self-hosted runner is not restarted (`/tmp` is not a mounted volume).
  - We don't have to worry about the cache too much. Uv handles it automatically.
    It is also save regarding multi-threading, different uv/python versions, and minimal
    dependencies etc.
    See: https://docs.astral.sh/uv/concepts/cache/#cache-safety
  - The variable is automatically used by uv. We don't have to specify it in commands.

### Environment Information

- The environment is in `${{ github.workspace }}/.venv` which corresponds to the `.venv`
  directory in the repository root (same as for local development). The environment is
  not persistent across jobs.
- The cache is in `/tmp/setup-uv-cache` which is persistent across jobs. Restart the
  runner to clear the cache.
- Python is installed to `/gh-actions/_work/_tool/Python/3` which is persistent across
  jobs.

### astral-sh/setup-uv Action Information

- `cache-local-path` sets the cache directory (`UV_CACHE_DIR`). See `UV_CACHE_DIR` above
  for more information.
- `prune-cache: false` disables cache pruning. Cache pruning is efficient for GitHub
  hosted action runners but not for self-hosted runners.
  See: https://github.com/astral-sh/setup-uv?tab=readme-ov-file#disable-cache-pruning
- `enable_cache: true` is NOT set in the action settings. This is because we use a
  local cache. `enable_cache` only makes sense in combination with GitHub Actions
  Cache (`actions/cache`) and would upload the cache to GitHub.
- `cache-dependency-glob` is NOT set in the action settings. My understanding
  (Guarin, 10/24) is that this is also only used in combination with GitHub Actions
  Cache (`actions/cache`) and would determine when the cache is invalidated.
