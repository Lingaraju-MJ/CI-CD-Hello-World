# CI-CD-Hello-World

Tiny Python hello world used to learn Jenkins CI. Separate from `AI-Learning-Journey`.

```powershell
pip install -r requirements.txt
python app.py
python -m pytest test_app.py
python -m ruff check .
python -m black --check .
```

If `ruff` or `black` is not recognized, use the `python -m` form above. Windows often does not put those scripts on PATH.

Jenkins reads `Jenkinsfile` from Git. The job is usually on `main`; point it at the feature branch while we test.

Lab notes: [docs/ci-cd-notes.md](docs/ci-cd-notes.md).
