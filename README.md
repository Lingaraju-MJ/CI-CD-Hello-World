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

Jenkins reads `Jenkinsfile` from Git. Builds start on a GitHub push (webhook), not on a 5-minute poll. While we test, point the job at this feature branch instead of `main`.
