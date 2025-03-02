from flask import Blueprint, request, jsonify
from db import db
from .utils import fieldcheck,allowed_file,create_upload_path,save_uploaded_image
import logging
from flask_jwt_extended import  jwt_required ,get_jwt_identity,get_jwt
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from config import Config

tshirts_routes = Blueprint('tshirts', __name__)

UPLOAD_FOLDER = Config.UPLOAD_FOLDER
STATIC_URL_PATH ='/static/photos' 
print(f"upload folder is {UPLOAD_FOLDER}")


@tshirts_routes.route("/api/tshirts", methods=["POST"])
@jwt_required()
def add_shirt():
    claims=get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access forbidden, admin role required"}), 403
    


    data = request.form
    if not data:
        return jsonify({"message":"invalid request"})

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    

    tshirt_id=data["tshirt_id"]
    name = data["name"]
    sizes = data["sizes"]
    max_number = data["max_number"]
    collabration_with = data["collabration_with"]

    try:
        tshirt_exists=db.execute("select * from tshirts where name = ? " , name)
        if tshirt_exists:
            return jsonify({"message":"tshirt already exists"})
        
        tshirt_id_exists=db.execute("select * from tshirts where id = ? " , tshirt_id)
        if tshirt_id_exists:
            return jsonify({"message":"tshirt id already exists"})
        

        if file and allowed_file(file.filename):
            image_url=save_uploaded_image(file.read(), original_extension=".jpg")
            print(f"image url is {image_url}")
        else:
            return jsonify({"message": "Invalid file type"}), 400


        db.execute("INSERT INTO Tshirts (id, name, sizes, collabration_with, image_path,max_number) VALUES (?, ?, ?, ?, ?,?)",
                   tshirt_id, name, sizes, collabration_with, image_url,max_number)
    except Exception as e:
        logging.error(f"Error adding shirt: {e}")
        return jsonify({"message": "An error occurred while adding the shirt"}), 500
    
    return jsonify({"message": "Shirt added successfully"}), 200







@tshirts_routes.route("/api/tshirts", methods=["DELETE"])
@jwt_required()
def delete_tshirt():
    identity = get_jwt_identity()  
    claims=get_jwt()
     

    if claims.get("role") != "admin":
        return jsonify({"message": "Access forbidden, admin role required"}), 403
    
    data = request.get_json()

    if not data:
        return jsonify({"message":"invalid request"})

    field_check=fieldcheck(data,"tshirt_id")
    if field_check:
        return field_check

    tshirt_id=data["tshirt_id"]

    try:

        db.execute("DELETE FROM Tshirts WHERE id = ?", (tshirt_id,))
        
    except Exception as e:
        logging.error(f"Error deleting tshirt: {e}")
        return jsonify({"error": "database error"}), 500

    return jsonify({"message": "Tshirt and related orders deleted successfully"}), 200