# ======================================================
# IMPORTS
# ======================================================

import os
import random

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(

    page_title="Smart Interview Preparation Assistant",

    page_icon="🧠",

    layout="wide",

    initial_sidebar_state="expanded"

)



# ======================================================
# SESSION STATE
# ======================================================

DEFAULTS = {


    "users": {

        "admin": "1234"

    },


    "page": "login",


    "user": "",


    "attempted": 0,


    "scores": [],


    "history": [],


    "current_question": 0,


    "answered": False,


    "daily_question": None,


    "selected_category": "",


    "selected_subcategory": ""


}



for key,value in DEFAULTS.items():


    if key not in st.session_state:


        st.session_state[key] = value




# ======================================================
# FIXED CSV LOADER
# ======================================================

def load_questions(csv_file, category):

    """
    Universal CSV Loader

    Fixes:
    - ParserError
    - Extra commas
    - Missing Answer column
    - Empty rows
    """



    if not os.path.exists(csv_file):

        st.warning(

            f"CSV file not found:\n{csv_file}"

        )

        return []



    try:


        df = pd.read_csv(

            csv_file,

            encoding="utf-8",

            quotechar='"',

            engine="python",

            on_bad_lines="skip"

        )



    except Exception as e:


        st.error(

            f"CSV Loading Error: {e}"

        )


        return []





    # Remove spaces from column names


    df.columns = (

        df.columns

        .astype(str)

        .str.strip()

    )





    # Remove empty columns


    df = df.loc[

        :,

        ~df.columns.str.contains(

            "^Unnamed"

        )

    ]





    # Required question column


    if "Question" not in df.columns:


        st.error(

            "CSV must contain Question column"

        )


        st.write(

            "Columns Found:",

            list(df.columns)

        )


        return []





    # Create Answer column if missing


    if "Answer" not in df.columns:


        df["Answer"] = (

            "Answer not available"

        )





    # Aptitude columns


    if category == "Aptitude":



        aptitude_columns = [

            "Option_A",

            "Option_B",

            "Option_C",

            "Option_D"

        ]



        for col in aptitude_columns:


            if col not in df.columns:


                df[col] = ""





    df = df.fillna("")



    df = df.dropna(

        subset=["Question"]

    )



    return df.to_dict(

        orient="records"

    )






# ======================================================
# ANSWER EVALUATION USING NLP
# ======================================================

def evaluate_answer(

        user_answer,

        expected_answer

):



    if expected_answer.strip()=="":


        return 0




    vectorizer = TfidfVectorizer()



    vectors = vectorizer.fit_transform(

        [

            user_answer.lower(),

            expected_answer.lower()

        ]

    )



    similarity = cosine_similarity(

        vectors[0],

        vectors[1]

    )[0][0]



    return round(

        similarity*100,

        2

    )







# ======================================================
# LOGIN / REGISTER
# ======================================================


if st.session_state.page == "login":



    st.title(

        "🧠 Smart Interview Preparation Assistant"

    )



    st.subheader(

        "Login / Register"

    )




    login_tab,register_tab = st.tabs(

        [

            "🔐 Login",

            "📝 Register"

        ]

    )




    # ---------------- LOGIN ----------------


    with login_tab:



        username = st.text_input(

            "Username"

        )



        password = st.text_input(

            "Password",

            type="password"

        )





        if st.button(

            "Login"

        ):



            if (

                username in st.session_state.users

                and

                st.session_state.users[username]

                == password

            ):



                st.session_state.user=username


                st.session_state.page="home"


                st.success(

                    "Login Successful"

                )


                st.rerun()



            else:



                st.error(

                    "Invalid Username or Password"

                )





    # ---------------- REGISTER ----------------



    with register_tab:



        new_user = st.text_input(

            "New Username"

        )


        new_password = st.text_input(

            "New Password",

            type="password"

        )




        if st.button(

            "Register"

        ):



            if (

                new_user.strip()=="" 

                or

                new_password.strip()==""

            ):



                st.warning(

                    "Enter username and password"

                )



            elif new_user in st.session_state.users:



                st.error(

                    "Username already exists"

                )



            else:



                st.session_state.users[new_user]=new_password


                st.success(

                    "Registration Successful"

                )



    st.stop()
    # ======================================================
