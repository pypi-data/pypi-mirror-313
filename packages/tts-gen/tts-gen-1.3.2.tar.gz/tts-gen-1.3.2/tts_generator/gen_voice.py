#coding: utf-8

import time
import os.path
import requests
from requests.exceptions import RequestException
import json
import string
import multiprocessing
from tqdm import tqdm
from tts_generator import __server_url__, __server_gx_v2_url__, __server_bridge_url__

headers = {
        'User-Agent'         : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Accept-Language'    : 'zh-CN,zh;q=0.9',
        }

def gen_wav_dir_str(s):
    return s.replace(" ", "_")

def gen_gx_voice(texts, output_dir, server_url=None, voice_num=None, wav_type='all', tts_server_name='gx'):
    if not server_url:
        server_url = __server_url__
    server_synthesize_url = server_url + '/api/synthesize_multi'
    server_info_url = server_url + '/api/info'

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    with requests.Session() as session:
        r = session.get(url=server_info_url, headers=headers, verify=False)
        info = json.loads(r.text)
        if wav_type == 'train':
            max_voice_num = info['max_train_voice_num']
        elif wav_type == 'test':
            max_voice_num = info['max_test_voice_num']
        else:
            max_voice_num = info['max_voice_num']
        if not voice_num:
            total_voice_num = max_voice_num
        else:
            total_voice_num = min(max_voice_num, voice_num)

        for text in texts:
            print('generate %s wavs ...' % text)

            wav_dir_str = gen_wav_dir_str(text)
            text_dir = os.path.join(output_dir, wav_dir_str)
            if not os.path.exists(text_dir):
                os.mkdir(text_dir)

            if wav_type in ('train', 'test'):
                text_dir = os.path.join(text_dir, wav_type)
                if not os.path.exists(text_dir):
                    os.mkdir(text_dir)
                list_f_name = '%s_%s.list' % (wav_dir_str, wav_type)
                wav_dir = '%s/%s' % (wav_dir_str, wav_type)
            else:
                list_f_name = '%s.list' % wav_dir_str
                wav_dir = '%s' % wav_dir_str

            list_f_path = os.path.join(output_dir, list_f_name)
            list_f = open(list_f_path, "w")
            blk_voice_num = 10 # 分块传输
            for voice_index in tqdm(range(0, total_voice_num, blk_voice_num)):
                data = {
                    'text': text,
                    'voice_index': voice_index,
                    'voice_num': min(blk_voice_num, total_voice_num - voice_index),
                    'wav_type': wav_type,
                    }
                try:
                    r = session.post(url=server_synthesize_url, data=data, headers=headers, verify=False, timeout=600)
                    wav_split_map = json.loads(r.headers['Content-Type'])
                    content = r.content
                except RequestException:
                    print('warning: post timeout')
                    wav_split_map = {}
                    content = None
                    time.sleep(60)
                except json.decoder.JSONDecodeError:
                    print('warning: post result parse error')
                    wav_split_map = {}
                    content = None
                    time.sleep(60)
                for k, v in wav_split_map.items():
                    begin, end = v[0], v[1]
                    with open('%s' % os.path.join(text_dir, k), 'wb') as f:
                        f.write(content[begin:end])
                    list_f.write('%s,%s\n' % (os.path.join(wav_dir, k), text))
            list_f.close()


