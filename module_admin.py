from flask_app import app, db, Classroom, Teacher, Student, Activity, Question, HelpingHand, HelpingHandLog, send_confirmation_email
from flask_login import current_user
from flask import redirect, render_template, url_for, request, flash
from werkzeug.security import generate_password_hash
import sqlalchemy

from functools import wraps
import random

################################################################################
# Definition of administration tools
# Each app.route should use a login + admin verification
# use @admin_required
################################################################################

def admin_required(f, *args, **kwargs):
    @wraps(f) # to keep the name and docstring
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            # logged in
            if current_user.admin:
                return f(*args, **kwargs)
        return redirect(url_for('login'))
    return wrapper


@app.route("/admin/flash-msg/<msg>/", methods=["GET", "POST"])
@admin_required
def admin_flash_msg(msg):
    flash(msg)
    return redirect(url_for('admin'))


@app.route("/admin/", methods=["GET", "POST"])
@admin_required
def admin():
    template_html = "admin/index.html"
    # get all students in classrooms
    #classrooms = Classroom.query.filter_by(owner=current_user).all()
    #classrooms = current_user.teacherclassrooms
    return render_template(
        template_html,
        Student=Student,
        Activity=Activity
    )


@app.route("/admin/create-multi-account/", methods=["GET", "POST"])
@admin_required
def create_multi_account():
    template_html = "admin/create_multi_account.html"
    if 'text' in request.args:
        text = request.args['text']
    else:
        text=''
    if request.method == "GET":
        return render_template(template_html, text=text)

    # method == "POST"
    text = request.form['text']
    text = text.replace('\r\n','\n').replace('\t', ', ').strip()
    text_list = text.split('\n') # now a list
    # quick and dirty verification of the content
    try:
        for line in text_list:
            line = line.replace('\t', ',')
            (name, surname, email) = line.split(',')
            if not '@' in email and Student.query.filter_by(email=email).first() is None and Student.query.filter_by(username=email).first() is None:
                raise ValueError('Email should have an @')
    except ValueError:
        flash('Erreur dans la liste des élèves')
        return redirect(f'/admin/create-multi-account/?text={text}')
    # the content should be ok
    for line in text_list:
        line = line.replace('\t', ',')
        (name, surname, email) = line.split(',')

        email = email.lstrip().strip()
        name = name.lstrip().strip()
        surname = surname.lstrip().strip()

        teacher = Teacher.query.filter_by(email=email).first()
        student = Student.query.filter_by(email=email).first()
        if teacher:
            flash(f"L'adresse email {email} est déjà enregistrée pour un professeur.")
        elif student:
            try:
                current_user.students.append(student)
            except sqlalchemy.exc.InvalidRequestError:
                pass
            flash(f"L'adresse email {email} est déjà enregistrée, l'élève est ajouté à vos élèves.")
        else:
            try:
                student = Student(
                    username=email,
                    email=email,
                    name=name,
                    surname=surname,
                    password_hash=generate_password_hash(str(random.random())),
                    email_confirmed=False,
                    teachers=[current_user]
                )
                db.session.add(student)
                current_user.students.append(student)
                #send_confirmation_email(email) # bug if email is sent...
                flash(f'Compte créé pour {name} {surname}.')
            except Exception as e:
                print('Multiple account creation error', e)
                flash(f"Erreur inconnue pour {name} {surname}")
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/admin/remove-student/<student_id>/", methods=["POST"])
@admin_required
def remove_student(student_id):
    #student_username = request.form["student_username"]
    student = Student.query.filter_by(id=student_id).first()
    if student is None or student not in current_user.students:
        flash("L'élève ne fait pas partie de vos élèves.")
        return redirect(url_for('admin'))
    # delete student from classes

    current_user.students.remove(student)
    db.session.commit()
    flash(f"L'élève {student.name} {student.surname} a été enlevé de vos élèves")
    return redirect(url_for('admin'))


@app.route("/admin/link-student/", methods=["POST"])
@admin_required
def link_student():
    student_username = request.form["student_username"]
    student = Student.query.filter_by(username=student_username).first()
    if student is None:
        flash("L'élève demandé n'existe pas !")
        return redirect(url_for('admin'))

    #if StudentTeacher.query.filter_by(teacher=current_user, student=student).first() is not None:
    if student in current_user.students:
        flash(f"L'élève demandé est déjà présent dans vos élèves !")
        return redirect(url_for('admin'))

    current_user.students.append(student)
    db.session.commit()

    flash(f"Vous avez bien ajouté {student.name} {student.surname} à vos élèves. Vous pouvez maintenant l'ajouter dans une de vos classe.")
    return redirect(url_for('admin'))


