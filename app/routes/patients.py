from flask import Blueprint, render_template, session, request, redirect, url_for
from models.models_flask import Patient
from utils.db import db

patients = Blueprint('patients', __name__)

@patients.route('/patients')
def show_patients():
    return "desde patients"

@patients.route('/add-patients', methods=['GET', 'POST'])
def add_patients():
    return "paciente agregado"
    