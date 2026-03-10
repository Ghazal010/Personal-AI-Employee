#!/usr/bin/env python3
"""
Comprehensive Audit Logger for Personal AI Employee
Centralized logging system for all actions and events
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler

# Configuration
AUDIT_LOG_PATH = Path(__file__).parent / "logs" / "audit.jsonl"
AUDIT_LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
AUDIT_LOG_BACKUP_COUNT = 5

# Event types
class EventType:
    # Email events
    EMAIL_RECEIVED = "email_received"
    EMAIL_SENT = "email_sent"
    EMAIL_PROCESSED = "email_processed"
    EMAIL_ERROR = "email_error"

    # WhatsApp events
    WHATSAPP_RECEIVED = "whatsapp_received"
    WHATSAPP_SENT = "whatsapp_sent"
    WHATSAPP_PROCESSED = "whatsapp_processed"
    WHATSAPP_ERROR = "whatsapp_error"

    # System events
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    SYSTEM_ERROR = "system_error"
    SYSTEM_HEALTH_CHECK = "system_health_check"

    # Authentication events
    AUTH_SUCCESS = "auth_success"
    AUTH_FAILURE = "auth_failure"
    AUTH_REFRESH = "auth_refresh"

    # File operations
    FILE_CREATED = "file_created"
    FILE_MOVED = "file_moved"
    FILE_DELETED = "file_deleted"
    FILE_ERROR = "file_error"

    # MCP server events
    MCP_REQUEST = "mcp_request"
    MCP_RESPONSE = "mcp_response"
    MCP_ERROR = "mcp_error"


class AuditLogger:
    """Centralized audit logger for all system events"""

    def __init__(self, component_name: str):
        """
        Initialize audit logger for a specific component

        Args:
            component_name: Name of the component (e.g., "gmail_watcher", "whatsapp_monitor")
        """
        self.component_name = component_name
        self._setup_logger()

    def _setup_logger(self):
        """Setup rotating file handler for audit logs"""
        # Ensure log directory exists
        AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Create logger
        self.logger = logging.getLogger(f"audit.{self.component_name}")
        self.logger.setLevel(logging.INFO)

        # Remove existing handlers
        self.logger.handlers = []

        # Create rotating file handler
        handler = RotatingFileHandler(
            AUDIT_LOG_PATH,
            maxBytes=AUDIT_LOG_MAX_SIZE,
            backupCount=AUDIT_LOG_BACKUP_COUNT
        )

        # Use JSON formatter
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

        # Don't propagate to root logger
        self.logger.propagate = False

    def log_event(
        self,
        event_type: str,
        action: str,
        status: str = "success",
        details: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log an audit event

        Args:
            event_type: Type of event (use EventType constants)
            action: Description of the action
            status: Status of the action (success, failure, warning)
            details: Additional details about the event
            metadata: Extra metadata (user, session, etc.)
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "component": self.component_name,
            "event_type": event_type,
            "action": action,
            "status": status,
            "details": details or {},
            "metadata": metadata or {}
        }

        # Log as JSON line
        self.logger.info(json.dumps(event))

    # Convenience methods for common events

    def log_email_received(self, email_id: str, sender: str, subject: str):
        """Log email received event"""
        self.log_event(
            EventType.EMAIL_RECEIVED,
            "Email received from Gmail",
            details={
                "email_id": email_id,
                "sender": sender,
                "subject": subject
            }
        )

    def log_email_sent(self, recipient: str, subject: str, success: bool = True):
        """Log email sent event"""
        self.log_event(
            EventType.EMAIL_SENT,
            "Email sent via SMTP",
            status="success" if success else "failure",
            details={
                "recipient": recipient,
                "subject": subject
            }
        )

    def log_whatsapp_received(self, contact: str, message_count: int):
        """Log WhatsApp chat received event"""
        self.log_event(
            EventType.WHATSAPP_RECEIVED,
            "WhatsApp chat exported and detected",
            details={
                "contact": contact,
                "message_count": message_count
            }
        )

    def log_whatsapp_sent(self, phone_number: str, message: str, success: bool = True):
        """Log WhatsApp message sent event"""
        self.log_event(
            EventType.WHATSAPP_SENT,
            "WhatsApp message sent",
            status="success" if success else "failure",
            details={
                "phone_number": phone_number,
                "message_preview": message[:50] + "..." if len(message) > 50 else message
            }
        )

    def log_file_created(self, file_path: str, file_type: str):
        """Log file creation event"""
        self.log_event(
            EventType.FILE_CREATED,
            "Action file created",
            details={
                "file_path": file_path,
                "file_type": file_type
            }
        )

    def log_system_start(self):
        """Log system start event"""
        self.log_event(
            EventType.SYSTEM_START,
            f"{self.component_name} started"
        )

    def log_system_stop(self, reason: str = "user_request"):
        """Log system stop event"""
        self.log_event(
            EventType.SYSTEM_STOP,
            f"{self.component_name} stopped",
            details={"reason": reason}
        )

    def log_error(self, error_type: str, error_message: str, traceback: Optional[str] = None):
        """Log error event"""
        self.log_event(
            EventType.SYSTEM_ERROR,
            f"Error in {self.component_name}",
            status="failure",
            details={
                "error_type": error_type,
                "error_message": error_message,
                "traceback": traceback
            }
        )

    def log_auth_event(self, auth_type: str, success: bool, details: Optional[Dict] = None):
        """Log authentication event"""
        event_type = EventType.AUTH_SUCCESS if success else EventType.AUTH_FAILURE
        self.log_event(
            event_type,
            f"Authentication {auth_type}",
            status="success" if success else "failure",
            details=details or {}
        )

    def log_health_check(self, health_status: Dict[str, Any]):
        """Log system health check"""
        self.log_event(
            EventType.SYSTEM_HEALTH_CHECK,
            "System health check performed",
            details=health_status
        )

    def log_mcp_request(self, tool_name: str, parameters: Dict[str, Any]):
        """Log MCP server request"""
        self.log_event(
            EventType.MCP_REQUEST,
            f"MCP tool called: {tool_name}",
            details={
                "tool": tool_name,
                "parameters": parameters
            }
        )

    def log_mcp_response(self, tool_name: str, success: bool, result: Optional[str] = None):
        """Log MCP server response"""
        self.log_event(
            EventType.MCP_RESPONSE,
            f"MCP tool response: {tool_name}",
            status="success" if success else "failure",
            details={
                "tool": tool_name,
                "result": result
            }
        )


class AuditLogReader:
    """Read and analyze audit logs"""

    def __init__(self, log_path: Path = AUDIT_LOG_PATH):
        self.log_path = log_path

    def read_logs(
        self,
        limit: Optional[int] = None,
        event_type: Optional[str] = None,
        component: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list:
        """
        Read audit logs with optional filters

        Args:
            limit: Maximum number of logs to return
            event_type: Filter by event type
            component: Filter by component name
            start_date: Filter logs after this date
            end_date: Filter logs before this date

        Returns:
            List of log entries (dicts)
        """
        if not self.log_path.exists():
            return []

        logs = []

        try:
            with open(self.log_path, 'r') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())

                        # Apply filters
                        if event_type and log_entry.get('event_type') != event_type:
                            continue

                        if component and log_entry.get('component') != component:
                            continue

                        if start_date:
                            log_time = datetime.fromisoformat(log_entry['timestamp'])
                            if log_time < start_date:
                                continue

                        if end_date:
                            log_time = datetime.fromisoformat(log_entry['timestamp'])
                            if log_time > end_date:
                                continue

                        logs.append(log_entry)

                        if limit and len(logs) >= limit:
                            break

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            print(f"Error reading audit logs: {e}")

        return logs

    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """
        Get statistics from audit logs

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with statistics
        """
        from datetime import timedelta

        start_date = datetime.now() - timedelta(days=days)
        logs = self.read_logs(start_date=start_date)

        stats = {
            "total_events": len(logs),
            "events_by_type": {},
            "events_by_component": {},
            "success_count": 0,
            "failure_count": 0,
            "warning_count": 0
        }

        for log in logs:
            # Count by type
            event_type = log.get('event_type', 'unknown')
            stats['events_by_type'][event_type] = stats['events_by_type'].get(event_type, 0) + 1

            # Count by component
            component = log.get('component', 'unknown')
            stats['events_by_component'][component] = stats['events_by_component'].get(component, 0) + 1

            # Count by status
            status = log.get('status', 'unknown')
            if status == 'success':
                stats['success_count'] += 1
            elif status == 'failure':
                stats['failure_count'] += 1
            elif status == 'warning':
                stats['warning_count'] += 1

        return stats

    def generate_report(self, days: int = 7) -> str:
        """Generate human-readable audit report"""
        stats = self.get_statistics(days)

        report = f"""# Audit Report - Last {days} Days

## Summary
- Total Events: {stats['total_events']}
- Success: {stats['success_count']}
- Failures: {stats['failure_count']}
- Warnings: {stats['warning_count']}

## Events by Type
"""
        for event_type, count in sorted(stats['events_by_type'].items(), key=lambda x: x[1], reverse=True):
            report += f"- {event_type}: {count}\n"

        report += "\n## Events by Component\n"
        for component, count in sorted(stats['events_by_component'].items(), key=lambda x: x[1], reverse=True):
            report += f"- {component}: {count}\n"

        return report


# Example usage
if __name__ == "__main__":
    # Create audit logger
    logger = AuditLogger("test_component")

    # Log some events
    logger.log_system_start()
    logger.log_email_received("12345", "test@example.com", "Test Email")
    logger.log_file_created("/path/to/file.md", "email")
    logger.log_system_stop()

    # Read logs
    reader = AuditLogReader()
    logs = reader.read_logs(limit=10)
    print(f"Found {len(logs)} log entries")

    # Generate report
    report = reader.generate_report(days=7)
    print(report)
