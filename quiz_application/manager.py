from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required
from quiz_application.auth import is_manager
from quiz_application.forms import QuestionForm, SubjectForm

from quiz_application.models import Question, Subject, User 
from . import db


manager = Blueprint('manager', __name__)

@manager.route("manage-subjects")
@login_required
@is_manager
def manage_subjects():
    subjects = Subject.query.all()
    return render_template("manager/manager.html", user=current_user, subjects=subjects)

@manager.route('create-subject', methods=['GET', 'POST'])
@login_required
@is_manager
def create_subject(): 
    form = SubjectForm(request.form)
    if request.method == 'POST' and form.validate():
        subject_name = form.subject_name.data
        about = form.subject_about.data
        if not Subject.query.filter_by(name=subject_name).first():
            new_subject = Subject (name=subject_name, about=about, manager_id=current_user.id)
            db.session.add(new_subject)
            db.session.commit()
            flash("Successfully created subject!", category='success') 
            return redirect('/manager/manage-subjects')
        else:
            flash("A subject with such name already exists!", category='error')
    return render_template('/manager/create-subject.html', user=current_user, form=form)

@manager.route('update-subject/<int:id>', methods=['GET', 'POST'])
@login_required
@is_manager
def update_subject(id): 
    form = SubjectForm(request.form)
    subject_to_update = Subject.query.get_or_404(id)
    if subject_to_update.manager_id != current_user.id: 
        flash("You can only update your subject", category="error")
        return redirect("/manager/manage-subjects") 
    if request.method == 'POST' and form.validate():
        subject_to_update.name = form.subject_name.data
        subject_to_update.about = form.subject_about.data 
        try:
            db.session.commit()
            flash("Subject updated successfully!", category='success')
            return redirect('/manager/manage-subjects')
        except:
            flash("Couldn't update subject", category="error")  
    return render_template('/manager/update-subject.html', user=current_user, subject=subject_to_update, form=form)
     
@manager.route('delete-subject/<int:id>')
@login_required
@is_manager
def delete_subject(id):
    subject_to_delete = Subject.query.get_or_404(id)
    if subject_to_delete.manager_id != current_user.id:
        flash("You can only delete your subjects", category="error")
        return redirect("/manager/manage-subjects")
    try:
        db.session.delete(subject_to_delete)
        db.session.commit()
        flash("Successfully deleted!", category="success")
        return redirect("/manager/manage-subjects")
    except:
        flash("Something went wrong!", category="error")
        return redirect("manager/manage-subjects") 
        

@manager.route('/manage-questions')
@login_required
@is_manager
def manage_questions():
    questions = Question.query.all()
    return render_template("/manager/manage-questions.html", questions=questions,user=current_user)

@manager.route("create-question", methods=['GET', 'POST'])
@login_required
@is_manager
def create_question(): 
    form = QuestionForm(request.form)
    form.subjects.choices = [(subject.id, subject.name) for subject in Subject.query.all()]
    if request.method == "POST" and form.validate():
        question = form.question.data
        subject_id = form.subjects.data
        choice_one = form.choice_one.data
        choice_two = form.choice_two.data
        choice_three = form.choice_three.data
        answer = form.correct_answer.data
        if not Question.query.filter_by(question=question).first():
            new_question = Question(question=question, subject_id=subject_id, choice_one=choice_one, choice_two=choice_two, choice_three=choice_three, answer=answer, manager_id=current_user.id)
            db.session.add(new_question)
            db.session.commit()
            flash("Successfuly created the question!", category='success') 
            return redirect('/manager/manage-questions')
        else:
            flash("This question already exists!", category="error")
    return render_template("manager/create-question.html", user=current_user, form=form)

@manager.route("update-question/<int:id>", methods=['GET', 'POST'])
@login_required
@is_manager
def update_question(id): 
    question_to_update = Question.query.get_or_404(id)
    form = QuestionForm(request.form) 
    # making question's subject top on the select list
    form.subjects.choices.insert(0, (question_to_update.subject_id, question_to_update.subject.name))
    # adding rest of subjecting to the list
    for subject in Subject.query.all():
        if subject.id != question_to_update.subject_id and subject.name != question_to_update.subject.name: 
            form.subjects.choices.append((subject.id, subject.name))

    if question_to_update.manager_id != current_user.id:
            flash("You can only update your question!", category="error")
            return redirect("/manager/manage-questions")
    if request.method == "POST" and form.validate():  
        question_to_update.question = form.question.data
        question_to_update.subject_id = form.subjects.data
        question_to_update.choice_one = form.choice_one.data
        question_to_update.choice_two = form.choice_two.data
        question_to_update.choice_three = form.choice_three.data
        question_to_update.answer = form.correct_answer.data
        try: 
            db.session.commit()
            flash("Successfully updated question!", category='success') 
            return redirect('/manager/manage-questions')
        except:
            flash("something went wrong!", category="error") 
    return render_template("manager/update-question.html", question=question_to_update, user=current_user, form=form)

@manager.route("delete-question/<int:id>")
@login_required
@is_manager
def delete_question(id):
    question_to_delete = Question.query.get_or_404(id)
    if question_to_delete.manager_id != current_user.id:
        flash("You can only delete your questions", category="error")
        return redirect("/manager/manage-questions") 
    try:
        db.session.delete(question_to_delete)
        db.session.commit()
        flash("Successfully deleted!", category="success")
        return redirect('/manager/manage-questions')
    except:
        flash("Something went wrong!", category="error") 
        

@manager.route("/students-list")
@login_required
@is_manager
def see_students():
    students = User.query.filter_by(role="Student").all()
    return render_template("manager/students-list.html", user=current_user, students=students)

@manager.route("/students-list/results/<int:id>")
@login_required
@is_manager
def see_students_marks(id):
    student = User.query.get_or_404(id)
    marks = student.marks
    return render_template("manager/students-results.html", user=current_user, student=student, marks=marks)
    