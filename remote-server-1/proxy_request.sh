#!/bin/sh
echo "DEBUG: Starting script for Windows target" >&2
filename="$1"
echo "DEBUG: Got filename: $filename" >&2

if [ -z "$filename" ]; then
    echo "DEBUG: No filename provided" >&2
    echo "{\"status\":\"error\",\"data\":\"\",\"msg\":\"No filename provided\"}"
    exit 1
fi

echo "DEBUG: Creating HTTP request for Windows server" >&2

response=$(printf "GET /file/%s HTTP/1.1\r\nHost: remote-server-2\r\nUser-Agent: Legacy-Unix-Client/1.0\r\nAccept: application/json\r\nConnection: close\r\n\r\n" "$filename" | nc remote-server-2 8080 2>/dev/null)
result=$?

echo "DEBUG: netcat exit code: $result" >&2
echo "DEBUG: Response length: ${#response}" >&2

if [ $result -eq 0 ] && [ -n "$response" ]; then
    echo "DEBUG: Processing Windows server response" >&2
    final=$(echo "$response" | sed -n '/^{/,/^}/p' | tr -d '\r')
    echo "DEBUG: Extracted JSON: $final" >&2
    echo "$final"
else
    echo "DEBUG: Failed to communicate with Windows server" >&2
    echo "{\"status\":\"error\",\"data\":\"\",\"msg\":\"there was an error retrieving $filename\"}"
fi