# HOME SCREEN
# ======================================================


st.title(

    "🧠 Smart Interview Preparation Assistant"

)



st.sidebar.success(

    f"Welcome {st.session_state.user}"

)





# ======================================================
# CATEGORY DATABASE
# ======================================================


categories = {



    # ==========================
    # TECHNICAL
    # ==========================


    "Technical":[


        "Python",

        "Java",

        "C",

        "C++",

        "Computer Networks",

        "Operating System",

        "OOP",

        "Data Structures",

        "DBMS",

        "SQL"


    ],





    # ==========================
    # HR
    # ==========================


    "HR":[


        "HR"


    ],






    # ==========================
    # APTITUDE
    # ==========================


    "Aptitude":[


        "Profit Loss",

        "Percentage",

        "Simple Interest",

        "Compound Interest",

        "Ratio Proportion",

        "Average",

        "Time Work",

        "Time Speed Distance",

        "Probability",

        "Permutation Combination",

        "Logical Reasoning",

        "Data Interpretation"


    ],






    # ==========================
    # GOVERNMENT
    # ==========================


    "Government Sector":[


        "Banking",

        "UPSC",

        "SSC",

        "RRB",

        "TSPSC",

        "APPSC",

        "Current Affairs",

        "Indian Polity",

        "History",

        "Geography",

        "Economy",

        "Computer Awareness"


    ]

}







# ======================================================
# SIDEBAR CATEGORY SELECTION
# ======================================================


category = st.sidebar.selectbox(

    "Select Category",

    list(categories.keys())

)





subcategory = st.sidebar.selectbox(

    "Select Topic",

    categories[category]

)





st.session_state.selected_category = category


st.session_state.selected_subcategory = subcategory







# ======================================================
# MODULE MENU
# ======================================================


modules = [


    "Daily Challenge",

    "Performance Report",

    "History",

    "Weak Areas",

    "Leaderboard"


]





# ======================================================
# ENABLE INTERVIEW MODULE
# ======================================================


if category in [

    "Technical",

    "HR",

    "Aptitude",

    "Government Sector"

]:


    modules.insert(

        0,

        "Interview"

    )





menu = st.sidebar.selectbox(

    "Select Module",

    modules

)








# ======================================================
# QUESTION FILE PATH
# ======================================================

folder_name = (

    category

    .lower()

    .replace(" ", "_")

)


file_name = (

    subcategory

    .lower()

    .replace(" ", "_")

)


csv_file = (

    f"questions/{folder_name}/{file_name}.csv"

)








# ======================================================
# LOAD SELECTED QUESTIONS
# ======================================================


questions = load_questions(

    csv_file,

    category

)







# ======================================================
# DEBUG INFORMATION (OPTIONAL)
# ======================================================


with st.sidebar.expander(

    "📂 Current File"

):


    st.write(

        csv_file

    )


    st.write(

        "Questions Loaded:",

        len(questions)

    )







# ======================================================
# HELPER FUNCTION
# ======================================================


def save_history(

        category,

        subcategory,

        question,

        score

):


    st.session_state.attempted += 1


    st.session_state.scores.append(

        score

    )


    st.session_state.history.append(

        {

            "Category":category,

            "Subcategory":subcategory,

            "Question":question,

            "Score":score

        }

    )
    # ======================================================
# INTERVIEW MODULE
# ======================================================


