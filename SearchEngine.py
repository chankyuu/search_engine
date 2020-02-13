# -*- coding: utf-8 -*-
import requests
import string
import pickle


def only_string(h):
    now = 0  # <>사이의 문자는 순수문자열이 아니기 때문에 now 변수를 이용하여 판단하였다.
    script = 0  # 현재 인덱스의 위치가 script 태그 안에 있는지 체크하는 변수
    style = 0  # 현재 인덱스의 위치가 style 태그 안에 있는지 체크하는 변수
    result1 = ""  # 순수문자열이 추가될 빈 문자열 객체 생성
    line = source.split('\n')  # 한 문장씩 검사하기 위하여 source를 줄바꿈 문자로 split하여 리스트에 저장한다.

    for ch in line:
        for i in range(len(ch)):  # 한 문장의 하나의 단어씩 검사한다.
            if ch[i] == '>' and "<script" in ch:  # '>'로 끝나지만 그 문장이 script 태그 내부에 있다면 순수 문자열로 취급하지 않는다.(교수님 말씀)
                now = 0  # 따라서 now = 0, script = 1(script 태그 안에 위치해있음을 표현함) 을 대입하여 현 상황을 파악한다.
                script = 1
                continue
            if ch[i] == '>' and "</script" in ch:  # '>'로 끝나고 script 태그가 끝났다면 순수 문자열로 취급하여도 무관하다.
                now = 1  # 따라서 now = 1, script = 0 (script 태그 안에 위치해있지 않음을 표현함)을 대입한다.
                script = 0
                continue
            if ch[i] == '>' and "<sytle" in ch:  # script 태그와 같은 원리로 style 태그도 같은 방식을 이용한다.
                now = 0
                style = 1
            if ch[i] == '>' and "</style" in ch:
                now = 1
                style = 0
                continue
            if ch[i] == '<':  # script 태그나 style 태그 내부에 있지 않은 일반적인 경우에 '<'로 시작하면 html 태그의 시작을 알리므로 now에 0값을 대입한다.
                now = 0
                continue
            if ch[i] == '>' and script == 0:  # '>'로 끝나고, script 태그 내부에 있지 않으면 그 다음 문자부터는 순수 문자열로 취급함에 무관하다.
                now = 1
                continue
            if ch[i] == '>' and style == 0:  # '>'로 끝나고, style 태그 내부에 있지 않으면 그 다음 문자부터는 순수 문자열로 취급함에 무관하다.
                now = 1
                continue
            if now == 1:  # now가 1이면 순수문자열이므로 빈 문자열인 result1에 추가한다.
                result1 += ch[i]
    return result1


def div_by_punctuation(p):  # 구두문자를 모두 분리하는 함수
    result_demo = p.split()  # 먼저 p문자열을 result_demo에 공백문자로 분리하여 리스트로 저장한다.
    result_fin = []  # 최종결과를 저장할 변수
    for i in range(len(result_demo)):  # result_demo 내 모든 원소를 하나씩 검사하여 구두문자가 있다면 replace 메소드를 이용하여 제거
        for j in range(len(string.punctuation)):
            result_demo[i] = result_demo[i].replace(string.punctuation[j], "")
    for i in range(len(result_demo)):  # 구두문자를 모두 제거하고 만약 "" 만 남았다면 그것마저 제거
        if (result_demo[i] == ''):
            continue
        else:
            result_fin.append(result_demo[i])
    return result_fin


def div_one_by_one(d):  # 출현빈도와 키값을 사전으로 묶어주는 함수
    dict_result = {}  # 최종결과를 저장할 변수
    for i in d:
        if i in dict_result:  # key값이 이미 존재한다면 value 값(출현빈도) 1 증가
            dict_result[i] = dict_result[i] + 1
        else:
            dict_result[i] = 1  # 존재하지 않다면 key값과 value값 생성
    return dict_result


