import streamlit as st 



import joblib


import random
import string
import os

def password_gen(size):
    characters = string.digits + string.ascii_letters + string.punctuation
    generated_pswd = "".join(random.choice(characters) for x in range(size))
    return generated_pswd

def load_model(model_file):
    loaded_model = joblib.load(open(os.path.join(model_file), "rb"))
    return loaded_model

pswd_vectorizer = open("models/pswd_cv.pkl","rb")
pswd_cv = joblib.load(pswd_vectorizer)

def get_key(val,my_dict):
    for key,value in my_dict.items():
        if val == value:
            return key
        
password_labels = {"week":0,"average":1,"strong":2}

def main():
    """Password Strength Classifier"""
    st.title("Password Strength Classifier ML App")
    st.subheader("With Streamlit")
    
    activities = ["Classify Password","Generate Password","About"]
    choice = st.sidebar.selectbox("Select Activity",activities)
    
    
    if choice == "Classify Password":
        st.subheader("Classifying Password with ML")
        password = st.text_input("Enter Password",type="password") 
        model_list = ["LR", "Naive Bayes"]
        model_choice = st.selectbox("Select ML Model",model_list)
        if st.button("Classify"):
            vect_password = pswd_cv.transform([password]).toarray()
            if model_choice == 'LR':
                predictor = load_model("models/logit_pswd_model.pkl")
                prediction = predictor.predict(vect_password)
            
            if model_choice == 'Naive Bayes':
                predictor = load_model("models/nv_pswd_model.pkl")
                prediction = predictor.predict(vect_password)
                
            st.write(prediction)
            
            final_result = get_key(prediction,password_labels)
            st.info(final_result)
        
    elif choice == "Generate Password":
        st.subheader("Generate Random Password")
        number = st.number_input("Enter Length of Password",8,25)
        st.write(number)
        if st.button("Generate"):
            custom_password = password_gen(number)
            st.write(custom_password)
         
    
    
    
    elif choice == 'About':
        st.subheader("About App")
        
    
    
    
    
if __name__ == '__main__':
    main()
