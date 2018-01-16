# Create zip of your module
cd ./packedModule
python -m zipfile -c ../app.zip ./
cd ..

# Convert it into a binary
echo '#!/usr/bin/env python' >> app
cat app.zip >> app
chmod +x app

# Execute the binary
./app