def gen_gx_v2_voice(texts, output_dir, server_url=None, voice_num=None, wav_type='all',
                    age_group='adult', tts_server_name='gx_v2'):
    if not server_url:
        server_url = __server_gx_v2_url__
    server_synthesize_url = server_url + '/api/synthesize_multi'
    server_info_url = server_url + '/api/info'

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    with requests.Session() as session:
        r = session.get(url=server_info_url, headers=headers, verify=False)
        info = json.loads(r.text)

        for text in texts:
            print('generate %s wavs ...' % text)

            if is_english_text(text):
                language = 'en'
                if wav_type == 'train':
                    max_voice_num = info['max_en_train_voice_num'] if age_group == 'adult' else info['max_en_child_train_voice_num']
                elif wav_type == 'test':
                    max_voice_num = info['max_en_test_voice_num'] if age_group == 'adult' else info['max_en_child_test_voice_num']
                else:
                    max_voice_num = info['max_en_voice_num'] if age_group == 'adult' else info['max_en_child_voice_num']
            else:
                language = 'zh'
                if wav_type == 'train':
                    max_voice_num = info['max_zh_train_voice_num'] if age_group == 'adult' else info['max_zh_child_train_voice_num']
                elif wav_type == 'test':
                    max_voice_num = info['max_zh_test_voice_num'] if age_group == 'adult' else info['max_zh_child_test_voice_num']
                else:
                    max_voice_num = info['max_zh_voice_num'] if age_group == 'adult' else info['max_zh_child_voice_num']
            if not voice_num:
                total_voice_num = max_voice_num
            else:
                total_voice_num = min(max_voice_num, voice_num)

            wav_dir_str = gen_wav_dir_str(text)
            text_dir = os.path.join(output_dir, wav_dir_str)
            if not os.path.exists(text_dir):
                os.mkdir(text_dir)

            if wav_type in ('train', 'test'):
                text_dir = os.path.join(text_dir, wav_type)
                if not os.path.exists(text_dir):
                    os.mkdir(text_dir)
                list_f_name = '%s_%s.list' % (wav_dir_str, wav_type)
                wav_dir = '%s/%s' % (wav_dir_str, wav_type)
            else:
                list_f_name = '%s.list' % wav_dir_str
                wav_dir = '%s' % wav_dir_str

            list_f_path = os.path.join(output_dir, list_f_name)
            list_f = open(list_f_path, "w")
            blk_voice_num = 10 # 分块传输
            for voice_index in tqdm(range(0, total_voice_num, blk_voice_num)):
                data = {
                    'text': text,
                    'voice_index': voice_index,
                    'voice_num': min(blk_voice_num, total_voice_num - voice_index),
                    'language': language,
                    'wav_type': wav_type,
                    'age_group': age_group,
                    }
                try:
                    r = session.post(url=server_synthesize_url, data=data, headers=headers, verify=False, timeout=600)
                    wav_split_map = json.loads(r.headers['Content-Type'])
                    content = r.content
                except RequestException:
                    print('warning: post timeout')
                    wav_split_map = {}
                    content = None
                    time.sleep(60)
                except json.decoder.JSONDecodeError:
                    print('warning: post result parse error')
                    wav_split_map = {}
                    content = None
                    time.sleep(60)
                for k, v in wav_split_map.items():
                    begin, end = v[0], v[1]
                    with open('%s' % os.path.join(text_dir, k), 'wb') as f:
                        f.write(content[begin:end])
                    list_f.write('%s,%s\n' % (os.path.join(wav_dir, k), text))
            list_f.close()


def other_voice_post_task(lock, index, total_texts_num, total_voice_num, wav_type, tts_server_name,
                          server_synthesize_url, output_dir, text, language, with_style):
    try:
        wav_name = text
        if len(wav_name) > 20:
            wav_name = wav_name[:20]

        wav_dir_str = gen_wav_dir_str(wav_name)
        text_dir = os.path.join(output_dir, wav_dir_str)
        if not os.path.exists(text_dir):
            os.mkdir(text_dir)

        list_f_name = '%s.list' % wav_dir_str
        wav_dir = '%s' % wav_dir_str
        list_f_path = os.path.join(output_dir, list_f_name)
        list_f = open(list_f_path, "w")

        with lock:
            bar = tqdm(
                desc='[%d/%d] %s' % (index, total_texts_num, text),
                total=total_voice_num,
                position=index,
                leave=False
            )

        blk_voice_num = 10 # 分块传输
        with requests.Session() as session:
            for voice_index in range(0, total_voice_num, blk_voice_num):
                data = {
                    'text': text,
                    'voice_index': voice_index,
                    'voice_num': min(blk_voice_num, total_voice_num - voice_index),
                    'wav_type': wav_type,
                    'platform': tts_server_name,
                    'language': language,
                    'with_style': with_style,
                    }
                r = session.post(url=server_synthesize_url, data=data, headers=headers, verify=False)
                wav_split_map = json.loads(r.headers['Content-Type'])
                for k, v in wav_split_map.items():
                    begin, end = v[0], v[1]
                    with open('%s' % os.path.join(text_dir, k), 'wb') as f:
                        f.write(r.content[begin:end])
                    list_f.write('%s,%s\n' % (os.path.join(wav_dir, k), text))

                with lock:
                    bar.update(blk_voice_num)

        list_f.close()

        with lock:
            bar.close()
    except Exception as e:
        print(e)

