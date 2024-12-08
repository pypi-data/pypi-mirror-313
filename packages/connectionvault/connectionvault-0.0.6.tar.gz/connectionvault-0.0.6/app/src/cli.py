import argparse
import tomli

def get_version():
    with open('pyproject.toml', 'rb') as f:
        config = tomli.load(f)
        return config['tool']['poetry']['version']

def get_dependencies():
    with open('pyproject.toml', 'rb') as f:
        config = tomli.load(f)
        dependencies = config['tool']['poetry']['dependencies']
        return dependencies

def get_usage():
    with open('README.md', 'r') as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description='ConnectionVault CLI Tool')
    parser.add_argument('--version', action='version', version=f'ConnectionVault {get_version()}')
    parser.add_argument('--dependencies', action='store_true', help='Show project dependencies')
    parser.add_argument('--usage', action='store_true', help='Show usage information from README.md')
    
    args = parser.parse_args()

    if args.dependencies:
        dependencies = get_dependencies()
        print("Project Dependencies:")
        for dep, version in dependencies.items():
            print(f"{dep}: {version}")

    if args.usage:
        usage_info = get_usage()
        print("Usage Information:\n")
        print(usage_info)

if __name__ == '__main__':
    main()
