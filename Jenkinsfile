pipeline {
    agent any
    
    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chromium', 'firefox', 'webkit'],
            description: 'Select browser for testing'
        )
        booleanParam(
            name: 'HEADLESS_MODE',
            defaultValue: true,
            description: 'Run tests in headless mode'
        )
        string(
            name: 'PARALLEL_WORKERS',
            defaultValue: '2',
            description: 'Number of parallel test workers'
        )
    }
    
    environment {
        PYTHON_CMD = 'C:\\Users\\huuphuoc.nguyen\\AppData\\Local\\Python\\bin\\python3.exe'
        PYTHON_VERSION = '3.9'
        WORKSPACE_DIR = "${WORKSPACE}"
        REPORTS_DIR = "${WORKSPACE}/reports"
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '30'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out code from repository..."
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo "⚙️  Setting up Python environment..."
                bat '''
                    %PYTHON_CMD% --version
                    %PYTHON_CMD% -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Install Playwright') {
            steps {
                echo "🎭 Installing Playwright browsers..."
                bat '''
                    call venv\\Scripts\\activate.bat
                    playwright install chromium
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "🧪 Executing Playwright tests..."
                bat '''
                    call venv\\Scripts\\activate.bat
                    if not exist "%REPORTS_DIR%" mkdir "%REPORTS_DIR%"
                    pytest tests\\login_suite.py -v --junit-xml="%REPORTS_DIR%\\junit.xml"
                '''
            }
        }
    }
    
    post {
        always {
            echo "🧹 Publishing reports..."
            junit testResults: "${REPORTS_DIR}\\junit.xml", allowEmptyResults: true
            archiveArtifacts artifacts: "${REPORTS_DIR}/**/*", allowEmptyArchive: true
        }
        
        success {
            echo "✅ Pipeline completed successfully!"
        }
        
        failure {
            echo "❌ Pipeline failed! Check reports for details."
        }
    }
}
