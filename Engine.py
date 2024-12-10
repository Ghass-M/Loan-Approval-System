from experta import *
import streamlit as st

class ExpertSystem(KnowledgeEngine):
    @DefFacts()
    def initial(self):
        yield Fact(action="loan_grading")

    @Rule(Fact(action='loan_grading'), NOT(Fact(Age=W())))
    def ask_age(self):
        self.declare(Fact(Age=st.session_state['Age']))

    @Rule(Fact(action='loan_grading'), NOT(Fact(Salary=W())))
    def ask_salary(self):
        self.declare(Fact(Salary=st.session_state['Salary']))

    @Rule(Fact(action='loan_grading'), NOT(Fact(Property=W())))
    def ask_property(self):
        self.declare(Fact(Property=st.session_state['Property']))

    @Rule(Fact(action='loan_grading'), NOT(Fact(Vehicule=W())))
    def ask_vehicle(self):
        self.declare(Fact(Vehicule=st.session_state['Vehicle']))

    @Rule(Fact(action='loan_grading'), NOT(Fact(Reason=W())))
    def ask_reason(self):
        self.declare(Fact(Reason=st.session_state['Reason']))

    @Rule(Fact(action='loan_grading'), NOT(Fact(Amount=W())))
    def ask_amount(self):
        self.declare(Fact(Amount=st.session_state['Amount']))

    @Rule(Fact(action='loan_grading'), NOT(Fact(Other=W())))
    def ask_other_loans(self):
        self.declare(Fact(Other=st.session_state['OtherLoans']))

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
        st.session_state['Grade'] = Grade
        st.session_state['Decision'] = Decision

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

def main():
    st.title("Loan Grading Expert System")

    # Input fields
    with st.form(key='loan_form'):
        st.number_input("Age", min_value=18, max_value=99, key='Age')
        st.number_input("Salary (TND)", min_value=0, key='Salary')
        st.selectbox("Property Ownership", ["Owner", "Renter"], key='Property')
        st.radio("Do you own a vehicle?", [True, False], key='Vehicle')
        st.selectbox("Loan Reason", ["Business", "Personal"], key='Reason')
        st.number_input("Loan Amount (TND)", min_value=0, key='Amount')
        st.number_input("Other Loans in Payment", min_value=0, key='OtherLoans')
        submit = st.form_submit_button(label="Submit")

    if submit:
        engine = ExpertSystem()
        engine.reset()
        engine.run()
        if 'Grade' in st.session_state:
            st.success(f"Loan Grade: {st.session_state['Grade']}")
            st.success(f"Loan Grade: {st.session_state['Decision']}")
        else:
            st.warning("No decision could be made based on the inputs.")

if __name__ == "__main__":
    main()
