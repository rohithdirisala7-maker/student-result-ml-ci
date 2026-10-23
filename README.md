# Student Result Prediction — MLOps CI/CD

This repository implements the Student Result Prediction practical series using scikit-learn, Flask, GitHub Actions, Docker, and GitHub Container Registry (GHCR).

## Pipeline

1. Generate the student dataset and train a Logistic Regression model.
2. Evaluate the model and save `metrics.json` and `student_result_model.pkl`.
3. Enforce the minimum model accuracy quality gate (80%).
4. Run automated model and API tests.
5. Package a release candidate as the `student-result-ml-release` GitHub Actions artifact.
6. Build a Docker image and test its health and prediction endpoints.
7. Publish the tested image to GHCR with `latest` and commit-specific tags.

## API

The Flask service listens on port 5000.

- `GET /` — service information
- `GET /health` — health check
- `POST /predict` — predict PASS or FAIL

Example request body:

```json
{
  "attendance": 90,
  "internal_marks": 85,
  "assignment_marks": 88,
  "previous_score": 80
}
```

Run locally after training:

```bash
python -m pip install -r requirements.txt
python train_model.py
python quality_gate.py
python -m unittest test_ml_pipeline.py -v
python -m unittest test_app.py -v
python app.py
```

## Docker

The GitHub Actions workflow builds the model before building the Docker image, so the generated model and metrics are available in the Docker build context. To run the image locally after generating the model:

```bash
docker build -t student-result-prediction:local .
docker run --rm -p 5000:5000 student-result-prediction:local
```

## GHCR image

The publish workflow targets:

`ghcr.io/rohithdirisala7-maker/student-result-prediction:latest`

The workflow publishes only after the model quality gate, unit tests, Docker build, health check, and prediction request all pass. Ensure repository Actions are enabled. If an existing GHCR package is owned separately, grant this repository write access under the package's **Manage Actions access** settings.

## Render deployment (Practical-10)

After the GHCR workflow succeeds and the image is visible in GitHub Packages:

1. In Render, create **New → Web Service → Existing Image**.
2. Use image `ghcr.io/rohithdirisala7-maker/student-result-prediction:latest`.
3. If the GHCR package is private, configure a registry credential with read-package access. Never commit a token to this repository.
4. Configure the service to use port **5000** (the Flask app's port) and health-check path `/health`.
5. Deploy, then verify the public service URL with `/` and `/health`; send a JSON POST to `/predict` to test inference.

This repository currently follows the Flask/port-5000 API from Practicals 5–7. The later sample in Practical-10 mentions FastAPI and port 8000; use the actual image's port and endpoints rather than mixing the two configurations. Production deployment is not triggered automatically by these workflows.
