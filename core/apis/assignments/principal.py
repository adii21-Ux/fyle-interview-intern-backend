from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from core.apis.teachers.schema import TeacherSchema

from .schema import AssignmentSchema, AssignmentGradeSchema
prinicipal_assignment_resources = Blueprint('prinicipal_assignment_resources', __name__)

@prinicipal_assignment_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principal_assignments = Assignment.get_graded_or_submitted_assignments()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)

@prinicipal_assignment_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    teachers = Teacher.list_all_teachers()
    teachers_list_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_list_dump)

@prinicipal_assignment_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_regrade_assignment(p, incoming_payload):    
    assignment = AssignmentGradeSchema().load(incoming_payload)
    
    graded_assignment = Assignment.mark_grade(
        _id=assignment.id,
        grade=assignment.grade,
        auth_principal=p
    )
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)