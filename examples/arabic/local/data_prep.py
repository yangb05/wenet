import re
import csv
import json
from pathlib import Path

import torchaudio
from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import normalize_unicode, normalize_alef_ar, normalize_alef_maksura_ar, normalize_teh_marbuta_ar

def extract_MSA(meta_file: Path):
    audio_ids = set()
    with open(meta_file) as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            if row[5] == 'MSA':
                audio_ids.add(row[0])
    return audio_ids


def transfer_to_ms(str_time):
    res = re.match(r'([\d]+):([\d]{2}):([\d]{2}).([\d]{3})', str_time)
    h, m, s, ms = res[1], res[2], res[3], res[4]
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)


def preprocess_text(text):
    # the text should be processed by camel_arclean at first.
    # normalize text
    text = normalize_unicode(text)
    text = normalize_alef_ar(text)
    text = normalize_alef_maksura_ar(text)
    text = normalize_teh_marbuta_ar(text)
    # dediacritization
    text = dediac_ar(text)
    # remove punctuations
    punctuation_string = '!"#$&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    text = text.translate(str.maketrans('', '', punctuation_string))
    return text
    

def extract_dev_test_segments_info(segments_file: Path):
    segments_info = []
    with open(segments_file) as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            txt = preprocess_text(row[4])
            if txt:
                segments_info.append({
                    'audio_id': row[0],
                    'start': int(float(row[1]) * 1000),
                    'end': int(float(row[2]) * 1000),
                    'txt': txt
                })
    return segments_info


def extract_train_segments_info(data_dir, audio_ids):
    results = []
    for audio_id in audio_ids:
        with open(data_dir / 'subtitles' / f'camel_arclean_{audio_id}.ar.vtt', 'r', encoding='utf-8') as f:
            content = f.read()
            segments_info = content.split('\n\n')[1:]
            for seg_info in segments_info:
                seg_info = seg_info.strip()
                if seg_info:
                    seg_info = seg_info.split('\n')
                    if re.match(r'[\d]+:[\d]{2}:[\d]{2}.[\d]{3}', seg_info[0]):    
                        time_info = seg_info[0]
                        start, end = time_info.split(' --> ')
                        txt = ' '.join(seg_info[1:]).strip()
                    elif len(seg_info) > 1: # deal with RJUrUSP95Pc.ar.vtt
                        time_info = re.findall(r'[\d]+:[\d]{2}:[\d]{2}.[\d]{3}', seg_info[1])
                        start, end = time_info[0], time_info[1]
                        txt = ' '.join(seg_info[2:]).strip()
                    else:
                        continue
                    txt = preprocess_text(txt)
                    if txt:
                        start_time = transfer_to_ms(start)
                        end_time = transfer_to_ms(end)
                        results.append({
                            'audio_id': audio_id,
                            'start': start_time,
                            'end': end_time,
                            'txt': txt
                        })
    return results


def extract_segments(data_dir: Path, subset: str, audio_ids, segments_info):
    data_list = []
    seg_dir = data_dir / 'wavedata' /'segments' / subset
    seg_dir.mkdir(parents=True, exist_ok=True)
    duration = 0
    for audio_id in audio_ids:
        audio = AudioSegment.from_wav(data_dir / 'audios' / f'{audio_id}.wav')
        audio_segments_info = (seg for seg in segments_info if seg['audio_id'] == audio_id)
        for idx, seg in enumerate(audio_segments_info):
            key = audio_id + '_' + str(idx)
            wav = str(seg_dir / f'{key}.wav')
            data_list.append({
                'key': key,
                'wav': wav,
                'txt': seg['txt']
            })
            segment = audio[seg['start']: seg['end']+1]
            duration += seg['end'] - seg['start']
            segment.export(wav, format='wav')
    print(f'{subset} duration is: {duration / 3600000:.2f}h')
    return data_list
        

def write_info(data_dir: Path, subset: str, data_list):
    wave_dir = data_dir / 'wavedata' / subset
    wave_dir.mkdir(parents=True, exist_ok=True)
    with open(wave_dir / 'data.list', 'w') as f1:
        with open(wave_dir / 'wav.scp', 'w') as f2:
            with open(wave_dir / 'text', 'w') as f3:
                for data in data_list:
                    f1.write(json.dumps(data, ensure_ascii=False)+'\n')
                    f2.write(f"{data['key']} {data['wav']}\n")
                    f3.write(f"{data['key']} {data['txt']}\n")
    print(f'{subset} done!')    


def main():
    data_dir = Path('/mgData4/yangb/data/MASC/masc')
    data_files = {
        # 'clean_dev': ('camel_arclean_clean_dev.csv', 'clean_dev_meta.csv'),
        # 'clean_test': ('camel_arclean_clean_test.csv', 'clean_test_meta.csv'),
        # 'clean_train': ('clean_train.csv'),
        # 'noisy_dev': ('camel_arclean_noisy_dev.csv', 'noisy_dev_meta.csv'),
        # 'noisy_test': ('camel_arclean_noisy_test.csv', 'noisy_test_meta.csv'),
        'noisy_train': ('noisy_train.csv')
    }
    for subset in data_files:
        if 'train' not in subset:
            segments_file, meta_file = data_files[subset]
            audio_ids = extract_MSA(data_dir / 'subsets' / meta_file)
            segments_info = extract_dev_test_segments_info(data_dir / 'subsets' / segments_file)
            data_list = extract_segments(data_dir, subset, audio_ids, segments_info)
            write_info(data_dir, subset, data_list)
        else:
            meta_file = data_files[subset]
            audio_ids = extract_MSA(data_dir / 'subsets' / meta_file)
            segments_info = extract_train_segments_info(data_dir, audio_ids)
            data_list = extract_segments(data_dir, subset, audio_ids, segments_info)
            write_info(data_dir, subset, data_list)
            

if __name__ == '__main__':
    main()
    