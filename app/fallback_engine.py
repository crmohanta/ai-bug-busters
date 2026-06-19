def get_best_practices(issue: str):
    issue = issue.lower()

    # ✅ STORAGE / DISK
    if "disk" in issue or "storage" in issue:
        return [
            "Check disk usage using df -h (Linux) or disk manager (Windows)",
            "Clean log files and temporary files",
            "Enable log rotation to prevent future issues",
            "Monitor disk usage trends regularly"
        ]

    # ✅ CPU / PERFORMANCE
    elif "cpu" in issue or "performance" in issue:
        return [
            "Check running processes using top or task manager",
            "Identify high resource-consuming applications",
            "Restart affected services",
            "Monitor system load patterns"
        ]

    # ✅ MEMORY
    elif "memory" in issue:
        return [
            "Check memory usage using free -m or task manager",
            "Restart applications causing memory leaks",
            "Optimize application memory consumption",
            "Increase memory allocation if required"
        ]

    # ✅ NETWORK
    elif "network" in issue or "latency" in issue:
        return [
            "Check network connectivity and routing",
            "Verify firewall rules",
            "Restart networking services",
            "Check DNS resolution"
        ]

    # ✅ API / APPLICATION
    elif "api" in issue or "application" in issue:
        return [
            "Check application logs for errors",
            "Verify backend service health",
            "Validate request configuration",
            "Restart application services"
        ]

    # ✅ DATABASE
    elif "database" in issue or "db" in issue:
        return [
            "Check database connectivity",
            "Monitor query performance",
            "Restart database service if needed",
            "Verify connection pool configuration"
        ]

    # ✅ DEFAULT (GENERIC FALLBACK ✅)
    else:
        return [
            "Check system logs for errors",
            "Restart affected services",
            "Monitor CPU, memory, and disk usage",
            "Validate configuration settings",
            "Check network connectivity"
        ]