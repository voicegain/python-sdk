#!/usr/bin/env groovy
pipeline {

  agent {
    docker { image 'gcr.io/ascalon-dev/jenkins-tools:0.1.17' }
  }

  options {
    disableConcurrentBuilds()
    gitLabConnection('GitLab')
    gitlabBuilds(builds: ['deploy', 'report'])
  }

  environment {

    PYPI_REPO_URL = "http://nexus.office.resolvity.com:8081/repository/pypi-resolvity/"
    NEXUS_CREDENTIALS = credentials('9c5404f1-0abc-470b-a910-514f8250e529')

    NL = sh(
        script: "echo -n '\n'",
        returnStdout: true
      )
    GIT_COMMITTER_NAME = sh(
        script: "git --no-pager show -s --format=%cn ${env.GIT_COMMIT}",
        returnStdout: true
      ).trim()
    GIT_COMMITTER_EMAIL = sh(
        script: "git --no-pager show -s --format=%ce ${env.GIT_COMMIT}",
        returnStdout: true
      ).trim()
    GIT_COMMITTER_DATE = sh(
        script: "git --no-pager show -s --format=%cd ${env.GIT_COMMIT}",
        returnStdout: true
      ).trim()
  }

  stages {


    stage('release') {

      steps {
        sh("python setup.py sdist")
        // sh(" VERSION="$(grep -Eo '[0-9.]{6,7}' setup.py | head -1)" ")
        VERSION = sh(grep -Eo '[0-9.]{6,7}' setup.py | head -1)
        // sh("gh release create $("$(grep -Eo '[0-9.]{6,7}' setup.py | head -1)")")
        sh("gh release create ${VERSION}")
        withCredentials([usernamePassword(credentialsId: 'devops-voicegain', passwordVariable: '?????DOCK1_PASSWORD', usernameVariable: 'DOCK1_USERNAME')]){
        sh("python -m twine upload dist/voicegain_speech-${VERSION}.tar.gz")
      }}
      post {
        success {
          updateGitlabCommitStatus name: 'deploy', state: 'success'
        }
        failure {
          updateGitlabCommitStatus name: 'deploy', state: 'failed'                    
        }
      }
    }




      post {
        success {
          updateGitlabCommitStatus name: 'web-doc', state: 'success'
        }
        failure {
          updateGitlabCommitStatus name: 'web-doc', state: 'failed'
        }
      }
    }


    stage('report') {

      steps {
        script {
          PACKAGE_INFO = sh(
            script: "get_python_package_version",
            returnStdout: true
          ).trim()
        }
      }
      post {
        success {
          updateGitlabCommitStatus name: 'report', state: 'success'
        }
        failure {
          updateGitlabCommitStatus name: 'report', state: 'failed'                    
        }
      }
    }

  }

  post {
    success {
      slackSend(
         channel: '#jenkins',
         color: '#00ff00',
         message: "*SUCCESS!* @here${NL}*Repo:* ${env.GIT_URL}${NL}*Branch:* ${env.GIT_BRANCH}${NL}*Commit:* ${env.GIT_COMMIT}${NL}*Job:* ${env.BUILD_URL}${NL}${NL}*Details:* ${NL}Deploy python package ${PACKAGE_INFO} to ${PYPI_REPO_URL}${NL}:smiley::thumbsup: *\"${GIT_COMMITTER_NAME}\"* at ${GIT_COMMITTER_DATE}"
      )
    }
    failure {
      slackSend(
        channel: '#jenkins',
        color: '#ff0000',
        message: "*FAILED!* @here${NL}*Repo:* ${env.GIT_URL}${NL}*Branch:* ${env.GIT_BRANCH}${NL}*Commit:* ${env.GIT_COMMIT}${NL}*Job:* ${env.BUILD_URL}${NL}:rage::point_right: *\"${GIT_COMMITTER_NAME}\"* at ${GIT_COMMITTER_DATE}"
      )
    }
  }
}
