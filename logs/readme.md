# Logs

## Overview

This directory is used to store application log files generated while running the project.

Application logs are collected by the Datadog Agent and forwarded to Datadog Log Management, where they are parsed, indexed, and used for troubleshooting and incident investigation.

---

## Purpose

The log files generated in this directory are used to:

- Validate log collection by the Datadog Agent.
- Test the custom Grok parsing pipeline.
- Generate structured log attributes.
- Support log analysis in Datadog Log Explorer.
- Correlate application logs with distributed traces during incident investigations.

---

## Version Control

Runtime log files are excluded from version control using `.gitignore` because they are generated dynamically during execution.

Example:

```gitignore
logs/*.log
```

---

## Expected Log File

During normal execution, the application generates:

```text
app.log
```

This file is created automatically when the Flask application is running.

---

## Note

If the `logs` directory is empty after cloning the repository, simply run the application to generate new log files.