def is_english_text(text):
    en_list = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    for t in text:
        if t not in en_list:
            return False
    return True

def gen_other_voice(texts, output_dir, bridge_server_url, voice_num, wav_type,
                    tts_server_name, process_num, with_style):
    if not bridge_server_url:
        bridge_server_url = __server_bridge_url__
    server_synthesize_url = bridge_server_url + '/api/synthesize_multi'
    server_info_url = bridge_server_url + '/api/info'

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    with requests.Session() as session:
        # 中文
        r = session.get(url=server_info_url, headers=headers,
                        params={'platform':tts_server_name,'language':'zh','with_style':with_style},
                        verify=False)
        info = json.loads(r.text)
        zh_max_voice_num = info['max_voice_num']

        # 英文
        r = session.get(url=server_info_url, headers=headers,
                        params={'platform':tts_server_name,'language':'en','with_style':with_style},
                        verify=False)
        info = json.loads(r.text)
        en_max_voice_num = info['max_voice_num']

        if not voice_num:
            zh_total_voice_num = zh_max_voice_num
            en_total_voice_num = en_max_voice_num
        else:
            zh_total_voice_num = min(zh_max_voice_num, voice_num)
            en_total_voice_num = min(en_max_voice_num, voice_num)

        lock = multiprocessing.Manager().Lock()

        with multiprocessing.Pool(process_num) as pool:
            for i, text in enumerate(texts):
                if is_english_text(text):
                    total_voice_num = en_total_voice_num
                    language = 'en'
                else:
                    total_voice_num = zh_total_voice_num
                    language = 'zh'
                pool.apply_async(other_voice_post_task, args=(lock, i, len(texts), total_voice_num, wav_type,
                                                              tts_server_name, server_synthesize_url, output_dir,
                                                              text, language, with_style))
            pool.close()
            pool.join()


def gen_voice(texts, output_dir, server_url=None, bridge_server_url=None, voice_num=None, wav_type='all',
        age_group='adult', tts_server_name='gx', process_num=3, with_style=False):
    if tts_server_name == 'gx':
        return gen_gx_voice(texts, output_dir, server_url, voice_num, wav_type)
    elif tts_server_name == 'gx_v2':
        return gen_gx_v2_voice(texts, output_dir, server_url, voice_num, wav_type, age_group)
    else:
        max_process_num = 1
        if tts_server_name == 'aliyun':
            max_process_num = 2
        elif tts_server_name == 'mobvoi':
            max_process_num = 3
        if process_num > max_process_num:
            process_num = max_process_num
        if server_url is not None:
            bridge_server_url = server_url
        return gen_other_voice(texts, output_dir, bridge_server_url, voice_num, wav_type,
                tts_server_name, process_num, with_style)


if __name__ == '__main__':
    texts = []
    texts.append('你好小爱')
    texts.append('天猫精灵')
    #gen_voice(texts, './wavs')
    gen_voice(texts, './wavs', tts_server_name='aliyun')
    #gen_voice(texts, './wavs', tts_server_name='mobvoi')
    #gen_voice(texts, './aliyun_wavs', tts_server_name='aliyun')
    #gen_voice(texts, './xfyun_wavs', tts_server_name='xfyun')

