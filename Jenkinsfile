pipeline {

    agent any

    environment {

        // Способ для типа "Username with password"
        SELENOID_CREDS = credentials('SELENOID_CREDS')
        SELENOID_LOGIN = "${SELENOID_CREDS_USR}"
        SELENOID_PASS  = "${SELENOID_CREDS_PSW}"

        // Способ для типа "String (Secret text)"
        SELENOID_URL = credentials('SELENOID_URL')

        // Так же для Spotify
        SPOTIFY_CREDS = credentials('SPOTIFY_CREDS')
        SPOTIFY_USERNAME = "${SPOTIFY_CREDS_USR}"
        SPOTIFY_PASSWORD = "${SPOTIFY_CREDS_PSW}"

        SPOTIFY_CREDS = credentials('SPOTIFY_CREDS_ALT')
        SPOTIFY_USERNAME = "${SPOTIFY_CREDS_USR}"
        SPOTIFY_PASSWORD = "${SPOTIFY_CREDS_PSW}"

    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/AlishaMeier/diploma_project_spotify'
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'

            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --alluredir=allure-results'
            }
        }
    }

    post {
        always {
            allure includeProperties: false, report: 'allure-report', results: [[path: 'allure-results']]
        }
    }
}