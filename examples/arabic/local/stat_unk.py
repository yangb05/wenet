import re


def main(file):
    with open(file, 'r') as f:
         all_unks = re.findall(r'<unk>', f.read())
    print(f'number of unks: {len(all_unks)}')


if __name__ == '__main__':
    file = '/mgData2/yangb/wenet/examples/masc/exp/masc_conformer_bidecoder_large_online_10000/clean_test_ctc_greedy_search_epoch_17/text_bpe_value_tmp'
    main(file)