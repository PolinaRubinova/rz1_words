import matplotlib.pyplot as plt

voiceless = ['п', 'ф', 'т', 'с', 'ш', 'к', 'ч', 'щ', 'ц', 'х']
voiced = ['б', 'в', 'д', 'з', 'ж', 'г', 'л', 'м', 'н', 'р', 'й']
vowels = ['а', 'о', 'и', 'е', 'ё', 'э', 'ы', 'у', 'ю', 'я']
signs = ['ь', 'ъ']


def find_let_info(let):
    if let == '': return ''
    if let in signs: return 's'
    if let.islower(): info = 'l'
    else: info = 'u'

    let_l = let.lower()
    if let_l in voiceless: info = info + ' v_s'
    elif let_l in voiced: info = info + ' v_d'
    elif let_l in vowels: info = info + ' v_l'
    return info


def pi_letter(pi_word, let):
    return len([a for a in pi_word if a.lower() == let.lower()]) / len(pi_word)


def pi_info(pi_word, pos, info):
    if pos >= len(pi_word) or info != find_let_info(pi_word[pos]): return 0
    return 1 / len(pi_word)


file = open('task_1_words.txt', 'r', encoding='utf-8')
n_Exp = int(file.readline().split(' = ')[1])
file.readline()
info_list = []

for i in range(n_Exp):
    dct = {}
    line_letter = file.readline().split(': ')

    if len(line_letter) == 2: dct['let'] = line_letter[1][1]
    else:
        dct['pos'] = int(line_letter[1]) - 1
        info_letter = ''
        for item in line_letter[2].rstrip().split(' '):
            if item == 'заглавная': info_letter = 'u'
            if item == 'строчная': info_letter = 'l'
            if item == 'знак': info_letter = info_letter + 's'
            if item == 'гласная': info_letter = info_letter + ' v_l'
            if item == 'звонкая': info_letter = info_letter + ' v_d'
            if item == 'глухая': info_letter = info_letter + ' v_s'
        dct['info'] = info_letter
    info_list.append(dct)
file.close()

list_of_words = []
with open('russian_nouns.txt', 'r', encoding='utf-8') as file:
    for line in file: list_of_words.append(line.rstrip())

plt.style.use('bmh')

# ---1a-----------------------------------------------------------------------------------------------------------------
prob = {}
for word in list_of_words: prob[word] = 1 / len(list_of_words)
possible_words = [word for word in list_of_words]
step = 0

for item in info_list:
    step += 1
    if 'let' in item:
        for word in possible_words:
            prob[word] = prob[word] * pi_letter(word, item['let'])
    else:
        for word in possible_words:
            prob[word] = prob[word] * pi_info(word, item['pos'], item['info'])

    sum_values = sum(prob.values())
    for word in possible_words: prob[word] /= sum_values

    possible_words = [word for word in possible_words if prob[word] != 0]

    if step % 2 == 1:
        fig, plot1 = plt.subplots(figsize=(11, 8), dpi=100)
        plt.title("Ряд распределения апостериорных вероятносте гипотез "
                  "- какое слово загадано №" + str(step) + "\n", fontsize=16)
        plt.xlabel('\nНомер слова')
        plt.ylabel('Вероятность\n')

        plot1.plot(list(prob.values()), color="blue")
        plt.show()

    if len(possible_words) == 1: break

# ---1b and 1с----------------------------------------------------------------------------------------------------------
possible_words = list_of_words
list_of_codes = []
best_words = {'': 0}
list_of_nums = []

for item in info_list:
    if 'let' in item:
        for word in possible_words: prob[word] = pi_letter(word, item['let'])
    else:
        for word in possible_words:
            prob[word] = pi_info(word, item['pos'], item['info'])

    sum_values = sum(prob.values())
    for word in possible_words: prob[word] /= sum_values

    possible_words = [word for word in possible_words if prob[word] != 0]
    word = max(prob, key=prob.get)

    if word in best_words:
        list_of_codes.append(best_words[word])
    else:
        best_words[word] = max(best_words.values()) + 1
        list_of_codes.append(best_words[word])

    num_of_hyps = 0
    total_prob = 0
    list_of_prob = prob.values()

    for pr in sorted(list_of_prob, reverse=True):
        num_of_hyps += 1
        total_prob += pr
        if total_prob > 0.99: break
    list_of_nums.append(num_of_hyps)

    if len(possible_words) == 1: break

# ------график 1b------
fig2, plot2 = plt.subplots(figsize=(16, 8), dpi=150)
plot2.set_yticks(range(len(best_words)))
plot2.set_yticklabels([['$' + key + '$' for key, value
                        in best_words.items() if value == i][0]
                       for i in range(len(best_words))], fontsize=15)
plot2.plot(list_of_codes, color="blue")
plot2.set_title('Эволюция изменения наиболее вероятного слова\n', fontsize=20)
plt.xlabel('\nНомер опыта', fontsize=14)
plt.show()

