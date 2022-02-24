# -*-coding:utf-8-*-
from morsecode import morse_write


def main():
    with open('test.txt')as f:
        text = f.read()
    morse_write(text, 'test.wav')


if __name__ == '__main__':
    main()
