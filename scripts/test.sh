

echo "Testing System Stability Solution..."

# Test Remote Server 2 directly
echo "1. Testing Remote Server 2 directly..."
curl -s http://localhost:8080/file/test.txt | jq '.'

# Test full flow through Local Server
echo -e "\n2. Testing full flow through Local Server..."
curl -s http://localhost:5001/file/test.txt | jq '.'

# Test error case
echo -e "\n3. Testing error case (non-existent file)..."
curl -s http://localhost:5001/file/nonexistent.txt | jq '.'

# Test health endpoints
echo -e "\n4. Testing health endpoints..."
curl -s http://localhost:5001/health | jq '.'
curl -s http://localhost:8080/health | jq '.'

echo -e "\nTest complete!"