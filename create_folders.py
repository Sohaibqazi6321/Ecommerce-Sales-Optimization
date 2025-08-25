import os

# Create required directories
directories = ['data', 'visualizations']

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created folder: {directory}")
    else:
        print(f"Folder already exists: {directory}")

print("\nProject structure setup complete!")
print("Next: Download dataset to data/ folder")
