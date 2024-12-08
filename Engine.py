from experta import *

class ExpertSystem(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(action="loan_grading")

    # Reading inputs from console
    @Rule(Fact(action='loan_grading'),NOT(Fact(Age=W())),salience=1)
    def feature_0(self):
        self.declare(Fact(Age=int(input(" Age: "))))

    @Rule(Fact(action='loan_grading'),NOT(Fact(Salary=W())),salience=1)
    def feature_1(self):
        self.declare(Fact(Salary=int(input(" Salary(TND): "))))

    @Rule(Fact(action='loan_grading'),NOT(Fact(Property=W())),salience=1)
    def feature_2(self):
        self.declare(Fact(Property=input(" Property: ")))

    @Rule(Fact(action='loan_grading'),NOT(Fact(Vehicule=W())),salience=1)
    def feature_3(self):
        self.declare(Fact(Vehicule=bool(input(" Vehicule: "))))  

    @Rule(Fact(action='loan_grading'),NOT(Fact(Reason=W())),salience=1)
    def feature_4(self):
        self.declare(Fact(Reason=input(" Reason: ")))

    @Rule(Fact(action='loan_grading'),NOT(Fact(Amount=W())),salience=1)
    def feature_5(self):
        self.declare(Fact(Amount=int(input(" Amount(TND): "))))
    
    @Rule(Fact(action='loan_grading'),NOT(Fact(Other=W())),salience=1)
    def feature_6(self):
        self.declare(Fact(Other=int(input(" Other loans in payment: "))))


    @Rule(Fact(action='loan_grading'),
          Fact(Age=MATCH.Age),
          Fact(Salary=MATCH.Salary),
          Fact(Property=MATCH.Property),
          Fact(Vehicule=MATCH.Vehicule),
          Fact(Reason=MATCH.Reason),
          Fact(Amount=MATCH.Amount),
          Fact(Other=MATCH.Other),
          TEST(lambda Age: Age >= 25 and Age <= 60),
          TEST(lambda Salary: Salary >= 1000),
          TEST(lambda Property: Property == "Owner"),
          TEST(lambda Vehicule: True),
          TEST(lambda Reason: Reason == "Business"),
          TEST(lambda Amount: Amount <= 10000),
          TEST(lambda Other: Other == 0)
          )
    def Grade_A_0(self):
        self.declare(Fact(Grade="A"))

    @Rule(Fact(action='loan_grading'),
          Fact(Age=MATCH.Age),
          Fact(Salary=MATCH.Salary),
          Fact(Property=MATCH.Property),
          Fact(Vehicule=MATCH.Vehicule),
          Fact(Reason=MATCH.Reason),
          Fact(Amount=MATCH.Amount),
          Fact(Other=MATCH.Other),
          TEST(lambda Age: Age > 60),
          TEST(lambda Salary: Salary < 1000),
          TEST(lambda Property: Property == "Renter"),
          TEST(lambda Vehicule: False),
          TEST(lambda Reason: Reason == "Personal"),
          TEST(lambda Amount: Amount > 100000),
          TEST(lambda Other: Other >= 0), salience=1
          )
    def Grade_G_0(self):
        self.declare(Fact(Grade="G"))
    

    @Rule(Fact(action='loan_grading'),
          Fact(Age=MATCH.Age),
          Fact(Salary=MATCH.Salary),
          Fact(Property=MATCH.Property),
          Fact(Vehicule=MATCH.Vehicule),
          Fact(Reason=MATCH.Reason),
          Fact(Amount=MATCH.Amount),
          Fact(Other=MATCH.Other),
          Fact(Grade=MATCH.Grade),salience=3)
    def Grade(self,Age,Salary,Property,Vehicule,Reason,Amount,Other,Grade):
        print("--------------------------------------------------")
        print("Age: "+str(Age))
        print("Salary: "+str(Salary))
        print("Property: "+Property)
        print("Vehicule: "+str(Vehicule))
        print("Reason: "+Reason)
        print("Amount: "+str(Amount))
        print("Other loans in payment: "+str(Other))
        print("Loan Grade: "+Grade)
        print("--------------------------------------------------")
        predictionResult["Age"]=Age
        predictionResult["Salary"]=Salary
        predictionResult["Property"]=Property
        predictionResult["Vehicule"]=Vehicule
        predictionResult["Reason"]=Reason
        predictionResult["Amount"]=Amount
        predictionResult["Other"]=Other
        predictionResult["Grade"]=Grade
        
        
    @Rule(Fact(action='loan_grading'),
          Fact(Age=MATCH.Age),
          Fact(Salary=MATCH.Salary),
          Fact(Property=MATCH.Property),
          Fact(Vehicule=MATCH.Vehicule),
          Fact(Reason=MATCH.Reason),
          Fact(Amount=MATCH.Amount),
          Fact(Other=MATCH.Other),
          NOT(Fact(Grade=MATCH.Grade)),salience=-999)
    def not_matched(self,Age,Salary,Property,Vehicule,Reason,Amount,Other):
        print("Your inputs are not considered in the knowledge base")
        predictionResult["Grade"]="Undefined"

   # Decision rules based on loan grades, Salary, and Amount
    @Rule(Fact(action='loan_grading'), Fact(Grade="A"), Fact(Salary=MATCH.Salary), Fact(Amount=MATCH.Amount),
          TEST(lambda Salary, Amount: Salary > 3000 and Amount <= 5000), salience=2)
    def approve_loan_A(self, Salary, Amount):
        self.declare(Fact(Decision="Approved: Best Conditions"))
    
    @Rule(Fact(action='loan_grading'), Fact(Grade="B"), Fact(Salary=MATCH.Salary), Fact(Amount=MATCH.Amount),
          TEST(lambda Salary, Amount: Salary > 2500 and Amount <= 7000), salience=2)
    def approve_loan_B(self, Salary, Amount):
        self.declare(Fact(Decision="Approved: Good Conditions"))

    @Rule(Fact(action='loan_grading'), Fact(Grade="C"), Fact(Salary=MATCH.Salary), Fact(Amount=MATCH.Amount),
          TEST(lambda Salary, Amount: Salary > 2000 and Amount <= 10000), salience=2)
    def approve_loan_C(self, Salary, Amount):
        self.declare(Fact(Decision="Approved: Standard Conditions"))

    @Rule(Fact(action='loan_grading'), Fact(Grade="D"), Fact(Salary=MATCH.Salary), Fact(Amount=MATCH.Amount),
          TEST(lambda Salary, Amount: Salary > 1500 and Amount <= 15000), salience=2)
    def approve_loan_D(self, Salary, Amount):
        self.declare(Fact(Decision="Approved: Restrictive Conditions"))

    @Rule(Fact(action='loan_grading'), Fact(Grade="E"), Fact(Salary=MATCH.Salary), Fact(Amount=MATCH.Amount),
          TEST(lambda Salary, Amount: Salary > 1000 and Amount <= 20000), salience=2)
    def approve_high_risk_loan(self, Salary, Amount):
        self.declare(Fact(Decision="Approved: High-Risk Conditions"))

    @Rule(Fact(action='loan_grading'), Fact(Grade="F"), Fact(Salary=MATCH.Salary), Fact(Amount=MATCH.Amount),
          TEST(lambda Salary, Amount: Salary <= 1000 or Amount > 20000), salience=2)
    def conditional_rejection(self, Salary, Amount):
        self.declare(Fact(Decision="Rejected: Alternative Options Offered"))

    @Rule(Fact(action='loan_grading'), Fact(Grade="G"), salience=2)
    def reject_loan_G(self):
        self.declare(Fact(Decision="Rejected: High Risk"))

    @Rule(Fact(action='loan_grading'), Fact(Grade=MATCH.Grade), Fact(Decision=MATCH.Decision), salience=1)
    def display_decision(self, Grade, Decision):
        """
        Displays the loan grade and final decision to the user.
        Updates the global predictionResult with the decision.
        """
        print("--------------------------------------------------")
        print(f"Loan Grade: {Grade}")
        print(f"Loan Decision: {Decision}")
        print("--------------------------------------------------")
        predictionResult["Grade"] = Grade
        predictionResult["Decision"] = Decision

    @Rule(Fact(action='loan_grading'), Fact(Grade=MATCH.Grade), NOT(Fact(Decision=W())), salience=-999)
    def undefined_decision(self, Grade):
        """
        Handles cases where the grade does not match predefined decision rules.
        Updates the decision to 'Undefined'.
        """
        print("--------------------------------------------------")
        print(f"Loan Grade: {Grade}")
        print("Loan Decision: Undefined")
        print("--------------------------------------------------")
        predictionResult["Grade"] = Grade
        predictionResult["Decision"] = "Undefined"    
        
global predictionResult
predictionResult={}

engine=ExpertSystem()
engine.reset()
engine.run()

"""


def main(inputU):
    if (not inputU):
        print("Enter user characteristics")
    engine=ExpertSystem()
    engine.reset()
    engine.run()
    return predictionResult
    
"""