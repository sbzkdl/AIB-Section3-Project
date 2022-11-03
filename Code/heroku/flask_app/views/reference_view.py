from flask import Blueprint, render_template, request
import pickle

reference_bp = Blueprint('reference', __name__, url_prefix='/reference')

@reference_bp.route('/')
def reference():
  return render_template('reference.html')

@reference_bp.route('/result', methods=['POST', 'GET'])
def reference_result():
  return render_template('reference_result.html')