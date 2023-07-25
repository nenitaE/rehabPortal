from flask import Blueprint, jsonify, session, request
from app.models import User, db, ExercisePrescription
from sqlalchemy import and_, or_
from .auth_routes import validation_errors_to_error_messages
from app.forms.create_exercise_rx_form import ExerciseRxForm
from flask_login import login_required, current_user

exercise_rx_routes = Blueprint('exercisePrescriptions', __name__)


@exercise_rx_routes.route('/<int:exercisePrescriptionId>', methods=['DELETE'])
@login_required
def delete_curr_exercise_rx(exercisePrescriptionId):
    """
    Deletes a exercisePrescription by Id for logged in user
    """


@exercise_rx_routes.route('/current', methods=['GET'])
@login_required
def get_current_exercise_prescriptions():
    """
    Query for all exercise prescriptions of current user
    """
    current_user_id = current_user.get_id()
    print('CURRENT USERID', current_user_id)
    user = User.query.get(current_user_id)

    #verify that user is logged in
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    else:
        exercise_prescriptions = ExercisePrescription.query.filter((ExercisePrescription.clinicianId == current_user_id) | (ExercisePrescription.patientId == current_user_id))
        return {'Exercise Prescriptions': [exercise_prescription.to_dict() for exercise_prescription in exercise_prescriptions]}



@exercise_rx_routes.route('/<int:exercisePrescriptionId>', methods=['GET'])
@login_required
def get_exercise_prescription(exercisePrescriptionId):
    '''
    Query for a specific exercise_prescription by Id
    '''

    exercise_prescription = ExercisePrescription.query.get(exercisePrescriptionId)
    print(exercise_prescription, "**********EX RX***********")
    if exercise_prescription is None:
        return jsonify({'error: Exercise Prescription not found'}), 404
    
    else:
        return jsonify(exercise_prescription.to_dict())
    

@exercise_rx_routes.route('', methods=['POST'])
@login_required
def add_exercise_prescriptions():
    """
    Creates a new exercise_prescription 
    """
    current_user_id = current_user.get_id()
    print('CURRENT USERID', current_user_id)
    #check if current_user is a clinician
    curr_user_is_clinician = User.query.filter(
        and_(
            User.id == current_user_id
        )
    ).filter(User.isClinician.is_(True)).first()

    form = ExerciseRxForm()
    # print(form.data, "**********FORM*************")
    form['csrf_token'].data = request.cookies['csrf_token']

    if curr_user_is_clinician and form.validate_on_submit():
        data = form.data
        clinicianId = data['clinicianId']
        patientId = data['patientId']
        print(clinicianId, "**********clinicianId**************")
        print(patientId, "**********patientId**************")
        exercise_prescriptions = ExercisePrescription.query.filter(
            and_(
                ExercisePrescription.clinicianId == clinicianId
            )
        ).all()

        # print(exercise_prescriptions, "**********exercise_prescriptionS**************")

        for exercisePrescription in exercise_prescriptions:
            if data["dailyFrequency"] <= 0:
                return {'errors': 'Daily frequency must be greater than 0.'}, 400
            if data["weeklyFrequency"] <= 0:
                return {'errors': 'Weekly frequency must be greater than 0.'}, 400


        #Create new exercise rx
        new_exercise_prescription = ExercisePrescription(
                                            patientId=data["patientId"],
                                            clinicianId=data["clinicianId"],
                                            title=data["title"],
                                            dailyFrequency=data["dailyFrequency"],
                                            weeklyFrequency=data["weeklyFrequency"],
                                            status=data["status"],
                                            )
        # print(new_exercisePrescription, "*******NEWEXRX******")
        db.session.add(new_exercise_prescription)
        db.session.commit()
        return new_exercise_prescription.to_dict()
    return {'Error': 'User must be a clinician to use this feature.'}, 401
