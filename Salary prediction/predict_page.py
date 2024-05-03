import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
     data = pickle.load(file)
     return data
    

data=load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
   # CSS to customize title background and font color
   st.markdown("""
        <style>
        .title {
            background-color: #171717;
            color: #ffffff;
            padding: 5px 10px;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Use the custom CSS class for the title
   st.markdown('<h1 class="title">Software Developer Salary Prediction</h1>', unsafe_allow_html=True)

   st.write("""### We need some information to predict the salary""")
  
   countries=(
   "United States of America",                                                
   "Germany",                                                  
   "United Kingdom of Great Britain and Northern Ireland",   
   "Canada",                                                   
   "India",                                                    
   "France",                                                   
   "Netherlands",                                              
   "Australia",                                                
   "Brazil",                                                   
   "Spain",                                                    
   "Sweden",                                                   
   "Italy" ,                                                   
   "Poland",                                                   
   "Switzerland",                                              
   "Denmark,"                                                  
   "Norway",                                                   
   "Israel",           
    )

   education=(
   "Bachelor’s degree", "Less than a Bachelors", "Master’s degree",
       "Post grad",
     )
   country=st.selectbox("Country",countries)
   education=st.selectbox("Education level",education)
   experience=st.slider("Years of Experience",0,50,1)
   
   ok = st.button("Calculate Salary")
   if ok:
      X = np.array([[country, education, experience ]])
      X[:, 0] = le_country.transform(X[:,0])
      X[:, 1] = le_education.transform(X[:,1])
      X = X.astype(float)

      salary=regressor.predict(X)
      st.subheader(f"The estimated salary is ${salary[0]:.2f}")
      
   