# -*- coding: UTF-8 -*-
# Copyright©2022 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

"""
from typing import Dict, Union, List, Any, NoReturn, Tuple
#!python
from math import log
class HalfPatten:

    def __init__(self,x):
        self.x = x
        self.type = "halfPatten"
        self.shan = 0.
        self.regShan= 0.
        self.x_length = [len(i) for i in x]
        for i in set(self.x_length):
            self.shan -= (float(self.x_length.count(i))/len(self.x_length))*log(float(self.x_length.count(i))/len(self.x_length))
        for c in set(self.x):
            self.regShan -= (float(self.x.count(c))/len(self.x))*log(float(self.x.count(c))/len(self.x))


    def detection(self,string):
        s = ''.join(string)
        if len(s)==0:
            return ""
        if s.isalnum():
            if s.isdigit():
                return "\d"
            return "\w"
        else:
            return "."

    def gener(self,patten):
        if patten=="all":
            return "%s+"%(self.detection(self.x))
        elif patten=="zone":
            x_len = self.x_length
            x_len.sort()

            return "%s{%i,%i}"%(self.detection(self.x),x_len[0],x_len[-1])
        else:
            return "%s{%i}"%(self.detection(self.x),self.x_length[0])

    def regex(self,shanRule):
        if self.detection(self.x)=="":
            return ""
        if self.shan>0:
            if self.shan>shanRule:
                return self.gener("all")
            else:
                return self.gener("zone")
        else:
            return self.gener("length")


class FullPatten:

    def __init__(self,x):
        self.x = x
        self.type = "fullPatten"
        self.shan = 0.
        self.regShan = 0.

    def gener(self,patten):
        if patten=="all":
            return "(%s)"%(self.x[0])
        else:
            return "(%s)"%('|'.join(list(set(self.x))))

    def regex(self,shanRule):
        if len(set(self.x))>1:
            return self.gener("half")
        else:
            return self.gener("all")

class strspl:

    def __init__(self,y,shan):
        self.sentence = []
        self.y = y
        self.shan = shan

    def re_split(self,string):
        s = []
        for x in self.y:
            s.append([x[:x.index(string)],string,x[x.index(string)+len(string):]])
        half_1 = []
        full_1 = []
        half_2 = []
        for q,w,e in s:
            half_1.append(q)
            full_1.append(w)
            half_2.append(e)
        self.sentence.append(HalfPatten(half_1))
        self.sentence.append(FullPatten(full_1))
        self.sentence.append(HalfPatten(half_2))

        for l,i in enumerate(self.sentence):
            if i.shan!=0.:
                if i.regShan<self.shan:
                    self.sentence[l]=FullPatten(i.x)

def main(shan=1.5):
    example = ['asb.baidu.go','ww.baidu.com','www.baidu.fuck']
    a = strspl(example,shan)
    a.re_split('.baidu.')
    sentence=[]
    regex = []
    for i in a.sentence:
        sentence.append(i.type)
        regex.append(i.regex(0.))
    return sentence,''.join(regex)

if __name__ == "__main__":
    s,r = main()
    print(s)
    print(r)
    s,r = main(0.)
    print(s)
    print(r)