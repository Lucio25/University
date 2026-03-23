from odoo import models, fields


class UniversityTeacher(models.Model):
    _name = 'university.teacher'
    _description = 'Profesor'

    name = fields.Char(string='Nombre del Profesor', required=True)
    email = fields.Char(string='Correo Electrónico')
    phone = fields.Char(string='Teléfono')

    # Usamos 'groups' para que estos campos no aparezcan si el usuario no pertenece al grupo de Finanzas
    cuit = fields.Char(
        string='CUIT',
        groups="university.group_university_finance",
        help="Clave Única de Identificación Tributaria"
    )

    bank_account = fields.Char(
        string='CBU / Alias',
        groups="university.group_university_finance"
    )

    salary = fields.Float(
        string='Sueldo Base',
        groups="university.group_university_finance",
        digits=(16, 2)  # Para decimales en moneda
    )

    # Relación académica
    subject_ids = fields.One2many(
        'university.subject',
        'teacher_id',
        string='Materias a Cargo'
    )