if menu == "Interview":


    st.header(

        f"📘 {category} - {subcategory}"

    )



    # ------------------------------------------
    # CHECK QUESTIONS
    # ------------------------------------------


    if len(questions) == 0:


        st.warning(

            "No questions found for this topic."

        )


        st.stop()





    total_questions = len(questions)





    if st.session_state.current_question >= total_questions:


        st.session_state.current_question = 0






    index = st.session_state.current_question



    question = questions[index]





    # ------------------------------------------
    # PROGRESS
    # ------------------------------------------


    st.progress(

        (index + 1) / total_questions

    )



    st.write(

        f"### Question {index+1} of {total_questions}"

    )



    st.markdown("---")








    # ==================================================
    # APTITUDE MCQ SECTION
    # ==================================================


    if category == "Aptitude":



        st.subheader(

            question.get(

                "Question",

                ""

            )

        )




        options = [


            question.get(

                "Option_A",

                ""

            ),


            question.get(

                "Option_B",

                ""

            ),


            question.get(

                "Option_C",

                ""

            ),


            question.get(

                "Option_D",

                ""

            )


        ]



        option = st.radio(


            "Choose Correct Answer",


            options,


            key=f"apt_{index}"


        )





        col1,col2 = st.columns(2)





        # ----------------------------------
        # SUBMIT
        # ----------------------------------


        with col1:



            if st.button(

                "Submit Answer",

                key=f"submit_{index}"

            ):



                correct_answer = str(

                    question.get(

                        "Answer",

                        ""

                    )

                ).strip()





                selected_answer = str(

                    option

                ).strip()





                if selected_answer == correct_answer:



                    score = 100



                    st.success(

                        "✅ Correct Answer"

                    )



                else:



                    score = 0



                    st.error(

                        "❌ Wrong Answer"

                    )



                    st.info(

                        f"Correct Answer: {correct_answer}"

                    )





                save_history(

                    category,

                    subcategory,

                    question.get(

                        "Question",

                        ""

                    ),

                    score

                )





                st.metric(

                    "Score",

                    f"{score}%"

                )





                st.progress(

                    score / 100

                )





                explanation = question.get(

                    "Explanation",

                    ""

                )



                if explanation != "":



                    st.subheader(

                        "Explanation"

                    )


                    st.write(

                        explanation

                    )





                st.session_state.answered = True







        # ----------------------------------
        # NEXT QUESTION
        # ----------------------------------


        with col2:



            if st.button(

                "Next Question",

                key=f"next_{index}"

            ):



                if not st.session_state.answered:



                    st.warning(

                        "Submit answer first."

                    )



                else:



                    st.session_state.answered = False



                    if index < total_questions - 1:



                        st.session_state.current_question += 1



                    else:



                        st.success(

                            "🎉 Aptitude Completed"

                        )


                        st.balloons()



                        st.session_state.current_question = 0



                    st.rerun()











    # ==================================================
    # TEXT INTERVIEW SECTION
    # TECHNICAL + HR + GOVERNMENT
    # ==================================================


    else:



        st.subheader(

            question.get(

                "Question",

                ""

            )

        )





        answer = st.text_area(


            "Write Your Answer",


            height=220,


            key=f"text_answer_{index}"


        )







        col1,col2 = st.columns(2)







        # ----------------------------------
        # EVALUATE ANSWER
        # ----------------------------------


        with col1:



            if st.button(

                "Evaluate Answer",

                key=f"evaluate_{index}"

            ):



                if answer.strip() == "":



                    st.warning(

                        "Please enter your answer."

                    )



                else:



                    expected_answer = question.get(

                        "Answer",

                        ""

                    )





                    score = evaluate_answer(

                        answer,

                        expected_answer

                    )





                    save_history(

                        category,

                        subcategory,

                        question.get(

                            "Question",

                            ""

                        ),

                        score

                    )





                    st.metric(

                        "Similarity Score",

                        f"{score}%"

                    )





                    st.progress(

                        score / 100

                    )







                    if score >= 90:



                        st.success(

                            "🌟 Outstanding"

                        )



                    elif score >= 75:



                        st.success(

                            "✅ Excellent"

                        )



                    elif score >= 60:



                        st.info(

                            "👍 Good"

                        )



                    elif score >= 40:



                        st.warning(

                            "🙂 Average"

                        )



                    else:



                        st.error(

                            "❌ Needs Improvement"

                        )







                    st.subheader(

                        "Expected Answer"

                    )





                    st.info(

                        expected_answer

                    )





                    explanation = question.get(

                        "Explanation",

                        ""

                    )



                    if explanation != "":



                        st.subheader(

                            "Explanation"

                        )


                        st.write(

                            explanation

                        )





                    st.session_state.answered = True







        # ----------------------------------
        # NEXT QUESTION
        # ----------------------------------


        with col2:



            if st.button(

                "Next Question",

                key=f"text_next_{index}"

            ):



                if not st.session_state.answered:



                    st.warning(

                        "Evaluate answer first."

                    )



                else:



                    st.session_state.answered = False



                    if index < total_questions - 1:



                        st.session_state.current_question += 1



                    else:



                        st.success(

                            "🎉 Interview Completed"

                        )


                        st.balloons()



                        st.session_state.current_question = 0



                    st.rerun()