# ------график 1c------
fig, plot3 = plt.subplots(figsize=(10, 8), dpi=100)
plot3.plot(list_of_nums, color="blue")
plot3.set_yscale('log')
plot3.set_title('Зависимость числа превалирующих гипотез от числа проведеннных опытов\n')
plt.xlabel('\nНомер опыта')
plt.ylabel('Количество гипотез\n')
plt.show()


# ---2a and 2b----------------------------------------------------------------------------------------------------------
def symbol_at_position(word, position):
    if position < len(word): return word[position]
    return ''


prob = {}

for position in range(max([len(word) for word in list_of_words])):
    hyps = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
            'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь',
            'ы', 'ъ', 'э', 'ю', 'я']
    hyps = hyps + [x.upper() for x in hyps] + ['']

    for word in list_of_words: prob[word] = 1 / len(list_of_words)
    possible_words = list_of_words
    prob_letter = {}
    num_of_possible_letters = len(hyps)
    best_hyps = []

    for hyp in hyps: prob_letter[hyp] = sum([prob[word] for word in possible_words
                                             if symbol_at_position(word, position) == hyp])

    hyps = [h for h in hyps if prob_letter[h] != 0]
    plt.xticks(list(range(1, 1 + len(hyps))), hyps)

    for item in info_list:
        if 'let' in item:
            for word in possible_words: prob[word] = pi_letter(word, item['let'])
        else:
            for word in possible_words: prob[word] = pi_info(word, item['pos'], item['info'])

        sum_values = sum(prob.values())
        for word in possible_words: prob[word] /= sum_values

        for hyp in hyps: prob_letter[hyp] = sum([prob[word] for word in possible_words
                                                 if symbol_at_position(word, position) == hyp])

        possible_words = [word for word in possible_words if prob[word] != 0]
        best_hyps.append(hyps.index(max(prob_letter, key=prob_letter.get)))

        if len([x for x in prob_letter.values() if x != 0]) / num_of_possible_letters < 0.6:
            plt.bar(list(range(1, len(hyps) + 1)), [prob_letter[let] for let in hyps])
            num_of_possible_letters = len([x for x in prob_letter.values() if x != 0])

        if len(possible_words) == 1 or num_of_possible_letters == 1: break

    # ------график 2a------
    plt.title(str(position + 1) + ' позиция символа в слове ')
    plt.ylabel('Вероятность')
    plt.show()

    # ------график 2b------
    fig, plot5 = plt.subplots(figsize=(5, 7), dpi=100)
    plot5.plot(best_hyps, color='blue')
    plt.yticks(list(range(0, len(hyps))), hyps)
    plt.title('Наиболее вероятная гипотеза на ' + str(position + 1) + ' шаге')
    plt.xlabel('\nНомер опыта')
    plt.show()
    if prob_letter[''] == 1: break

# ---3a-----------------------------------------------------------------------------------------------------------------
fr_letters = {}
types_of_letters = {}

for item in info_list:
    if 'let' in item:
        if item['let'] in fr_letters: fr_letters[item['let']] += 1
        else: fr_letters[item['let']] = 1
    else: types_of_letters[item['pos']] = item['info']

print('\nЭкспериментальный профиль:')
frequency = {}
sum_of_values = sum(fr_letters.values())
for el in fr_letters:
    frequency[el] = fr_letters[el] / sum_of_values
print(frequency)

plt.xticks(list(range(1, len(frequency) + 1)),
           [let for let in frequency.keys()])
plt.bar(list(range(1, len(frequency) + 1)),
        [let for let in frequency.values()], color='blue')
plt.title('Частота сообщаемых символов')
plt.ylabel('Частота\n')
plt.show()

# ---3b-----------------------------------------------------------------------------------------------------------------
for word in list_of_words:
    letters = [word[i] for i in range(len(word))]
    types = {}
    for i in range(len(letters)): types[i] = find_let_info(letters[i])

    check = types == types_of_letters

    for let in frequency:
        if len([x for x in letters if x.lower() == let]) != frequency[let]:
            check = False
            break
    if check: print('\nСлово: ' + str(word) + '\n')

# ---3d-----------------------------------------------------------------------------------------------------------------
list_of_letters = []
for i in range(n_Exp + 1):
    fr_letters = {l: 0 for l in list_of_letters}
    types_of_letters = {}

    for item in info_list[:i]:
        if 'let' in item:
            if item['let'] in fr_letters: fr_letters[item['let']] += 1
            else:
                fr_letters[item['let']] = 1
                list_of_letters.append(item['let'])
        else: types_of_letters[item['pos']] = item['info']

    if i == 1 or i == 10 or i == 100 or i == 1000 or i == 10000:
        plt.bar(list(range(1, len(fr_letters) + 1)),
                [fr_letters[let] for let in list_of_letters], color='blue')
        plt.xticks(list(range(1, len(fr_letters) + 1)),
                   [let for let in list_of_letters])
        plt.title('Экперимент №' + str(i))
        plt.ylabel('Количество опытов')
        plt.show()
