import sys
import json

if __name__ == "__main__":
    piped_input = sys.stdin.read()
    data = json.loads(piped_input)

    vulnerable_packages = set([
        feature['Name'] + ':' + feature['Version']
        for feature in data['Layer']['Features']
        if 'Vulnerabilities' in feature
    ])

    print('\n'.join(vulnerable_packages))
    exit(0)
