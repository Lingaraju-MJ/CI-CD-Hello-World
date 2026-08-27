# CI/CD Hello World notes

Lab log for this repo. Read this when you need to remember what we set up.

When we change the pipeline later, add a new dated section at the bottom under **Later additions**. Do not rewrite the old steps unless something in them is now wrong.

Repo: https://github.com/Lingaraju-MJ/CI-CD-Hello-World

---

## What we ended up with

A tiny Python app on GitHub. Jenkins on this machine (Docker) watches `main`, and when someone pushes, it installs deps, runs the test, and prints the greeting.

Current loop:

```
edit code → commit → push to main → Jenkins polls GitHub (~every 5 min) → build
```

---

## Step by step (what we already did)

### 1. Repo and branch

- Created a separate GitHub repo: `CI-CD-Hello-World` (not mixed into `AI-Learning-Journey`).
- Worked on `feature/jenkins-pipeline` first, then merged to `main`.
- That feature branch was deleted after the PR merged.

### 2. The app (no Jenkins yet)

Three files only:

| File | Why it exists |
| --- | --- |
| `app.py` | The program. `get_greeting()` returns a string. Running the file prints it. |
| `test_app.py` | One pytest. If the greeting is wrong, CI fails. |
| `requirements.txt` | Lists `pytest` so Jenkins (and we) can install it. |

Run it locally if you want:

```powershell
pip install -r requirements.txt
python app.py
python -m pytest test_app.py
```

### 3. Jenkinsfile

`Jenkinsfile` is the recipe Jenkins reads from Git. Stages, in order:

1. **Install** — create a venv, install `requirements.txt`
2. **Test** — run `test_app.py`
3. **Run** — print the greeting (only if the test passed)

We use `sh` (Linux shell), not `bat`. That is fine because Jenkins itself runs in a Linux Docker container. WSL is not required for the job.

`agent any` means “use whatever Jenkins machine is free.” Here that is the Jenkins container itself.

Polling trigger in the file:

```groovy
triggers {
    pollSCM('H/5 * * * *')
}
```

That is a schedule, not “watch every branch.” It means: about every 5 minutes, check the branch this job is pointed at. `H/5` spreads jobs out so they do not all hit GitHub at once.

### 4. Jenkins on this PC

Jenkins is not installed as a Windows service. It is a Docker container:

- Container name: `jenkins-hello-world`
- Image: `jenkins/jenkins:lts-jdk17`
- UI: http://localhost:8080
- Ports: `8080` (web), `50000` (agents, unused for now)
- Data volume: `jenkins_hello_home` (jobs and config survive a container restart)

Start it again later:

```powershell
docker start jenkins-hello-world
```

Then open http://localhost:8080 and log in with the admin user created in the setup wizard.

The official Jenkins image has Java and Git. It did **not** have Python. We installed Python 3 inside the running container (`python3`, `pip`, `venv`). That install lives in the container filesystem, not in the Jenkins home volume.

If you ever **remove** the container and create a new one from the same image, Python is gone and Install will fail with `python3: not found` until you install it again:

```powershell
docker exec -u root jenkins-hello-world bash -lc "apt-get update && apt-get install -y python3 python3-pip python3-venv"
```

`docker restart` / `docker start` keeps Python. `docker rm` then `docker run` does not.

### 5. First Jenkins job

In the UI:

1. Unlock Jenkins (first-time password from the container).
2. Install suggested plugins.
3. Create an admin user.
4. **New Item** → `hello-world` → **Pipeline**.
5. Pipeline script from SCM → Git.
6. Repo: `https://github.com/Lingaraju-MJ/CI-CD-Hello-World.git`
7. Branch was `*/feature/jenkins-pipeline` during the first builds.
8. Script path: `Jenkinsfile`
9. **Build Now**.

Checkout from GitHub worked. **Install failed** (`python: not found`, exit 127). Test and Run were skipped.

Fix:

- Installed Python 3 on the agent (the container).
- Changed the Jenkinsfile to `python3` + a venv. On Debian, `python` often does not exist, and system `pip` fights OS packages, so a venv is the straightforward approach.

After that, the job went green.

### 6. PR into main

- Opened PR #1: `feature/jenkins-pipeline` → `main`.
- Merged it.
- Deleted `feature/jenkins-pipeline` locally and on GitHub.
- Pointed the Jenkins job branch from `*/feature/jenkins-pipeline` to `*/main`.

### 7. Proved polling works

Changed the greeting to `Hello, World from CI!`, updated the test, committed, pushed to `main`. Did not click Build Now.

