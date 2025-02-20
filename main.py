import streamlit as st
import mysql.connector
import datetime
from streamlit_option_menu import option_menu
from mysql.connector import Error

def db_con():
    try:
        connection = mysql.connector.connect(host="localhost",user="root",password="",database="jitjai_journal")
        if connection.is_connected():
            return connection
    except Error as e:
        st.error("Error connecting to DB: %s" % e)
    return None

def login():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Don't Have an Account?",type="tertiary"):
        st.session_state["current_page"] = "Register"  

    if st.button("Login"):
        con = db_con()
        if con:
            cursor = con.cursor()
            try:
                cursor.execute("SELECT * FROM account WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()
                if user:
                    st.toast('Login สำเร็จ!', icon='✅')
                    st.session_state["logged_in"] = True
                    st.session_state["email"] = email
                    st.session_state["current_page"] = "Home"
                    st.session_state["user_data"] = {"email": user[1],"name": user[3],"lastname": user[4]}
                else:
                    st.toast('Email หรือ Password ไม่ถูกต้อง', icon='⛔')
            except Error as e:
                st.error("Error: %s" % e)
            finally:
                cursor.close()
                con.close()

def register():
    st.title("📝 Register")
    name = st.text_input("Name")
    lastname = st.text_input("Lastname")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("already have an account?",type="tertiary"):
        st.session_state["current_page"] = "Login" 
    
    if st.button("Register"):
        if not name or not lastname or not email or not password or not confirm_password:
            st.toast('กรุณากรอกข้อมูลให้ครบทุกช่อง', icon='⚠️')
        elif password != confirm_password:
            st.toast('Password และ Confirm Password ไม่ตรงกัน', icon='⚠️')
        else:
            con = db_con()
            if con:
                cursor = con.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO account (email, password, name, lastname) VALUES (%s, %s, %s, %s)",
                        (email, password, name, lastname),
                    )
                    con.commit()
                    st.toast('ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ', icon='📝')
                    st.session_state["current_page"] = "Login" 
                except Error as e:
                    st.error("Error: %s" % e)
                finally:
                    cursor.close()
                    con.close()

def home():                   
    st.markdown(
        "<h1 style='text-align: center;'>JitJai-Journal</h1>", 
        unsafe_allow_html=True  
    )
    
    user_data = st.session_state.get("user_data", {})
    email = st.session_state["email"]
    st.subheader(f"Welcome K.{user_data.get('name')} {user_data.get('lastname')} to JitJai-Journal!")

    d = st.date_input("When's your write", datetime.date(2025, 2, 20))
    st.write("You write is :", d)

    heading = st.text_input("Heading"," ")
    Diary_write = st.text_area("Write something today", " ")
    st.markdown(f"Diary Preview:\n\n{Diary_write.replace(chr(10), '<br>')}", unsafe_allow_html=True)


    if st.button("Save Diary"):
        if Diary_write == "":
            st.toast('ยังไม่มีข้อความใน Diary', icon='⚠️')
        else:
            con = db_con()
            if con:
                cursor = con.cursor()
                try:
                    cursor.execute(
                    "INSERT INTO diary (email, heading ,diarytext) VALUES (%s, %s, %s)", 
                    (email, heading, Diary_write),
                    )
                    con.commit()
                    st.toast('บันทึกไดอารี่สำเร็จ!', icon='📝')
                    st.session_state["current_page"] = "Diary" 
                except Error as e:
                    st.error("Error: %s" % e)
                finally:
                    cursor.close()
                    con.close()

def Diary():      
    con = db_con()
    cursor = con.cursor()
    cursor.execute("SELECT heading, diarytext FROM diary ORDER BY id DESC") 
    data = cursor.fetchall()             
    st.markdown(
        "<h1 style='text-align: center;'>📖 My Diary</h1>", 
        unsafe_allow_html=True  
    )
    diary_dict = {str(row[0]): row[1] for row in data}
    st.markdown("เลือกไดอารี่ของคุณเพื่อดูเนื้อหา")
    selected_id = st.selectbox("📌 เลือกไดอารี่:", list(diary_dict.keys()), index=0)
    st.subheader("📝 เนื้อหาไดอารี่")
    st.write(diary_dict[selected_id])
    con.close()




def MonthlyReport():                   
    st.markdown(
        "<h1 style='text-align: center;'>Monthly Report</h1>", 
        unsafe_allow_html=True  
    )

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    with st.sidebar:
        selected = option_menu("Main Menu",["Home", "Diary","Monthly Report", "Logout"],
            icons=["house", "book" ,"bar-chart", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,)
        
    if selected == "Home":
        home()
    elif selected == "Diary":
        Diary()
    elif selected == "Monthly Report":
        MonthlyReport()
    elif selected == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["current_page"] = "Login" 
else:
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Login"
    
    if st.session_state["current_page"] == "Login":
        login()
    elif st.session_state["current_page"] == "Register":
        register()