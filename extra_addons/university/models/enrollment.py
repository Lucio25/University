from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class UniversityEnrollment(models.Model):
    _name = 'university.enrollment'
    _description = 'Inscripción de Estudiantes'

    # La inscripción se identifica por el alumno
    _rec_name = 'student_id'

    # Relaciones principales
    student_id = fields.Many2one('university.student', string='Estudiante', required=True)
    career_id = fields.Many2one('university.career', string='Carrera', required=True)

    # Filtrar planes por carrera
    study_plan_id = fields.Many2one(
        'university.study_plan',
        string='Plan de Estudios',
        required=True,
        domain="[('career_id', '=', career_id)]"
    )

    year = fields.Selection([
        ('1', 'Primer Año'),
        ('2', 'Segundo Año'),
        ('3', 'Tercer Año'),
        ('4', 'Cuarto Año'),
        ('5', 'Quinto Año')
    ], string='Año de cursada', default='1')

    # Vínculo con el detalle
    line_ids = fields.One2many(
        'university.enrollment.line',
        'enrollment_id',
        string='Detalle de Materias Inscriptas'
    )

    grouped_subject_ids = fields.Many2many(
        'university.subject',
        string='Materias (agrupadas)',
        compute='_compute_grouped_subject_ids',
    )

    # Un estudiante no puede inscribirse dos veces a la misma carrera
    _sql_constraints = [
        ('unique_student_career', 'unique(student_id, career_id)',
         'El estudiante ya posee una inscripción activa en esta carrera.')
    ]

    # Valida que las materias en las líneas no superen el cupo máximo
    @api.constrains('line_ids')
    def _check_subject_capacity(self):

        for record in self:
            # Buscamos las materias a través de las líneas
            for line in record.line_ids:
                subject = line.subject_id
                if not subject:
                    continue

                max_capacity = getattr(subject, 'max_capacity', 30) or 30
                enrolled_count = getattr(subject, 'enrolled_count', 0)
                subject_name = subject.name

                if enrolled_count > max_capacity:
                    raise ValidationError(_(
                        "No hay cupo disponible en la materia: %s. Máximo permitido: %s"
                    ) % (subject_name, max_capacity))

    @api.depends(
        'student_id',
        'career_id',
        'study_plan_id',
        'year',
        'line_ids.subject_id',
        'student_id.enrollment_ids.line_ids.subject_id',
    )
    def _compute_grouped_subject_ids(self):
        for enrollment in self:
            if not enrollment.student_id:
                enrollment.grouped_subject_ids = self.env['university.subject']
                continue

            same_group_enrollments = enrollment.student_id.enrollment_ids.filtered(
                lambda e: e.career_id == enrollment.career_id
                and e.study_plan_id == enrollment.study_plan_id
                and e.year == enrollment.year
            )
            enrollment.grouped_subject_ids = same_group_enrollments.mapped('line_ids.subject_id')

