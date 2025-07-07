#!/bin/bash

echo "Testing Debug Setup..."
echo "========================"

# Check if containers are running
echo "1. Checking container status:"
docker compose -f docker-compose.debug.yml ps

echo -e "\n2. Checking debug ports:"
netstat -ln | grep -E ":(5678|5679)" || echo "Debug ports not found"

echo -e "\n3. Testing connection to debug ports:"
timeout 2 telnet localhost 5678 < /dev/null && echo "Service1 debug port (5678) is accessible" || echo "Service1 debug port (5678) not responding"
timeout 2 telnet localhost 5679 < /dev/null && echo "Service2 debug port (5679) is accessible" || echo "Service2 debug port (5679) not responding"

echo -e "\n4. Ready for VS Code debugging!"
echo "Next steps:"
echo "- Open VS Code Debug view (Ctrl+Shift+D)"
echo "- Select 'Debug Both Services' configuration"
echo "- Press F5 to attach debugger"
echo "- Set breakpoints in your Python files"
