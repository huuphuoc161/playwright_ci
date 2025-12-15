# Playwright CI - Automation Testing Framework

Playwright-based automation testing framework for web application testing with pytest integration, extended reporting, and CI/CD pipeline support.

## Project Structure

```
playwright_ci/
├── .env                          # ✅ Environment variables (TEST_USERNAME, TEST_PWD)
├── .gitignore, .github/         # Git configuration
├── pytest.ini                    # Pytest config
├── requirements.txt              # Dependencies
├── conftest.py                   # ✅ Updated with python-dotenv
│
├── pages/                        # Page Object Model
│   ├── base_page.py
│   ├── election_page.py          # Election app page object
│   ├── login_page.py             # SauceDemo page object
│   ├── inventory_page.py
│   └── __init__.py
│
├── tests/
│   ├── conftest.py               # ✅ Loads .env and manages test fixtures
│   ├── login_suite.py            # ✅ 5 test cases (election app + saucedemo)
│   └── __init__.py
│
├── reports/
│   └── result.txt                # ✅ Plain text test results
│
└── utils/ (minimal)   
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- Visual Studio Code (for running tests via UI)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd playwright_ci
```

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Create/Update `.env` file with your credentials:
```env
TEST_USERNAME=
TEST_PWD=
TEST_PWD_WRONG=
```

## Test Suite Overview

### Current Test Cases (5 total)

#### 1. Election App Tests 
- **test_election_app_login_correct_password** ✅
  - Tests login with valid credentials from `.env`
  - Verifies successful dashboard access

- **test_election_app_login_wrong_password** ✅
  - Tests login failure with incorrect password
  - Verifies user remains on login page
  - Marks: `@pytest.mark.election_app`

#### 2. SauceDemo Tests (Demo Website)
- **test_saucedemo_login_standard_user** ✅
  - Tests standard user login
  - Verifies inventory page access
  - Marks: `@pytest.mark.saucedemo`, `@pytest.mark.smoke`

- **test_saucedemo_login_wrong_credentials** ✅
  - Tests login failure with invalid credentials
  - Verifies error message display
  - Marks: `@pytest.mark.saucedemo`

- **test_saucedemo_login_locked_out_user** ✅
  - Tests locked user account scenario
  - Verifies specific error message
  - Marks: `@pytest.mark.saucedemo`

## Running Tests

### Via Command Line

#### Run all tests
```bash
pytest tests/login_suite.py -v
```

#### Run specific test category
```bash
# Election app tests only
pytest tests/login_suite.py -m election_app -v

# SauceDemo tests only
pytest tests/login_suite.py -m saucedemo -v

# Smoke tests only
pytest tests/login_suite.py -m smoke -v
```

#### Run with detailed output
```bash
pytest tests/login_suite.py -v --tb=short
```

### Test Results
Results are automatically written to `reports/result.txt` with format:
```
Test Results
================================================================================

================================================================================
Tests finished
```

## Jenkins Pipeline Integration

### Setup Jenkins Job

1. **Create New Pipeline Job**
   - In Jenkins Dashboard: `New Item` → `Pipeline` → Enter job name

2. **Configure Pipeline Script**
   - Select `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `<your-github-repo-url>`
   - Credentials: Add GitHub credentials
   - Script Path: `Jenkinsfile`

### Jenkinsfile Configuration

Use the existing `Jenkinsfile` in the project root:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    playwright install
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/login_suite.py -v --junit-xml=test-results.xml
                '''
            }
        }
    }
    
    post {
        always {
            junit 'test-results.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
        failure {
            echo 'Tests failed!'
        }
        success {
            echo 'All tests passed!'
        }
    }
}
```

### Running Jenkins Job

#### Method 1: Manual Trigger
1. Open Jenkins Dashboard
2. Click on your Pipeline job
3. Click `Build Now`
4. Monitor build progress in `Build Console Output`

#### Method 2: GitHub Webhook (Auto-trigger)
1. In GitHub repository:
   - Go to `Settings` → `Webhooks`
   - Click `Add webhook`
   - Payload URL: `http://jenkins-server:8080/github-webhook/`
   - Content type: `application/json`
   - Events: Select `Push events`
   - Click `Add webhook`

2. Pipeline will automatically trigger on push

#### Method 3: Scheduled Build (Cron)
1. In Jenkins job configuration:
   - Click `Build Triggers`
   - Enable `Build periodically`
   - Cron expression: `H 2 * * *` (daily at 2 AM)
   - Save

### View Test Results in Jenkins

1. After build completes, click on build number
2. View results:
   - **Build Console Output**: Full test logs
   - **Test Result**: JUnit format results
   - **Artifacts**: Generated reports in `reports/result.txt`

### Environment Variables in Jenkins

Set in Jenkins job configuration → Build Environment:

```
TEST_USERNAME=httlpk@httlpk.org
TEST_PWD=your_secret_password
TEST_PWD_WRONG=wrong_password_123
```

Or use Jenkins Credentials:
1. Create Secret text credentials for each variable
2. Reference in pipeline: `credentials('CREDENTIAL_ID')`

### Troubleshooting Jenkins Build

| Issue | Solution |
|-------|----------|
| Python not found | Ensure Python installed on Jenkins agent |
| Playwright fails | Run `playwright install` in Setup stage |
| .env not found | Set environment variables in Jenkins |
| Build timeout | Increase Jenkins build timeout in job config |
| Chrome not found | Install chromium: `playwright install chromium` |

### Jenkins Pipeline Monitoring

- **Build Status**: Dashboard shows latest build status
- **Build History**: View all previous builds and results
- **Test Trends**: Track pass/fail rates over time
- **Console Output**: Debug specific test failures

### CI/CD Best Practices

1. **Run smoke tests first** (`@pytest.mark.smoke`)
2. **Run nightly full suite** (all tests)
3. **Send notifications** on build failure
4. **Archive test reports** for audit trail
5. **Use different branches** for different test suites
6. **Store credentials securely** in Jenkins Credentials Store