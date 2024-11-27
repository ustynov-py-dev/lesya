from lesya.language.case_helpers import NamePart, CaseUA, NCLNameCaseWord, Gender


class NameCaseCore:
    """
    Base class for name case handling.
    """
    def __init__(self):
        self.case_count = 7
        # System readiness:
        # - All words are identified (know which part of FIO the word belongs to)
        # - Gender is determined for all words
        # If all is done, the flag is set to true, adding a new word resets the flag to false
        self._ready = False
        # If all current words have been declined and each word already has a declination result,
        # then true. Adding a new word resets the flag to false
        self._finished = False
        # Array contains elements of type NCLNameCaseWord. These are all the words to be processed and declined
        self.words = []
        # Variable into which the current working word is placed
        self.working_word = None
        # Array contains the result of the declination of the word - the word in all cases
        self.last_result = []
        # Array contains information about which words from the array <var>$this->words</var> belong to
        # the surname, which to the patronymic, and which to the first name. The array is needed because when adding words
        # we do not always know which part of the FIO it is, so after identifying all words, an array of
        # indexes for quick search is generated.
        self.index = {NamePart.FIRSTNAME: [], NamePart.LASTNAME: [], NamePart.PATRONYMIC: []}
        self.cases = CaseUA().all('ua')

    def __repr__(self):
        return f'{self.words}'

    def forms(self):
        pass

    @property
    def ready(self):
        return self._ready

    @property
    def finished(self):
        return self._finished

    def full_reset(self):
        """
        Resets all information to the initial state. Clears all words added to the system.
        After execution, the system is ready to work from scratch.
        :return: NCLNameCaseCore
        """
        self.words = []
        self.last_result = []
        self.index = {NamePart.FIRSTNAME: [], NamePart.LASTNAME: [], NamePart.PATRONYMIC: []}
        self.not_ready()
        return self

    def not_ready(self):
        """
        Sets flags that the system is not ready and the words have not yet been declined.
        """
        self._ready = False
        self._finished = False

    def rules_chain(self, gender, rules_array):
        for rule_id in rules_array:
            rule_method = f"{gender}_rule{rule_id}"
            if getattr(self, rule_method)():
                return True
        return False

    def word_forms(self, word, endings, replace_last=0):
        result = [self.working_word]
        # word = NCLStr.substr(word, 0, len(word) - replace_last)
        word = word[0:len(word) - replace_last]
        for case_index in range(1, self.case_count):
            result.append(word + endings[case_index - 1])
        self.last_result = result

    def set_first_name(self, firstname=""):
        if firstname:
            index = len(self.words)
            self.words.append(NCLNameCaseWord(firstname))
            self.words[index].name_part = NamePart.FIRSTNAME
            self.not_ready()
        return self

    def set_second_name(self, secondname=""):
        if secondname:
            index = len(self.words)
            self.words.append(NCLNameCaseWord(secondname))
            self.words[index].name_part = NamePart.LASTNAME
            self.not_ready()
        return self

    def set_father_name(self, fathername=""):
        if fathername:
            index = len(self.words)
            self.words.append(NCLNameCaseWord(fathername))
            self.words[index].name_part = NamePart.PATRONYMIC
            self.not_ready()
        return self

    def set_gender(self, gender):
        for word in self.words:
            word.set_true_gender(gender)
        return self

    def set_full_name(self, second_name="", first_name="", father_name=""):
        self.set_first_name(first_name)
        self.set_second_name(second_name)
        self.set_father_name(father_name)
        return self

    def set_name(self, firstname=""):
        return self.set_first_name(firstname)

    def set_last_name(self, secondname=""):
        return self.set_second_name(secondname)

    def set_sir_name(self, secondname=""):
        return self.set_second_name(secondname)

    def prepare_name_part(self, word):
        if not word.name_part:
            self.detect_name_part(word)

    def prepare_all_name_parts(self):
        for word in self.words:
            self.prepare_name_part(word)

    def prepare_gender(self, word):
        if not word.is_gender_solved():
            name_part = word.name_part
            if name_part == NamePart.FIRSTNAME:
                self.gender_by_first_name(word)
            elif name_part == NamePart.PATRONYMIC:
                self.gender_by_patronym(word)
            elif name_part == NamePart.LASTNAME:
                self.gender_by_lastname(word)

    def solve_gender(self):
        for word in self.words:
            if word.is_gender_solved():
                self.set_gender(word.gender())
                return True
        man, woman = 0, 0
        for word in self.words:
            self.prepare_gender(word)
            gender = word.get_gender()
            man += gender[Gender.MAN]
            woman += gender[Gender.WOMAN]
        self.set_gender(Gender.MAN if man > woman else Gender.WOMAN)
        return True

    def generate_index(self):
        self.index = {NamePart.FIRSTNAME: [], NamePart.LASTNAME: [], NamePart.PATRONYMIC: []}
        for index, word in enumerate(self.words):
            name_part = word.name_part
            self.index[name_part].append(index)

    def prepare_everything(self):
        if not self._ready:
            self.prepare_all_name_parts()
            self.solve_gender()
            self.generate_index()
            self._ready = True

    def split_full_name(self, fullname):
        fullname = fullname.strip()
        words_list = [w for w in fullname.split() if w]
        for word in words_list:
            self.words.append(NCLNameCaseWord(word))
        self.prepare_everything()
        return self.words

    def word_case(self, word):
        gender = 'male' if word.gender() == Gender.MAN else 'female'
        name_part = {NamePart.FIRSTNAME: 'first', NamePart.LASTNAME: 'second', NamePart.PATRONYMIC: 'father'}.get(
            word.name_part)
        method = f'{gender}_{name_part}_name'
        tmp = word.word_orig
        cur_words = tmp.split('-')
        o_cur_words = []
        result = ['']*self.case_count
        cnt = len(cur_words)
        for k, cur_word in enumerate(cur_words):
            is_norm_rules = True
            o_ncw = NCLNameCaseWord(cur_word)
            if word.name_part == NamePart.LASTNAME and cnt > 1 and k < cnt - 1:
                if cur_word.lower() not in ('тулуз'):
                    self.detect_name_part(o_ncw)
                    is_norm_rules = o_ncw.name_part == NamePart.LASTNAME
                else:
                    is_norm_rules = False

            self.working_word = cur_word

            if is_norm_rules and getattr(self, method)():
                result_tmp = self.last_result
            else:
                result_tmp = [cur_word] * self.case_count

            o_ncw.set_name_cases(result_tmp)
            o_cur_words.append(o_ncw)

        for o_ncw in o_cur_words:
            namecases = o_ncw.get_name_cases()
            for k, namecase in enumerate(namecases):
                if result[k]:
                    result[k] = result[k] + '-' + namecase
                else:
                    result[k] = namecase

        word.set_name_cases(result, False)

    def all_word_cases(self):
        if not self._finished:
            self.prepare_everything()
            for word in self.words:
                self.word_case(word)
            self._finished = True

    def get_word_case(self, word, number=None):
        cases = word.get_name_cases()
        if number is None or number < 0 or number > (self.case_count - 1):
            return cases
        else:
            return cases[number]

    def get_cases_connected(self, index_array, number=None):
        ready = []
        for index in index_array:
            ready.append(self.get_word_case(self.words[index], number))

        all_cases = len(ready)
        if all_cases:
            if isinstance(ready[0], list):
                result = []
                for case in range(self.case_count):
                    tmp = []
                    for i in range(all_cases):
                        tmp.append(ready[i][case])
                    result.append(' '.join(tmp))
                return result
            else:
                return ' '.join(ready)
        return ''

    def get_firstname_case(self, number=None):
        self.all_word_cases()
        return self.get_cases_connected(self.index[NamePart.FIRSTNAME], number)

    def get_lastname_case(self, number=None):
        self.all_word_cases()
        return self.get_cases_connected(self.index[NamePart.LASTNAME], number)

    def get_patronymic_case(self, number=None):
        self.all_word_cases()
        return self.get_cases_connected(self.index[NamePart.PATRONYMIC], number)

    def get_formatted_array(self, format_):
        if isinstance(format_, list):
            return self.get_formatted_array_forced(format_)
        result = []
        cases = {
            NamePart.LASTNAME: self.get_cases_connected(self.index[NamePart.LASTNAME]),
            NamePart.FIRSTNAME: self.get_cases_connected(self.index[NamePart.FIRSTNAME]),
            NamePart.PATRONYMIC: self.get_cases_connected(self.index[NamePart.PATRONYMIC])
        }
        for cur_case in range(self.case_count):
            line = ""
            for symbol in format_.split():
                if symbol == 'S':
                    line += cases[NamePart.LASTNAME][cur_case]
                elif symbol == 'N':
                    line += cases[NamePart.FIRSTNAME][cur_case]
                elif symbol == 'F':
                    line += cases[NamePart.PATRONYMIC][cur_case]
                else:
                    line += symbol
            result.append(line)
        return result

    def get_formatted_array_forced(self, format_):
        result = []
        cases = []
        for word in format_:
            cases.append(word.get_name_cases())
        for curCase in range(self.case_count):
            line = ""
            for value in cases:
                line += value[curCase] + ' '
            result.append(line.strip())
        return result

    @staticmethod
    def get_formatted_forced(case_num=0, format_=None):
        format_ = format_ if format_ else []
        result = ""
        for word in format_:
            cases = word.get_name_cases()
            result += cases[case_num] + ' '
        return result.strip()

    def get_formatted(self, case_num=0, format_="S N F"):
        self.all_word_cases()
        if case_num is None or not case_num:
            return self.get_formatted_array(format_)
        elif isinstance(format_, list):
            return self.get_formatted_forced(case_num, format_)
        else:
            result = ""
            for symbol in format_.split():
                if symbol == 'S':
                    result += self.get_lastname_case(case_num)
                elif symbol == 'N':
                    result += self.get_firstname_case(case_num)
                elif symbol == 'F':
                    result += self.get_patronymic_case(case_num)
                else:
                    result += symbol
            return result

    def q(self, fullname, case_num=None, gender=None):
        self.full_reset()
        format_ = self.split_full_name(fullname)
        if gender:
            self.set_gender(gender)
        return self.get_formatted(case_num, format_)

    def male_first_name(self):
        return False

    def female_first_name(self):
        return False

    def male_second_name(self):
        return False

    def female_second_name(self):
        return False

    def male_father_name(self):
        return False

    def female_father_name(self):
        return False

    def gender_by_first_name(self, word):
        pass

    def gender_by_lastname(self, word):
        pass

    def gender_by_patronym(self, word):
        pass

    def detect_name_part(self, word):
        pass

    def __getitem__(self, item):
        if not self._finished:
            return None
        if isinstance(item, int) and item in range(self.case_count):
            return self.forms[self.cases[item]]
        if isinstance(item, str):
            if item in self.cases:
                return self.forms[item]
            if item in CaseUA().all():
                index = CaseUA().all().index(item)
                return self[index]