@app.route("/admin/view-student-logs/<id>/")
@admin_required
def view_student_logs(id):
    template_html = "/admin/view_student_log.html"

    # check if access to student
    student = Student.query.filter_by(id=id).first()
    if (student is None) or (student not in current_user.students):
        flash("Élève non existant")
        return redirect(url_for('admin'))

    return render_template(
        template_html,
        student=student
    )

@app.route("/admin/view-activity-logs/<activity_id>/")
@admin_required
def view_activity_logs(activity_id):
    template_html = "/admin/view_activity_log.html"

    # check if access to activity
    activity = Activity.query.filter_by(id=activity_id).first()
    if (activity is None) or (activity not in current_user.activities):
        flash("Activité non existante")
        return redirect(url_for('admin'))

    return render_template(
        template_html,
        activity=activity
    )

@app.route("/admin/edit-helping-hand/<id>/", methods=["GET", "POST"])
@admin_required
def edit_helping_hand(id):
    template_html = "admin/edit_helping_hand.html"

    activity = Activity.query.filter_by(id=id).first()
    if (activity is None) or (activity not in current_user.activities):
        flash("Activité non existante")
        return redirect(url_for('admin'))

    if request.method == "GET":
        data_hh = {'title':activity.title, 'data':[]}
        for question in activity.questions:
            data_hh['data'].append({
                'titre':question.title,
                'cdp':[helping_hand.content for helping_hand in question.helping_hands]
            })
        return render_template(template_html, data_hh=data_hh)

    # method == "POST"
    # We need to actualize the questions and helping hands
    data_hh = request.get_json() # dict containing helping hand data
    if data_hh["title"] == "":
        flash("L'activité doit avoir un titre")
        return render_template(template_html)

    if HelpingHandLog.query.filter(HelpingHandLog.helping_hand_id.in_([helping_hand.id for question in activity.questions for helping_hand in question.helping_hands])).first() is None:
        # we can overwrite without any problems!
        current_user.activities.remove(activity)
        create_activity(data_hh)
        flash('L\'activité a été modifiée')
    else:
        flash('Vous ne pouvez pas modifier le contenu car il y a des logs associés')
    return (''), 204


@app.route("/admin/create-helping-hand/", methods=["GET", "POST"])
@admin_required
def create_helping_hand():
    template_html = "admin/create_helping_hand.html"

    if request.method == "GET":
        return render_template(template_html)

    # method == "POST"
    data_hh = request.get_json() # dict containing helping hand data

    if data_hh["title"] == "":
        flash("L'activité doit avoir un titre")
        return render_template(template_html)
    create_activity(data_hh)
    flash(f"Activité {data_hh['title']} créée.")
    return (''), 204

def create_activity(data_hh):
    # create activity
    activity = Activity(
        title=data_hh["title"],
        teacher=current_user
    )
    db.session.add(activity)
    #print(f"adding {activity.title}")

    # create questions and helping_hands
    for (j,question_dict) in enumerate(data_hh["data"]):
        question = Question(
            title=question_dict["titre"],
            activity=activity,
            n_question=j+1
        )
        db.session.add(question)
        #print(f"adding {question.title}")
        # create helping_hands
        for (i,content) in enumerate(question_dict["cdp"]):
            helping_hand = HelpingHand(
                n_helping_hand=i+1,
                question=question,
                content=content
            )
            #print(f"adding {helping_hand.content}")
            db.session.add(helping_hand)

    db.session.commit()


