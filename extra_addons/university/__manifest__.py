{
    'name': 'University',
    'version': '19.0.1.0.0',
    'summary': 'Gestion de estudiantes, carreras, planes y asignaturas',
    'category': 'Education',
    'license': 'LGPL-3',
    'author': 'Lucio Malgioglio',
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/actions.xml',
        'views/career_views.xml',
        'views/student_views.xml',
        'views/subject_views.xml',
        'views/teacher_views.xml',
        'views/enrollment_views.xml',

        'views/menus.xml',
        'data/demo_data.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
