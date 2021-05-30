import requests
import random
import html



def call_trivia_api(category):
    """getting data from Trivia Api by user selected category"""
    try:
        response  =  requests.get("https://opentdb.com/api.php", params={
                                                                          "amount"  : "10",
                                                                          "category": category,
                                                                          "type"    : "multiple",
                                                                         })
        trivia_api_questions_data = response.json()["results"]
    except Exception as e:
        trivia_api_questions_data = "Maximum Limit Reached Please try again"
    return trivia_api_questions_data



def format_api_data(api_data):
    """this will format api data"""
    quiz_questions = [] # this will store Quiz Questions from Trivia API
    for each_question in api_data:
          options =  [
                        html.unescape(each_question["correct_answer"]),
                        html.unescape(each_question["incorrect_answers"][0]),
                        html.unescape(each_question["incorrect_answers"][1]),
                        html.unescape(each_question["incorrect_answers"][2])
                     ]

          # shuffling each answer by using shuffle method from random module
          random.shuffle(options)

          # adding question,correct_answer,options to quiz_questions list
          quiz_questions.append(
                {
                  'question'      : html.unescape(each_question["question"]),
                  'correct_answer': html.unescape(each_question["correct_answer"]),
                  'options'       : options,
                  'user_answer'   : '',
                }
             )
    return quiz_questions
