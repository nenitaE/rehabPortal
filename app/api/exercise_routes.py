from flask import Blueprint, jsonify, session, request
from app.models import User, db, Exercise, ExercisePrescription
from sqlalchemy import and_, or_
from .auth_routes import validation_errors_to_error_messages
from app.forms.create_exercise_form import ExerciseForm
from flask_login import login_required, current_user

exercise_routes = Blueprint('exercises', __name__)

@exercise_routes.route('/current', methods=['GET'])
@login_required
def get_current_exercises():
    """
    Query for all exercises of current user
    """
    userId = session['_user_id']
    exercisePrescription = ExercisePrescription.query.filter(ExercisePrescription.clinicianId == userId)

    #verify that user is logged in
    if exercisePrescription is None:
        return jsonify({'error': 'Exercise not found'}), 404

    else:
        return jsonify(exercisePrescription.to_dict_with_exercises())


@exercise_routes.route('/<int:exerciseId>', methods=['GET'])
@login_required
def get_exercise(exerciseId):
    '''
    Query for a specific exercise by Id
    '''

    exercise = Exercise.query.get(exerciseId)
    print(exercise, "**********EXERCISE***********")
    if exercise is None:
        return jsonify({'error: Exercise not found'}), 404
    
    else:
        return jsonify(exercise.to_dict())