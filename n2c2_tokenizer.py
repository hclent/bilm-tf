import nltk

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktLanguageVars
from nltk.tokenize.treebank import TreebankWordTokenizer

from clinical_tokenizers import ClinicalSentenceTokenizer, IndexTokenizer

from PyRuSH.RuSH import RuSH

class CustomSentenceBreakingLangVars(PunktLanguageVars):
    mything = 'something'
    # this does nothing -- these must be changed after construction
    #send_end_chars = ('.', '!')

def build_n2c2_tokenizer(keep_token_strings = False, enable_pyrush_sentence_tokenizer = False, disable_custom_preprocessing = True):
    print('Building n2c2 tokenizer...')
    cs_preprocess_split_re_strings = []
    # double newlines
    cs_preprocess_split_re_strings.append(r'[\r\n]{2,}')
    # newlines with only spaces
    cs_preprocess_split_re_strings.append(r'[\r\n]+\s+[\r\n]+')
    # numbered lists (e.g. "1.", "2)")
    cs_preprocess_split_re_strings.append(r'(^|\r|\n)+\s*\d+[.)-]')
    # bulleted lists (e.g."*", "-")
    cs_preprocess_split_re_strings.append(r'(^|\r|\n)+\s*[*-]')
    # starting labels (e.g. "WEIGHT:")
    cs_preprocess_split_re_strings.append(r'(^|\r|\n)+\s*\w+[:]')
    # break up other lines separated by dates
    cs_preprocess_split_re_strings.append(r'(^|\r|\n)+\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}')
    # MIMIC has many lines that start with this [**YYYY-M-DD**]
    cs_preprocess_split_re_strings.append(r'^\[\*+\d{4}-\d{1,2}-\d{1,2}\*+\]')
    # TIU notes have long bars like this : '***********' or '===========' or '------'
    cs_preprocess_split_re_strings.append(r'[*=-]{3,}')
    
    # NOTE : This breaking rule was disabled 2-13-18 since the UMass MADE challenge data often ended each line with 2 spaces and a 
    # newline which caused this aggressive rule to fire over and over again.
    # aggressively break anything with lots of spaces (tabular data)
    #cs_preprocess_split_re_strings.append(r'\s{3,}')
    
        
    custom_lang_vars = CustomSentenceBreakingLangVars()
    custom_lang_vars.sent_end_chars = ('.', '!')
    print(custom_lang_vars.sent_end_chars)

    punkt_tokenizer2 =  PunktSentenceTokenizer(lang_vars = custom_lang_vars)
    treebank_tokenizer = TreebankWordTokenizer()

    # looks like "pt." and "D.R." and "P.R." are already being handled
    #punkt_tokenizer2._params.abbrev_types.update(extra_abbrev)    
        
    sentence_tokenizer = None
    if enable_pyrush_sentence_tokenizer:
        print('Enabling PyRuSH for sentence tokenization...')
        pyrush_sentence_tokenizer = RuSH('resources/PyRuSH/conf/rush_rules.tsv')
        sentence_tokenizer = pyrush_sentence_tokenizer
    else:
        print('Enabling NLTK Punkt for sentence tokenization...')
        sentence_tokenizer = punkt_tokenizer2
        
    print('Type of sentence tokenizer : {}'.format(type(sentence_tokenizer)))
        
    enabled_preprocessing_expressions = []
    if not disable_custom_preprocessing:
        print('Enabling custom preprocessing expressions.  Total : {}'.format(len(cs_preprocess_split_re_strings)))
        enabled_preprocessing_expressions = cs_preprocess_split_re_strings
    else:
        print('Not allowing custom preprocessing expressions...')
        
    cs_tokenizer = ClinicalSentenceTokenizer(default_sentence_tokenizer = sentence_tokenizer, preprocess_split_re_strs = enabled_preprocessing_expressions)

    index_tokenizer = IndexTokenizer(cs_tokenizer, treebank_tokenizer, keep_token_strings = keep_token_strings)
    
    return index_tokenizer
