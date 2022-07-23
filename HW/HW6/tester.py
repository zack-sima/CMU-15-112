def handInWord(word, hand): #helper-fn
    for i in word:
        if hand.count(i) < word.count(i):
            return False
    return True
def calculateScore(word, letterScores):
    score = 0
    for char in word:
        score += letterScores[ord(char.lower()) - ord("a")]
    return score

def bestScrabbleScore(dictionary, letterScores, hand):
    highestScore = 0
    bestWords = []
    for word in dictionary:
        if handInWord(list(word), hand):
            score = calculateScore(word, letterScores)
            if score >= highestScore:
                if score > highestScore:
                    highestScore = score
                    bestWords = [word]
                else:
                    bestWords.append(word)

    if highestScore == 0:
        return None
    if len(bestWords) == 1:
        return (bestWords[0], highestScore)
    else:
        return (bestWords, highestScore)

print(bestScrabbleScore(["a", "b", "c"], [1] * 26, list("ace")))