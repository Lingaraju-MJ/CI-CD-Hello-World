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

The job page (Status, Configure, Build Now) is not where tests and logs live. Open **Build History**, click a build number (for example `#12`). On that build you get **Console Output**. After a green run, the same page also has **Test Result** and **Build Artifacts** (the zip).

Local monitoring (Prometheus + Grafana):

```powershell
docker compose up -d --build
```

- App: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (`admin` / `admin`)

Basic security scan (OWASP ZAP). The app must already be running. ZAP uses the Docker network, so the target is `http://app:8000`:

```powershell
docker run --rm --network ci-cd-hello-world_default -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://app:8000
```

Notes from the scan: `docs/zap-findings.md`

How this local stack maps to AWS and Azure: `docs/aws-azure-mapping.md`
