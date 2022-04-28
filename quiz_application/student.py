import json
import random
from flask import Blueprint, flash, redirect, render_template, request
from quiz_application.auth import is_student
from quiz_application.models import Mark, Question, Subject, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user 

student = Blueprint('student', __name__)

@student.route("/enrol")
@is_student
@login_required
def show_courses(): 
    return render_template("/pages/student/courses-enrol.html", user=current_user, subjects=Subject.query.all())

@student.route("/enrol/<int:course_id>/<int:student_id>", methods=["GET","POST"])
@is_student
@login_required
def enroll_in_course(course_id, student_id):
    subjects = Subject.query.all() 
    user = User.query.get_or_404(student_id)
    subject = Subject.query.get_or_404(course_id)
    try:
        user.subjects.append(subject)
        db.session.commit()
        flash("Selected course successfully!", category='success')
        return redirect('/student')
    except:
        flash("Couldn't update subject", category="error")  
    return render_template("/pages/student/courses-enrol.html", user=current_user, subjects=subjects)
   
@student.route("/drop-course/<int:course_id>/<int:student_id>")
@is_student
@login_required
def drop_course(course_id, student_id):
    user = User.query.get_or_404(student_id)
    subject = Subject.query.get_or_404(course_id)
    try:
        user.subjects.remove(subject)
        db.session.commit()
        flash("Dropped subject successfully!", category='success')
        return redirect('/student')
    except:
        flash("Couldn't update subject", category="error")  

@student.route("/quiz", methods=["GET", "POST"])
@is_student
@login_required
def quiz():
    subjects = current_user.subjects
    questions = [] 
    total_answers = [] 
    for subject in subjects:
        for question in subject.questions:
            question_structure = {
                "id": question.id,
                "question": question.question,
                "choices": [question.choice_one, question.choice_two, question.choice_three, question.answer],
                "answer": question.answer
            }
            random.shuffle(question_structure["choices"])
            questions.append(question_structure) 

    if request.method == "POST": 
        data = request.form 
        attempts = []
        for question,attempt_answer in data.items():
            attempt_structure = {
                "question": question,
                "attempt": attempt_answer.split(",")[0],
                "correct": attempt_answer.split(",")[1]
            }
            attempts.append(attempt_structure) 

        for each_question in attempts:
            if each_question["attempt"] == each_question["correct"]:
                total_answers.append(5)
            else:
                total_answers.append(0) 
                
        total_marks = f"{sum(total_answers)} out of {len(questions) * 5}"  
        marks = Mark(total_marks=total_marks, user_id=current_user.id)
        try: 
            db.session.add(marks)
            db.session.commit()
            flash("Your quiz was submitted successfully", category='success') 
            return redirect('/student')
        except:
            flash("something went wrong!", category="error") 
            db.session.rollback()
            return redirect("/student")      
        
    return render_template("/pages/student/quiz.html", user=current_user, subjects=subjects, questions=questions)

@student.route("/results", methods=["GET", "POST"])
@is_student
@login_required
def results():
    marks = current_user.marks  
    return render_template("/pages/student/result.html", user=current_user, marks=marks)