# ======================================================
# INTERVIEW TIPS
# ======================================================


if menu == "Interview":



    st.markdown("---")



    st.subheader(

        "💡 Interview Tips"

    )





    if category == "Technical":



        st.info(

"""

✔ Explain concepts clearly

✔ Give practical examples

✔ Mention time complexity

✔ Write optimized solutions

"""

        )




    elif category == "HR":



        st.info(

"""

✔ Use STAR method

✔ Be confident

✔ Give genuine answers

✔ Maintain positive attitude

"""

        )





    elif category == "Aptitude":



        st.info(

"""

✔ Practice daily

✔ Improve calculation speed

✔ Learn shortcuts

✔ Avoid calculation mistakes

"""

        )





    elif category == "Government Sector":



        st.info(

"""

✔ Revise current affairs regularly

✔ Practice previous year papers

✔ Improve accuracy

✔ Manage exam time

✔ Focus on static GK

"""

        )
        # ======================================================
# DAILY CHALLENGE MODULE
# ======================================================


elif menu == "Daily Challenge":


    st.header(

        "🏆 Daily Challenge"

    )




    all_questions = []




    folders = {


        "Technical": "technical",


        "HR": "hr",


        "Aptitude": "aptitude",


        "Government Sector": "government_sector"


    }







    # ==================================================
    # LOAD ALL QUESTIONS
    # ==================================================


    for category_name, folder in folders.items():



        folder_path = (

            f"questions/{folder}"

        )



        if not os.path.exists(folder_path):


            continue





        for file in os.listdir(folder_path):



            if not file.endswith(".csv"):


                continue





            file_path = os.path.join(

                folder_path,

                file

            )





            try:



                df = pd.read_csv(

                    file_path,

                    encoding="utf-8",

                    quotechar='"',

                    engine="python",

                    on_bad_lines="skip"

                )





                df.columns = (

                    df.columns

                    .astype(str)

                    .str.strip()

                )





                if "Question" not in df.columns:


                    continue





                if "Answer" not in df.columns:


                    df["Answer"] = (

                        "Answer not available"

                    )





                # Aptitude columns fix


                for col in [

                    "Option_A",

                    "Option_B",

                    "Option_C",

                    "Option_D"

                ]:


                    if col not in df.columns:


                        df[col] = ""





                df = df.fillna("")





                for _,row in df.iterrows():



                    item = dict(row)





                    item["Category"] = category_name





                    item["Subcategory"] = (

                        file

                        .replace(

                            ".csv",

                            ""

                        )

                        .replace(

                            "_",

                            " "

                        )

                        .title()

                    )





                    all_questions.append(

                        item

                    )





            except Exception:



                continue







    if len(all_questions) == 0:



        st.warning(

            "No questions available."

        )



        st.stop()







    # ==================================================
    # SELECT RANDOM QUESTION
    # ==================================================


    if st.session_state.daily_question is None:



        st.session_state.daily_question = random.choice(

            all_questions

        )





    q = st.session_state.daily_question





    st.success(

        f"{q.get('Category','')} ➜ {q.get('Subcategory','')}"

    )





    st.markdown("---")







    # ==================================================
    # APTITUDE DAILY QUESTION
    # ==================================================


    if q.get("Category") == "Aptitude":





        st.subheader(

            q.get(

                "Question",

                ""

            )

        )





        options = [



            q.get(

                "Option_A",

                ""

            ),



            q.get(

                "Option_B",

                ""

            ),



            q.get(

                "Option_C",

                ""

            ),



            q.get(

                "Option_D",

                ""

            )



        ]





        option = st.radio(

            "Choose Correct Answer",

            options,

            key="daily_option"

        )







        if st.button(

            "Check Answer",

            key="daily_check"

        ):





            correct = str(

                q.get(

                    "Answer",

                    ""

                )

            ).strip()





            if option.strip() == correct:



                st.success(

                    "✅ Correct Answer"

                )



            else:



                st.error(

                    "❌ Wrong Answer"

                )



                st.info(

                    f"Correct Answer: {correct}"

                )





            if q.get(

                "Explanation",

                ""

            ) != "":



                st.subheader(

                    "Explanation"

                )



                st.write(

                    q.get(

                        "Explanation"

                    )

                )









    # ==================================================
    # TECHNICAL / HR / GOVERNMENT DAILY QUESTION
    # ==================================================


    else:





        st.subheader(

            q.get(

                "Question",

                ""

            )

        )






        answer = st.text_area(

            "Your Answer",

            height=200,

            key="daily_text"

        )






        if st.button(

            "Evaluate",

            key="daily_evaluate"

        ):




            if answer.strip()=="":



                st.warning(

                    "Please enter your answer."

                )



            else:



                score = evaluate_answer(

                    answer,

                    q.get(

                        "Answer",

                        ""

                    )

                )





                st.metric(

                    "Similarity Score",

                    f"{score}%"

                )





                st.progress(

                    score/100

                )





                if score >= 90:



                    st.success(

                        "🌟 Outstanding"

                    )



                elif score >= 75:



                    st.success(

                        "✅ Excellent"

                    )



                elif score >= 60:



                    st.info(

                        "👍 Good"

                    )



                elif score >= 40:



                    st.warning(

                        "🙂 Average"

                    )



                else:



                    st.error(

                        "❌ Needs Improvement"

                    )





                st.subheader(

                    "Expected Answer"

                )





                st.info(

                    q.get(

                        "Answer",

                        ""

                    )

                )






    # ==================================================
    # NEW CHALLENGE BUTTON
    # ==================================================


    st.markdown("---")





    if st.button(

        "🎲 New Challenge"

    ):



        st.session_state.daily_question = random.choice(

            all_questions

        )



        st.rerun()
        # ======================================================
