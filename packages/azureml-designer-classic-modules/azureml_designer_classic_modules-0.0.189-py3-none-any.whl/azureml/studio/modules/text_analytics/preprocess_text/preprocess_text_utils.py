import re
from azureml.studio.modulehost.attributes import ItemInfo
from azureml.studio.common.types import AutoEnum


class PreprocessTextLanguage(AutoEnum):
    # for now we only support english
    English: ItemInfo(name='English', friendly_name='English') = ()


class PreprocessTextTrueFalseType(AutoEnum):
    TRUE: ItemInfo(name='True', friendly_name='True') = ()
    FALSE: ItemInfo(name='False', friendly_name='False') = ()


class PreprocessTextConstant:
    SentenceSeparator = "|||"
    TokenSeparator = " "
    PreprocessedColumnPrefix = "Preprocessed"
    LanguageModelDict = {PreprocessTextLanguage.English: "en_core_web_sm"}


class PreprocessTextPattern:
    URLPattern = re.compile("(f|ht)(tp)(s?)(://)(.*)[./][^ ]+", flags=re.IGNORECASE)
    EmailPattern = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
                              r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",
                              flags=re.IGNORECASE)
    SpecialCharsPattern = re.compile(r"([!,\.#$%&<>\"'*“”+/=?^_`{|}~-]){3,}", flags=re.IGNORECASE)
    DuplicateCharsPattern = re.compile(r"([a-z])\1{2,}", flags=re.IGNORECASE)
    VerbContractionDict = {re.compile("&", flags=re.IGNORECASE): "and",
                           re.compile("cannot|cant|can't|can’t", flags=re.IGNORECASE): "can not",
                           re.compile("it['’]s", flags=re.IGNORECASE): "it is",
                           re.compile("won['’]t", flags=re.IGNORECASE): "will not",
                           re.compile("let['’]s", flags=re.IGNORECASE): "let us",
                           re.compile("I ['’] m |I ['’]m |I['’]m ", flags=re.IGNORECASE): "I am",
                           re.compile("you ['’] re |you ['’]re |you['’]re ", flags=re.IGNORECASE): "you are",
                           re.compile("(has|had|have|would|should|could|do|does|did)(n'|n’)t",
                                      flags=re.IGNORECASE): r"\1 not"}


class POSTag:
    Num = "NUM"
    Sym = "SYM"
    Punct = "PUNCT"
    Pron = "PRON"
