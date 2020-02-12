import argparse
import json
from datetime import datetime, timezone
from src.routes import get_controller_cls


parser = argparse.ArgumentParser(description='Crawler configurations')
parser.add_argument('controller',
                    type=str, help='Controller name to use')
parser.add_argument('filename',
                    type=str, help='Way to JSON inputs file')


if __name__ == '__main__':
    args = parser.parse_args()

    file_name = args.filename
    with open(file_name) as f:
        data = json.loads(f.read())

    controller_name = args.controller
    controller_cls = get_controller_cls(controller_name)

    resp = controller_cls(input_data=data).run()

    output_filename = f'outputs/output_{controller_name}' \
                      f'-{datetime.now(tz=timezone.utc).strftime("%m-%d-%YT%H:%M:%S")}.json'
    with open(output_filename, 'w+') as outfile:
        json.dump(resp, outfile, indent=2)