# INTERVIEW MODULE
# ======================================================

if menu == "Interview":

    st.header(
        f"📘 {category} - {subcategory}"
    )


    if len(questions) == 0:

        st.warning(
            "No questions found for this topic."
        )

        st.stop()



    total_questions = len(questions)


    if st.session_state.current_question >= total_questions:

        st.session_state.current_question = 0



    index = st.session_state.current_question


    question = questions[index]



    st.progress(

        (index + 1) / total_questions

    )


    st.write(

        f"### Question {index+1} of {total_questions}"

    )


    st.markdown("---")



    # ==================================================
    # APTITUDE + GOVERNMENT MCQ SECTION
    # ==================================================


    if category in [

        "Aptitude",

        "Government Sector"

    ]:


        st.subheader(

            question.get(

                "Question",

                ""

            )

        )



        options = [


            str(question.get(

                "Option_A",

                ""

            )),


            str(question.get(

                "Option_B",

                ""

            )),


            str(question.get(

                "Option_C",

                ""

            )),


            str(question.get(

                "Option_D",

                ""

            ))

        ]



        option = st.radio(

            "Select Correct Answer",

            options,

            key=f"option_{index}"

        )



        col1,col2 = st.columns(2)



        # -------------------------------
        # SUBMIT
        # -------------------------------


        with col1:


            if st.button(

                "Submit Answer"

            ):



                correct = str(

                    question.get(

                        "Answer",

                        ""

                    )

                ).strip()



                selected = str(

                    option

                ).strip()



                # Handle A/B/C/D answers also


                if selected == correct or selected.startswith(correct):


                    score = 100


                    st.success(

                        "✅ Correct Answer"

                    )


                else:


                    score = 0


                    st.error(

                        "❌ Wrong Answer"

                    )


                    st.info(

                        f"Correct Answer : {correct}"

                    )



                st.metric(

                    "Score",

                    f"{score}%"

                )


                st.progress(

                    score/100

                )



                explanation = question.get(

                    "Explanation",

                    ""

                )


                if explanation:


                    st.subheader(

                        "Explanation"

                    )


                    st.write(

                        explanation

                    )



                st.session_state.attempted += 1



                st.session_state.scores.append(

                    score

                )



                st.session_state.history.append(

                    {


                    "Category":

                    category,


                    "Subcategory":

                    subcategory,


                    "Question":

                    question.get(

                        "Question",

                        ""

                    ),


                    "Score":

                    score


                    }

                )



                st.session_state.answered=True





        # -------------------------------
        # NEXT QUESTION
        # -------------------------------


        with col2:


            if st.button(

                "Next Question"

            ):



                if not st.session_state.answered:


                    st.warning(

                        "Submit answer first"

                    )



                else:


                    st.session_state.answered=False



                    if index < total_questions-1:


                        st.session_state.current_question += 1



                    else:


                        st.success(

                            "🎉 Completed Successfully"

                        )


                        st.balloons()


                        st.session_state.current_question=0



                    st.rerun()



    # ==================================================
    # TECHNICAL / HR TEXT ANSWER SECTION
    # ==================================================


    else:



        st.subheader(

            question.get(

                "Question",

                ""

            )

        )



        answer = st.text_area(

            "Write Your Answer",

            height=200,

            key=f"text_{index}"

        )



        col1,col2 = st.columns(2)



        with col1:


            if st.button(

                "Evaluate Answer"

            ):



                if answer.strip()=="":


                    st.warning(

                        "Enter your answer"

                    )


                else:



                    expected = question.get(

                        "Answer",

                        ""

                    )



                    score = evaluate_answer(

                        answer,

                        expected

                    )



                    st.metric(

                        "Similarity Score",

                        f"{score}%"

                    )



                    st.progress(

                        score/100

                    )



                    st.session_state.attempted +=1



                    st.session_state.scores.append(

                        score

                    )



                    st.session_state.history.append(

                        {


                        "Category":

                        category,


                        "Subcategory":

                        subcategory,


                        "Question":

                        question.get(

                            "Question",

                            ""

                        ),


                        "Score":

                        score


                        }

                    )



                    st.subheader(

                        "Expected Answer"

                    )



                    st.info(

                        expected

                    )



                    st.session_state.answered=True



        with col2:


            if st.button(

                "Next Question"

            ):



                if not st.session_state.answered:


                    st.warning(

                        "Evaluate answer first"

                    )


                else:


                    st.session_state.answered=False



                    if index < total_questions-1:


                        st.session_state.current_question +=1



                    else:


                        st.success(

                            "🎉 Interview Completed"

                        )


                        st.session_state.current_question=0



                    st.rerun()



