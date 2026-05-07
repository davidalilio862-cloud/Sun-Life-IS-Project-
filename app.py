import streamlit as st
from datetime import datetime
import google.generativeai as genai

# --- GEMINI SETUP ---
# Siguraduhing "GOOGLE_API_KEY" ang nakasulat sa Streamlit Secrets box
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# --- SYSTEM SETUP ---
if 'client_info' not in st.session_state:
    st.session_state.client_info = {}
if 'appointment_schedule' not in st.session_state:
    st.session_state.appointment_schedule = {}

# --- DATA DICTIONARIES ---
benefits = {
    "Estate Preservation Insurance": "Passing Your Wealth to the Next Generation\nWealth transfer and preservation is not just for the rich. Estate planning is essential for anyone who wants to ensure that their loved ones benefit from their inheritance and not burdened by it.\n\nSun Life offers a variety of life insurance plans that ensure your legacy is passed on to your beneficiaries hassle-free, securing their future even when you’re gone.",
    "Health Insurance": "Protect yourself and your family financially in case of medical expenses.\nMedical expenses could get costly, so it pays to be financially prepared!\nBased on research, here are the usual costs of treatment for the top health risks in the Philippines:\n- Heart attack: PHP 978,650\n- Cancer: PHP 2,234,800\n- Stroke: PHP 1,850,150\n- Chronic Kidney Disease: PHP 2,319,286\n- Diabetes: PHP 1,020,714\n\nThe number may look steep, but the good news is, you don't have to shell out the entire amount!",
    "Education Insurance": "Secure a Brighter Future for Your Child\nEducation opens the door to brighter opportunities, but the rising cost makes it challenging for families to afford it without proper planning.",
    "Retirement Insurance": "Guaranteed income during retirement.\nSun Legacy\n- Coverage until age 100\n- Lifetime Insurance Coverage\n- Lifetime Guaranteed Cash Benefits\n- Convenient Short-Term Payment Options",
    "Group Life Insurance": "Group Life Options for Your Organization:\nPro Student, Group Life Insurance, Creditor's Group Life, 5 Plus Group Life, Group Personal Accident, Sun Family Assure.",
    "Digital Insurance": "Protection against cyber threats and data loss."
}

premium_amounts = {
    "Estate Preservation Insurance": {
        "Monthly Premium": {
            "SUN Smarter Life Classic": 1000,
            "Sun Safer Life": 1100,
            "Sun StartUp": 1200,
            "Sun Legacy": 1500,
        },
        "Years to Pay": 12
    },
    "Health Insurance": {"Monthly Premium": 1300, "Years to Pay": 5},
    "Education Insurance": {
        "Monthly Premium": {
            "Sun Dream Achiever": 1200,
            "Sun Smarter Life Elite": 1500,
            "Sun Acceler8": 1000,
            "Sun FlexiLink": 800,
            "Sun MaxiLink Prime": 1100,
            "Sun MaxiLink 100": 900,
            "Sun Wealth Prime 7": 800,
        },
        "Years to Pay": 10
    },
    "Group Life Insurance": {
        "Monthly Premium": {
            "Pro Student": 1000,
            "Group Life Insurance": 1200,
            "Creditor's Group Life": 1300,
            "5 Plus Group Life": 1400,
            "Group Personal Accident": 1500,
            "Sun Family Assure": 1800,
        },
        "Years to Pay": 7
    },
    "Retirement Insurance": {"Monthly Premium": 1200, "Years to Pay": 10},
    "Digital Insurance": {"Monthly Premium": 700, "Years to Pay": 3}
}

# --- HEADER/UI ---
st.title("☀️ Sun Life Insurance IS")
st.subheader('"YOUR FUTURE IS OUR PRIORITY"')
st.info("Why choose Sun Life?\nWe're building sustainable and healthier communities for life. With constant innovation, we aim to provide long-term value to our Clients, Advisors, Employees, and the communities we serve.")
st.divider()

# --- SIDEBAR MENU ---
menu = ["All About Sun Life Insurance", "Avail Insurance", "View Appointments"]
choice = st.sidebar.selectbox("Main Menu", menu)

