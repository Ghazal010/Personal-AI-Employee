#!/usr/bin/env python3
"""
Test script for Email MCP Server
Verifies the server responds correctly to MCP protocol requests
"""

import json
import subprocess
import sys


def test_mcp_server():
    """Test the MCP server with sample requests"""

    print("🧪 Testing Email MCP Server...\n")

    # Test 1: Initialize
    print("Test 1: Initialize request")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }

    result = send_request(init_request)
    if result and "serverInfo" in result:
        print("✅ Initialize: PASSED\n")
    else:
        print("❌ Initialize: FAILED\n")
        return False

    # Test 2: List tools
    print("Test 2: List tools request")
    list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }

    result = send_request(list_request)
    if result and "tools" in result and len(result["tools"]) > 0:
        print(f"✅ List tools: PASSED (found {len(result['tools'])} tools)\n")
    else:
        print("❌ List tools: FAILED\n")
        return False

    # Test 3: Send email
    print("Test 3: Send email request")
    email_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "send_email",
            "arguments": {
                "to": "test@example.com",
                "subject": "Test Email from MCP Server",
                "body": "This is a test email to verify the MCP server is working correctly."
            }
        }
    }

    result = send_request(email_request)
    if result and "content" in result:
        print("✅ Send email: PASSED\n")
        print("Email content:")
        print(result["content"][0]["text"])
    else:
        print("❌ Send email: FAILED\n")
        return False

    print("\n🎉 All tests passed! MCP server is working correctly.")
    return True


def send_request(request):
    """Send a request to the MCP server and get response"""
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, "email_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/user/Documents/GitHub/Personal AI Employee/mcp_server"
        )

        # Send request
        request_json = json.dumps(request) + "\n"
        stdout, stderr = process.communicate(input=request_json, timeout=5)

        # Parse response
        if stdout:
            response = json.loads(stdout.strip())
            return response
        else:
            print(f"Error: {stderr}")
            return None

    except subprocess.TimeoutExpired:
        process.kill()
        print("Error: Server timeout")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
