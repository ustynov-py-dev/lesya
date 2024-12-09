import re
from lesya.language.nc_core import NameCaseCore, NamePart
from lesya.language.name_constants import NAMES, FEMALE_NAMES, LASTNAME_ENDINGS2, LASTNAME_ENDINGS3
from lesya.language.case_helpers import CaseUA

NAMES_LIST = {n.lower() for n in NAMES + FEMALE_NAMES}
NAMES = {n.lower() for n in NAMES}
FEMALE_NAMES = {n.lower() for n in FEMALE_NAMES}


class NameCaseUa(NameCaseCore):
    def __init__(self):
        super().__init__()
        self.vowels = 'аеиоуіїєюя'
        self.consonant = "бвгджзйклмнпрстфхцчшщ"
        self.hissing = "жчшщ"
        self.nonhissing = "бвгдзклмнпрстфхц"
        self.soft = 'ьюяєї'
        self.labial = 'мвпбф'

    @property
    def forms(self):
        if self.finished:
            all_forms = dict()
            for i, case in enumerate(self.cases):
                all_forms[case] = ' '.join([w.name_cases[i] for w in self.words])
            return all_forms
        return None

    def get_firstname(self):
        words = [w for w in self.words if w.name_part == NamePart.FIRSTNAME]
        return words[0].word_orig if words else None

    def get_lastname(self):
        words = [w for w in self.words if w.name_part == NamePart.LASTNAME]
        return words[0].word_orig if words else None

    def get_patronym(self):
        words = [w for w in self.words if w.name_part == NamePart.PATRONYMIC]
        return words[0].word_orig if words else None

    @staticmethod
    def inverse_gkh(letter):
        return {'г': 'з', 'к': 'ц', 'х': 'с'}.get(letter, letter)

    @staticmethod
    def inverse_gk2(letter):
        return {'к': 'ч', 'г': 'ж'}.get(letter, letter)

    @staticmethod
    def is_apostrof(char):
        return char in "'`’\""

    @staticmethod
    def first_last_vowel(word, vowels):
        for char in word[::-1]:
            if char in vowels:
                return char
        return None

    def get_base_word(self, word):
        base_word = word.lower()
        while base_word[-1] in self.vowels + 'ь':
            base_word = base_word[:-1]
        return base_word.lower()

    def male_rule1(self):
        last2 = self.working_word[-2]
        if self.working_word[-1] == 'а':
            self.word_forms(self.working_word,
                            [last2 + 'и', self.inverse_gkh(last2) + 'і', last2 + 'у', last2 + 'ою',
                             self.inverse_gkh(last2) + 'і', last2 + 'о'], 2)
            return True
        elif self.working_word[-1] == 'я':
            if last2 == 'і':
                self.word_forms(self.working_word, ['ї', 'ї', 'ю', 'єю', 'ї', 'є'], 1)
                return True
            else:
                self.word_forms(self.working_word,
                                [last2 + 'і', self.inverse_gkh(last2) + 'і', last2 + 'ю',
                                 last2 + 'ею', self.inverse_gkh(last2) + 'і',
                                 last2 + 'е'], 2)
                return True
        return False

    def male_rule2(self):
        if self.working_word[-1] == 'р':
            base_word = self.working_word
            if self.working_word in ('Ігор', 'Лазар') or self.working_word.lower().endswith('якір'):
                endings = ['я', 'еві', 'я', 'ем', 'еві', 'е']
                if base_word[-2] == 'і':
                    base_word = base_word[:-2] + 'о' + base_word[-1]
            else:
                # це має працювати на іменах (Федір -Федора, Сидір-Сидора)
                # а не на прізвищах (Кушнір -Кушніра)
                if base_word[-2] == 'і':
                    word = [w for w in self.words if w == self.working_word]
                    if word[0].name_part == NamePart.FIRSTNAME:
                        base_word = base_word[:-2] + 'о' + base_word[-1]
                endings = ['а', 'у', 'а', 'ом', 'ові', 'е']
            self.word_forms(base_word, endings)
            return True
        return False

    def male_rule3(self):
        last2 = self.working_word[-2]
        if self.working_word[-1] in self.consonant + 'оь':
            group = self.detect_second_group(self.working_word)
            base_word = self.get_base_word(self.working_word)
            last = base_word[-1]
            if (last not in 'йм' and base_word[-2] == 'і'
                    and not base_word.lower() in ('світ', 'цвіт')
                    and self.working_word not in ('Гліб', 'Леонід')
                    and not self.working_word[-2:] in ('ік', 'іч')):
                if self.working_word[-4:] in ('бідь', 'мінь'):
                    # заміна на -е-
                    base_word = base_word[:-2] + 'е' + base_word[-1]
                elif self.working_word[-4:] in ('сіль', 'двіг', 'цвіг'):
                    # не змінюється
                    pass
                else:
                    # заміна на -о-
                    base_word = base_word[:-2] + 'о' + base_word[-1]

            if (base_word[0] in ('о', 'О') and self.first_last_vowel(base_word, self.vowels + 'гк') == 'е'
                    and not self.working_word[-2:] in ('сь', 'ць', 'нь', 'ть', 'дь', 'ль', 'рь')):
                delim = base_word.rfind('е')
                base_word = base_word[:delim] + base_word[delim + 1:]
            if group == 1:
                if self.working_word[-2:] == 'ок' and self.working_word[-3:] != 'оок':
                    self.word_forms(self.working_word, ['ка', 'кові', 'ка', 'ком', 'кові', 'че'], 2)
                    return True
                elif self.working_word[-2:] in ('ов', 'ев', 'єв') and not self.working_word in ('Лев', 'Остромов'):
                    self.word_forms(base_word, [last + 'а', last + 'у', last + 'а', last + 'им', last + 'у',
                                                self.inverse_gk2(last) + 'е'], 1)
                    return True
                elif self.working_word[-2:] in ('ін', 'ин'):
                    self.word_forms(self.working_word, ['а', 'у', 'а', 'им', 'у', 'е'])
                    return True
                else:
                    if self.working_word.lower() == 'пес':
                        base_word = 'пс'
                    if self.working_word[-3:] in ('ких', 'гих', 'чих', 'дих'):
                        return False
                    if self.working_word[-2:] in ('ко'):
                        vocative_end = 'ку'
                    else:
                        vocative_end = self.inverse_gk2(last) + 'е'
                    endings = [last + 'а', last + 'у', last + 'а', last + 'ом', last + 'ові',
                                                vocative_end]
                    self.word_forms(base_word, endings, 1)
                    return True
            if group == 2:
                self.word_forms(base_word, ['а', 'у', 'а', 'ем', 'еві', 'е'])
                return True
            if group == 3:
                if self.working_word[-2:] == 'ей' and self.working_word[-3] in self.labial:
                    base_word = self.working_word[:-2] + '’'
                    self.word_forms(base_word, ['я', 'єві', 'я', 'єм', 'єві', 'ю'])
                    return True
                elif self.working_word[-1] == 'й' or last2 == 'і':
                    if self.working_word[-3:] == 'ній':
                        self.word_forms(self.working_word, ['ього', 'ьому', 'ього', 'ім', 'ьому', 'ій'], 2)
                    else:
                        self.word_forms(self.working_word, ['я', 'єві', 'я', 'єм', 'єві', 'ю'], 1)
                    return True
                elif self.working_word[-3:] == 'ець':
                    base_word = self.get_exclusions(base_word)
                    self.word_forms(base_word, ['ця', 'цеві', 'ця', 'цем', 'цеві', 'цю'], 2)
                    return True
                elif self.working_word[-3:] in ('єць', 'яць'):
                    self.word_forms(self.working_word, ['йця', 'йцеві', 'йця', 'йцем', 'йцеві', 'йцю'], 3)
                    return True
                else:
                    if self.working_word[-4:] in ('вель', 'вень', 'день'):
                        base_word = self.working_word[:-3] + base_word[-1]
                    self.word_forms(base_word, ['я', 'еві', 'я', 'ем', 'еві', 'ю'])
                    return True
        return False

    def male_rule4(self):
        if self.working_word[-1] == 'і':
            self.word_forms(self.working_word, ['их', 'им', 'их', 'ими', 'их', 'і'], 1)
            return True
        return False

    def male_rule5(self):
        if self.working_word[-2:] in ('ий', 'ой'):
            self.word_forms(self.working_word, ['ого', 'ому', 'ого', 'им', 'ому', 'ий'], 2)
            return True
        return False

    def noun_is_not_declined(self):
        """ exclusions for words that are not declined """
        if re.search(f"[{''.join(self.vowels)}]{{2}}$", self.working_word):
            return True
        if re.search(r'(ьє|ні|лі|рі|ьї|те|се|же|хе|до|го|со|не|мі)$', self.working_word):
            return True
        if self.working_word.lower() in ('педро', 'дюма', 'дідро', 'джо', 'камю'):
            return True
        if self.working_word.lower() in ('ван', 'да', 'де', 'ді', 'дю', 'дер', 'ед', 'ель', 'ла', 'ле', 'фон', 'ібн'):
            return True
        return False

    def get_exclusions(self, base_word):
        if base_word[-3] in self.labial + "н" and sum([1 for ch in base_word if ch in self.vowels]) > 1:
            # Кравець, правдивець, але не Швець
            return base_word[:-2] + 'ц*'
        if base_word[-3:] == 'лец' and sum([1 for ch in base_word if ch in self.vowels]) > 1:
            # Слепець, але не Лець
            return base_word[:-3] + 'льц*'
        return self.working_word

    def female_rule1(self):
        last2 = self.working_word[-2]
        if self.working_word[-1] == 'а':
            self.word_forms(self.working_word,
                            [last2 + 'и', self.inverse_gkh(last2) + 'і', last2 + 'у', last2 + 'ою',
                             self.inverse_gkh(last2) + 'і', last2 + 'о'], 2)
            return True
        elif self.working_word[-2:] == 'яя':
            self.word_forms(self.working_word, ['ьої', 'ій', 'ю', 'ьою', 'ій', 'яя'], 2)
            return True
        elif self.working_word[-1] == 'я':
            if last2 in self.vowels or self.is_apostrof(last2):
                self.word_forms(self.working_word, ['ї', 'ї', 'ю', 'єю', 'ї', 'є'], 1)
                return True
            else:
                self.word_forms(self.working_word,
                                [last2 + 'і', self.inverse_gkh(last2) + 'і', last2 + 'ю',
                                 last2 + 'ею', self.inverse_gkh(last2) + 'і',
                                 last2 + 'е'], 2)
                return True
        return False

    def female_rule2(self):
        if self.working_word[-1] in self.consonant + 'ь':
            base_word = self.get_base_word(self.working_word)
            apostrof = ''
            duplicate = ''
            last = base_word[-1]
            last2 = base_word[-2]
            if last in self.labial and last2 in self.vowels:
                apostrof = '’'
            if last in 'дтзсцлн':
                duplicate = last
            if self.working_word[-1] == 'ь':
                self.word_forms(base_word, ['і', 'і', 'ь', duplicate + apostrof + 'ю', 'і', 'е'])
                return True
            else:
                self.word_forms(base_word, ['і', 'і', '', duplicate + apostrof + 'ю', 'і', 'е'])
                return True
        return False

    def female_rule3(self):
        last2 = self.working_word[-2]
        if self.working_word[-2:] == 'ая':
            self.word_forms(self.working_word, ['ої', 'ій', 'ую', 'ою', 'ій', 'ая'], 2)
            return
        if self.working_word[-1] == 'а' and (self.working_word[-2] in 'чнв' or self.working_word[-3:-1] in ['ьк']):
            self.word_forms(self.working_word,
                            [last2 + 'ої', last2 + 'ій', last2 + 'у', last2 + 'ою',
                             last2 + 'ій', last2 + 'о'], 2)
            return True
        return False

    def detect_second_group(self, word):
        base_word = word
        stack = []
        while base_word[-1] in self.vowels + 'ь':
            stack.append(base_word[-1])
            base_word = base_word[0: -1]
        last = 'Z'
        if stack:
            last = stack[- 1]
        base_word_end = base_word[-1]
        if base_word_end in self.nonhissing and last not in self.soft:
            return 1
        elif base_word_end in self.hissing and last not in self.soft:
            return 2
        else:
            return 3

    def male_first_name(self):
        if self.noun_is_not_declined():
            return False
        return self.rules_chain('male', [1, 2, 3])

    def female_first_name(self):
        return self.rules_chain('female', [1, 2])

    def male_second_name(self):
        if self.noun_is_not_declined():
            return False
        return self.rules_chain('male', [5, 1, 2, 3, 4])

    def female_second_name(self):
        return self.rules_chain('female', [3, 1])

    def male_father_name(self):
        if self.working_word[-2:] in ('ич', 'іч'):
            self.word_forms(self.working_word, ['а', 'у', 'а', 'ем', 'у', 'у'])
            return True
        return False

    def female_father_name(self):
        if self.working_word[-3:] == 'вна':
            self.word_forms(self.working_word, ['и', 'і', 'у', 'ою', 'і', 'о'], 1)
            return True
        return False

    def gender_by_first_name(self, word):
        self.working_word = word.word
        man = 0
        woman = 0
        if self.working_word[-1] == 'й':
            man += 0.9
        if self.working_word in NAMES:
            man += 30
        if self.working_word in FEMALE_NAMES:
            woman += 30
        if self.working_word[-2:] in {'ро', 'яр', 'ус', 'ис', 'ст', 'ив', 'им', 'ам', 'іт', 'ід', 'ат', 'іб', 'нн',
                                      'ап', 'ік', 'ів', 'ас', 'ир', 'ил', 'ет', 'ип', 'ик', 'ол', 'лк', 'ім', 'єр',
                                      'ок', 'ур', 'їл', 'ох', 'сл', 'ад', 'др', 'ор', 'ар', 'ав', 'сь', 'ій', 'ло',
                                      'ко', 'ен', 'ин', 'юб', 'ін', 'ид', 'од', 'ем', 'ум', 'рт', 'ян', 'ег', 'он'}:
            man += 0.5
        if self.working_word[-3:] in {"'я", 'ая', 'га', 'да', 'дь', 'ер', 'ея', 'за', 'ит', 'иф', 'йя', 'на', 'па',
                                      'ря', 'ся', 'тя', 'фа', 'ха', 'ша', 'ія'}:
            woman += 0.5
        if self.working_word[-1] in self.consonant:
            man += 0.01
        if self.working_word[-1] == 'ь':
            man += 0.02

        word.set_gender(man, woman)

    def gender_by_patronym(self, word):
        self.working_word = word.word
        if self.working_word[-2:] in ('ич', 'іч'):
            word.set_gender(10, 0)
        if self.working_word[-2:] == 'на':
            word.set_gender(0, 12)

    def detect_name_part(self, word):
        name_part = word.word
        self.working_word = name_part

        first = 0
        second = 0
        father = 0

        if self.working_word[-3:] in ('вна', 'чна', 'ліч') or self.working_word[-4:] in ('ьмич', 'ович', 'огли'):
            father += 3
        if (self.working_word[-3:] == 'тин'
                or self.working_word[-4:] in ('ьмич', 'юбов', 'івна', 'явка', 'орив', 'кіян')):
            first += 0.5
        if name_part in NAMES_LIST:
            first += 10
        if self.working_word[-2:] in LASTNAME_ENDINGS2:
            second += 0.4
        if self.working_word[-3:] in LASTNAME_ENDINGS3:
            second += 0.4

        max_val = max(first, second, father)
        if first == max_val:
            word.name_part = NamePart.FIRSTNAME
        elif second == max_val:
            word.name_part = NamePart.LASTNAME
        else:
            word.name_part = NamePart.PATRONYMIC


class Lesya:
    def __init__(self, name, gender=None):
        self._core = NameCaseUa()
        self._core.q(name, gender=gender)
        self.forms = self._core.forms

    @property
    def nominative(self):
        return self._core[CaseUA.NOMINATIVE]

    @property
    def genitive(self):
        return self._core[CaseUA.GENITIVE]

    @property
    def dative(self):
        return self._core[CaseUA.DATIVE]

    @property
    def accusative(self):
        return self._core[CaseUA.ACCUSATIVE]

    @property
    def instrumental(self):
        return self._core[CaseUA.INSTRUMENTAL]

    @property
    def prepositional(self):
        return self._core[CaseUA.PREPOSITIONAL]

    @property
    def vocative(self):
        return self._core[CaseUA.VOCATIVE]

    def __getitem__(self, item):
        if not self._core.finished:
            return None
        if isinstance(item, int) and item in range(self._core.case_count):
            return self._core.forms[self._core.cases[item]]
        if isinstance(item, str):
            if item in self._core.cases:
                return self._core.forms[item]
            if item in CaseUA().all():
                index = CaseUA().all().index(item)
                return self[index]

    def __repr__(self):
        return self.nominative