def removeStopWords(sen):  # 불용어 제거 함수
    stopWords_eng = ['a', 'about', 'above', 'across', 'after', 'again', 'against', 'all',
                     'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'among',
                     'an', 'and', 'another', 'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are',
                     'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at', 'away',
                     'b', 'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become',
                     'becomes', 'been', 'before', 'began', 'behind', 'being', 'beings', 'best',
                     'better', 'between', 'big', 'both', 'but', 'by', 'c', 'came', 'can', 'cannot',
                     'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could',
                     'd', 'did', 'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'down',
                     'downed', 'downing', 'downs', 'during', 'e', 'each', 'early', 'either', 'end', 'ended',
                     'ending', 'ends', 'enough', 'even', 'evenly', 'ever', 'every', 'everybody', 'everyone',
                     'everything', 'everywhere', 'f', 'face', 'faces', 'fact', 'facts', 'far', 'felt', 'few',
                     'find', 'finds', 'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered',
                     'furthering', 'furthers', 'g', 'gave', 'general', 'generally', 'get', 'gets', 'give', 'given',
                     'gives', 'go', 'going', 'good', 'goods', 'got', 'great', 'greater', 'greatest', 'group', 'grouped',
                     'grouping', 'groups', 'h', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'herself', 'high',
                     'high', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 'however', 'i', 'if',
                     'important', 'in', 'interest', 'interested', 'interesting', 'interests', 'into', 'is', 'it',
                     'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows',
                     'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like',
                     'likely', 'long', 'longer', 'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may',
                     'me', 'member', 'members', 'men', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much',
                     'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed', 'needing', 'needs', 'never',
                     'new', 'new', 'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing',
                     'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 'older', 'oldest',
                     'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered',
                     'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p', 'part', 'parted', 'parting',
                     'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 'possible',
                     'present', 'presented', 'presenting', 'presents', 'problem', 'problems', 'put', 'puts', 'q',
                     'quite',
                     'r', 'rather', 'really', 'right', 'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say',
                     'says',
                     'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees', 'several', 'shall',
                     'she',
                     'should', 'show', 'showed', 'showing', 'shows', 'side', 'sides', 'since', 'small', 'smaller',
                     'smallest',
                     'so', 'some', 'somebody', 'someone', 'something', 'somewhere', 'state', 'states', 'still', 'still',
                     'such', 'sure', 't', 'take', 'taken', 'than', 'that', 'the', 'their', 'them', 'then', 'there',
                     'therefore',
                     'these', 'they', 'thing', 'things', 'think', 'thinks', 'this', 'those', 'though', 'thought',
                     'thoughts',
                     'three', 'through', 'thus', 'to', 'today', 'together', 'too', 'took', 'toward', 'turn', 'turned',
                     'turning',
                     'turns', 'two', 'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w',
                     'want',
                     'wanted', 'wanting', 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what',
                     'when',
                     'where', 'whether', 'which', 'while', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within',
                     'without',
                     'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years', 'yet', 'you', 'young',
                     'younger',
                     'youngest', 'your', 'yours', 'z']
    stopWords_kor = ['!', '"', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '...', '0', '1', '2', '3', '4',
                     '5',
                     '6', '7', '8', '9', ';', '<', '=', '>', '?', '@', '^', '_', '`', '|', '~', '·', '—', '——', '‘',
                     '’',
                     '“', '”', '…', '、', '。', '〈', '〉', '《', '》', '가', '가까스로', '가령', '각', '각각', '각자', '각종',
                     '갖고말하자면', '같다', '같이', '개의치않고', '거니와', '거바', '거의', '것', '것과', '같이', '것들', '게다가',
                     '게우다', '겨우', '견지에서', '결과에', '이르다', '결국', '결론을', '낼', '수', '있다', '겸사겸사', '고려하면',
                     '고로', '곧', '공동으로', '과', '과연', '관계가', '있다', '관계없이', '관련이', '있다', '관하여', '관한', '관해서는',
                     '구', '구체적으로', '구토하다', '그', '그들', '그때', '그래', '그래도', '그래서', '그러나', '그러니', '그러니까',
                     '그러면', '그러므로', '그러한즉', '그런', '까닭에', '그런데', '그런즉', '그럼', '그럼에도', '불구하고', '그렇게',
                     '함으로써', '그렇지', '그렇지', '않다면', '그렇지', '않으면', '그렇지만', '그렇지않으면', '그리고', '그리하여',
                     '그만이다', '그에', '따르는', '그위에', '그저', '그중에서', '그치지', '않다', '근거로', '근거하여', '기대여',
                     '기점으로', '기준으로', '기타', '까닭으로', '까악', '까지', '까지', '미치다', '까지도', '꽈당', '끙끙', '끼익',
                     '나', '나머지는', '남들', '남짓', '너', '너희', '너희들', '네', '넷', '년', '논하지', '않다', '놀라다', '누가',
                     '알겠는가', '누구', '다른', '다른', '방면으로', '다만', '다섯', '다소', '다수', '다시', '말하자면', '다시말하면',
                     '다음', '다음에', '다음으로', '단지', '답다', '당신', '당장', '대로', '하다', '대하면', '대하여', '대해', '말하자면',
                     '대해서', '댕그', '더구나', '더군다나', '더라도', '더불어', '더욱더', '더욱이는', '도달하다', '도착하다', '동시에',
                     '동안', '된바에야', '된이상', '두번째로', '둘', '둥둥', '뒤따라', '뒤이어', '든간에', '들', '등', '등등', '딩동',
                     '따라', '따라서', '따위', '따지지', '않다', '딱', '때', '때가', '되어', '때문에', '또', '또한', '뚝뚝', '라',
                     '해도', '령', '로', '로', '인하여', '로부터', '로써', '륙', '를', '마음대로', '마저', '마저도', '마치', '막론하고',
                     '만', '못하다', '만약', '만약에', '만은', '아니다', '만이', '아니다', '만일', '만큼', '말하자면', '말할것도',
                     '없고', '매', '매번', '메쓰겁다', '몇', '모', '모두', '무렵', '무릎쓰고', '무슨', '무엇', '무엇때문에', '물론',
                     '및', '바꾸어말하면', '바꾸어말하자면', '바꾸어서', '말하면', '바꾸어서', '한다면', '바꿔', '말하면', '바로',
                     '바와같이', '밖에', '안된다', '반대로', '반대로', '말하자면', '반드시', '버금', '보는데서', '보다더', '보드득',
                     '본대로', '봐', '봐라', '부류의', '사람들', '부터', '불구하고', '불문하고', '붕붕', '비걱거리다', '비교적',
                     '비길수', '없다', '비로소', '비록', '비슷하다', '비추어', '보아', '비하면', '뿐만', '아니라', '뿐만아니라',
                     '뿐이다', '삐걱', '삐걱거리다', '사', '삼', '상대적으로', '말하자면', '생각한대로', '설령', '설마', '설사',
                     '셋', '소생', '소인', '솨', '쉿', '습니까', '습니다', '시각', '시간', '시작하여', '시초에', '시키다', '실로',
                     '심지어', '아', '아니', '아니나다를가', '아니라면', '아니면', '아니었다면', '아래윗', '아무거나', '아무도',
                     '아야', '아울러', '아이', '아이고', '아이구', '아이야', '아이쿠', '아하', '아홉', '안', '그러면', '않기',
                     '위하여', '않기', '위해서', '알', '수', '있다', '알았어', '앗', '앞에서', '앞의것', '야', '약간', '양자',
                     '어', '어기여차', '어느', '어느', '년도', '어느것', '어느곳', '어느때', '어느쪽', '어느해', '어디', '어때',
                     '어떠한', '어떤', '어떤것', '어떤것들', '어떻게', '어떻해', '어이', '어째서', '어쨋든', '어쩔수', '없다',
                     '어찌', '어찌됏든', '어찌됏어', '어찌하든지', '어찌하여', '언제', '언젠가', '얼마', '얼마', '안', '되는',
                     '것', '얼마간', '얼마나', '얼마든지', '얼마만큼', '얼마큼', '엉엉', '에', '에', '가서', '에', '달려', '있다',
                     '에', '대해', '에', '있다', '에', '한하다', '에게', '에서', '여', '여기', '여덟', '여러분', '여보시오', '여부',
                     '여섯', '여전히', '여차', '연관되다', '연이서', '영', '영차', '옆사람', '예', '예를', '들면', '예를', '들자면',
                     '예컨대', '예하면', '오', '오로지', '오르다', '오자마자', '오직', '오호', '오히려', '와', '와', '같은', '사람들',
                     '와르르', '와아', '왜', '왜냐하면', '외에도', '요만큼', '요만한', '것', '요만한걸', '요컨대', '우르르', '우리',
                     '우리들', '우선', '우에', '종합한것과같이', '운운', '월', '위에서', '서술한바와같이', '위하여', '위해서', '윙윙',
                     '육', '으로', '으로', '인하여', '으로서', '으로써', '을', '응', '응당', '의', '의거하여', '의지하여', '의해',
                     '의해되다', '의해서', '이', '이', '되다', '이', '때문에', '이', '밖에', '이', '외에', '이', '정도의', '이것',
                     '이곳', '이때', '이라면', '이래', '이러이러하다', '이러한', '이런', '이럴정도로', '이렇게', '많은', '것',
                     '이렇게되면', '이렇게말하자면', '이렇구나', '이로', '인하여', '이르기까지', '이리하여', '이만큼', '이번',
                     '이봐', '이상', '이어서', '이었다', '이와', '같다', '이와', '같은', '이와', '반대로', '이와같다면', '이외에도',
                     '이용하여', '이유만으로', '이젠', '이지만', '이쪽', '이천구', '이천육', '이천칠', '이천팔', '인', '듯하다', '인젠',
                     '일', '일것이다', '일곱', '일단', '일때', '일반적으로', '일지라도', '임에', '틀림없다', '입각하여', '입장에서',
                     '잇따라', '있다', '자', '자기', '자기집', '자마자', '자신', '잠깐', '잠시', '저', '저것', '저것만큼', '저기',
                     '저쪽', '저희', '전부', '전자', '전후', '점에서', '보아', '정도에', '이르다', '제', '제각기', '제외하고', '조금',
                     '조차', '조차도', '졸졸', '좀', '좋아', '좍좍', '주룩주룩', '주저하지', '않고', '줄은', '몰랏다', '줄은모른다',
                     '중에서', '중의하나', '즈음하여', '즉', '즉시', '지든지', '지만', '지말고', '진짜로', '쪽으로', '차라리', '참',
                     '참나', '첫번째로', '쳇', '총적으로', '총적으로', '말하면', '총적으로', '보면', '칠', '콸콸', '쾅쾅', '쿵', '타다',
                     '타인', '탕탕', '토하다', '통하여', '툭', '퉤', '틈타', '팍', '팔', '퍽', '펄렁', '하', '하게될것이다', '하게하다',
                     '하겠는가', '하고', '있다', '하고있었다', '하곤하였다', '하구나', '하기', '때문에', '하기', '위하여', '하기는한데',
                     '하기만', '하면', '하기보다는', '하기에', '하나', '하느니', '하는', '김에', '하는', '편이', '낫다', '하는것도',
                     '하는것만', '못하다', '하는것이', '낫다', '하는바', '하더라도', '하도다', '하도록시키다', '하도록하다', '하든지',
                     '하려고하다', '하마터면', '하면', '할수록', '하면된다', '하면서', '하물며', '하여금', '하여야', '하자마자', '하지',
                     '않는다면', '하지', '않도록', '하지마', '하지마라', '하지만', '하하', '한', '까닭에', '한', '이유는', '한', '후',
                     '한다면', '한다면', '몰라도', '한데', '한마디', '한적이있다', '한켠으로는', '한항목', '할', '따름이다', '할',
                     '생각이다', '할', '줄', '안다', '할', '지경이다', '할', '힘이', '있다', '할때', '할만하다', '할망정', '할뿐',
                     '할수있다', '할수있어', '할줄알다', '할지라도', '할지언정', '함께', '해도된다', '해도좋다', '해봐요', '해서는',
                     '안된다', '해야한다', '해요', '했어요', '향하다', '향하여', '향해서', '허', '허걱', '허허', '헉', '헉헉',
                     '헐떡헐떡', '형식으로', '쓰여', '혹시', '혹은', '혼자', '훨씬', '휘익', '휴', '흐흐', '흥', '힘입어', '︿',
                     '！', '＃', '＄', '％', '＆', '（', '）', '＊', '＋', '，', '０', '１', '２', '３', '４', '５', '６', '７',
                     '８', '９', '：', '；', '＜', '＞', '？', '＠', '［', '］', '｛', '｜', '｝', '～', '￥']
    if (type(sen) == dict):  # 매개변수로 받는 타입마다 내장함수가 다르기 때문에 그에 맞게 불용어를 제거
        for i in stopWords_eng:
            if (i in sen):
                sen.pop(i)
        for i in stopWords_kor:
            if (i in sen):
                sen.pop(i)
        return sen
    elif (type(sen) == str):
        for i in stopWords_eng:
            if (i in sen and len(i) == len(sen)):
                sen = sen.replace(i, "")
        for i in stopWords_kor:
            if (i in sen and len(i) == len(sen)):
                sen = sen.replace(i, "")
        return sen


