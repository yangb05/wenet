import json

def extract_txt(infile, outfile):
    with open(infile, 'r') as fin:
        with open(outfile, 'w') as fout:
            for idx, line in enumerate(fin.readlines(), start=1):
                dic = json.loads(line.strip())
                key = dic['key']
                txt = dic['txt']
                fout.write(f'{key} {txt}\n')
            print(f'txt lines: {idx}')


if __name__ == '__main__':
    infile = '/mgData4/yangb/data/MASC/masc/wavedata/noisy_train/data.list'
    outfile = '/mgData4/yangb/data/MASC/masc/wavedata/noisy_train/text'
    extract_txt(infile, outfile)
            