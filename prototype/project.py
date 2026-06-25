import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    national_id = Column(String(10), unique=True)
    fixed_tuition = 20000000 
    
    payments = relationship("Payment", back_populates="student")

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship("Student", back_populates="payments")

Base.metadata.create_all(engine)

def main_menu():
    while True:
        print("\nsystem shahrie va pardakht")
        print("1. sabt nam ")
        print("2.moshahede vaziet pardakht")
        print("3. khoroj")
        
        choice = input("entekhab konid :")

        if choice == '1':
            name = input(" nam va nam khanevadegi")
            national_id = input("kod meli : ")
            
            exists = session.query(Student).filter_by(national_id=national_id).first()
            if exists:
                print("ghablan in danesh jo sabt shode")
            else:
                new_student = Student(name=name, national_id=national_id)
                session.add(new_student)
                session.commit()
                print(f"sabtnam{name} ba movafaqiat anjam shod")
                print(f"shahrie paie {new_student.fixed_tuition:,}")

        elif choice == '2':
            nid = input("kode meli daneshjo ra vared knid !")
            student = session.query(Student).filter_by(national_id=nid).first()
            
            if student:
                total_paid = sum(p.amount for p in student.payments)
                remaining = student.fixed_tuition - total_paid
                
                print(f"\n👤 daneshjo : {student.name}")
                print(f"shahrie kol : {student.fixed_tuition:,}")
                print(f"majmoe pardakhti :{total_paid:,}")
                print(f"mande bedehi : {remaining:,}")
                
                pay_choice = input("\n ghast pardakht darid ?(yes/no)")
                if pay_choice == 'yes':
                    try:
                        amount = float(input("mablagh pardakhti :"))
                        if amount > remaining:
                            print(" az mekhdar shahrie bishtar ast")
                        else:
                            new_payment = Payment(amount=amount, student=student)
                            session.add(new_payment)
                            session.commit()
                            print(f"mablagh {amount:,} pardakht shod !")
                            print(f"mande bedehi : {(remaining - amount):,}")
                    except ValueError:
                        print("error lotfan adad ra vared knid")
            else:
                print("error daneshjo yaft nashod")

        elif choice == '3':
            print("khoroj")
            break
        else:
            print("na motabar")

if __name__ == "__main__":
    main_menu()