def html_to_StringCountDict(html):  # url주소의 순수문자열만 가져와 구두문자로 분리 후 단어의 출현빈도를 사전으로 출력하는 함수
    onlyString = only_string(html)
    divByPunc = div_by_punctuation(onlyString)
    hToString = div_one_by_one(divByPunc)
    remove_stop_words = removeStopWords(hToString)
    return remove_stop_words


html_address = ['https://www.cj.net', 'https://www.youtube.com', 'https://www.naver.com',
                'http://www.interpark.com', 'https://www.wemakeprice.com']
StringCountDict = []
for i in range(5):  # url주소 5개를 가져와 html파일을 생성하고, 출현빈도를 저장한 사전객체를 pickle모듈을 이용하여 파일로 생성
    req = requests.get(html_address[i])
    source = req.text
    StringCountDict.append(html_to_StringCountDict(req))
    print(only_string(source))

    htmlFile = open(html_address[i].split('//')[1] + '.html', 'w', encoding='UTF8')
    htmlFile.write(source)
    htmlFile.close()

    with open(html_address[i].split('//')[1] + '.words_frequency.pickle', 'wb') as f:
        pickle.dump(StringCountDict[i], f)

words_frequency_dict = []
for i in range(5):  # 각 url의 pickle로 부터 출현빈도를 저장한 사전을 불러와 출현빈도가 높은 순으로 정렬
    with open(html_address[i].split('//')[1] + '.words_frequency.pickle', 'rb') as f:
        a = pickle.load(f)  # pickle 모듈로 저장한 5개 이상의 pickle 파일들을 다시 5개 이상의 사전 객체로 로드
    words_frequency_dict.append(a)  # 공리스트 words_frequency_dict에 5개의 url에 관한 출현빈도를 나타내는 사젠 객체를 리스트로 추가
    words_frequency_dict[i] = sorted(a.items(), key=lambda x: x[1], reverse=True)  # 각 url별로 단어의 출현빈도가 높은 순으로 정렬
    print(html_address[i].split('//')[1] + '.words_frequency.pickle의 최다 출현 단어 : ')
    print(words_frequency_dict[i][0][0] + " : " + str(words_frequency_dict[i][0][1]) + "번" + "\n"
          + words_frequency_dict[i][1][0] + " : " + str(words_frequency_dict[i][1][1]) + "번" + "\n"
          + words_frequency_dict[i][2][0] + " : " + str(words_frequency_dict[i][2][1]) + "번" + "\n")


