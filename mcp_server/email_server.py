#!/usr/bin/env python3
"""
Simple Email MCP Server for Personal AI Employee
Implements Model Context Protocol for sending emails
"""

import json
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict


class EmailMCPServer:
    """MCP Server for email operations"""

    def __init__(self):
        self.tools = [
            {
                "name": "send_email",
                "description": "Send an email to a recipient",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body content"
                        }
                    },
                    "required": ["to", "subject", "body"]
                }
            }
        ]

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request"""
        method = request.get("method")

        if method == "tools/list":
            return {
                "tools": self.tools
            }

        elif method == "tools/call":
            tool_name = request.get("params", {}).get("name")
            arguments = request.get("params", {}).get("arguments", {})

            if tool_name == "send_email":
                return self.send_email(arguments)
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }

        elif method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "email-server",
                    "version": "1.0.0"
                }
            }

        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }

    def send_email(self, args: Dict[str, str]) -> Dict[str, Any]:
        """Send email using SMTP"""
        try:
            to_addr = args.get("to")
            subject = args.get("subject")
            body = args.get("body")

            # For demo purposes, just log the email
            # In production, configure SMTP settings
            log_message = f"""
EMAIL SENT (Demo Mode):
To: {to_addr}
Subject: {subject}
Body: {body}
---
Note: Configure SMTP settings in production for actual email sending.
"""

            return {
                "content": [
                    {
                        "type": "text",
                        "text": log_message
                    }
                ]
            }

        except Exception as e:
            return {
                "error": {
                    "code": -32000,
                    "message": f"Failed to send email: {str(e)}"
                }
            }

    def run(self):
        """Run the MCP server (stdio mode)"""
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)

                # Add request ID if present
                if "id" in request:
                    response["id"] = request["id"]

                response["jsonrpc"] = "2.0"

                print(json.dumps(response), flush=True)

            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    server = EmailMCPServer()
    server.run()
