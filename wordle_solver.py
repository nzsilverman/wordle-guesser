import argparse
import re

def get_starting_word_list(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f]

def pick_best_word(word_list):
    print(f"len(word_list): {len(word_list)}")
    return word_list[0]

def is_input_valid(grade):
    if len(grade) != 5:
        return False

    valid_set = set(('x', '!', '?'))
    if not set(grade).issubset(valid_set):
        return False

    return True

def filter_word_list(word_list, grade, guess):
    word_list.remove(guess)

    exclude=[]
    letter_in_wrong_spot_list = [] # Contains tuples of (idx, letter)
    letter_in_correct_spot_str = ""

    for idx, char in enumerate(grade):
        if char == 'x':
            print(f"adding guess[{idx}] to exclude: {guess[idx]}")
            exclude.append(guess[idx])
            letter_in_correct_spot_str += "."
        elif char == '!':
            letter_in_correct_spot_str += guess[idx]
        elif char == '?':
            letter_in_wrong_spot_list.append((idx, guess[idx]))
            letter_in_correct_spot_str += "."

    letters_that_must_be_present = [x[1] for x in letter_in_wrong_spot_list]

    # Filter out letters from exclude that must be present and were incorrectly marked when building list
    exclude = [x for x in exclude if x not in letters_that_must_be_present]
    exclude = [x for x in exclude if x not in letter_in_correct_spot_str]

    # Special cases of letters repeating but being marked as an x
    guess_idx_with_wrong_letters = [idx for idx,letter in enumerate(guess) if (letter in letters_that_must_be_present or letter in letter_in_correct_spot_str) and grade[idx]=='x']
    print(f"guess_idx_with_wrong_letters: {guess_idx_with_wrong_letters}")
    for idx in guess_idx_with_wrong_letters:
        wrong_spot_str = idx*'.' + guess[idx]
        wrong_spot_regex = re.compile(wrong_spot_str)
        word_list = list(filter(lambda x: not wrong_spot_regex.match(x), word_list))

    print(f"exclude: {exclude}")
    print(f"letter_in_wrong_spot_list: {letter_in_wrong_spot_list}")
    print(f"letter_in_correct_spot_str: {letter_in_correct_spot_str}")

    if 'x' in grade and exclude:
        exclude_regex = re.compile("[" + ''.join(exclude) + "]")
        print("word list lenght before exclude: {}".format(len(word_list)))
        word_list = list(filter(lambda x: not exclude_regex.search(x), word_list))
        print("word list lenght after exclude: {}".format(len(word_list)))
        # print(word_list)

    if '?' in grade:
        print(letters_that_must_be_present)
        for idx, letter in letter_in_wrong_spot_list:
            # Filter out all words that have a letter in the wrong spot
            wrong_spot_str = idx*'.' + letter
            print('wrong_spot_str: ' + wrong_spot_str)
            wrong_spot_regex = re.compile(wrong_spot_str)
            word_list = list(filter(lambda x: not wrong_spot_regex.match(x), word_list))

            # Filter out all words that do not contain the letter thats in the wrong spot
            count = letters_that_must_be_present.count(letter)
            query_str = "[" + letter + "]" + "{" + str(count) + "}"
            print("query_str: " + query_str)
            word_must_contain_letter_in_wrong_spot_regex = re.compile(query_str)
            word_list = list(filter(word_must_contain_letter_in_wrong_spot_regex.search, word_list))

    if '!' in grade:
        correct_spot_regex = re.compile(letter_in_correct_spot_str)
        word_list = list(filter(correct_spot_regex.match, word_list))

    return word_list

def main():
    parser = argparse.ArgumentParser(description="Interactively help you solve the wordle puzzle")
    parser.add_argument('--word-list', default="words.txt")
    args = parser.parse_args()

    print("\n*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#\n")
    print("Welcome to the Wordle solver!")
    print("\n*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#\n")
    print("Instructions:")
    print("\tGuess the word I supply into the wordle game.")
    print("\tAfter guessing, tell me how the guess did by entering 5 characters in a row.")
    print("\t\t- \"WIN\" if you won. Congrats!")
    print("\t\t- \"invalid\" if the word is rejected by the wordle software.")
    print("\t\t- Use a \'x\' to represent that a character is not used (i.e. grayed out)")
    print("\t\t- Use a \'?\' to represent that a character is used and in the incorrect spot (i.e. yellow)")
    print("\t\t- Use a \'!\' to represent that a character is used and in the correct spot (i.e. green)")
    print("\tAs an example, if the solution is CRANE and the guess was SLATE, enter: \"xx!x!\"")
    print("")

    word_list = get_starting_word_list(args.word_list)

    i = 1
    while True:
        word_to_pick = pick_best_word(word_list)
        print(f"Guess #{i}:\t\"{word_to_pick}\"")
        invalid_found = False
        while True:
            grade = input("How did that guess do? ")
            if grade == 'WIN':
                print("\nYay! Congrats you won!!!")
                return
            elif grade == "invalid":
                invalid_found = True
                break
            elif not is_input_valid(grade):
                print("Uh Oh! That is not a valid input. Please try entering that again.")
            else:
                break

        if not invalid_found:
            word_list = filter_word_list(word_list, grade, word_to_pick)
            i += 1
        else:
            word_list.remove(word_to_pick)

if __name__ == '__main__':
    main()
