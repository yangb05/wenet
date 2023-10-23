import json
from pathlib import Path
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(description='remove bad samples.')
    parser.add_argument('--data_dir',
                        default=None,
                        type=str,
                        help='directory of original data.list, wav.scp and bad_samples')
    return parser.parse_args()


def main(args):
    data_dir = Path(args.data_dir)
    original_data_list = data_dir / 'data.list'
    original_data_list = original_data_list.rename(data_dir / 'data.list.orginal')
    original_wav_scp = data_dir / 'wav.scp'
    original_wav_scp = original_wav_scp.rename(data_dir / 'wav.scp.original')
    new_data_list = []
    with open(data_dir / 'bad_samples', 'r') as f:
        bad_samples = f.read().split('\n')
    with open(original_data_list, 'r') as f:
        for line in f.readlines():
            data = json.loads(line.strip())
            if data['key'] not in bad_samples:
                new_data_list.append(data)
    with open(data_dir / 'data.list', 'w') as f1:
        with open(data_dir / 'wav.scp', 'w') as f2:
            for data in new_data_list:
                f1.write(json.dumps(data, ensure_ascii=False)+'\n')
                f2.write(f"{data['key']} {data['wav']}\n")


if __name__ == '__main__':
    args = get_args()
    main(args)
    
    