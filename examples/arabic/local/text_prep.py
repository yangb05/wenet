from pathlib import Path
from argparse import ArgumentParser
from maha.processors import StreamFileProcessor


def get_args():
    parser = ArgumentParser()
    parser.add_argument('--original_text', type=str, default=None, help='the file hold the original arabic text')
    parser.add_argument('--processed_text', type=str, default=None, help='the file hold the processed arabic text')
    return parser.parse_args()

def main():
    args = get_args()
    processor = StreamFileProcessor(args.original_text)
    processor = processor.remove(punctuations=True).normalize(all=True).drop_empty_lines()
    processor.process_and_save(Path(args.processed_text), n_lines=10000000)


if __name__ == '__main__':
    main()