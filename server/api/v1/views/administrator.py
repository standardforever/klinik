from api.v1.views import app_views
from models import storage
from flask import request, abort, make_response, jsonify
from datetime import datetime, time
from  api.utils import verifyDetails, hashPassword, unhashpassword, admin_required
# from models.patient_details import PatientDetails
# from models.staff import Staff
from flasgger.utils import swag_from


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from multiprocessing import Value
from datetime import datetime

counter = Value('i', 0)


@app_views.route("/regstaff", methods=["POST"])
@jwt_required
@swag_from("documentation/profile/create_staff_profile.yml")
def regStaff():
    """Register a Staff to the database"""
    class_ = "Staff"
    details = request.get_json()
    new = {}
    new["first_name"] = details.get("first_name")
    new["last_name"] = details.get("last_name")
    new["email"] = details.get("email")
    new["address"] = details.get("address")
    new["phone"] = details.get("phone")
    new["user_type"] = details.get("user_type")
    new["licence_no"] = details.get("licence_no")
    new["user_role"] = details.get("user_role")
    new["password"] = hashPassword(details.get("first_name"))
    new["sex"] = details.get("sex")
    new["next_of_kin"] = details.get("next_of_kin")
    new["next_of_kin_phone"] = details.get("next_of_kin_phone")
    new["next_of_kin_address"] = details.get("next_of_kin_address")
    new["relationship"] = details.get("relationship")

    # """Increment the doctor Reg_no"""
    # with counter.get_lock():
    #     counter.value += 1
    #     out = counter.value
    # new["reg_no"] = "out"

    check = verifyDetails(new)
    obj = {"class_": class_, "obj": {"reg_no": new.get("reg_no")}}
    data = storage.get_one(**obj)
    if not check or data != None:
        return (jsonify({"error": "invalid input"}), 400)
    obj["obj"] = new
    staff = storage.new(**obj)
    new["created_at"] = staff.created_at
    new["updated_at"] = staff.updated_at
    new["id"] = staff.id
    del new["password"]
    return  (jsonify(new), 201)


@app_views.route("/getprofile/<id>", methods=["GET"])
@swag_from("documentation/profile/get_staff.yml")
def getProfile(id):
    """Get the Patient or Staff Profile details """
    class_name = id.split('.')
    class_ = class_name[0]
    obj = {"class_": class_, "obj": {"id": id}}
    patient = storage.get_one(**obj)
    if not patient:
        """not found request"""
        return (make_response(jsonify({'error': "Not found"}), 404))
    obj = patient.to_dict()
    return (make_response(jsonify(obj), 200))


@app_views.route("/allstaffprofile", methods=["GET"])
@swag_from("documentation/profile/get_all_staff.yml")
def allStaffProfile():
    """Get all Staff profile Details"""
    lis = storage.get_all("Staff")
    if not lis:
        return (jsonify({}))
    return (make_response(jsonify(lis), 200))


@app_views.route("/updateprofile/<id>", methods=["PUT"])
@swag_from("documentation/profile/update_profile.yml")
def updatetprofile(id):
    """Update users profile"""
    class_name = id.split(".")
    class_ = class_name[0]
    obj = {"class_": class_, "obj": {"id": id}}
    profile = storage.get_one(**obj)
    req = request.get_json()
    if not profile or not req:
        return (jsonify({"error": "bad request"}), 400)
    profileDetails = profile.to_dict()
    for key, value in req.items():
        if value == None:
            return (jsonify({"error": "bad request"}), 400)
        if profileDetails.get(key) != value and profileDetails.get(key) != None:
            if key == "create_at":
                setattr(profile, key, datetime.strptime(value, time))
            elif key == "updated_at":
                setattr(profile, key, datetime.strptime(value, time))
            else:
                setattr(profile, key, value)
    name = profile.to_dict()
    profile.save()
    return(make_response(jsonify(name), 201))


@app_views.route("/deleteprofile/<id>", methods=["DELETE"])
@swag_from("documentation/profile/delete_profile.yml")
def deleteprofile(id):
    """Delete Patient or Staff profile"""
    class_lis = id.split(".")
    class_ = class_lis[0]
    obj = {"class_": class_, "obj": {"id": id}}
    record = storage.get_one(**obj)
    storage.delete(record)
    return ({}, 200)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app_views.route("/login", methods=["POST"])
def login():
    obj = {}
    reg_no = request.json.get("reg_no", None)
    file_no = request.json.get("file_no", None)
    password = request.json.get("password", None)
    # if username != "test" or password != "test":
    """Check if the request is correct"""
    if file_no != None and password != None:
        obj["class_"] = "PatientDetails"
        obj["obj"] = {"file_no": file_no}
    elif reg_no != None and password != None:
        obj["class_"] = "Staff"
        obj["obj"] = {"reg_no": reg_no}
    else:
        return jsonify({"msg": "Bad username or password"}), 401
    
    """Check if user in database"""
    user = storage.get_one(**obj)
    if user and unhashpassword(user.password, password):
        return (jsonify({"access_token": create_access_token(identity=user.email),
         "details": user.to_dict()}))
        # if file_no and user.file_no != None:
        #     access_token = create_access_token(identity=user.file_no)
        # elif reg_no and user.user_role == "admin":
        #     access_token = create_access_token(identity=user.reg_no, additional_claims={"is_admin": True})
        # elif reg_no and user.reg_no != None:
        #     access_token = create_access_token(identity=user.reg_no, additional_claims={"is_staff": True})
        # return jsonify(access_token=access_token)
    else:
        return (jsonify({"msg": "username or password not found!"}), 401)
        
    # return jsonify({"msg": "Bad username or password"}), 401



@app_views.route("/duty")
def staff_duty():
    obj = {"class_": "Staff", "key": "Staff.status", "val": "True"}
    user = storage.filter_all(**obj)
    return (jsonify(user))


# @app_views.route("/duty")
# def get():
#     obj = {"class_": "Staff", "key": "Staff.status", "val": "True"}
#     user = storage.filter_all(**obj)
#     return (jsonify(user))