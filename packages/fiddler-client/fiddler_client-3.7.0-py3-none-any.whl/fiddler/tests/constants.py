import os
from pathlib import Path

URL = 'https://dev.fiddler.ai'
TOKEN = 'footoken'
ORG_ID = '5531bfd9-2ca2-4a7b-bb5a-136c8da09ca0'
ORG_NAME = 'fiddler_dev'
SERVER_VERSION = '24.12.2'
PROJECT_NAME = 'bank_churn'
PROJECT_ID = '1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1'
MODEL_NAME = 'bank_churn'
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'
MODEL_VERSION = 'v1'
USER_ID = '5531bfd9-2ca2-4a7b-bb5a-136c8da09ca3'
USER_NAME = 'foo'
USER_EMAIL = 'foo@fiddler.ai'
JOB_ID = '9df70575-7ced-42fd-bb50-a0e4351d2c9d'
JOB_NAME = f'Deleting model {MODEL_NAME}'
DATASET_ID = 'ba6ec4e4-7188-44c5-ba84-c2cb22b4bb00'
DATASET_NAME = 'dataset3'
BASELINE_ID = 'af05646f-0cef-4638-84c9-0d195df2575d'
ALERT_RULE_ID = 'ed8f18e6-c319-4374-8884-71126a6bab85'
TEST_EMAILS = ['test@fiddler.ai', 'admin@fiddler.ai']
TEST_PAGERDUTY_SERVICES = ['service1', 'service2']
TEST_PAGERDUTY_SEVERITY = 'critical'
TEST_WEBHOOKS = [
    'e20bf4cc-d2cf-4540-baef-d96913b14f1b',
    '6e796fda-0111-4a72-82cd-f0f219e903e1',
]
BASELINE_NAME = 'test_baseline'
MODEL_DEPLOYMENT_ID = 'fc07562a-1a27-4f66-9154-732d3b14b98a'
WEBHOOK_ID = 'a5b654eb-15c8-43c8-9d50-9ba6eea9a0ff'
WEBHOOK_NAME = 'test_webhook_config_name'
WEBHOOK_URL = 'https://www.slack.com'
WEBHOOK_PROVIDER = 'SLACK'
BASE_TEST_DIR = f'{Path(__file__).resolve().parent}'
OUTPUT_DIR = os.path.join(BASE_TEST_DIR, 'artifact_test_dir')
