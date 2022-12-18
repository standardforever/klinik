import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from models.doctor_report import DoctorReport
from models.drugs import Drugs
from models.lab_report import LabReport
from models.nurse_report import NuresReport
from models.patient_details import PatientDetails
from models.staff import Staff
from models.base_model import Base, BaseModel

class DBStorage:
    """Interacts with the MYSQL database """
    __engine = None
    # session = None
    
    def __init__(self):
        self.__engine = create_engine('sqlite:///project.db', echo=True)
        Base.metadata.create_all(self.__engine)
        Session = sess_factory = sessionmaker(bind=self.__engine)
        self.session = Session()

    # def reload(self):
    #     """Reloads data from the database"""
    #     Base.metadata.create_all(self.__engine)
    #     Session = sess_factory = sessionmaker(bind=self.__engine)
    #     # sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    #     # Session = scoped_session(sess_factory)
    #     self.__session = Session()

    def get_one(self, **kwargs):
        class_ = kwargs["class_"]
        data = self.session.query(eval(class_)).filter_by(**kwargs["obj"]).first()
        return (data)

    def new(self, **kwargs):
        """Add new object to session"""
        class_ = eval(kwargs["class_"])
        obj = class_(**kwargs["obj"])
        self.session.add(obj)
        self.session.commit()
        return (obj)
        
    
    def get_all(self, args):
        """Get all instance of the class in database"""
        lis = []
        patients = self.session.query(eval(args)).all()
        if not patients:
            abort(404)
        for patient in patients:
            obj = patient.to_dict()
            lis.append(obj)
            del(obj)
            obj = {}
        return (lis)


    def save(self):
        """ Save obj to the database"""
        self.session.commit()

    def close(self):
        """Remove the current session"""
        self.session.remove()

    
    def get(self, cls, id):
        """ Returns the object base on class name and its ID"""
        pass
