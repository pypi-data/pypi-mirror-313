# zcp-alert-backend

![Platform Badge](https://img.shields.io/badge/platform-zmp-red)
![Component Badge](https://img.shields.io/badge/compolent-alert-red)
![CI Badge](https://img.shields.io/badge/ci-github_action-green)
![License Badge](https://img.shields.io/badge/license-Apache_2.0-green)
![PyPI - Version](https://img.shields.io/pypi/v/zcp-alert-backend)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/zcp-alert-backend)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zcp-alert-backend)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/zcp-alert-backend)

<!-- ![Language Badge](https://img.shields.io/badge/language-python-blue)
![Version Badge](https://img.shields.io/badge/version-^3.12-blue) -->

The zcp-alert-backend is the software that manages alerts, channels, integrations, and silences for alert notifications.

## Architecture
![Alert architecture on the cloudzcp platform](alert-architecture.png)

## Features
### 1. Alert Management
The alert-backend receives the alert from the alertmanager of the corext monitoring system and the OpenSearch.
And then saves the alert playload into the MongoDB for the lifecyle managment.

#### State Diagram
![alt text](alert-state-diagram.png)

### 2. Channel Management
The alert-backend manages the notification channel.

Supported the third-party is
- Slack
- MS Teams
- Goole Chat
- Kakaotalk
- Emal
- Webhook

### 3. Integration Management
The alert-backend manages the integrations for the notification to the channels using the alert information.

e.g.) prioity, severity, cluster, project and labels

### 4. Silence Management
The alert-backend manages the silence to snooze the alert notification to the channel during defined period (for maintenance job)

### 5. Dashboard
The alert-backend provides the status dashboard and MTTA, MTTR dashbord