# --- MENU 1: ALL ABOUT SUN LIFE ---
if choice == "All About Sun Life Insurance":
    st.header("Available Insurance Types")
    selected_insurance = st.selectbox("Select an Insurance Type to learn more:", list(benefits.keys()))
    
    if selected_insurance:
        st.write(f"### {selected_insurance}")
        tab1, tab2, tab3 = st.tabs(["View Benefits", "Monthly Premium", "Calculate Total Cost"])
        
        with tab1:
            st.write(benefits[selected_insurance])
            
        with tab2:
            premium_info = premium_amounts[selected_insurance]["Monthly Premium"]
            if isinstance(premium_info, dict):
                st.write("Available Plans and Monthly Premiums:")
                for plan, price in premium_info.items():
                    st.write(f"- **{plan}**: ₱{price}")
            else:
                st.write(f"Monthly Premium: **₱{premium_info}**")
                
        with tab3:
            years_to_pay = premium_amounts[selected_insurance]["Years to Pay"]
            st.write(f"Maximum years to pay: **{years_to_pay} years**")
            premium_info = premium_amounts[selected_insurance]["Monthly Premium"]
            if isinstance(premium_info, dict):
                selected_plan = st.selectbox("Select Plan to calculate:", list(premium_info.keys()))
                monthly = premium_info[selected_plan]
            else:
                monthly = premium_info
                
            years_input = st.number_input(f"Enter number of years (1-{years_to_pay}):", min_value=1, max_value=years_to_pay, value=1)
            
            if st.button("Calculate"):
                total = monthly * 12 * years_input
                st.success(f"The total cost for {years_input} years is: **₱{total:,}**")

# --- MENU 2: AVAIL INSURANCE ---
elif choice == "Avail Insurance":
    st.header("Avail Insurance & Schedule Appointment")
    selected_insurance = st.selectbox("Select Insurance Type:", list(benefits.keys()))
    
    with st.form("avail_form"):
        st.write("Please fill out your information:")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=18, max_value=100, step=1)
        address = st.text_input("Address")
        phone = st.text_input("Phone Number")
        date_str = st.date_input("Select Appointment Date", min_value=datetime.today())
        
        submitted = st.form_submit_button("Submit & Schedule Appointment")
        
        if submitted:
            if name and address and phone:
                st.session_state.appointment_schedule[name] = {
                    "Insurance Type": selected_insurance,
                    "Age": age,
                    "Address": address,
                    "Phone": phone,
                    "Appointment Date": date_str.strftime("%m/%d/%Y")
                }
                st.success("Appointment scheduled successfully! Please take a screenshot for verification.")
            else:
                st.error("Please fill in all required text fields.")

# --- MENU 3: VIEW APPOINTMENTS ---
elif choice == "View Appointments":
    st.header("Scheduled Appointments")
    if not st.session_state.appointment_schedule:
        st.warning("No appointments scheduled yet.")
    else:
        for name, details in st.session_state.appointment_schedule.items():
            with st.expander(f"Appointment for: {name}"):
                for key, value in details.items():
                    st.write(f"**{key}:** {value}")
                if st.button(f"Cancel Appointment for {name}", key=name):
                    del st.session_state.appointment_schedule[name]
                    st.rerun()

# --- SLI CHATBOT (SIDEBAR VERSION WITH VISIBLE FAQs) ---
st.sidebar.divider()
with st.sidebar.expander("🤖 SLI Chatbot", expanded=False):
    st.markdown("### 🤖 SLI Assistant")
    
    # Visible FAQ list for the user
    st.write("**Frequently Asked Questions:**")
    st.caption("• Paano mag-appointment?\n• Paano bumili ng insurance?\n• Paano mag-calculate ng cost?\n• Paano mag-cancel ng appointment?")
    st.divider()
    
    # Internal knowledge manual for Gemini
    system_knowledge = """
    Kabatiran tungkol sa Sun Life Insurance IS website:
    1. Paano mag-appointment? Piliin ang 'Avail Insurance' sa Main Menu (sidebar), punan ang form, at i-click ang 'Submit & Schedule Appointment'.
    2. Paano makita ang benefits? Pumunta sa 'All About Sun Life Insurance', pumili ng insurance type, at i-click ang 'View Benefits' tab.
    3. Paano mag-calculate ng cost? Sa 'All About Sun Life Insurance' menu, piliin ang 'Calculate Total Cost' tab, ilagay ang years to pay, at i-click ang 'Calculate'.
    4. Paano i-view o i-cancel ang appointment? Pumunta sa 'View Appointments' menu sa sidebar. Makikita doon ang listahan at may button na 'Cancel Appointment'.
    5. Magkano ang premiums? Makikita ang mga presyo sa ilalim ng 'Monthly Premium' tab sa 'All About Sun Life Insurance' menu.
    """

    user_input = st.sidebar.text_input("Mag-type ng tanong dito...", key="chatbot_input")
    
    if user_input:
        try:
            prompt = f"""
            You are SLI, the virtual assistant of the 'Sun Life Insurance IS' website. 
            Guide users on how to use THIS specific website using this info:
            {system_knowledge}
            
            If the question is about site functions, use the info above. 
            If it's general insurance info, use your general knowledge.
            Answer politely in Taglish: {user_input}
            """
            response = model.generate_content(prompt)
            st.sidebar.info(response.text)
        except Exception as e:
            st.sidebar.error(f"System Error: {e}")
