#!/bin/bash

echo "🚀 TOMAS Frontend Setup Script"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully!"
echo ""

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local file..."
    cat > .env.local << EOF
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Feature Flags (optional)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=false
EOF
    echo "✅ .env.local created!"
else
    echo "ℹ️  .env.local already exists, skipping..."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Make sure the backend is running on http://localhost:8000"
echo "  2. Run: npm run dev"
echo "  3. Open http://localhost:3000 in your browser"
echo ""
echo "Theme Features:"
echo "  • Light Mode: Very light blue background"
echo "  • Dark Mode: Very dark navy blue background"
echo "  • Toggle between themes using the button in the header"
echo ""
echo "Happy coding! 🚀"
