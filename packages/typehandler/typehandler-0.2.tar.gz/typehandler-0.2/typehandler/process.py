import random
from typing import List, Dict, Tuple, Set, Optional

class Process:
    __HIRAGANA = dict(
               あ=['a'],
               い=['i','yi'],
               う=['u','wu','whu'],
               え=['e'],
               お=['o'],
               か=['ka','ca'],
               き=['ki'],
               く=['ku','cu','qu'],
               け=['ke'],
               こ=['ko','co'],
               さ=['sa'],
               し=['si','ci','shi'],
               す=['su'],
               せ=['se'],
               そ=['so'],
               た=['ta'],
               ち=['ti','chi'],
               つ=['tu','tsu'],
               て=['te'],
               と=['to'],
               な=['na'],
               に=['ni'],
               ぬ=['nu'],
               ね=['ne'],
               の=['no'],
               は=['ha'],
               ひ=['hi'],
               ふ=['hu','fu'],
               へ=['he'],
               ほ=['ho'],
               ま=['ma'],
               み=['mi'],
               む=['mu'],
               め=['me'],
               も=['mo'],
               や=['ya'],
               ゆ=['yu'],
               よ=['yo'],
               ら=['ra'],
               り=['ri'],
               る=['ru'],
               れ=['re'],
               ろ=['ro'],
               わ=['wa'],
               を=['wo'],
               ん=['nn','xn'],
               が=['ga'],
               ぎ=['gi'],
               ぐ=['gu'],
               げ=['ge'],
               ご=['go'],
               ざ=['za'],
               じ=['ji','zi'],
               ず=['zu'],
               ぜ=['ze'],
               ぞ=['zo'],
               だ=['da'],
               ぢ=['di'],
               づ=['du'],
               で=['de'],
               ど=['do'],
               ば=['ba'],
               び=['bi'],
               ぶ=['bu'],
               べ=['be'],
               ぼ=['bo'],
               ぱ=['pa'],
               ぴ=['pi'],
               ぷ=['pu'],
               ぺ=['pe'],
               ぽ=['po'],
               ぁ=['la','xa'],
               ぃ=['li','xi','lyi','xyi'],
               ぅ=['lu','xu'],
               ぇ=['le','xe','lye','xye'],
               ぉ=['lo','xo'],
               ゃ=['lya','xya'],
               ゅ=['lyu','xyu'],
               ょ=['lyo','xyo'],
               っ=['ltu','xtu'],
               ゎ=['lwa','xwa'],
               きゃ=['kya','kilya', 'kixya'],
               きぃ=['kyi','kili', 'kixi', 'kilyi', 'kixyi'],
               きゅ=['kyu','kilyu', 'kixyu'],
               きぇ=['kye','kile', 'kixe', 'kilye', 'kixye'],
               きょ=['kyo','kilyo', 'kixyo'],
               ぎゃ=['gya','gilya', 'gixya'],
               ぎぃ=['gyi','gili', 'gixi', 'gilyi', 'gixyi'],
               ぎゅ=['gyu','gilyu', 'gixyu'],
               ぎぇ=['gye','gile', 'gixe', 'gilye', 'gixye'],
               ぎょ=['gyo','gilyo', 'gixyo'],
               しゃ=['sya','sha','silya', 'sixya', 'cilya', 'cixya', 'shilya', 'shixya'],
               しぃ=['syi','sili', 'sixi', 'silyi', 'sixyi', 'cili', 'cixi', 'cilyi', 'cixyi', 'shili', 'shixi', 'shilyi', 'shixyi'],
               しゅ=['syu','shu','silyu', 'sixyu', 'cilyu', 'cixyu', 'shilyu', 'shixyu'],
               しぇ=['sye','she','sile', 'sixe', 'silye', 'sixye', 'cile', 'cixe', 'cilye', 'cixye', 'shile', 'shixe', 'shilye', 'shixye'],
               しょ=['syo','sho','silyo', 'sixyo', 'cilyo', 'cixyo', 'shilyo', 'shixyo'],
               じゃ=['ja','zya','jya','zilya', 'zixya', 'jilya', 'jixya'],
               じぃ=['zyi','jyi','zili', 'zixi', 'zilyi', 'zixyi', 'jili', 'jixi', 'jilyi', 'jixyi'],
               じゅ=['ju','zyu','jyu','zilyu', 'zixyu', 'jilyu', 'jixyu'],
               じぇ=['je','zye','jye','zile', 'zixe', 'zilye', 'zixye', 'jile', 'jixe', 'jilye', 'jixye'],
               じょ=['jo','zyo','jyo','zilyo', 'zixyo', 'jilyo', 'jixyo'],
               ちゃ=['tya','cha','cya','tilya', 'tixya', 'chilya', 'chixya'],
               ちぃ=['tyi','cyi','tili', 'tixi', 'tilyi', 'tixyi', 'chili', 'chixi', 'chilyi', 'chixyi'],
               ちゅ=['tyu','chu','cyu','tilyu', 'tixyu', 'chilyu', 'chixyu'],
               ちぇ=['tye','che','cye','tile', 'tixe', 'tilye', 'tixye', 'chile', 'chixe', 'chilye', 'chixye'],
               ちょ=['tyo','cho','cyo','tilyo', 'tixyo', 'chilyo', 'chixyo'],
               ぢゃ=['dya','dilya', 'dixya'],
               ぢぃ=['dyi','dili', 'dixi', 'dilyi', 'dixyi'],
               ぢゅ=['dyu','dilyu', 'dixyu'],
               ぢぇ=['dye','dile', 'dixe', 'dilye', 'dixye'],
               ぢょ=['dyo','dilyo', 'dixyo'],
               てゃ=['tha','telya', 'texya'],
               てぃ=['thi','teli', 'texi', 'telyi', 'texyi'],
               てゅ=['thu','telyu', 'texyu'],
               てぇ=['the','tele', 'texe', 'telye', 'texye'],
               てょ=['tho','telyo', 'texyo'],
               でゃ=['dha','delya', 'dexya'],
               でぃ=['dhi','deli', 'dexi', 'delyi', 'dexyi'],
               でゅ=['dhu','delyu', 'dexyu'],
               でぇ=['dhe','dele', 'dexe', 'delye', 'dexye'],
               でょ=['dho','delyo', 'dexyo'],
               にゃ=['nya','nilya', 'nixya'],
               にぃ=['nyi','nili', 'nixi', 'nilyi', 'nixyi'],
               にゅ=['nyu','nilyu', 'nixyu'],
               にぇ=['nye','nile', 'nixe', 'nilye', 'nixye'],
               にょ=['nyo','nilyo', 'nixyo'],
               ひゃ=['hya','hilya', 'hixya'],
               ひぃ=['hyi','hili', 'hixi', 'hilyi', 'hixyi'],
               ひゅ=['hyu','hilyu', 'hixyu'],
               ひぇ=['hye','hile', 'hixe', 'hilye', 'hixye'],
               ひょ=['hyo','hilyo', 'hixyo'],
               びゃ=['bya','bilya', 'bixya'],
               びぃ=['byi','bili', 'bixi', 'bilyi', 'bixyi'],
               びゅ=['byu','bilyu', 'bixyu'],
               びぇ=['bye','bile', 'bixe', 'bilye', 'bixye'],
               びょ=['byo','bilyo', 'bixyo'],
               ぴゃ=['pya','pilya', 'pixya'],
               ぴぃ=['pyi','pili', 'pixi', 'pilyi', 'pixyi'],
               ぴゅ=['pyu','pilyu', 'pixyu'],
               ぴぇ=['pye','pile', 'pixe', 'pilye', 'pixye'],
               ぴょ=['pyo','pilyo', 'pixyo'],
               ふゃ=['fua','hulya', 'huxya', 'fulya', 'fuxya'],
               ふゅ=['fyu','hulyu', 'huxyu', 'fulyu', 'fuxyu'],
               ふょ=['fyo','hulyo', 'huxyo', 'fulyo', 'fuxyo'],
               みゃ=['mya','milya', 'mixya'],
               みぃ=['myi','mili', 'mixi', 'milyi', 'mixyi'],
               みゅ=['myu','milyu', 'mixyu'],
               みぇ=['mye','mile', 'mixe', 'milye', 'mixye'],
               みょ=['myo','milyo', 'mixyo'],
               りゃ=['rya','rilya', 'rixya'],
               りぃ=['ryi','rili', 'rixi', 'rilyi', 'rixyi'],
               りゅ=['ryu','rilyu', 'rixyu'],
               りぇ=['rye','rile', 'rixe', 'rilye', 'rixye'],
               りょ=['ryo','rilyo', 'rixyo'],
               いぇ=['ye','ile', 'ixe', 'ilye', 'ixye', 'yile', 'yixe', 'yilye', 'yixye'],
               うぁ=['wha','ula', 'uxa', 'wula', 'wuxa', 'whula', 'whuxa'],
               うぃ=['wi','whi','uli', 'uxi', 'ulyi', 'uxyi', 'wuli', 'wuxi', 'wulyi', 'wuxyi', 'whuli', 'whuxi', 'whulyi', 'whuxyi'],
               うぇ=['we','whe','ule', 'uxe', 'ulye', 'uxye', 'wule', 'wuxe', 'wulye', 'wuxye', 'whule', 'whuxe', 'whulye', 'whuxye'],
               うぉ=['who','ulo', 'uxo', 'wulo', 'wuxo', 'whulo', 'whuxo'],
               ヴぁ=['va','vula', 'vuxa'],
               ヴぃ=['vi','vuli', 'vuxi', 'vulyi', 'vuxyi'],
               ヴ=['vu'],
               ヴぇ=['ve','vule', 'vuxe', 'vulye', 'vuxye'],
               ヴぉ=['vo','vulo', 'vuxo'],
               くぁ=['qwa','qa','kula', 'kuxa', 'cula', 'cuxa', 'qula', 'quxa'],
               くぃ=['qwi','qi','qyi','kuli', 'kuxi', 'kulyi', 'kuxyi', 'culi', 'cuxi', 'culyi', 'cuxyi', 'quli', 'quxi', 'qulyi', 'quxyi'],
               くぅ=['qwu','kulu', 'kuxu', 'culu', 'cuxu', 'qulu', 'quxu'],
               くぇ=['qwe','qe','qye','kule', 'kuxe', 'kulye', 'kuxye', 'cule', 'cuxe', 'culye', 'cuxye', 'qule', 'quxe', 'qulye', 'quxye'],
               くぉ=['qwo','qo','kulo', 'kuxo', 'culo', 'cuxo', 'qulo', 'quxo'],
               ぐぁ=['gwa','gula', 'guxa'],
               ぐぃ=['gwi','guli', 'guxi', 'gulyi', 'guxyi'],
               ぐぅ=['gwu','gulu', 'guxu'],
               ぐぇ=['gwe','gule', 'guxe', 'gulye', 'guxye'],
               ぐぉ=['gwo','gulo', 'guxo'],
               すぁ=['swa','sula', 'suxa'],
               すぃ=['swi','suli', 'suxi', 'sulyi', 'suxyi'],
               すぅ=['swu','sulu', 'suxu'],
               すぇ=['swe','sule', 'suxe', 'sulye', 'suxye'],
               すぉ=['swo','sulo', 'suxo'],
               つぁ=['tsa','tula', 'tuxa', 'tsula', 'tsuxa'],
               つぃ=['tsi','tuli', 'tuxi', 'tulyi', 'tuxyi', 'tsuli', 'tsuxi', 'tsulyi', 'tsuxyi'],
               つぇ=['tse','tule', 'tuxe', 'tulye', 'tuxye', 'tsule', 'tsuxe', 'tsulye', 'tsuxye'],
               つぉ=['tso','tulo', 'tuxo', 'tsulo', 'tsuxo'],
               とぁ=['twa','tola', 'toxa'],
               とぃ=['twi','toli', 'toxi', 'tolyi', 'toxyi'],
               とぅ=['twu','tolu', 'toxu'],
               とぇ=['twe','tole', 'toxe', 'tolye', 'toxye'],
               とぉ=['two','tolo', 'toxo'],
               どぁ=['dwa','dola', 'doxa'],
               どぃ=['dwi','doli', 'doxi', 'dolyi', 'doxyi'],
               どぅ=['dwu','dolu', 'doxu'],
               どぇ=['dwe','dole', 'doxe', 'dolye', 'doxye'],
               どぉ=['dwo','dolo', 'doxo'],
               ふぁ=['fa','fwa','hula', 'huxa', 'fula', 'fuxa'],
               ふぃ=['fi','fwi','fyi','huli', 'huxi', 'hulyi', 'huxyi', 'fuli', 'fuxi', 'fulyi', 'fuxyi'],
               ふぅ=['fwu','hulu', 'huxu', 'fulu', 'fuxu'],
               ふぇ=['fe','fwe','fye','hule', 'huxe', 'hulye', 'huxye', 'fule', 'fuxe', 'fulye', 'fuxye'],
               ふぉ=['fo','fwo','hulo', 'huxo', 'fulo', 'fuxo'],
               ー=['-']
    )

    __EXCEPTION_NN = {'n', 'y', 'a', 'i', 'u', 'e', 'o'}
    __EXCEPTION_LTU = {'n', 'a', 'i', 'u', 'e', 'o', '-'}    #記号追加するなら記号もここに
    @classmethod
    def __validate_input(cls, hurigana: str) -> None:
        valid_chars = set(cls.__HIRAGANA.keys())
        for char in hurigana:
            if char not in valid_chars:
                 raise ValueError(f"Invalid character found: {char} in input: {hurigana}")
    
    #ユーザーが呼び出すためのほう（エラーハンドリング付き）
    @classmethod
    def divide(cls, hurigana: str) -> List[str]:
        cls.__validate_input(hurigana)
        return cls.__divide(hurigana)
    
    #フリガナを受け取って、取りうるローマ字のパターンを生成する（文字ごとに入力パターンがあるので二次元リスト）
    @classmethod
    def __divide(cls, hurigana: str) ->List[str]:
        hiragana_dict = cls.__HIRAGANA
        divided_roman = []
        hurigana = hurigana
        chunk = None           #特定のひらがなをいくつかの文字で一つの塊とする

        #文章を先頭からチャンクごとに区切って入力パターンを作る（「ん」と「っ」に関しては処理が違うので個別に扱う）
        while len(hurigana):
            if hurigana[0] == 'ん' and len(hurigana) != 1:    #文字が「ん」かつ最後じゃない時
                pattern, hurigana = cls.__handle_nn(hurigana, hiragana_dict)
            elif hurigana[0] == 'っ' and len(hurigana) != 1:    #文字が「っ」かつ最後じゃない時
                pattern, hurigana = cls.__handle_ltu(hurigana, hiragana_dict)
            else:
                pattern, hurigana = cls.__handle_pair(hurigana, hiragana_dict)
            #特殊な処理がなかったら、1文字を１チャンクとして扱う
            if pattern is None:
                chunk = hurigana[0]
                pattern = hiragana_dict[chunk]
                hurigana = hurigana[1:]
            #チャンクごとの入力パターンをリストに追加していく       
            divided_roman.append(pattern)
        return divided_roman
    #文字が「ん」のときはnを二回入力しなければならないのか、１回でいいのかを調べ、「ん」を含む数文字を１チャンクとして入力パターンを作成
    @classmethod
    def __handle_nn(cls, hurigana: str, hiragana_dict: Dict[str, str]) ->Tuple[List[str], str]:
        pattern, hurigana = cls.__handle_special_letter(hurigana, hiragana_dict, cls.__EXCEPTION_NN, 'n')
        return pattern, hurigana
    #文字が「っ」のときは、後ろの文字の最初のローマ字を打つだけでいいのか調べ、「っ」を含む数文字を１チャンクとして入力パターンを作成
    @classmethod
    def __handle_ltu(cls, hurigana: str, hiragana_dict: Dict[str, str]) ->Tuple[List[str], str]:
        pattern, hurigana = cls.__handle_special_letter(hurigana, hiragana_dict, cls.__EXCEPTION_LTU)
        return pattern, hurigana
    #「ん」または「っ」に関しては、それらを含む数文字を１チャンクとして入力パターンを作成
    @staticmethod
    def __handle_special_letter(hurigana: str, hiragana_dict: Dict[str, str], exception: Set[str], special_char: str = None) ->Tuple[List[str], str]:
        #後ろ2文字または1文字が辞書にあれば複数文字のチャンクとして扱う
        chunk_length = 3 if hurigana[1:3] in hiragana_dict else 2
        if hurigana[1:chunk_length] in hiragana_dict:
            chunk = hurigana[0:chunk_length]
            hurigana = hurigana[chunk_length:]
        if special_char:
            pattern = [special_char+i for i in hiragana_dict[chunk[1:]] if i[0] not in exception]
        else:
            pattern = [i[0]+i for i in hiragana_dict[chunk[1:]] if i[0] not in exception]
        pattern += [i+j for i in hiragana_dict[chunk[0]] for j in hiragana_dict[chunk[1:]]]
        return pattern, hurigana
    #例外処理のない文字
    @staticmethod
    def __handle_pair(hurigana: str, hiragana_dict: Dict[str, str]) ->Tuple[List[str], str]:
        #「しゃ」など２文字の塊で辞書に登録されているものは１チャンクとして扱う
        chunk = hurigana[0:2]
        pattern = hiragana_dict.get(chunk)
        if pattern:
            hurigana = hurigana[2:]
        return pattern, hurigana
        
    def __init__(self, words: Dict[str, str] = None) ->None:
        self.__input_count = 0          #入力回数
        self.__current_chunk_num = 0    #現在入力しているひらがなが何番目か
        self.input = ''                 #入力済みのローマ字の文字列
        self.show_roman = ''            #画面に出力するローマ字
        self.words = words              #文章の一覧
        if words is None:
            self.sentence = self.hurigana = self.divided_roman = None
        else:
            for i in list(words.values()):
                self.__validate_input(i)
            self.sentence, self.hurigana, self.divided_roman = self.__create_sentence()    #文章、ふりがな、入力パターン

    def __create_sentence(self, words: Dict[str, str] = None) ->Tuple[str, str, List[str]]:
        #引数で文章の辞書が渡されなかったら自分の辞書から
        if words is None:
            words = self.words
        sentence = random.choice(list(words.keys()))    #辞書からランダムに文章を選ぶ
        hurigana = words[sentence]
        divided_roman = self.__divide(hurigana)
        return sentence, hurigana, divided_roman

    #お題の文章、ひらがな、ローマ字を更新（辞書を渡せば、一回だけ別の辞書から参照するのにも使える）
    def set_new_sentence(self, words: Dict[str, str] = None) ->None:
        #これが直接呼び出された時のためにリセットしておく
        self.__input_count = 0    
        self.__current_chunk_num = 0    
        self.input = '' 
        self.sentence, self.hurigana, self.divided_roman = self.__create_sentence(words)
        
    #別の辞書を設定したい時に使う
    def set_new_words(self, words: Dict[str, str]) ->None:
        for i in list(words.values()):
            self.__validate_input(i)
        self.words = words
        set_new_sentence(words)

    #正しい文字が入力されたか判定する
    def check_correct_input(self, key: str) ->bool:
        saved = [x for x in self.divided_roman[self.__current_chunk_num] if x[self.__input_count] == key]    #入力されたローマ字と一致する入力パターンのみを残す
        #入力が正しい時（入力パターンが残っているとき）
        if len(saved) != 0:
            self.divided_roman[self.__current_chunk_num] = saved    #入力パターンを更新
            self.input = self.input + key   
            self.__input_count += 1    
            return True
        return False
    #正しい文字が入力された結果、ひらがなが打ち終わったか判定する
    def check_chunk_completion(self) ->bool:        
        #現在入力しているひらがなの入力パターンが残りひとつ かつ 最後に残っているパターンの長さと、入力回数が一致している
        if len(self.divided_roman[self.__current_chunk_num]) == 1 and len(self.divided_roman[self.__current_chunk_num][0]) == self.__input_count:
            self.__current_chunk_num += 1    
            self.__input_count = 0    
            return True
        return False
    #ひらがなが打ち終わった結果、文章が打ち終わったか判定する
    def check_sentence_completion(self) ->bool:        
        if self.__current_chunk_num == len(self.divided_roman):
            self.__input_count = 0    
            self.__current_chunk_num = 0    
            self.input = ''    
            return True
        return False
            
    #画面に出すための入力例
    def update_show_roman(self) ->str:
        self.show_roman = ''
        #チャンクごとのパターンのリストから先頭だけ抜き出してローマ字を作成
        for i in self.divided_roman:
            self.show_roman = self.show_roman + i[0]
        return self.show_roman

    #音声とか付けないなら、これだけ呼び出せば使える
    def main(self, key: str) ->None:
        correct_input = self.check_correct_input(key)    #ミスタイプを判定
        if correct_input:
            chunk_completed = self.check_chunk_completion()    #文章の打ち終わりを判定
            if chunk_completed:
                sentence_completed = self.check_sentence_completion()
                if sentence_completed:
                    self.sentence, self.hurigana, self.divided_roman = self.__create_sentence()    #新しい文章を用意
