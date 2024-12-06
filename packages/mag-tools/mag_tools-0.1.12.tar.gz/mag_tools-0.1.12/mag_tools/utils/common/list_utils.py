import re
from typing import List


class ListUtils:
    @staticmethod
    def split_by_boundary(lines, keyword_map):
        text = "\n".join(lines)
        segments = {segment_name: [] for segment_name in keyword_map}
        segments["FIRST"] = []
        segments["END"] = []

        # 找到第一个有效段落的开始和最后一个有效段落的结束位置
        first_segment_start = None
        last_segment_end = None

        for segment_name, (begin_keyword, end_keyword) in keyword_map.items():
            pattern = rf"{segment_name}\n{begin_keyword}.*?\n{end_keyword}"
            matches = re.finditer(pattern, text, re.DOTALL)

            for match in matches:
                if first_segment_start is None:
                    first_segment_start = match.start()
                last_segment_end = match.end()

                block_lines = match.group().split("\n")
                segments[segment_name] = block_lines

        # 将第一个有效段落之前的内容放在 FIRST 段落
        if first_segment_start is not None:
            segments["FIRST"] = text[:first_segment_start].strip().split("\n")

        # 将最后一个有效段落之后的内容放在 END 段落
        if last_segment_end is not None:
            segments["END"] = text[last_segment_end:].strip().split("\n")

        return segments

    @staticmethod
    def split_by_keyword(lines, keywords):
        text = "\n".join(lines)
        segments = {keyword: [] for keyword in keywords}

        # 构建正则表达式模式
        pattern = "|".join([re.escape(keyword) for keyword in keywords])
        matches = list(re.finditer(pattern, text))

        if not matches:
            return segments

        # 处理每个段落
        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            segment_name = match.group()
            segments[segment_name] = text[start:end].strip().split("\n")

        return segments

    @staticmethod
    def trim(lines: List[str]) -> List[str]:
        """
        去掉字符串数组的起始和结尾的空行
        :param lines: 字符串数组
        :return: 去掉空行后的字符串数组
        """
        # 去掉起始的空行
        while lines and lines[0].strip() == '':
            lines.pop(0)

        # 去掉结尾的空行
        while lines and lines[-1].strip() == '':
            lines.pop()

        return lines

if __name__ == '__main__':
    # 示例用法
    data = """MODELTYPE BlackOil
FIELD

GRID
##################################################
DIMENS
 5 2 1

BOX FIPNUM 1 5 1 2 1 1 = 2

PERMX
49.29276      162.25308      438.45926      492.32336      791.32867
704.17102      752.34912      622.96875      542.24493      471.45953

COPY PERMX  PERMY  1 5 1 2 1 1 
COPY PERMX  PERMZ  1 5 1 2 1 1

BOX  PERMZ  1 5 1 2 1 1  '*' 0.01

PORO
 5*0.087
 5*0.097

TOPS 10*9000.00

BOX TOPS   1  1  1 2  1  1  '='  9000.00
BOX TOPS   2  2  1 2  1  1  '='  9052.90

DXV
 5*300.0

DYV
 2*300.0

DZV
 20

#GRID END#########################################

WELL
##################################################

TEMPLATE
'MARKER' 'I' 'J' 'K1' 'K2' 'OUTLET' 'WI' 'OS' 'SATMAP' 'HX' 'HY' 'HZ' 'REQ' 'SKIN' 'LENGTH' 'RW' 'DEV' 'ROUGH' 'DCJ' 'DCN' 'XNJ' 'YNJ' /
WELSPECS
NAME 'INJE1'
''  24  25  11  11  NA  NA  SHUT  NA  0  0  0  NA  NA  NA  0.5  NA  NA  NA  1268.16  NA  NA  
''  24  25  11  15  NA  NA  OPEN  NA  0  0  DZ  NA  NA  NA  0.5  NA  NA  NA  0  NA  NA  

NAME 'PROD2'
''  5  1  2  2  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA  
''  5  1  3  3  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA  
''  5  1  4  4  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA 
#WELL END#########################################

PROPS
##################################################
SWOF
#           Sw         Krw       Krow       Pcow(=Po-Pw)
       0.15109           0           1         400
       0.15123           0     0.99997      359.19
       0.15174           0     0.99993      257.92

#PROPS END########################################

SOLUTION
##################################################

EQUILPAR
# Ref_dep    Ref_p    GWC/OWC  GWC_pc/OWC_pc   dh
  9035       3600      9950        0.0         2
# GOC       GOC_pc
  8800        0.0    
PBVD
   5000        3600
   9000        3600

#SOLUTION END######################################

TUNE
TSTART  1990-01-01 
MINDT  0.1  MAXDT  31  DTINC  2.0  DTCUT  0.5  CHECKDX  
MAXDP  200  MAXDS  0  MAXDC  0  MBEPC  1E-4  MBEAVG  1E-6   
SOLVER  1034


RESTART

RPTSCHED
BINOUT SEPARATE NETONLY GEOM RPTONLY RSTBIN SOLVD 
POIL SOIL SGAS SWAT RS NOSTU  TECPLOT 
 /

RPTSUM
POIL 1 2 1 /
POIL AVG Reg 2 /
"""
    # keyword_map = {
    #     "GRID": ("##################################################", "#GRID END#########################################"),
    #     "WELL": ("##################################################", "#WELL END#########################################"),
    #     "PROPS": ("##################################################", "#PROPS END########################################"),
    #     "SOLUTION": ("##################################################", "#SOLUTION END######################################")
    # }
    #
    # _segments = ListUtils.split_by_boundary(data.splitlines(), keyword_map)
    #
    # for segment_name, segment in _segments.items():
    #     print(f"Segment: {segment_name}")
    #     for line in segment:
    #         print(f"    {line}")
    #     print()
    #
    # 示例用法
    lines = [
        "PVDG",
        "1234   3kd  kjfd",
        "djjf  kjkfdj kjkj",
        "PVTO",
        "kfd jkfd kfd",
        "fdj kjk kjkj"
    ]

    keywords = ["PVDG", "PVTO"]

    splitter = ListUtils()
    segments = splitter.split_by_keyword(lines, keywords)
    for key, segment in segments.items():
        print(key)
        print(segment)

