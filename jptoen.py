# -*- coding: utf-8 -*-
import os
from googletrans import  Translator

class JptoEn:
    def __init__(self):
        self.tr = Translator()
    
    def Trans(self, jpmsg):
        enmsg = self.tr.translate(jpmsg, src="ja", dest="en").text
        return enmsg

class plantuml:
    # cps_str = "CPS"
    # ipodut_str = "iPodUT"
    # ipoddt_str = "iPodDT"
    # SPI_str = "SPI"

    # syncline_str = "->"
    # asyncline_str = "->>"
    # resyncline_str = "<-"
    # reasyncline_str = "<<-"

    ng_word =\
        {"CPS": "aaa",
         "iAP": "bbb"}

    msgline = \
        ["->",
        "<-"]

    idllist = []
    count = 0

    #初期化
    def __init__(self):
        self.save_file = None
        return
        

    def savefile_open(self):
        conversion_fname = 'en_' + self.fname
        if os.path.isfile(conversion_fname):
            os.remove(conversion_fname)
        self.save_file = open(conversion_fname, 'w', encoding='utf-8')

    def eng_conversion(self, line):
        self.save_file.write(line)
        # if line in '\n':
        #     self.save_file.write(line)
        # else:
        #     self.save_file.write(line + '\n')

    def opencheck(self, obj):
        if obj is None:
            return True
        return False
    
    #対象のメッセージ線をチェック
    def linecheck(self, line):
        chk = False
        for l in self.msgline:
            if l in line:
                self.count += 1
                chk = self.check(line)
        return chk
        
    #対象のメッセージなのかチェック
    def check(self, line: str):
        print('check function :: %s' % line)
        strstr1: str = line.split(': ')
        if strstr1[1] is not None:
            print('strstr1 :: %s' % strstr1[1])
            strstr2 = strstr1[1].split('\\n')
            print('strstr2 :: %s' % strstr2[0])
        else:
            return False

        src_trans = strstr2[0]
        jtoe = JptoEn()
        undoflg = False
        for word in self.ng_word:
            if word in strstr2[0]:
                if word in self.ng_word:
                    undoflg = True
                    val = self.ng_word.get(word)
                    src_trans = strstr2[0].replace(word, val)

        if undoflg:
            if src_trans is not None:
                print('src_trans :: %s' % src_trans)
                eng = jtoe.Trans(src_trans)
                eng = eng.lower()
                print('eng :: %s' % eng)
                ret = self.Undo_ngword(eng)
                self.conv_str = self.Undo_linestr(ret, strstr1[0], strstr2)
                return True
        else:
            eng = jtoe.Trans(src_trans)
            eng = eng.lower()
            self.conv_str = self.Undo_linestr(eng, strstr1[0], strstr2)
            return True

        print('check fucntion end.')
        return False

    def Undo_ngword(self, eng : str):
        ret : str = None
        for word in self.ng_word:
            val = self.ng_word.get(word)

            if val in eng:
                ret = eng.replace(val, word)
                print('Undo_ngword function :: %s' % ret)
        
        return ret

    def Undo_linestr(self, ret, strstr1, strstr2):
        return strstr1 + ': ' + strstr2[0] + ' / ' + ret + '\\n' + strstr2[1]

    #plantumlファイルを読む
    def read(self, obj):
        self.count  = 0
        self.savefile_open()
        while True:
            line = obj.readline()
            if self.linecheck(line):
                self.eng_conversion(self.conv_str)
            else:
                self.eng_conversion(line)
                
            if not line:
                break

        self.save_file.close()

    #Plantumlファイルを開く
    def open(self, filename):
        self.fname = filename
        return open(filename, 'r', encoding='utf-8')

def main():
    
    plt = plantuml()
    #mainでplantumlクラスの保存要をチェックして
    #excの保存メソッドをコールする

    for file in os.listdir():
        if '.puml' in file:
            if 'en_' in file:
                continue
            obj = plt.open(file)
            if obj is None:
                continue
            else:
                plt.read(obj)

    return

if __name__ == '__main__':
    main()
