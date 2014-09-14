import json
import os
import random
import datetime
from string import digits, ascii_uppercase
from avatar_generator import Avatar


class AvatarGenerator(Avatar):
    @staticmethod
    def _text(string):
        """
            Returns the text to draw.
        """
        if len(string) == 0:
            return "#"
        else:
            return string[0:2].upper()


def get_data():
    this_dir = os.path.dirname(__file__)
    return json.load(open(os.path.join(this_dir, 'random_data.json'), 'r'))


class UserGenerator(object):
    def __init__(self, contaminant="", age_from=0, age_to=100, second_name=None, used_names=set()):
        self.age_from = age_from
        self.age_to = age_to
        self.second_name = second_name
        self.used_names = used_names
        self.contaminant = contaminant
        data = get_data()
        self.male_names = map(lambda s: self.contaminant + s, data['male'])
        self.female_names = map(lambda s: self.contaminant + s, data['female'])
        self.second_names = map(lambda s: self.contaminant + s, data['second_names'])
        self.sentences = map(lambda s: self.contaminant + s, data['sentences'])
        self.streets = map(lambda s: self.contaminant + s, data['streets'])
        self.cities = map(lambda s: self.contaminant + s, data['cities'])

    def generate_user(self):
        """
        Generates user information for display.
        :return: A dictionary of user informations. Such as: Avatar, Biography, E-mail, First name, Second name,
        Full name, Gender, Birth date, Mobile number, Phone number, Postcode, Country, Town, Street
        """
        gender = random.choice([1, 2])
        first_name, second_name_supplied = self._get_name(gender)
        second_name = self.second_name if self.second_name else second_name_supplied
        self.used_names.add((first_name, second_name))

        email = 'testing+%s_%s@tutorcruncher.com' % (first_name, second_name)
        email = email.replace(self.contaminant, '')

        return {
            'avatar': AvatarGenerator().generate(128, first_name[0] + second_name[0]),
            'biography': self._get_bio(),
            'email': self.contaminant + email,
            'first_name': first_name,
            'second_name': second_name,
            'full_name': first_name + ' ' + second_name,
            'gender': gender,
            'birth_date': datetime.date.today() - datetime.timedelta(
                days=random.randint(365 * self.age_from, 365 * self.age_to)),
            'mobile': '07' + ''.join(random.choice(digits) for _ in range(9)),
            'phone': '01' + ''.join(random.choice(digits) for _ in range(9)),
            'postcode': self._generate_postcode(),
            'country': 'United Kingdom',
            'street': str(random.randint(1, 300)) + ' ' + random.choice(self.streets),
            'town': random.choice(self.cities)
        }

    def _get_bio(self):
        biography = ''
        for i in random.sample(range(len(self.sentences)), 3):
            biography += ' ' + self.sentences[i]
        return biography.strip()

    def _get_name(self, gender, depth=0):
        random.seed()
        first_name = random.choice(self.male_names if gender == 1 else self.female_names)
        second_name = random.choice(self.second_names)
        if depth > 5:
            return first_name, second_name
        if (first_name, second_name) in self.used_names:
            return self._get_name(gender, depth + 1)
        return first_name, second_name

    @staticmethod
    def _generate_postcode():
        postcode = "%s%s%s %s%s%s" % (random.choice(ascii_uppercase), random.choice(ascii_uppercase),
                                      random.choice(digits),  random.choice(digits), random.choice(ascii_uppercase),
                                      random.choice(digits))
        return postcode

if __name__ == "__main__":
    print UserGenerator().generate_user()