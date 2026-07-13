SHEET_CATALOG = {
    "Users": {
        "description": "Login, role, department, designation, access and reporting manager details.",
        "access": ["founder", "executive"],
        "columns": [
            "user_id", "employee_name", "role", "department",
            "designation", "secret_key", "manager_id"
        ]
    },

    "Employees": {
        "description": "Employee profile, skill, domain, availability and salary reference.",
        "access": ["founder", "executive"],
        "columns": [
            "employee_id", "employee_name", "designation",
            "primary_skill", "domain", "availability_percent",
            "monthly_ctc", "monthly_inhand"
        ]
    },

    "Attendance": {
        "description": "Daily/monthly attendance, leave, absence and LOP information.",
        "access": ["founder", "HR Executive", "Finance Executive"],
        "columns": [
            "attendance_id", "employee_id", "date", "month",
            "status", "leave_applied", "leave_status",
            "is_lop", "remarks"
        ]
    },

    "Payroll": {
        "description": "Gross salary, net salary, deductions and salary-related data.",
        "access": ["founder", "Finance Executive"],
        "columns": [
            "employee_id", "gross_salary", "net_salary",
            "pf", "tax", "deductions"
        ]
    },

    "Projects": {
        "description": "Active and completed project information, progress and value.",
        "access": ["founder", "Operations Executive", "Sales Executive"],
        "columns": [
            "project_id", "project_name", "client_id",
            "project_value", "status", "expected_progress",
            "actual_progress", "estimated_duration_months"
        ]
    },

    "Project_Assignments": {
        "description": "Which employee works on which project and their bandwidth allocation.",
        "access": ["founder", "Operations Executive"],
        "columns": [
            "project_id", "employee_id", "employee_name",
            "allocation_percent", "weekly_hours"
        ]
    },

    "Leads": {
        "description": "Future project opportunities before they become active projects.",
        "access": ["founder", "Sales Executive"],
        "columns": [
            "lead_id", "company", "industry", "project_type",
            "expected_budget", "urgency", "competition_level",
            "existing_client"
        ]
    },

    "Project_Requirements": {
        "description": "Resource requirement by project type.",
        "access": ["founder", "Sales Executive", "Operations Executive", "HR Executive"],
        "columns": [
            "project_type", "required_role",
            "required_people", "estimated_months"
        ]
    },

    "Company_Expenses": {
        "description": "Monthly company expenses such as rent, cloud, tools and admin costs.",
        "access": ["founder", "Finance Executive"],
        "columns": [
            "expense_type", "monthly_cost"
        ]
    },

    "Onboarding": {
        "description": "New joinee onboarding status.",
        "access": ["founder", "HR Executive"],
        "columns": [
            "employee_id", "forms_submitted", "virtual_id_created",
            "laptop_issued", "email_created", "onboarding_status"
        ]
    }
}