@app.route("/admin/add-student-to-classroom/<student_id>/", methods=["POST"])
@admin_required
def add_student_to_classroom(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if student is None:
        flash("Élève inconnu")
        return redirect(url_for('admin'))

    classroom_id = request.form["classroom_id"]
    classroom = Classroom.query.filter_by(id=classroom_id).first()

    if student in classroom.students:
        flash(f"L'élève {student.name} {student.surname} est déjà dans la classe {classroom.name}")
        return redirect(url_for('admin'))

    classroom.students.append(student)
    db.session.commit()
    flash(f"{student.name} {student.surname} ajouté à la classe {classroom.name}.")
    return redirect(url_for('admin'))


@app.route("/admin/add-multi-students-to-classroom/<classroom_id>/", methods=['POST', 'GET'])
@admin_required
def add_multi_students_to_classroom(classroom_id):
    template_html = "admin/add_student.html"

    classroom = Classroom.query.filter_by(id=classroom_id).first()
    if classroom is None or classroom not in current_user.classrooms:
        flash('Classe inconnue')
        return redirect(url_for('admin'))

    if request.method == "GET":
        return render_template(template_html, classroom=classroom, students=current_user.students)

    # method == 'POST'
    student_usernames = request.form.getlist('student_usernames')
    for student_username in student_usernames:
        student = Student.query.filter_by(username=student_username).first()
        if student is None:
            flash(f"Élève {student_username} inconnu")
        else:
            classroom.students.append(student)
            flash(f"{student.name} {student.surname} ajouté à la classe {classroom.name}.")
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/admin/remove-student-from-classroom/<student_id>/", methods=["POST"])
@admin_required
def remove_student_from_classroom(student_id):
    classroom_id = request.form["classroom_id"]
    return _remove_student_from_classroom(student_id, classroom_id)


@app.route("/admin/_remove-student-from-classroom/<student_id>/<classroom_id>/", methods=["POST"])
@admin_required
def _remove_student_from_classroom(student_id, classroom_id):
    student = Student.query.filter_by(id=student_id).first()
    if student is None:
        flash("Élève inconnu")
        return redirect(url_for('admin'))

    classroom = Classroom.query.filter_by(id=classroom_id).first()

    if student not in classroom.students:
        flash(f"L'élève {student.name} {student.surname} n'est pas dans la classe {classroom.name}")
        return redirect(url_for('admin'))

    classroom.students.remove(student)
    db.session.commit()
    flash(f"{student.username} {student.surname} enlevé de la classe {classroom.name}.")
    return redirect(url_for('admin'))


@app.route("/admin/add-activity-to-classroom/<activity_id>/", methods=["POST"])
@admin_required
def add_activity_to_classroom(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity is None:
        flash("Activité inconnue")
        return redirect(url_for('admin'))

    classroom_id = request.form["classroom_id"]
    classroom = Classroom.query.filter_by(id=classroom_id).first()

    if activity in classroom.activities:
        flash(f"L'activité {activity.title} est déjà dans la classe {classroom.name}")
        return redirect(url_for('admin'))

    classroom.activities.append(activity)
    db.session.commit()
    flash(f"L'activité {activity.title} ajoutée à la classe {classroom.name}.")
    return redirect(url_for('admin'))


@app.route("/admin/remove-activity-from-classroom/<activity_id>/", methods=["POST"])
@admin_required
def remove_activity_from_classroom(activity_id):
    classroom_id = request.form["classroom_id"]
    return _remove_activity_from_classroom(activity_id, classroom_id)


@app.route("/admin/_remove-activity-from-classroom/<activity_id>/<classroom_id>/")
@admin_required
def _remove_activity_from_classroom(activity_id, classroom_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity is None:
        flash("Activité inconnue")
        return redirect(url_for('admin'))

    classroom = Classroom.query.filter_by(id=classroom_id).first()

    if activity not in classroom.activities:
        flash(f"L'activité {activity.title} n'est pas dans la classe {classroom.name}")
        return redirect(url_for('admin'))

    classroom.activities.remove(activity)
    db.session.commit()
    flash(f"L'activité {activity.title} enlevée de la classe {classroom.name}.")
    return redirect(url_for('admin'))


@app.route("/admin/create-classroom/", methods=["GET", "POST"])
@admin_required
def create_classroom():
    template_html = "admin/create_classroom.html"

    if request.method == "GET":
        return render_template(template_html)

    # method == "POST"
    class_name = request.form["class_name"]
    classroom = Classroom(
        name=class_name
    )
    current_user.classrooms.append(classroom)
    db.session.commit()
    flash(f"Salle de classe {class_name} créée.")
    return redirect(url_for('admin'))


@app.route("/admin/delete-classroom/<classroom_id>/", methods=["GET"])
@admin_required
def delete_classroom(classroom_id):
    classroom = Classroom.query.filter_by(id=classroom_id).first()
    if classroom is None or classroom not in current_user.classrooms:
        flash("La classe n'existe pas")
        return redirect(url_for('admin'))
    current_user.classrooms.remove(classroom)
    db.session.commit()
    flash(f"Salle de classe {classroom.name} supprimée.")
    return redirect(url_for('admin'))


@app.route("/admin/delete-activity/<activity_id>/", methods=["GET"])
@admin_required
def delete_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity is None or activity not in current_user.activities:
        flash("L'activité n'existe pas")
        return redirect(url_for('admin'))
    current_user.activities.remove(activity)
    db.session.commit()
    flash(f"Activity {activity.title} supprimée.")
    return redirect(url_for('admin'))