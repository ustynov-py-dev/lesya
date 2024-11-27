class Gender:
    """
    A class containing constants for gender determination
    """
    MALE = 'male'
    FEMALE = 'female'
    MAN = 'male'
    WOMAN = 'female'


class CaseUA:
    """
    A class containing constants for grammatical cases in Ukrainian
    """
    NOMINATIVE = "nominative"  # "Називний відмінок (Nominative)"  # Nominative case
    GENITIVE = "genitive"  # "Родовий відмінок (Genitive)"  # Genitive case
    DATIVE = "dative"  # "Давальний відмінок (Dative)"  # Dative case
    ACCUSATIVE = "accusative"  # "Знахідний відмінок (Accusative)"  # Accusative case
    INSTRUMENTAL = "instrumental"  # "Орудний відмінок (Instrumental)"  # Instrumental case
    PREPOSITIONAL = "prepositional"  # "Місцевий відмінок (Prepositional)"  # Prepositional case
    VOCATIVE = "vocative"  # "Кличний відмінок (Vocative)"  # Vocative case

    @classmethod
    def __getitem__(cls, number: int):
        if number in range(7):
            return {0: cls.NOMINATIVE,
                    1: cls.GENITIVE,
                    2: cls.DATIVE,
                    3: cls.ACCUSATIVE,
                    4: cls.INSTRUMENTAL,
                    5: cls.PREPOSITIONAL,
                    6: cls.VOCATIVE}.get(number)
        raise TypeError("The number must be in the range from 0 to 6")

    def all(self, lang='en'):
        if lang == 'en':
            return [self.NOMINATIVE, self.GENITIVE, self.DATIVE, self.ACCUSATIVE, self.INSTRUMENTAL, self.PREPOSITIONAL,
                    self.VOCATIVE]
        elif lang == 'ua':
            return ['називний', 'родовий', 'давальний', 'знахідний', 'орудний', 'місцевий', 'кличний']

    @staticmethod
    def count():
        return 7

    @classmethod
    def __len__(cls):
        return cls.count()


class NamePart:
    FIRSTNAME = 'firstname'
    LASTNAME = 'lastname'
    PATRONYMIC = 'patronymic'


class NCLNameCaseWord:
    """
    A class representing a word with additional properties and methods for handling name cases and gender determination.
    """
    def __init__(self, word):
        self.word = word.lower()
        self.word_orig = word
        self.name_part = None
        self.gender_man = 0
        self.gender_woman = 0
        self.gender_solved = None
        # mask to define origin capital and string letters: X, or x
        self.letter_mask = ''
        # array of cases for the word
        self.name_cases = []
        # self.rule = 0
        self.create_mask(word)

    def create_mask(self, word):
        """
        Generating mask for the word
        """
        for letter in word:
            if letter.isupper():
                self.letter_mask += 'X'
            else:
                self.letter_mask += 'x'

    def return_mask(self):
        """ Convert the word to the capital / small letter format according to its mask
        """
        mask_length = len(self.letter_mask)
        for i, case in enumerate(self.name_cases):
            case_length = len(case)
            max_len = min(case_length, mask_length)
            new_case = ''
            for j in range(max_len):
                letter = case[j]
                if self.letter_mask[j] == 'X':
                    letter = letter.upper()
                new_case += letter
            new_case += case[max_len:case_length]
            self.name_cases[i] = new_case

    def set_name_cases(self, name_cases, is_return_mask=True):
        self.name_cases = name_cases
        if is_return_mask:
            self.return_mask()

    def get_name_cases(self):
        return self.name_cases

    def gender(self):
        if not self.gender_solved:
            if self.gender_man >= self.gender_woman:
                self.gender_solved = Gender.MALE
            else:
                self.gender_solved = Gender.FEMALE
        return self.gender_solved

    def set_gender(self, man, woman):
        self.gender_man = man
        self.gender_woman = woman

    def set_true_gender(self, gender):
        self.gender_solved = gender

    def get_gender(self):
        return {Gender.MALE: self.gender_man, Gender.FEMALE: self.gender_woman}

    def is_gender_solved(self):
        return bool(self.gender_solved)

    def __repr__(self):
        return f'{self.word_orig} - {self.name_cases}'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.word_orig == other
        elif isinstance(other, NCLNameCaseWord):
            return self.word_orig == other.word_orig
        return False
