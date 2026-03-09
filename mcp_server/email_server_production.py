#!/usr/bin/env python3
"""
Production Email MCP Server with Environment Variables
Secure configuration using environment variables
"""

import json
import sys
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict


class EmailMCPServer:
    """MCP Server for email operations"""

    def __init__(self):
        # Get configuration from environment variables
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.from_email = os.environ.get('EMAIL_ADDRESS', '')
        self.app_password = os.environ.get('EMAIL_PASSWORD', '')

        # Check if production mode is enabled
        self.production_mode = bool(self.from_email and self.app_password)

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
            mode = "Production" if self.production_mode else "Demo"
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "email-server",
                    "version": "1.0.0",
                    "mode": mode
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

            if self.production_mode:
                # PRODUCTION MODE - Real email sending
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = to_addr
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                # Send via SMTP
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.from_email, self.app_password)
                server.send_message(msg)
                server.quit()

                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"✅ Email sent successfully!\n\nFrom: {self.from_email}\nTo: {to_addr}\nSubject: {subject}\n\nEmail delivered via {self.smtp_server}"
                        }
                    ]
                }
            else:
                # DEMO MODE - Just log the email
                log_message = f"""
EMAIL SENT (Demo Mode):
To: {to_addr}
Subject: {subject}
Body: {body}
---
Note: Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables for production mode.

To enable production mode:
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
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
