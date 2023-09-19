from flask import Flask, render_template, request, redirect, url_for, flash, session 
from flask_debugtoolbar import DebugToolbarExtension 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flask-survey-key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

app.secret_key = app.config['SECRET_KEY']
app.config['SESSION_TYPE'] = 'filesystem'

responses = session.get('responses', []) #retrieve the list from the session 
responses.append("User's response") #append the new response to the list 
session['responses']= responses #rebind thee name in the session to the modified list 

from surveys import Survey
from surveys import satisfaction_survey


@app.route('/')
def index():
    return render_template(
        'survey.html',
        title= satisfaction_survey.title,
        instructions= satisfaction_survey.instructions,
        button_text= "Start Survey",
        next_question= 0
    )

@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def question(question_number):
     total_questions = len(satisfaction_survey.questions)

     if question_number == total_questions: # redirect to thank-you page if all questions have been answered 
        return redirect('/thank-you')

    # check if the question number is out of bounds 
    if question_number < 0 or question_number >= total_questions:
        flash("Invalid question number. Redirected to the first question.")
        return redirect('/questions/0') # redirect to the first question if the question number is out of bounds 

    if request.method == 'POST':
        response = request.form.get('response')
        responses.append(response)

    
    question_text = satisfaction_survey.questions[question_number].question
    choices = satisfaction_survey.questions[question_number].choices

    return render_template(
        'survey.html',
        title=satisfaction_survey.title,
        instructions= question_text,
        button_text="Next Question",
        next_question= question_number + 1,
        choices= choices
    )


@app.route('/thank-you')
def thank_you():
    return "Thank you for completing the survey!"