def LikeGoogle():  # 검색엔진 함수
    word = input("Enter the words : ")  # 사용자로부터 단어를 입력 받는다.
    word = removeStopWords(word)
    print("입력받은 단어(불용어 처리 후) : " + word)
    similarity = {}  # 유사도를 따진 후 출현빈도를 update한다.
    index = 0
    for i in range(len(html_address)):  # 가져온 address 개수 만큼 비교
        with open(html_address[i].split('//')[1] + '.words_frequency.pickle', 'rb') as f:
            s = list((pickle.load(f)).items())
        for j in range(len(s)):  # 각 url pickle 파일에서 출현빈도 사전객체를 가져온 후 단어가 있는지 비교하여
            if word in s[j][0] or word.lower() == str(
                    s[j][0]).lower():  # 있다면 그 사전의 value 값을 저장한다.(+ 제 생각에 대 소문자는 무시할 수 있으므로 방법 추가했습니다.)
                index = j  # 또한 사용자가 입력한 단어가 일부라도 포함되어 있으면 연관이 있다고 생각했습니다.
                count = 0  # 그에 맞는 코드를 작성하였습니다.
                temp = similarity.keys()  # ex) 사용자입력 : 캐스트 ---> 네이버 출현빈도 사전객체 중에 {'쇼핑캐스트' : 2, '날씨캐스트' : 1} 라면 빈도수는 3이 출력되게끔
                if html_address[
                    i] in temp:  # ex) 사용자입력 : 쇼핑 ---> 네이버 출현빈도 사전객체 중에 {'쇼핑홈' : 2, '오늘의쇼핑' : 2} 라면 빈도수는 4가 출력되게끔 했습니다.
                    count = similarity[html_address[i]]
                similarity.update({html_address[i]: (count + s[index][1])})
        temp = similarity.keys()
        if html_address[i] not in temp:
            similarity.update({html_address[i]: 0})

    result = list(similarity.items())  # 사전의 key,value 값을 튜플로 받아서 리스트로 변환
    result.sort(key=lambda x: x[1], reverse=True)  # 빈도가 가장 높은 순대로 정렬

    print("유사도가 높은 웹사이트 : ")
    for i in range(len(result)):
        print(result[i][0] + " : " + str(result[i][1]))


LikeGoogle()
