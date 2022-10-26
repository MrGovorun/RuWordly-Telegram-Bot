class UserTry():
    def __init__(self, variants):
        self.words = []
        self.answers = []
        self.current_result = Result(variants)

    def wait_answer(self):
        return len(self.words) != len(self.answers)

    def need_restart(self):
        return len(self.current_result.variants) <= 1
    
    def add_word(self, word:str) -> str:
        if self.wait_answer():
            if self._correct_code(word):
                self.answers.append(word)
            else:
                return 'Error'
        else:
            if self._correct_word(word): 
                self.words.append(word)
            else:
                return 'Error'
        return 'Ok'

    def _correct_word(self, word: str) -> bool:
        if (len(word)==5 
                and word.isalpha()
                and word not in self.words):
            return True
        return False

    def _correct_code(self, code: str) -> bool:
        if (len(code)==5 
                and all(num in '012' for num in code)):
            return True
        return False

    def words_selection(self):
        result = self.current_result.check_word(self.words[-1],self.answers[-1])
        if not result:
            self.words.pop()
            self.answers.pop()
            return False
        self.current_result.search()
        return True
    
    def next_step(self, word):
        result = self.add_word(word)
        if result != 'Ok' and not self.wait_answer():
            return 'wrong_word'
        elif result == 'Ok' and self.wait_answer():
            return 'code_ask'
        elif result != 'Ok':
            return 'wrong_code'
        else:
            self.words_selection()
            return result


class Result():
    def __init__(self, variants):
        self.variants = set(variants)
        self.wrong_letters = set()
        self.correct_letters = {i:'_' for i in range(5)}
        self.wrong_place = {}

    def __str__(self):
        res = 'Wrong: '+', '.join(self.wrong_letters)+'\n'
        res += 'Variants: '+', '.join(self.variants)+'\n'
        res += 'Correct: '+''.join(self.correct_letters.values())
        return res

    def check_word(self, word, code):
        """Проверяем каждую букву согласно ответу игры
        """
        if not self._logical_check(word, code):
            return False
        for position, digit in enumerate(code):
            if digit == '0':
                self.wrong_letters.add(word[position])
            elif digit == '1':
                self.wrong_place.setdefault(position,set()).add(word[position])
            else:
                self.correct_letters[position] = word[position]
        return True
    
    def search(self):
        tmp_variants = set()
        for word in self.variants:
            if  (not(any(bukva in word for bukva in self.wrong_letters))
                and all((word[position] == bukva for position, bukva in
                    self.correct_letters.items() if bukva != '_'))
                and self._wrong_place_check(word)):
                tmp_variants.add(word)
        self.variants = tmp_variants
    
    def _wrong_place_check(self,word):
        flag = True
        if not self.wrong_place:
            return flag
        for position, letters in self.wrong_place.items():
            if not(all(letter in word for letter in letters) 
                    and word[position] not in letters):
                flag = False
                break
        return flag
    
    def _logical_check(self, word:str, code:str) -> bool:
        for i, (letter, num) in enumerate(zip(word,code)):
            if num == '0':
                if (letter in self.correct_letters.values()
                        or any(letter in possible 
                            for possible in self.wrong_place.values())):
                    return False
            elif num == '1':
                if (letter in self.wrong_letters
                        or self.correct_letters[i] == letter):
                    return False
            elif num == '2':
                if (letter in self.wrong_letters
                        or letter in self.wrong_place.get(i,[])):
                    return False
        return True

class UserGame():
    def __init__(self, answer:str):
        self.answer = answer
        self.try_number = 0
    
    def check_word(self, word: str) -> str:
        res = []
        for w, a in zip(word, self.answer):
            if a == w:
                res.append('2')
            elif w in self.answer:
                res.append('1')
            else:
                res.append('0')
        self.try_number += 1
        return ''.join(res)
    
    def try_end(self) -> bool:
        return self.try_number == 6

    def is_correct(self, word):
        if self.try_end():
            return None
        if word == self.answer:
            return 'ok'
        return self.check_word(word)
