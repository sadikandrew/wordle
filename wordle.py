from typing import Tuple, List


def readDict() -> list:
	with open("./englishDict.txt") as f:
		words = []
		for line in f:
			line = line.strip("\n").strip(" ")
			words.append(line)
	return words


def wordPrompt(tries: int, numlet: int) -> str:
	return input("\t\t{:d}: Enter a {:d}-letter word:\n".format(tries+1, numlet)).lower()


def chkLtr(char: str, truth: str, used: set) -> str:
	if char in used:
		if char in truth:
			return "✓"
		else:
			return "x"
	else:
		return " "


def countWordChars(truth) -> dict:
	my_dict = dict()
	for char in truth:
		if char in my_dict.keys():
			my_dict[char] += 1
		else:
			my_dict[char] = 1
	return my_dict


def isWord(guess: str, truth: str, sign: str) -> Tuple[bool, str]:
	# The old logic does account for mulitples of the same letter
	# i.e. if the word was 'moist', which has 1 s, then something like
	# 'mossy' should have ✓✓x✓x, not ✓✓~✓x, because the 1 s is already there
	# similarly, if the word was 'sunny' and we guessed mossy, we should get xx~x✓

	char_count = countWordChars(truth)
	# annoying thing about this logic is u have to check for checkmarks first,
	res = [""] * len(guess)
	for idx in range(len(guess)):
		if guess[idx] == truth[idx]:
			res[idx] = "✓"
			char_count[guess[idx]] -= 1
	for idx in range(len(guess)):
		if guess[idx] in truth and char_count[guess[idx]] >= 1:
			res[idx] = "~"
			char_count[guess[idx]] -= 1
		elif res[idx] == "":
			res[idx] = "x"

	res = "".join(res)
	print(res)
	sign += res + '\n'
	return guess == truth, sign


def printKeys(used: set, truth: str, words_guessed: List[str], signature: str) -> None:
	signs = signature.rstrip("\n").split("\n")
	alphabet = ["abcdefghijklm", "nopqrstuvwxyz"]
	for i, halfAlpha in enumerate(alphabet):
		print("\t\t"+halfAlpha, end="")
		if i*2 < len(words_guessed):
			print("\t\t{:s}\t{:s}".format(words_guessed[i*2], signs[i*2]), end="")
		print("\n\t\t", end="")
		for char in halfAlpha:
			print(chkLtr(char, truth, used), end="")
		if i*2 + 1 < len(words_guessed):
			print("\t\t{:s}\t{:s}".format(words_guessed[i*2 + 1], signs[i*2 + 1]), end="")
		print()
	i = len(alphabet)*2
	while i < len(words_guessed):
		print("\t\t" + (" "*len(alphabet[0])) + "\t\t{:s}\t{:s}".format(words_guessed[i], signs[i]))
		i += 1


def main() -> None:
	from random import randint
	from random import seed
	from time import time
	words = readDict()

	while input("\t\t"+"Enter 'yes' to play:\n\t\t") == 'yes':

		numlet = 1
		while numlet <= 2 or numlet >= 9:
			try:
				numlet = int(input('\t\tNum of letters to use? (between 3 and 8)\n\t\t'))
			except ValueError:
				print('\t\tThe number of letters must be an integer')
		subwords = [word for word in words if len(word) == numlet]
		num_tries = 11 - numlet
		print("\t\tYou have {:d} guesses, good luck".format(num_tries))

		randWord = subwords[randint(0, len(subwords)-1)]
		# seed(time() // 3600)  # gives the same word every time
		usedLtrs = set([])
		signature = ""

		words_guessed = []

		for tries in range(num_tries):
			word = wordPrompt(tries, numlet)
			while len(word) != numlet or word not in subwords or word in words_guessed:
				if len(word) != numlet:
					print("\t\t" + "Wrong Length, Try again.")
				elif word in words_guessed:
					print("\t\t" + "You already guessed that.")
				else:
					print("\t\t" + "Idk this word, Try again.")
				printKeys(usedLtrs, randWord, words_guessed, signature)
				word = wordPrompt(tries, numlet)
			isWon, signature = isWord(word, randWord, signature)
			if isWon:
				print("YOU DID IT! CONGRATS")
				break
			for ltr in list(word):
				usedLtrs.add(ltr)
			words_guessed.append(word)
			printKeys(usedLtrs, randWord, words_guessed, signature)
			if tries == num_tries - 1:
				print("LOSER!! HA!")

		print("The word was: " + randWord)
		print("\n\n" + signature)

	print("Goodbye!")


if __name__ == "__main__":
	main()
