# Agriculturals-Dashboard

# Build and deploy

Command to build the application. PLease remeber to change the project name and application name

```
gcloud builds submit --tag gcr.io/agricultural-reports/Agricultural Reports  --project=agricultural-reports
```

Command to deploy the application

```
gcloud run deploy --image gcr.io/agricultural-reports/Agricultural Reports --platform managed  --project=agricultural-reports --allow-unauthenticated
```
# agri-v1
