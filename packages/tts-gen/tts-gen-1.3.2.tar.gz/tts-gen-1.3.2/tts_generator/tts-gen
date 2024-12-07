#!/usr/bin/env python

import sys
import argparse
from tts_generator import __version__, __server_url__, __server_gx_v2_url__, __server_bridge_url__
from tts_generator.gen_voice import gen_voice

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='tts-gen', description='TTS Generator')
    parser.add_argument('-V', '--version', action='version', version='tts-gen %s' % __version__)
    parser.add_argument('-f', '--file', help='tts keywords file, one keyword per line')
    parser.add_argument('-o', '--output', help='output wavs directory')
    parser.add_argument('-n', '--num', type=int, help='number of wavs to be generated per keyword (default: max)')
    parser.add_argument('-u', '--url', help='url of tts server (default: gx: %s, gx_v2: %s, aliyun/mobvoi: %s)'
            % (__server_url__, __server_gx_v2_url__, __server_bridge_url__))
    parser.add_argument('-b', '--bridge_url', help='(LEGACY) url of aliyun/mobvoi tts server (default: %s)' % __server_bridge_url__)
    parser.add_argument('-t', '--type', choices=['all', 'train', 'test'], default='all',
                        help='generate train, test, or all wavs (default: all) (only valid when gx or gx_v2 selected)')
    parser.add_argument('-a', '--age_group', choices=['adult', 'child'], default='adult',
                        help='generate adult or child wavs (default: adult) (only valid when gx_v2 selected)')
    parser.add_argument('-i', '--infer', choices=['gx', 'gx_v2', 'aliyun', 'mobvoi'], default='gx',
                        help='tts server (default: gx)')
    parser.add_argument('-p', '--process', type=int, default=3, help='multiply process num (default/max: mobvoi 3, aliyun 2, gx 1, gx_v2 1)')
    parser.add_argument('-s', '--style', action="store_true", help='generate wavs with speaker style')
    args = parser.parse_args()
    if args.file and args.output:
        texts = []
        for line in open(args.file, 'r'):
            line = line.strip(' ').strip('\t').strip('\n')
            if line:
                texts.append(line)
        gen_voice(texts, args.output, server_url=args.url, bridge_server_url=args.bridge_url,
                  voice_num=args.num, wav_type=args.type, age_group=args.age_group, tts_server_name=args.infer,
                  process_num=args.process, with_style=args.style)
    else:
        parser.print_help()
        sys.exit(0)
