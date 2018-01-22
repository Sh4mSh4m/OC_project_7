#! /usr/bin/env python
import json
import codecs

msg = """La phrase1 avec stuff. Une phrase2 du stuff. La blabla et 
         la question1 ? Le blabla et sa question2 ? Une phrase3 and more."""
parserDictionnary = json.load(codecs.open("grandpyapp/parserDictionnary.json",
                                          "r", "utf-8-sig"))


def stripStopWords(phrases):
    """
    Input is list
    Eliminates all the stop words from the phrases
    Returns a list of lists
    """
    cleanWordArrays = []
    for phrase in phrases:
        if len(phrase) is not 0:
            words = phrase.split()
            result = ([word for word in words if word not in 
                       parserDictionnary['stopWords']])
            if len(result) is not 0:
                cleanWordArrays.append(result)
    return cleanWordArrays


def sentencesProc(lstSentences, msgResponse):
    """
    Inputs lists of strings and dictionnary
    Builds the json reponse by appending strings to json entry,
    depending on words encountered in the msg input from client
    Returns the dictionnary updated
    """
    wordArrays = stripStopWords(lstSentences)
    for wordArray in wordArrays:
        for word in wordArray:
            if word in parserDictionnary['salutations']:
                msgResponse['interaction'] += "Salut mec. "
            elif word in parserDictionnary['insults']:
                msgResponse['interaction'] += "S'toi le "+ word+ ". "
            elif word == "appelle":
                index = wordArray.index(word)
                prenom = (wordArray[index + 1]).capitalize()
                if prenom == "Hieu":
                    msgResponse['interaction'] += "Hey Bogoss. OKLM"
                else:
                    msgResponse['interaction'] += "Enchanté "
                                                   + prenom + ". "
    return msgResponse


def questionsProc(lstQuestions, msgResponse):
    """
    Inputs lists of strings and dictionnary
    Builds the json response by appending strings to json entry
    Depending on the type of questions, it may retrieve key words to
    request APIs
    Returns the dictionnary updated
    """
    wordArrays = stripStopWords(lstQuestions)
    for wordArray in wordArrays:
        for locationAnchor in parserDictionnary['locationAnchor']:
            if locationAnchor in wordArray:
                index = wordArray.index(locationAnchor)
                for i in range(index+1, len(wordArray)):
                    msgResponse['keyWord'] += wordArray[i] + " "
#        LATER UPGRADE
#        for questionAnchor in parserDictionnary['questionAnchor']:
#            if questionAnchor in wordArray:
#                index = wordArray.index(questionAnchor)
#                msgResponse['complement'] += "Sinon check "
#                for i in range(index, len(wordArray)+1):
#                    msgResponse['complement'] += wordArray[i] + " "
    return msgResponse


def msgParser(msg):
    """
    Input is a string as input and returns:
    - a list of sentences
    - and a list  questions
    Returns dictionnary with two keys and lists as values
    """
    sentences = []
    sentences.append(msg.lower())
    questions = []
    punctuation = parserDictionnary['punctuation']

    for p in punctuation:
        if p is not "?":
            for sentence in sentences:
                if p in sentence:
                    sentences.remove(sentence)
                    sentences += sentence.split(p)
        else:
            for sentence in sentences:
                if p in sentence:
                    sentences.remove(sentence)
                    results = sentence.split(p)
                    len_results = len(results)
                    for k in (range(len_results-1)):
                        questions.append(results[k])
                    sentences.append(results[-1])
    parsedBatch = {'sentences': sentences, 'questions': questions}
    return parsedBatch


def msgProcessor(parsedBatch):
    """
    Input: dictionnary of sentences and questions which are lists
    Returns a JSON object
    """
    msgResponse = {'interaction': "",
                   'complement': "",
                   'keyWord': "",
                   'response': ""}
    msgResponse = sentencesProc(parsedBatch['sentences'], msgResponse)
    msgResponse = questionsProc(parsedBatch['questions'], msgResponse)
    return msgResponse


def main():
    msgProcessor(msgParser(msg))

if __name__ == "__main__":
    main()
