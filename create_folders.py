import os

# Create required directories
directories = ['data', 'visualizations']

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"✅ Created {directory}/ folder")
    else:
        print(f"📁 {directory}/ folder already exists")

print("\n🎯 Folder structure ready!")
print("Next: Download dataset to data/ folder")
