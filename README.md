# Pygame WebAssembly via GCP Cloud Run CI/CD

This repository features the classic Snake game written in Python, configured to build directly to WebAssembly (`pygbag`), and statically served via an Nginx container on GCP Cloud Run. It includes a DevSecOps GitHub Actions pipeline handling multi-environment deployments.

## DevSecOps Pipeline Overview
The `.github/workflows/deploy.yml` pipeline handles:
- **Linting**: Flake8
- **Dependency Scan**: Safety
- **SAST**: Bandit
- **Secret Scanning**: TruffleHog
- **Building**: Pygbag (Compiling Python source to WASM) -> Docker
- **Deployment**: Google Cloud Run (Services: `dev`, `test`, `prod`)

## Prerequisites for Cloud Deployment
Before pushing to GitHub, you MUST configure GCP Workload Identity Federation so GitHub can securely deploy to your GCP project.

### 1. Configure Workload Identity Federation (Keyless Auth)
Run these commands in Google Cloud Shell or your local gcloud CLI:

```bash
PROJECT_ID="snakegame-492002"
export PROJECT_ID

gcloud iam workload-identity-pools create "github-actions-pool" --project="$snakegame-492002" --location="global" --display-name="GitHub Actions Pool"

#the following listed command work: 

gcloud iam workload-identity-pools providers create-oidc "github-provider" --location="global" --workload-identity-pool="github-actions-pool" --display-name="GitHub Actions Provider" --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" --issuer-uri="https://token.actions.githubusercontent.com" --attribute-condition="attribute.repository == 'YOUR_GITHUB_USER/YOUR_REPO'"

```

### 2. Create and Bind the Service Account
This Service Account gives GitHub Actions permission to push to Artifact Registry and deploy to Cloud Run.

```bash
gcloud iam service-accounts create my-github-sa --project="${PROJECT_ID}"

# Allow GitHub Action from your REPO to impersonate the service account:
REPO="rajivrparikh-cissp/snake-game-repo" # e.g. "octocat/snake"

gcloud iam service-accounts add-iam-policy-binding "my-github-sa@snakegame-492002.iam.gserviceaccount.com" --project="snakegame-492002" --role="roles/iam.workloadIdentityUser" --member="principalSet://iam.googleapis.com/projects/960477142846/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/rajivrparikh-cissp/snake-game-repo"

```

### 3. Setup GitHub Secrets
In your GitHub Repository, go to **Settings > Secrets and variables > Actions**, and add:
- `WIF_PROVIDER`: The full path to your Identity Provider (e.g., `projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider`)
- `WIF_SERVICE_ACCOUNT`: The email address of the service account you created (e.g., `my-github-sa@${PROJECT_ID}.iam.gserviceaccount.com`).

Once configured, pushing to `dev`, `test`, or `main` will automatically build the WebAssembly and deploy it to a live Cloud Run URL!

## Feature Deployment Workflow
To roll out a new feature (like the Golden Apple) through your environments, follow this Git workflow:

### 1. Test in Dev
Commit your feature to the `dev` branch to trigger the Dev pipeline:
```bash
git checkout -b dev
git add .
git commit -m "feat: Add Golden Apple logic"
git push -u origin dev
```
*Wait for the GitHub Action to finish and test your `snake-game-dev` Cloud Run URL.*

### 2. Test in Staging/Test
Merge the feature into the `test` branch to trigger the Test pipeline:
```bash
git checkout -b test
git merge dev
git push -u origin test
```
*Wait for the GitHub Action to finish and test your `snake-game-test` Cloud Run URL.*

### 3. Deploy to Production
Merge the feature into the `main` branch to trigger the Prod pipeline:
```bash
git checkout main
git merge test
git push origin main
```
*Your feature is now live on `snake-game-prod`!*
