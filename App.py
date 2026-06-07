import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Smart Analytics Tool",
    layout="wide"
)

# Title
st.title("📊 Smart Analytics Tool")

# File Upload
uploaded_file = st.file_uploader(
    "Upload a CSV File",
    type=["csv"]
)

# Run only after file upload
if uploaded_file is not None:

    # Read Dataset
    df = pd.read_csv(uploaded_file)

    # Dataset Preview
    st.header("Dataset Preview")
    st.dataframe(df.head())

    # Dataset Information
    st.header("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    # Missing Value Analysis
    st.header("Missing Value Analysis")

    missing = df.isnull().sum()

    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values
    })

    st.table(missing_df)

    # Statistical Summary
    st.header("Statistical Summary")

    st.table(df.describe())

    # Dynamic Visualizations
    st.header("Dynamic Visualizations")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Histogram", "Bar Chart", "Pie Chart"]
    )

    # Numeric Columns
    numeric_cols = df.select_dtypes(include="number").columns

    # Categorical Columns
    category_cols = df.select_dtypes(exclude="number").columns

    # Histogram
    if chart_type == "Histogram":

        if len(numeric_cols) > 0:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig = px.histogram(
                df,
                x=column,
                title=f"Histogram of {column}"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns available.")

    # Bar Chart
    elif chart_type == "Bar Chart":

        if len(category_cols) > 0:

            category = st.selectbox(
                "Select Category Column",
                category_cols
            )

            counts = df[category].value_counts().reset_index()
            counts.columns = [category, "Count"]

            fig = px.bar(
                counts,
                x=category,
                y="Count",
                title=f"Bar Chart of {category}"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No categorical columns available.")

    # Pie Chart
    elif chart_type == "Pie Chart":

        if len(category_cols) > 0:

            category = st.selectbox(
                "Select Category Column",
                category_cols
            )

            counts = df[category].value_counts().reset_index()
            counts.columns = [category, "Count"]

            fig = px.pie(
                counts,
                names=category,
                values="Count",
                title=f"Pie Chart of {category}"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No categorical columns available.")

else:
    st.info("Please upload a CSV file to begin analysis.")