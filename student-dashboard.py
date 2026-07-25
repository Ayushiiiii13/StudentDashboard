import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)


st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

h1{
    color:#1565C0;
    text-align:center;
}

.stButton>button{
    background:#1565C0;
    color:white;
}

div[data-testid="metric-container"]{
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:2px 2px 10px #cccccc;
}

</style>
""", unsafe_allow_html=True)



st.title("🎓 Student Performance Analytics Dashboard")

st.write("""
Analyze student academic performance using interactive charts and filters.
""")


df = pd.read_csv("student_performance.csv")


st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

semester = st.sidebar.multiselect(
    "Semester",
    options=sorted(df["Semester"].unique()),
    default=sorted(df["Semester"].unique())
)

attendance = st.sidebar.slider(
    "Attendance Range",
    int(df["Attendance"].min()),
    int(df["Attendance"].max()),
    (int(df["Attendance"].min()),
     int(df["Attendance"].max()))
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Semester"].isin(semester)) &
    (df["Attendance"].between(attendance[0], attendance[1]))
]



st.subheader("Filtered Student Data")

st.dataframe(filtered_df, use_container_width=True)



st.subheader("Summary Statistics")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Students", len(filtered_df))
col2.metric("Average Marks", round(filtered_df["Marks"].mean(),2))
col3.metric("Average Attendance", round(filtered_df["Attendance"].mean(),2))
col4.metric("Highest Marks", filtered_df["Marks"].max())

st.write(filtered_df.describe())



st.subheader("Visualizations")

col1,col2 = st.columns(2)

with col1:
    st.write("### Average Marks by Department")

    avg_marks = filtered_df.groupby("Department")["Marks"].mean()

    fig,ax = plt.subplots()

    ax.bar(avg_marks.index,avg_marks.values)

    ax.set_ylabel("Average Marks")

    st.pyplot(fig)

with col2:
    st.write("### Semester Distribution")

    sem = filtered_df["Semester"].value_counts()

    fig,ax = plt.subplots()

    ax.pie(
        sem.values,
        labels=sem.index,
        autopct="%1.1f%%",
        startangle=90
    )

    st.pyplot(fig)

col3,col4 = st.columns(2)

with col3:

    st.write("### Marks Distribution")

    fig,ax = plt.subplots()

    ax.hist(filtered_df["Marks"],bins=10)

    ax.set_xlabel("Marks")

    ax.set_ylabel("Frequency")

    st.pyplot(fig)

with col4:

    st.write("### Attendance vs Marks")

    fig,ax = plt.subplots()

    ax.scatter(
        filtered_df["Attendance"],
        filtered_df["Marks"]
    )

    ax.set_xlabel("Attendance")

    ax.set_ylabel("Marks")

    st.pyplot(fig)



csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv,
    file_name="filtered_students.csv",
    mime="text/csv"
)