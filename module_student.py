from flask_app import app, db, Classroom, Teacher, Student, Activity, Question, HelpingHand, HelpingHandLog
from flask_login import current_user, login_required
from flask import redirect, render_template, url_for, request, flash

from functools import wraps
from datetime import datetime

################################################################################
# Definition of student accesses to helping-hands
# Each app.route should use a login verification
# @login_required
################################################################################

@app.route("/student/", methods=["GET", "POST"])
@login_required
def student():
    template_html = "student/index.html"
    return render_template(
        template_html
    )


@app.route("/student/link-to-teacher/", methods=["GET", "POST"])
@login_required
def link_to_teacher():
    template_html = "student/link_to_teacher.html"

    if request.method == "GET":
        return render_template(template_html)

    if current_user.admin:
        flash('Ne fonctionne que pour les élèves')
        return redirect('/student/')

    teacher_username = request.form["teacher_username"]
    teacher = Teacher.query.filter_by(username=teacher_username).first()
    if teacher is None:
        flash("Le professeur demandé n'existe pas !")
        return render_template(template_html)
    if current_user in teacher.students:
        flash(f"Vous vous êtes déjà signalé à {teacher.name} {teacher.surname} !")
        return render_template(template_html)

    teacher.students.append(current_user)
    db.session.commit()

    flash(f"Vous vous êtes bien signalé à {teacher.name} {teacher.surname}")
    return redirect(url_for('student'))


@app.route("/student/show-helping-hand/<classroom_id>/<activity_id>/<question_id>/<helping_hand_id>/")
@login_required
def show_helping_hand(classroom_id, activity_id, question_id, helping_hand_id):
    classroom = Classroom.query.filter_by(id=classroom_id).first()
    if (classroom is None) or (not classroom in current_user.classrooms):
        flash("Classe non accessible")
        return redirect(url_for('student'))
    # check if access to activity
    activity = Activity.query.filter_by(id=activity_id).first()
    if (activity is None) or (not activity in classroom.activities):
        flash("Activité non diponible")
        return redirect(url_for('student'))
    question = Question.query.filter_by(id=question_id).first()
    if (question is None) or (not question in activity.questions):
        flash("Question non diponible")
        return redirect(url_for('student'))
    helping_hand = HelpingHand.query.filter_by(id=helping_hand_id).first()
    if (helping_hand is None) or (not helping_hand in question.helping_hands):
        flash("Coup de pouce non diponible")
        return redirect(url_for('student'))

    # log the access (only if student, if admin -> corresponds to a teacher testing its activities)
    if not current_user.admin:
        log = HelpingHandLog(
            timestamp=datetime.now(),
            helping_hand=helping_hand,
            student=current_user
        )
        db.session.add(log)
        db.session.commit()
    template_html = "student/show_helping_hand.html"

    return render_template(
        template_html,
        activity=activity,
        question=question,
        helping_hand=helping_hand,
        classroom=classroom
    )

@app.route("/student/access-activity/<classroom_id>/<activity_id>/")
@login_required
def access_activity(classroom_id, activity_id):
    classroom = Classroom.query.filter_by(id=classroom_id).first()
    if (classroom is None) or (not classroom in current_user.classrooms):
        flash("Classe non accessible")
        return redirect(url_for('student'))
    # check if access to activity
    activity = Activity.query.filter_by(id=activity_id).first()
    if (activity is None) or (not activity in classroom.activities):
        flash("Activité non diponible")
        return redirect(url_for('student'))

    template_html = "student/access_activity.html"
    return render_template(
        template_html,
        activity=activity,
        classroom=classroom
    )