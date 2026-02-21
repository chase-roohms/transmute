# Contributing

First off, thank you for your interest in contributing ❤️

This project is intended to be a reliable, self-hosted tool, and contributions of all kinds are welcome: code, documentation, bug reports, ideas, and feedback.

---

## Ways to Contribute

You can help by:

* Reporting bugs
* Suggesting features or improvements
* Improving documentation
* Adding new converters
* Fixing issues
* Reviewing pull requests

If you are unsure where to start, check the open issues or look for issues labeled `good first issue`.

---

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/transmute-app/transmute.git
cd <repo>
```

### 2. Install Python dependencies

`pip3 install requirements.txt`

### 3. Spin up the app locally

`python3 backend/main.py`

Feel free to reach out via issue if you hit any snags here ^

### 4. Create a Branch

```bash
git checkout -b feature/my-feature
```

Use descriptive branch names.

Examples:

* `feature/csv-to-png`
* `fix/job-progress`
* `docs/api-clarification`

---

## Development Environment
> [!WARNING]
> This is the desired state for this project, but it has not been dockerized yet. Stay tuned!

The project is designed to run via Docker.

### Start the Stack

```bash
docker compose up --build
```

The API will typically be available at:

```
http://localhost:3313
```

(Port may vary depending on configuration.)

---

## Project Architecture (High Level)

Core components:

* **API** — FastAPI application
* **Workers** — background job processing (Not yet implemented)
* **Converters** — plugin-style conversion modules
* **Storage** — filesystem for files, SQLite for metadata
* **Queue** — Redis (Not yet implemented)

Converters follow a shared base class and are registered via the converter registry.

---

## Adding a New Converter

Contributions adding new converters are very welcome.

General expectations:

* Extend the base `Converter` class
* Declare supported inputs and outputs
* Implement the `convert()` method
* Include basic validation and error handling

Please keep converters:

* Deterministic
* Side-effect limited
* Safe for untrusted input files

If external binaries are required (e.g., ffmpeg, pandoc), document them clearly.

---

## Code Style

We aim for clean, readable code.

General guidelines:

* Prefer clarity over cleverness
* Keep functions focused and small
* Add docstrings where helpful
* Use type hints when possible
* Follow existing patterns in the codebase

Formatting and linting tools may be added or enforced over time.

---

## Pull Request Process

1. Ensure your branch is up to date with `main`
2. Make focused changes (avoid unrelated modifications)
3. Add or update tests if applicable
4. Update documentation if behavior changes
5. Open a Pull Request with a clear description

PRs should explain:

* What changed
* Why it changed
* How it was tested

Small PRs are preferred over large ones.

---

## Reporting Bugs

Please use the bug report template and include:

* Steps to reproduce
* Expected behavior
* Actual behavior
* Logs or screenshots (if available)
* Environment details

---

## Feature Requests

Feature requests are welcome. Please describe:

* The problem you want solved
* Proposed solution (if any)
* Alternatives considered

---

## Security

If you discover a security vulnerability, **do not open a public issue**.

Instead, please contact the maintainers privately (see [SECURITY](https://github.com/transmute-app/transmute/security/policy)).

---

## Philosophy

This project prioritizes:

* Simplicity
* Reliability
* Self-host friendliness
* Transparency
* Extensibility

We try to avoid unnecessary complexity and heavy dependencies unless they provide clear value.

---

## Questions

If you have questions, feel free to ask it using the "Question" issue template.

---

## License

By contributing, you agree that your contributions will be licensed under the same license as this project.