Jenkins polled GitHub, saw commit `4d3454c`, and started **build #6**:

- Cause: **Started by an SCM change**
- Printed `Hello, World from CI!`
- **Finished: SUCCESS**

That is the confirmation that push → poll → build works.

---

## Current Jenkins job settings (as of this write-up)

Job name: `hello-world`

- Type: single Pipeline job (not Multibranch)
- SCM: GitHub HTTPS
- Branch specifier: `*/main`
- Script path: `Jenkinsfile`
- Trigger: Poll SCM, `H/5 * * * *`

So this job only cares about **main**. A push to a feature branch does not start `hello-world`.

Polling is used because GitHub cannot call `http://localhost:8080`. A webhook would be instant, but it needs a public URL (or a tunnel). For local Jenkins, polling is the honest setup.

---

## Files in the repo

```
app.py              greeting function + print
test_app.py         one pytest
requirements.txt    pytest
Jenkinsfile         pipeline
.gitignore          venv, pyc, editor junk
docs/ci-cd-notes.md this log
```

---

## Things that bit us (keep these)

1. **`python: not found`** — Jenkins agent had no Python. Git working does not mean the language runtime is there.
2. **Use `python3` on the Linux agent** — Windows local `python` vs Linux `python3`.
3. **Venv on Debian** — avoid installing pip packages onto the OS Python.
4. **Each `sh` step is a new shell** — activate the venv in Install, Test, and Run.
5. **Polling is not instant** — wait up to ~5 minutes, or click Build Now if you do not want to wait.
6. **Polling ≠ all branches** — the job’s branch field decides *what* is polled.
7. **Python on the agent is easy to lose** — gone if the container is recreated.
8. **Do not put secrets in this file** — no Jenkins passwords, no GitHub tokens.

---

## What this flow does not do yet

- Build feature branches or pull requests automatically.
- Instant builds on push (no GitHub webhook).
- Deploy anywhere (there is no CD yet, only CI).
- Notify Slack/email on failure.
- Use a Docker agent image that already has Python (we installed Python on the Jenkins controller instead).

---

## Useful commands

```powershell
# Jenkins
docker ps
docker start jenkins-hello-world
docker logs -f jenkins-hello-world
docker exec -u root jenkins-hello-world bash -lc "python3 --version"

# Last polling check
docker exec jenkins-hello-world bash -lc "cat /var/jenkins_home/jobs/hello-world/scm-polling.log"
```

Job UI: http://localhost:8080/job/hello-world/

---

## Later additions

Add entries below as we go. Newest at the bottom is fine.

### Template

```
### YYYY-MM-DD — short title

What we changed:
Why:
How to verify:
Anything that broke:
```

<!-- new work starts here -->

### 2026-08-26 — extra pipeline checks (on a feature branch first)

Lead wanted more than install / test / run. Same job, extra stages. We are trying this on a feature branch before merging to `main`.

What we changed:

- Lint: `ruff check .` (Python, so not ESLint).
- Format: `black --check .` on Jenkins. It does not rewrite files there. If it fails, run `python -m black .` locally and commit.
- Tests write `reports/junit.xml` so Jenkins can show a test report.
- Coverage: fail under 80% on `app`. The `if __name__ == "__main__"` line is left out of the count or the tiny file never reaches 80%.
- Package: zip `app.py` and keep it on the build as an artifact. `python3 -m zipfile` so we do not need a zip package in the container.
- `githubPush()` is in the Jenkinsfile next to polling. Polling stays until GitHub can actually reach Jenkins.
- Sonar: `sonar-project.properties` plus a stage that is skipped unless `SONAR_HOST_URL` is set. No Sonar server yet. Pick that up later.

Why:
Keep the old flow working, add the checks the lead asked for.

How to verify:

1. On Windows: `python -m ruff check .`, `python -m black --check .`, `python -m pytest test_app.py --cov=app --cov-fail-under=80`.
2. Push this feature branch. In the Jenkins job, set the branch to that feature branch (not `main`), then Build Now.
3. You should see Lint, Format, Test, Sonar skipped, Package, Run. Open Test Result and the zip on the build.

If Jenkins will not load the file and talks about `githubPush`, the GitHub plugin is missing. Install it or drop that one line. Polling still works.

Webhook later: tunnel to port 8080, GitHub webhook to `/github-webhook/`. Do not put secrets in this file.

Sonar later (remind me):

- SonarQube in Docker, or SonarCloud
- project token
- scanner or Jenkins Sonar plugin
- `SONAR_HOST_URL` and `SONAR_TOKEN` on the job

