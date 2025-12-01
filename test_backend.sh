#!/bin/bash

# Quick test script for TOMAS backend
# Tests that all modes are registered and backend is working

set -e

echo "🧪 Testing TOMAS Backend"
echo ""

# Check if backend is running
echo "Checking if backend is running on port 8000..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Backend is not running on port 8000"
    echo ""
    echo "Please start the backend first:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  python main.py"
    exit 1
fi

echo "✅ Backend is running"
echo ""

# Test health endpoint
echo "Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
echo "Response: $HEALTH"
echo ""

# Test modes endpoint
echo "Testing modes list..."
MODES=$(curl -s http://localhost:8000/api/modes)
echo "Modes response:"
echo "$MODES" | python3 -m json.tool
echo ""

# Count modes
MODE_COUNT=$(echo "$MODES" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('count', 0))")
echo "✅ Found $MODE_COUNT registered modes"
echo ""

# Test each mode details
echo "Testing mode details..."
for MODE_ID in research rfp_sow itops; do
    echo "  Checking $MODE_ID..."
    DETAILS=$(curl -s http://localhost:8000/api/modes/$MODE_ID 2>&1)
    if echo "$DETAILS" | grep -q "\"id\""; then
        echo "  ✅ $MODE_ID registered correctly"
    else
        echo "  ❌ $MODE_ID not found or error"
        echo "  Response: $DETAILS"
    fi
done

echo ""
echo "🎉 Backend tests complete!"
echo ""
echo "To test execution, try:"
echo "  curl -X POST http://localhost:8000/api/execute \\"
echo "    -F 'mode_id=research' \\"
echo "    -F 'input_data={\"data_description\":\"Test data\",\"llm\":\"gpt-4o\"}'"
