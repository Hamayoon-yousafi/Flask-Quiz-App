import re
from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required
from quiz_application.auth import is_manager

from quiz_application.models import Question, Subject, User 
from . import db


manager = Blueprint('manager', __name__)

@manager.route('/create-subject', methods=['GET', 'POST'])
@login_required
@is_manager
def create_subject(): 
    if request.method == 'POST':
        subject_name = request.form.get('name')
        about = request.form.get('about')
        new_subject = Subject (name=subject_name, about=about)
        db.session.add(new_subject)
        db.session.commit()
        flash("Success!", category='success') 
        return redirect('/manager')
    return render_template('/pages/manager/create-subject.html', user=current_user)

@manager.route('/update-subject/<int:id>', methods=['GET', 'POST'])
@login_required
@is_manager
def update_subject(id): 
    if request.method == 'POST':
        subject_to_update = Subject.query.get_or_404(id)
        subject_to_update.name = request.form.get('name')
        subject_to_update.about = request.form.get('about')
        try:
            db.session.commit()
            flash("Subject updated successfully!", category='success')
            return redirect('/manager')
        except:
            flash("Couldn't update subject", category="error") 
        return redirect('/manager')
    return render_template('/pages/manager/update-subject.html', user=current_user, subject=subject_to_update)
     
@manager.route('/delete-subject/<int:id>')
@login_required
@is_manager
def delete_subject(id): 
    try:
        subject_to_delete = Subject.query.get_or_404(id)
        db.session.delete(subject_to_delete)
        db.session.commit()
        flash("Successfully deleted!", category="success")
        return redirect('/manager')
    except:
        flash("Something went wrong!", category="error")

@manager.route('/manage-questions')
@login_required
@is_manager
def manage_questions():
    questions = Question.query.all()
    return render_template("/pages/manager/manage-questions.html", questions=questions,user=current_user)

@manager.route("/create-question", methods=['GET', 'POST'])
@login_required
@is_manager
def create_question():
    subjects = Subject.query.all()
    if request.method == "POST":
        question = request.form['question']
        subject_id = request.form['subject_id']
        choice_one = request.form['choice_one']
        choice_two = request.form['choice_two']
        choice_three = request.form['choice_three']
        answer = request.form['correct_answer']
        new_question = Question(question=question, subject_id=subject_id, choice_one=choice_one, choice_two=choice_two, choice_three=choice_three, answer=answer)
        db.session.add(new_question)
        db.session.commit()
        flash("Successfuly created the questoin!", category='success') 
        return redirect('/manage-questions')
    return render_template("pages/manager/create-question.html", subjects=subjects, user=current_user)

@manager.route("/update-question/<int:id>", methods=['GET', 'POST'])
@login_required
@is_manager
def update_question(id):
    subjects = Subject.query.all()
    question_to_update = Question.query.get_or_404(id)
    if request.method == "POST":
        question_to_update.question = request.form['question']
        question_to_update.subject_id = request.form['subject_id']
        question_to_update.choice_one = request.form['choice_one']
        question_to_update.choice_two = request.form['choice_two']
        question_to_update.choice_three = request.form['choice_three']
        question_to_update.answer = request.form['correct_answer']
        try: 
            db.session.commit()
            flash("Successfully updated question!", category='success') 
            return redirect('/manage-questions')
        except:
            flash("something went wrong!", category="error")
    return render_template("pages/manager/update-question.html", question=question_to_update , subjects=subjects, user=current_user)

@manager.route("/delete-question/<int:id>")
@login_required
@is_manager
def delete_question(id):
    try:
        question_to_delete = Question.query.get_or_404(id)
        db.session.delete(question_to_delete)
        db.session.commit()
        flash("Successfully deleted!", category="success")
        return redirect('/manage-questions')
    except:
        flash("Something went wrong!", category="error")

@manager.route("/students-list")
@login_required
@is_manager
def see_students():
    students = User.query.filter_by(role="Student").all()
    return render_template("/pages/manager/students-list.html", user=current_user, students=students)

@manager.route("/students-list/results/<int:id>")
@login_required
@is_manager
def see_students_marks(id):
    student = User.query.get_or_404(id)
    marks = student.marks
    return render_template("pages/manager/students-results.html", user=current_user, student=student, marks=marks)
    