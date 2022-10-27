import streamlit as st
import requests
import pymorphy2
import pandas as pd

from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)

st.title('ウダレーニエメーカー')
st.header('Программа расстановки ударений')

st.write("間違えることもあるので参考程度にお願いします")

st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")

text = st.text_input("検索 (Поиск слов)", "検索したい単語を入れてください Напишите слова")
doc = Doc(text)

segmenter = Segmenter()
emb = NewsEmbedding()
morph_vocab = MorphVocab()
morph_tagger = NewsMorphTagger(emb)

import pickle
with open (file="wordforms.dat", mode='rb') as f:
    wordforms = pickle.loads(f.read())

words_dict = {}

doc.segment(segmenter)
doc.tag_morph(morph_tagger)

for i in range(len(doc.tokens)):

    #featがない場合
    if not doc.tokens[i].feats:
        if doc.tokens[i].text.istitle():
            words_dict[doc.tokens[i].text] = ['', 1]
        else:
            words_dict[doc.tokens[i].text] = ['', 0]
    #featがある場合
    else:

        #Numがある場合
        try:
            #大文字から始まる
            if doc.tokens[i].text.istitle():
                words_dict[doc.tokens[i].text] = [doc.tokens[i].feats["Number"].lower(), 1]
            #小文字から始まる
            else:
                words_dict[doc.tokens[i].text] = [doc.tokens[i].feats["Number"].lower(), 0]
        except:
            #大文字から始まる
            if doc.tokens[i].text.istitle():
                words_dict[doc.tokens[i].text] = ['', 1]
            #小文字から始まる
            else:
                 words_dict[doc.tokens[i].text] = ['', 0]
            

accent_text = ""

if text == 'Напишите слова' or text == 'Напиши слова':
    accent_text = "Напиши́те слова́"
elif text == '検索したい単語を入れてください Напишите слова':
    accent_text = "検索したい単語を入れてください Напиши́те слова́"
else:
    for word in words_dict.keys():

        try:
        
            try:
                # wordsformのアクセントの位置が一つの場合
                if len(wordforms[word]) == 1 : 
                    accent_text += wordforms[word][0]["accentuated"]
                    accent_text += " "
                # wordsformのアクセントの位置が２つ以上の場合
                else:
                    for i in range(len(wordforms[word])):
                        if word == 'это':
                            accent_text += 'э́то'
                            accent_text += " "
                            break
                        if word == 'замок':
                            accent_text += 'замо́к/за́мок'
                            accent_text += " "
                            break
                        
                        if words_dict[word][0] in wordforms[word][i]["form"]:
                            accent_text += wordforms[word][i]["accentuated"]
                            accent_text += " "
                            break
                        else:
                            continue
            #wordが小文字でないとwordsformで見つからない場合
            except:
                # wordsformのアクセントの位置が一つの場合
                if len(wordforms[word.lower()]) == 1 :
                    #元々wordが大文字始まりだった場合
                    if words_dict[word][1] == 1:
                        accent_text += wordforms[word.lower()][0]["accentuated"].capitalize()
                        accent_text += " "
                    else:
                        accent_text += wordforms[word.lower()][0]["accentuated"]
                        accent_text += " "

                # wordsformのアクセントの位置が２つ以上の場合
                else:
                    for i in range(len(wordforms[word.lower()])):
                        if word == 'Это':
                            accent_text += 'Э́то'
                            accent_text += " "
                            break
                        if word == 'Замок':
                            accent_text += 'Замо́к/За́мок'
                            accent_text += " "
                            break
                        if words_dict[word][0] in wordforms[word.lower()][i]["form"]:
                            if words_dict[word][1] == 1:
                                accent_text += wordforms[word.lower()][i]["accentuated"].capitalize()
                                accent_text += " " 
                                break
                            else:
                                accent_text += wordforms[word.lower()][i]["accentuated"]
                                accent_text += " " 
                                break
                        else:
                            continue     
                            
        except:
            accent_text += word
            accent_text += " "


st.write("\n")
st.write("\n")
st.write("\n")     

st.text_input('ウダレーニエ付き (С ударением)', accent_text)

st.write("\n")
st.write("\n")
st.write("\n")

parts_of_speech ={

    "NOUN" : "名詞　Сущ",
    "ADJF" : "形容詞　П.При",
    "ADJS" : "形容詞短縮形　К.При",
    "COMP" : "比較詞　Компаратив",
    "VERB" : "動詞　Глагол",
    "INFN" : "不定形　Инфинитив",
    "PRTF" : "形動詞　П.Причастие",
    "PRTS" : "短縮形動詞　К.Причастие",
    "GRND" : "副動詞　Деепричасте",
    "NUMR" : "数詞　Числительное",
    "ADVB" : "副詞　Наречие",
    "NPRO" : "代名詞　Мест",
    "PRED" : "否定代名詞　Предикатив",
    "PREP" : "前置詞　Предлог",
    "PREP" : "接続詞　Союз",
    "PRCL" : "小詞　Частица",
    "INTJ" : "間投詞　Междометие",
    "<NA>" : " "
}

def lemmatize(words):

    words = words.replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace("'", "").replace("\"", "")
    words = words.split(" ")
    lemma_words = []
    word_types = []
    #trans_words = []

    for word in words:
        
        analyzer = pymorphy2.MorphAnalyzer()
        lemma_word = analyzer.parse(word)[0].normal_form
        lemma_words.append(lemma_word)
        word_type = analyzer.parse(word)[0].tag.POS

        try:
            word_types.append(parts_of_speech[word_type])
        except:
            word_types.append("")

    return words, lemma_words, word_types#, trans_words


lemma_df = pd.DataFrame(lemmatize(text), index=["元の単語 (Предыдущее слово)", "原形 (Инфинитив)", "タイプ (Часть речи)"]).T
st.write(lemma_df)


API_KEY = st.secrets.DeepL.api_key

target_lang = "ja"

def translation(words):

    params = {
                'auth_key' : API_KEY,
                'text' : words,
                "target_lang": target_lang
            }
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
    result = request.json()

    return result['translations'][0]['text']

try:
    translation_all = translation(text)
    st.text_input(""" 全訳 (Перевод всех слов)""", translation_all)
except:
    st.error('今月の翻訳上限超えました (Лимит поиска закончен в этом месяц)')

st.caption("@shiki_yoshida")
st.caption("問い合わせ・要望などはDMでお願いします　https://twitter.com/anya_ruski")
st.caption("参考文献: https://habr.com/ru/post/575100/")