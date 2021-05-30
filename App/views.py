from json import dumps,loads
from App.models import Quiz
from django.shortcuts import render,redirect,HttpResponse
from App.trivia.trivia_api  import call_trivia_api,format_api_data
from django.contrib.auth.decorators import login_required


final_score     = 0   # this will store user score
quiz_questions  = ''  # this will store Quiz Questions from Trivia API
category        = ''  # this will store category selected by the user
time            = 0   # this will store how many time taken by user to complete the quiz

def format_time(time):
	"""it will format time like (71 --> 1:11(1 minute 11 seconds))"""
	if time > 60:
		minute  = time // 60
		seconds = time % 60
		if seconds < 10:
			seconds = f"{seconds}0"
		time    = f"{minute}:{seconds}({minute} minute {seconds} seconds)"
	else:
		time    = f"{time} seconds"
	return time


@login_required
def home(request):
	"""this function will render Quiz Landing Page"""
	return render(request, "App/home.html")


@login_required
def quiz_page(request):
	"""this function will start Quiz
							-------------------------------------------
		1) User will select a category in Landing Page(by using POST method "saving category as a variable")
		2) call the call_trivia_api() method with category as a argument
		3) call_trivia_api() method will do a API Call to opentdb.com(which is Trivia API website)
		4) Finally call_trivia_api() method will return a dictionary(which contains Quiz Questions)
		   and save to a variable named as 'api_data'
        						-------------------------------------------
		5) call format_api_data() method with 'api_data' as a argument
		6) format_api_data() method will format the 'api_data'(which contains Quiz Questions)
		   and save it to a variable named as quiz_questions
        						-------------------------------------------
		7) call dumps() method with quiz_questions as a argument
		8) Finally dumps() method will convert quiz_questions into JSON
								-------------------------------------------
		9) Finally rendering the "quiz.html" page (that contains data as a context)

	"""
	if request.method == "POST":
		global quiz_questions,category
		category 			=   request.POST['category']
		api_data 			=   call_trivia_api(category)

		# checking for maximum limit --> if False --> format_api_data() & dumps()
		if type(api_data ) != str:
			quiz_questions 		=   format_api_data(api_data)
			data 				=   dumps(quiz_questions)
		# checking for maximum limit --> if TRUE --> display "Maximum Limit Reached Please try again"
		else:
			data = api_data

		return render(request, "App/quiz.html", {"quiz_questions": data})
	else:
		return redirect("home")


@login_required
def save_to_database(request):
	"""this function will save user_answers & Score to database"""
	if request.method == 'GET':
		global final_score,time
		final_score  =  int(request.GET['score'])             # this will store 'score'
		time         =  format_time(int(request.GET['time'])) # getting the time and calling format_time method
		answers_list =  loads(request.GET['user_answers'])    # this will store all answers in a list & converting JSON to python using loads()

		user_answers_string = ''
		# adding each_answer to the quiz_questions dictionary & to a string(which is user_answers_string)
		for each_answer in range(len(answers_list)):
			quiz_questions[each_answer]["user_answer"] = quiz_questions[each_answer]["options"][answers_list[each_answer]]
			user_answers_string                       += quiz_questions[each_answer]["options"][answers_list[each_answer]]

			if (each_answer+1)  != len(answers_list):
				user_answers_string += '*'

		# Saving Score,time_taken,user_answers_string etc to database
		Quiz(
		    manager         =   request.user,
			trivia_api_link =   f"https://opentdb.com/api.php?amount=10&category={category}&type=multiple",
			score           =   final_score,
			time_taken      =   time,
			user_answers    =   user_answers_string
			).save()
		return redirect('result')


@login_required
def result(request):
	"""this function will render result page (which contains final score,time_taken etc)"""
	return render(request, "App/result.html", {"questions": quiz_questions,"score":final_score,"time":time})


@login_required
def dashboard(request):
	"""this function will render Dashboard Page (which contains all played quiz information)"""
	quiz_query_set = Quiz.objects.filter(manager=request.user).order_by('-id')
	return render(request, "App/dashboard.html", {"quiz_query_set": quiz_query_set})
