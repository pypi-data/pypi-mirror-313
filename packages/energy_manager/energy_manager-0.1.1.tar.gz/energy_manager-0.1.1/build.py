import os

def fix_imports(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                content = content.replace('energy_manager.src.energy_manager', 'energy_manager')
                content = content.replace('energy_manager.src', 'energy_manager')
                with open(file_path, 'w') as f:
                    f.write(content)
    print(f"Import paths fixed in {directory}")

# Target the src folder
fix_imports('src')