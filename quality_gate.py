import json
import sys
from pathlib import Path

METRICS_PATH = Path('metrics.json')
MINIMUM_ACCURACY = 0.80


def main():
    if not METRICS_PATH.exists():
        print('FAIL: metrics.json was not generated.')
        return 1
    with METRICS_PATH.open(encoding='utf-8') as file:
        metrics = json.load(file)
    accuracy = float(metrics.get('accuracy', -1))
    print(f'Model accuracy: {accuracy:.4f}')
    print(f'Required accuracy: {MINIMUM_ACCURACY:.2f}')
    if not 0 <= accuracy <= 1 or accuracy < MINIMUM_ACCURACY:
        print('FAIL: model did not meet the quality threshold.')
        return 1
    print('PASS: model met the quality gate.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