# ======================================================
# END PART 5
# ======================================================
# ======================================================
# DAILY CHALLENGE MODULE
# ======================================================


elif menu == "Daily Challenge":


    st.header(

        "🏆 Daily Challenge"

    )



    all_questions = []



    folders = {


        "Technical": "technical",


        "HR": "hr",


        "Aptitude": "aptitude",


        "Government Sector": "government_sector"


    }





    # ==================================================
    # LOAD ALL QUESTIONS
    # ==================================================


    for category_name, folder in folders.items():



        folder_path = f"questions/{folder}"



        if not os.path.exists(folder_path):

            continue




        for file in os.listdir(folder_path):



            if not file.endswith(".csv"):

                continue



            file_path = os.path.join(

                folder_path,

                file

            )



            try:



                df = pd.read_csv(

                    file_path,

                    encoding="utf-8",

                    quotechar='"',

                    on_bad_lines="skip"

                )



                # remove spaces

                df.columns = (

                    df.columns

                    .str.strip()

                )



                if "Question" not in df.columns:

                    continue



                # Create missing columns


                if "Answer" not in df.columns:

                    df["Answer"] = ""



                if "Option_A" not in df.columns:

                    df["Option_A"] = ""



                if "Option_B" not in df.columns:

                    df["Option_B"] = ""



                if "Option_C" not in df.columns:

                    df["Option_C"] = ""



                if "Option_D" not in df.columns:

                    df["Option_D"] = ""



                if "Explanation" not in df.columns:

                    df["Explanation"] = ""





                df = df.fillna("")




                for _, row in df.iterrows():



                    item = dict(row)



                    item["Category"] = category_name



                    item["Subcategory"] = (

                        file

                        .replace(".csv","")

                        .replace("_"," ")

                        .title()

                    )



                    all_questions.append(item)



            except Exception:


                continue






    # ==================================================
    # CHECK QUESTIONS
    # ==================================================


    if len(all_questions)==0:



        st.warning(

            "No questions available."

        )

        st.stop()






    # ==================================================
    # RANDOM DAILY QUESTION
    # ==================================================


    if st.session_state.daily_question is None:



        st.session_state.daily_question = random.choice(

            all_questions

        )





    q = st.session_state.daily_question





    st.success(

        f"{q['Category']} ➜ {q['Subcategory']}"

    )



    st.markdown("---")





    # ==================================================
    # MCQ QUESTIONS
    # ==================================================


    if q["Category"] in [


        "Aptitude",


        "Government Sector"


    ]:



        st.subheader(

            q.get(

                "Question",

                ""

            )

        )





        options = [


            q.get(

                "Option_A",

                ""

            ),


            q.get(

                "Option_B",

                ""

            ),


            q.get(

                "Option_C",

                ""

            ),


            q.get(

                "Option_D",

                ""

            )

        ]





        option = st.radio(

            "Choose Answer",

            options,

            key="daily_option"

        )






        if st.button(

            "Check Answer"

        ):



            correct = str(

                q.get(

                    "Answer",

                    ""

                )

            ).strip()



            selected = str(

                option

            ).strip()





            if selected == correct or selected.startswith(correct):



                st.success(

                    "✅ Correct Answer"

                )



            else:



                st.error(

                    "❌ Wrong Answer"

                )


                st.info(

                    f"Correct Answer : {correct}"

                )






            if q.get(

                "Explanation",

                ""

            ):



                st.subheader(

                    "Explanation"

                )


                st.write(

                    q["Explanation"]

                )







    # ==================================================
    # TECHNICAL / HR QUESTIONS
    # ==================================================


    else:



        st.subheader(

            q.get(

                "Question",

                ""

            )

        )





        answer = st.text_area(

            "Your Answer",

            height=200,

            key="daily_answer"

        )





        if st.button(

            "Evaluate"

        ):



            if answer.strip()=="":



                st.warning(

                    "Enter your answer"

                )



            else:



                score = evaluate_answer(

                    answer,

                    q.get(

                        "Answer",

                        ""

                    )

                )





                st.metric(

                    "Similarity Score",

                    f"{score}%"

                )



                st.progress(

                    score/100

                )





                if score >=90:


                    st.success(

                        "🌟 Excellent"

                    )


                elif score >=75:


                    st.success(

                        "✅ Very Good"

                    )


                elif score >=60:


                    st.info(

                        "👍 Good"

                    )


                elif score >=40:


                    st.warning(

                        "🙂 Average"

                    )


                else:


                    st.error(

                        "❌ Need Improvement"

                    )





                st.subheader(

                    "Expected Answer"

                )



                st.info(

                    q.get(

                        "Answer",

                        ""

                    )

                )





    # ==================================================
    # NEW CHALLENGE BUTTON
    # ==================================================


    st.markdown("---")



    if st.button(

        "🎲 New Challenge"

    ):



        st.session_state.daily_question = random.choice(

            all_questions

        )


        st.rerun()



# ======================================================
# END PART 6
# ======================================================