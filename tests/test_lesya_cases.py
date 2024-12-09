import unittest
from parameterized import parameterized
from lesya import Lesya, CaseUA


class TestUkrainianNameDeclension(unittest.TestCase):
    def test_name_female(self):
        # Test with female name
        person = Lesya('Леся Українка')
        self.assertEqual(person.nominative, 'Леся Українка')
        self.assertEqual(person.genitive, 'Лесі Українки')
        self.assertEqual(person.dative, 'Лесі Українці')
        self.assertEqual(person.accusative, 'Лесю Українку')
        self.assertEqual(person.instrumental, 'Лесею Українкою')
        self.assertEqual(person.prepositional, 'Лесі Українці')
        self.assertEqual(person.vocative, 'Лесе Українко')

    def test_name_male(self):
        # Test with male name
        person = Lesya('Тарас Шевченко')
        self.assertEqual(person.nominative, 'Тарас Шевченко')
        self.assertEqual(person.genitive, 'Тараса Шевченка')
        self.assertEqual(person.dative, 'Тарасу Шевченку')
        self.assertEqual(person.accusative, 'Тараса Шевченка')
        self.assertEqual(person.instrumental, 'Тарасом Шевченком')
        self.assertEqual(person.prepositional, 'Тарасові Шевченкові')
        self.assertEqual(person.vocative, 'Тарасе Шевченку')

    def test_name_with_middle_name(self):
        # Test with name and patronymic
        person = Lesya('Іван Петрович Франко')
        self.assertEqual(person.nominative, 'Іван Петрович Франко')
        self.assertEqual(person.genitive, 'Івана Петровича Франка')
        self.assertEqual(person.dative, 'Івану Петровичу Франку')
        self.assertEqual(person.accusative, 'Івана Петровича Франка')
        self.assertEqual(person.instrumental, 'Іваном Петровичем Франком')
        self.assertEqual(person.prepositional, 'Іванові Петровичу Франкові')
        self.assertEqual(person.vocative, 'Іване Петровичу Франку')

    @parameterized.expand([
        ("Іван Семенович Нечуй-Левицький",  # Nominative хто
         "Івана Семеновича Нечуя-Левицького",  # Genitive кого
         "Івану Семеновичу Нечуєві-Левицькому",  # Dative кому
         "Івана Семеновича Нечуя-Левицького",  # Accusative кого
         "Іваном Семеновичем Нечуєм-Левицьким",  # Instrumental ким
         "Іванові Семеновичу Нечуєві-Левицькому",  # Prepositional  із ким
         "Іване Семеновичу Нечую-Левицький"),  # Vocative <name>!
        ("Людвіг ван Бетховен",
         "Людвіга ван Бетховена",
         "Людвігу ван Бетховену",
         "Людвіга ван Бетховена",
         "Людвігом ван Бетховеном",
         "Людвігові ван Бетховенові",
         "Людвіже ван Бетховене"),
        ("Тейлор Свіфт",
         "Тейлора Свіфта",
         "Тейлору Свіфту",
         "Тейлора Свіфта",
         "Тейлором Свіфтом",
         "Тейлорові Свіфтові",
         "Тейлоре Свіфте"),
        ("Джо Байден",
         "Джо Байдена",
         "Джо Байдену",
         "Джо Байдена",
         "Джо Байденом",
         "Джо Байденові",
         "Джо Байдене"),
        ("Долгушин Віталій Данилович",
         "Долгушина Віталія Даниловича",
         "Долгушину Віталієві Даниловичу",
         "Долгушина Віталія Даниловича",
         "Долгушиним Віталієм Даниловичем",
         "Долгушину Віталієві Даниловичу",
         "Долгушине Віталію Даниловичу"),
        ("Хасан ібн Хорезмі",
         "Хасана ібн Хорезмі",
         "Хасану ібн Хорезмі",
         "Хасана ібн Хорезмі",
         "Хасаном ібн Хорезмі",
         "Хасанові ібн Хорезмі",
         "Хасане ібн Хорезмі"),
        ("Швець Іван",
         "Швеця Івана",
         "Швецеві Івану",
         "Швеця Івана",
         "Швецем Іваном",
         "Швецеві Іванові",
         "Швецю Іване"),
        ("Петро Сергійович Півень",
         "Петра Сергійовича Півня",
         "Петру Сергійовичу Півневі",
         "Петра Сергійовича Півня",
         "Петром Сергійовичем Півнем",
         "Петрові Сергійовичу Півневі",
         "Петре Сергійовичу Півню"),
        ("Воробей Капітан Барбосович",
         "Вороб’я Капітана Барбосовича",
         "Вороб’єві Капітану Барбосовичу",
         "Вороб’я Капітана Барбосовича",
         "Вороб’єм Капітаном Барбосовичем",
         "Вороб’єві Капітанові Барбосовичу",
         "Вороб’ю Капітане Барбосовичу"),
        ("Тілець Федір Йосипович",
         "Тільця Федора Йосиповича",
         "Тільцеві Федору Йосиповичу",
         "Тільця Федора Йосиповича",
         "Тільцем Федором Йосиповичем",
         "Тільцеві Федорові Йосиповичу",
         "Тільцю Федоре Йосиповичу"),
        ("Емануель Макрон",
         "Емануеля Макрона",
         "Емануелеві Макрону",
         "Емануеля Макрона",
         "Емануелем Макроном",
         "Емануелеві Макронові",
         "Емануелю Макроне"),
        ("Кисіль Ліу",
         "Кисіля Ліу",
         "Кисілеві Ліу",
         "Кисіля Ліу",
         "Кисілем Ліу",
         "Кисілеві Ліу",
         "Кисілю Ліу"),
        ("Олександр Дюма",
         "Олександра Дюма",
         "Олександру Дюма",
         "Олександра Дюма",
         "Олександром Дюма",
         "Олександрові Дюма",
         "Олександре Дюма"),
        ("Заєць Миколай Йосипович",
         "Зайця Миколая Йосиповича",
         "Зайцеві Миколаєві Йосиповичу",
         "Зайця Миколая Йосиповича",
         "Зайцем Миколаєм Йосиповичем",
         "Зайцеві Миколаєві Йосиповичу",
         "Зайцю Миколаю Йосиповичу"),
        ("Завгородній Яків",
         "Завгороднього Якова",
         "Завгородньому Якову",
         "Завгороднього Якова",
         "Завгороднім Яковом",
         "Завгородньому Яковові",
         "Завгородній Якове"),
        ("Жуковський Іван",
         "Жуковського Івана",
         "Жуковському Івану",
         "Жуковського Івана",
         "Жуковським Іваном",
         "Жуковському Іванові",
         "Жуковський Іване"),
        ("Кузьмін Іван",
         "Кузьміна Івана",
         "Кузьміну Івану",
         "Кузьміна Івана",
         "Кузьміним Іваном",
         "Кузьміну Іванові",
         "Кузьміне Іване"),
        ("Мірошниченко Іван",
         "Мірошниченка Івана",
         "Мірошниченку Івану",
         "Мірошниченка Івана",
         "Мірошниченком Іваном",
         "Мірошниченкові Іванові",
         "Мірошниченку Іване"),
        ("Міщенко Іван",
         "Міщенка Івана",
         "Міщенку Івану",
         "Міщенка Івана",
         "Міщенком Іваном",
         "Міщенкові Іванові",
         "Міщенку Іване"),
        ("Палій Андрій",
         "Палія Андрія",
         "Палієві Андрієві",
         "Палія Андрія",
         "Палієм Андрієм",
         "Палієві Андрієві",
         "Палію Андрію"),
    ])
    def test_male_declension(self, nominative, genitive, dative, accusative, instrumental, prepositional,
                             vocative):
        person = Lesya(nominative, gender='male')
        self.assertEqual(person.nominative, nominative)
        self.assertEqual(person.genitive, genitive)
        self.assertEqual(person.dative, dative)
        self.assertEqual(person.accusative, accusative)
        self.assertEqual(person.instrumental, instrumental)
        self.assertEqual(person.prepositional, prepositional)
        self.assertEqual(person.vocative, vocative)

    @parameterized.expand([
        ("Тейлор Свіфт",
         "Тейлор Свіфт",
         "Тейлор Свіфт",
         "Тейлор Свіфт",
         "Тейлор Свіфт",
         "Тейлор Свіфт",
         "Тейлор Свіфт"),
        ("Камала Гаріс",
         "Камали Гаріс",
         "Камалі Гаріс",
         "Камалу Гаріс",
         "Камалою Гаріс",
         "Камалі Гаріс",
         "Камало Гаріс"),
        ("Шерон Стоун",
         "Шерон Стоун",
         "Шерон Стоун",
         "Шерон Стоун",
         "Шерон Стоун",
         "Шерон Стоун",
         "Шерон Стоун"),
        ("Єлізавета Устинова",
         "Єлізавети Устинової",
         "Єлізаветі Устиновій",
         "Єлізавету Устинову",
         "Єлізаветою Устиновою",
         "Єлізаветі Устиновій",
         "Єлізавето Устинова"),
        ("Глінських Роза Іванівна",
         "Глінських Рози Іванівни",
         "Глінських Розі Іванівні",
         "Глінських Розу Іванівну",
         "Глінських Розою Іванівною",
         "Глінських Розі Іванівні",
         "Глінських Розо Іванівно"),
        ("Завгородняя Лариса",
         "Завгородньої Лариси",
         "Завгородній Ларисі",
         "Завгородню Ларису",
         "Завгородньою Ларисою",
         "Завгородній Ларисі",
         "Завгородняя Ларисо"),

    ])
    def test_female_declension(self, nominative, genitive, dative, accusative, instrumental, prepositional,
                               vocative):
        person = Lesya(nominative, gender='female')
        self.assertEqual(person[CaseUA.NOMINATIVE], nominative)
        self.assertEqual(person[CaseUA.GENITIVE], genitive)
        self.assertEqual(person[CaseUA.DATIVE], dative)
        self.assertEqual(person[CaseUA.ACCUSATIVE], accusative)
        self.assertEqual(person[CaseUA.INSTRUMENTAL], instrumental)
        self.assertEqual(person[CaseUA.PREPOSITIONAL], prepositional)
        self.assertEqual(person[CaseUA.VOCATIVE], vocative)


if __name__ == '__main__':
    unittest.main()
