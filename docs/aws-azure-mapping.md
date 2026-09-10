# AWS and Azure mapping

This is a map, not a migration. We are not putting the Hello World app in the cloud.

Local Docker is for learning: you can see Jenkins, SonarQube, Prometheus, Grafana, and ZAP as separate boxes. In AWS or Azure you would not copy those boxes one-for-one onto VMs. You keep the same *jobs* (build, host, watch, scan) and pick the managed service that does that job.

Ruff, Black, pytest, and ZAP are not cloud products. They stay as steps in the pipeline wherever the pipeline runs.

## Same job, different box

| What we have on this PC | Closest AWS service | Closest Azure service |
| --- | --- | --- |
| GitHub repo | Stay on GitHub, or CodeCommit | Stay on GitHub, or Azure Repos |
| Jenkins pipeline | CodePipeline + CodeBuild, or GitHub Actions | Azure Pipelines, or GitHub Actions |
| Ruff / Black | Same tools, as a build step | Same tools, as a pipeline task |
| pytest + junit zip | CodeBuild reports + S3 for the zip | Azure Pipelines test results + Artifacts |
| SonarQube in Docker | SonarCloud (or Inspector later for the AWS account) | SonarCloud (or Defender for Cloud later) |
| Flask app in Compose | App Runner or Elastic Beanstalk. ECS if you already live in containers. | App Service. Container Apps if you have a few containers. |
| Prometheus | CloudWatch metrics first. Amazon Managed Prometheus when you have several services. | Application Insights first. Azure Monitor Prometheus later. |
| Grafana | CloudWatch dashboards, or Amazon Managed Grafana | Azure Managed Grafana, after App Insights is not enough |
| Datadog (we did not use it) | CloudWatch / X-Ray, or Datadog on AWS if the company already pays for it | App Insights / Azure Monitor, or Datadog on Azure |
| OWASP ZAP (local Docker) | Run ZAP in CodeBuild. AWS WAF in front of the site. Inspector for the account. | Run ZAP in the pipeline. Front Door / WAF. Defender for Cloud. |

GitHub Actions is a fair answer on both clouds. Use CodePipeline or Azure Pipelines when the rest of the team already lives there.

## How to choose as the app grows

**This lab (one tiny site):** GitHub + a pipeline (Actions, CodePipeline, or Azure Pipelines) + App Runner / App Service + CloudWatch or Application Insights. Skip Jenkins, self-hosted Sonar, Prometheus, and Grafana in the cloud.

**A real product (a few services, a few environments):** same pipeline, Container Apps or ECS, SonarCloud on every PR, App Insights or CloudWatch plus logs. Add managed Grafana only if several people need the same dashboards.

**A platform (many services and teams):** EKS or AKS, managed Prometheus + Grafana, WAF, Defender / Inspector. Keep SonarCloud or one shared SonarQube. Pick Datadog only if the org already standardizes on it. Do not run Datadog and CloudWatch/Azure Monitor for the same job.

One hello-world page does not need Kubernetes, Datadog, and a Jenkins VM.
