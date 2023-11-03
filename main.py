import numpy as np
import pickle
import streamlit as st
import pandas as pd
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="seproj"
)
mycursor=mydb.cursor()
print("Connection Established")
def get_grade_point(grade):
    grade_points = {"S": 10.0, "A": 9.0, "B": 8.0, "C": 7.0, "D": 6.0, "E": 5.0, "F": 0.0}
    return grade_points.get(grade, 0.0)
st.title("Placement Prediction for Engineering Students")
st.sidebar.header("Header")
# Create navigation options in the sidebar
selected_page = st.sidebar.radio("Select an Option", ["Login/Register", "CGPA Calculation","Placement Prediction","My Profile"])

if selected_page == "Login/Register":
    # Add your Login/Register content here
    st.write("Welcome to the Login/Register section.")
    login_or_register = st.radio("Choose an option", ["Login", "Register"])

    if login_or_register == "Login":
        # Login
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            mycursor.execute("SELECT name, name2 FROM demo WHERE name = %s AND name2 = %s", (username, password))
            result = mycursor.fetchone()
            if result:
                st.success("Login Successful!")
            else:
                st.error("Login Failed. Please check your credentials.")

    else:
        # Register
        st.subheader("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            sql= "insert into demo(name,name2) values(%s,%s)"
            val= (new_username,new_password)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Registration Successful!")


elif selected_page == "CGPA Calculation":
    # Add your CGPA Calculation content here
    st.write("Welcome to the CGPA Calculation section.")
    # You can add input fields and calculations related to CGPA here.
    st.header("CGPA Calculation")

    num_courses = st.number_input("Number of Courses", min_value=1, max_value=10, step=1)

    # Create lists to store course grades and credits
    course_grades = []
    course_credits = []

    for i in range(num_courses):
        st.subheader(f"Course {i + 1}")
        grade = st.selectbox(f"Select Grade for Course {i + 1}", ["S", "A","B", "C", "D", "E", "F"])
        credit = st.number_input(f"Enter Credits for Course {i + 1}", min_value=1, max_value=5, step=1)

        course_grades.append(grade)
        course_credits.append(credit)

    if st.button("Calculate CGPA"):
        # Calculate CGPA based on the provided grades and credits
        total_credits = sum(course_credits)
        weighted_grades = sum([get_grade_point(grade) * credit for grade, credit in zip(course_grades, course_credits)])
        cgpa = weighted_grades / total_credits

        st.write(f"Your CGPA is: {cgpa:.2f}")

elif selected_page == "Placement Prediction":
    # Add your CGPA Calculation content here
    st.write("Welcome to the Placement Prediction section.")
    # You can add input fields and calculations related to CGPA here.
    # Create input fields for user parameters
    st.header("Placement Prediction")
    model = pickle.load(open('model.pkl', 'rb'))
    # Create input fields for user parameters
    gender = st.selectbox("Select Gender", ["Male", "Female"])
    stream = st.selectbox("Select Stream", ["Engineering", "Computer Science", "Electrical", "Mechanical", "Other"])
    internship = st.number_input("Number of Internships", min_value=0, step=1, format="%d")
    backlogs = st.number_input("Number of Backlogs", min_value=0, step=1, format="%d")
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)
    # Academic criteria
    st.header("Academic Criteria")
    os_percentage = st.number_input("Percentage in Operating Systems", min_value=0.0, max_value=100.0, step=0.1)
    algo_percentage = st.number_input("Percentage in Algorithms", min_value=0.0, max_value=100.0, step=0.1)
    programming_percentage = st.number_input("Percentage in Programming Concepts", min_value=0.0, max_value=100.0, step=0.1)
    software_engineering_percentage = st.number_input("Percentage in Software Engineering", min_value=0.0, max_value=100.0, step=0.1)
    computer_networks_percentage = st.number_input("Percentage in Computer Networks", min_value=0.0, max_value=100.0, step=0.1)
    computer_architecture_percentage = st.number_input("Percentage in Computer Architecture", min_value=0.0, max_value=100.0, step=0.1)
    math_percentage = st.number_input("Percentage in Mathematics", min_value=0.0, max_value=100.0, step=0.1)
    # Create an array to store academic integer values
    academic_values = []

    # Append the academic percentage values to the array
    academic_values.append(os_percentage)
    academic_values.append(algo_percentage)
    academic_values.append(programming_percentage)
    academic_values.append(software_engineering_percentage)
    academic_values.append(computer_networks_percentage)
    academic_values.append(computer_architecture_percentage)
    academic_values.append(math_percentage)

    new_variable = 0

    # Loop through academic values and calculate the new variable
    for value in academic_values:
        if 0 <= value <= 40:
            new_variable += 1
        elif 40 < value <= 70:
            new_variable += 3
        elif 70 < value <= 100:
            new_variable += 5
    new_variable = (new_variable/35)*100
    # Non-academic criteria
    st.header("Non-Academic Criteria")
    communication_skills_percentage = st.number_input("Percentage in Communication Skills", min_value=0.0, max_value=100.0, step=0.1)
    logical_quotient_rating = st.number_input("Logical Quotient Rating", min_value=0.0, max_value=10.0, step=0.1)
    hackathons_participated = st.number_input("Hackathons Participated", min_value=0,max_value=10, step=1, format="%d")
    coding_skills_rating = st.number_input("Coding Skills Rating", min_value=0, max_value=10, step=1, format = "%d")
    public_speaking_points = st.number_input("Public Speaking Points", min_value=0,max_value=10, step=1, format="%d")
    self_learning_capability = st.radio("Self-Learning Capability (Yes/No)", ["Yes", "No"])
    certifications_count = st.number_input("Certifications Count", min_value=0, step=1, format="%d")
    workshops_count = st.number_input("Workshops Count", min_value=0, step=1, format="%d")
    team_capability = st.radio("Worked in Team ever? (Yes/No)", ["Yes", "No"])

    skills = 0.0
    skills = (communication_skills_percentage/10) + logical_quotient_rating + public_speaking_points

    coding = 0
    coding = hackathons_participated + coding_skills_rating

    capability_score = 0
    if team_capability == "Yes":
        capability_score += 10
    if self_learning_capability == "Yes":
        capability_score += 10

    technical_score =0
    technical_score = certifications_count + workshops_count


    # Create a button to trigger the prediction
    if st.button("Predict"):
        gender_value = 1 if gender == "Male" else 0
        stream_value = ["Engineering", "Computer Science", "Electrical", "Mechanical", "Other"].index(stream)
        # Create a numpy array from user input
        user_input = np.array([gender_value, stream_value, internship, cgpa, backlogs]).reshape(1, -1)

    # Make the prediction
        output = model.predict(user_input)

    # Display the prediction result
        st.header("Results and Analysis")
        if output == 1:
            st.write("You have high chances of getting placed!!!")
        else:
            st.write("You have low chances of getting placed. All the best.")

        basic_subject_message = "Your knowledge on basic Subjects need to be mastered to crack Interview" if new_variable < 50 else "Good work! You have good knowledge over basic subjects and revise before to crack interview"
        Interpersonal_Skills =  "Improve your communication skills, logic quotient, or public speaking skills" if skills < 20 else "Great job! Your combination of communication skills, logic quotient, and public speaking points is impressive."
        feedback_coding_hackathon = "Work on your coding and hackathon skills to improve your score." if coding < 13 else "Well done! Your coding and hackathon skills are strong and can be a valuable asset in interviews and competitions."
        personality_score = "Enhance your team collaboration skills and Invest in your self-learning ability " if capability_score < 11 else  "you are a collobarative and efficient self-learner"
        technical_score_analysis = " Try to attend more workshops and achieve certifications to prove your capabilities to the interviewer " if technical_score <3 else "Alas! Try to attend more "
    # Create a DataFrame
        data = {
        "Heading": [ "Basic Subject Analysis", "Interpersonal Skills ", "Coding skills" , " Personality Score" , " Certifications and Workshops"],
        "Message": [basic_subject_message , Interpersonal_Skills , feedback_coding_hackathon , personality_score , technical_score_analysis]
        }
        df = pd.DataFrame(data)
        # Display the DataFrame as a table
        st.write(df,max_rows=len(data["Heading"]))

elif selected_page == "My Profile":
    st.write("Welcome to the My Profile section.")
    st.button("Update")
    st.subheader("Update Profile")
    new_password = st.text_input("New Password", type="password")
    new_name = st.text_input("Name")
    new_email = st.text_input("Email")
