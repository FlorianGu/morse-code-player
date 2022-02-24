# -*-coding:utf-8-*-
from numpy import zeros, append, sin, pi, arange, hstack
from scipy.io.wavfile import write
from pynput.keyboard import Events, Key
from sounddevice import play


freq = 700  # 摩尔斯电码的音调频率
rate = 96000  # 生成、播放摩尔斯电码音频的采样率
duration = 0.06  # 摩尔斯电码中“点”的长度(秒)，用来控制发报速度
o = zeros(int(rate * duration))  # 以“点”的长度作为单位间隔
p = append(sin(2 * pi * freq / rate * arange(rate * duration)), o)  # “嘀”的正弦波 + 1份单位间隔
q = append(sin(2 * pi * freq / rate * arange(rate * duration * 3)), o)  # “”嗒的正弦波 + 1份单位间隔
encode = {  # 定义常用字符与摩尔斯电码间的映射
    'A': [p, q],
    'B': [q, p, p, p],
    'C': [q, p, q, p],
    'D': [q, p, p],
    'E': [p],
    'F': [p, p, q, p],
    'G': [q, q, p],
    'H': [p, p, p, p],
    'I': [p, p],
    'J': [p, q, q, q],
    'K': [q, p, q],
    'L': [p, q, p, p],
    'M': [q, q],
    'N': [q, p],
    'O': [q, q, q],
    'P': [p, q, q, p],
    'Q': [q, q, p, q],
    'R': [p, q, p],
    'S': [p, p, p],
    'T': [q],
    'U': [p, p, q],
    'V': [p, p, p, q],
    'W': [p, q, q],
    'X': [q, p, p, q],
    'Y': [q, p, q, q],
    'Z': [q, q, p, p],
    'a': [p, q],
    'b': [q, p, p, p],
    'c': [q, p, q, p],
    'd': [q, p, p],
    'e': [p],
    'f': [p, p, q, p],
    'g': [q, q, p],
    'h': [p, p, p, p],
    'i': [p, p],
    'j': [p, q, q, q],
    'k': [q, p, q],
    'l': [p, q, p, p],
    'm': [q, q],
    'n': [q, p],
    'o': [q, q, q],
    'p': [p, q, q, p],
    'q': [q, q, p, q],
    'r': [p, q, p],
    's': [p, p, p],
    't': [q],
    'u': [p, p, q],
    'v': [p, p, p, q],
    'w': [p, q, q],
    'x': [q, p, p, q],
    'y': [q, p, q, q],
    'z': [q, q, p, p],
    '0': [q, q, q, q, q],
    '1': [p, q, q, q, q],
    '2': [p, p, q, q, q],
    '3': [p, p, p, q, q],
    '4': [p, p, p, p, q],
    '5': [p, p, p, p, p],
    '6': [q, p, p, p, p],
    '7': [q, q, p, p, p],
    '8': [q, q, q, p, p],
    '9': [q, q, q, q, p],
    '.': [p, q, p, q, p, q],
    '?': [p, p, q, q, p, p],
    '/': [q, p, p, q, p],
    '(': [q, p, q, q, p, q],
    ')': [q, p, q, q, p, q],
    ',': [q, q, p, p, q, q],
    ':': [q, q, q, p, p, p],
    ' ': [o, o, o, o],
    '\n': [o, o, o, o],
    '\'': [p, q, q, q, q, p],
    'char_interval': [o, o],
    'error': [],
    Key.space: [o, o, o, o],
    Key.enter: [o, o, o, o]
}


def encoding(text):
    """对每个字符按上述映射进行编译并转换成正弦波，再整合并返回所转换的内容"""
    char_encoding = [hstack(encode.get(i, encode['error']) + encode['char_interval']) for i in text]  # 编译并转换
    str_encoding = hstack(char_encoding)  # 整合
    return str_encoding  # 返回以上正弦波


def morse_write(text, file):
    """将文本转换成摩尔斯电码形式的正弦波，再将正弦波写成音频文件"""
    result = encoding(text)  # 获取相应正弦波
    write(file, rate, result)  # 将正弦波写成音频文件


def morse_play_word():
    """实时将键盘的敲击情况转换成字符，以单词为单位（每敲击空格键或回车键视为一个单词敲击完成）播放相应的摩尔斯电码音频。即每敲击空格键或回车键一次就会播放相应单词的摩尔斯电码音频"""
    text = []  # 初始化
    with Events() as e:
        for i in e:  # 监听键盘
            if isinstance(i, Events.Press):  # 键盘敲击
                text.append(eval(str(i.key)))  # 将键盘敲击转换成字符并记录
                if i.key == Key.space or i.key == Key.enter:  # 单词敲击完成
                    result = encoding(text)  # 获取相应正弦波
                    play(result, rate, blocking=True)  # 播放正弦波
                    text = []  # 一个单词的摩尔斯电码播放完毕，初始化


def morse_play_letter():
    """实时将键盘的敲击情况转换成字符，以字符为单位播放相应的摩尔斯电码音频，即每敲击键盘一次就会播放相应字符的摩尔斯电码音频"""
    with Events() as e:
        for i in e:  # 监听键盘
            if isinstance(i, Events.Press):  # 键盘敲击
                text = [eval(str(i.key))]  # 将键盘敲击转换成字符
                result = encoding(text)  # 获取相应正弦波
                play(result, rate, blocking=True)  # 播放正弦波
