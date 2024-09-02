import streamlit as st
from query import query_data, lst_product, show_data
from llm import response
import re
import pdfkit
from jinja2 import Template

# List of product names
lst = lst_product()

# Function to sanitize text
def sanitize_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

# Function to parse data into a dictionary
def parse_output_to_dict(output):
    # Split the string by headings (assuming headings are in the format "**Heading Name:**")
    sections = re.split(r'\d+\.\s\*\*(.*?)\*\*', output)


    parsed_dict = {}
    
    for i in range(1, len(sections), 2):
        key = sections[i].strip().replace(":", "")
        value = sections[i+1].strip()
        
        # Handle sub-sections (like "Pros", "Cons", etc.)
        if "\n" in value:
            sub_sections = re.split(r'[a-z]\.\s\*\*(.*?)\*\*', value)
            if len(sub_sections) > 1:
                sub_dict = {}
                for j in range(1, len(sub_sections), 2):
                    sub_key = sub_sections[j].strip().replace(":", "")
                    sub_value = sub_sections[j+1].strip()
                    sub_dict[sub_key] = sub_value
                parsed_dict[key] = sub_dict
            else:
                parsed_dict[key] = value
        else:
            parsed_dict[key] = value

    return parsed_dict

# Streamlit app
def main():
    st.title("Product Review Analysis")

    if 'show_raw_data' not in st.session_state:
        st.session_state.show_raw_data = False
    if 'generate_clicked' not in st.session_state:
        st.session_state.generate_clicked = False

    lst = lst_product()
    selected_product = st.selectbox("Select a Product", lst)

    if st.button("Generate"):
        st.session_state.generate_clicked = True
        
        data = query_data(selected_product)
        sanitized_answer = response(data)
        
        
        parsed_dict = parse_output_to_dict(sanitized_answer)
        
        st.write("**Executive Summary:**")
        
        st.markdown(parsed_dict['Executive Summary'], unsafe_allow_html=True)

        html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Product Review Report</title>
            </head>
            <body>
                <h1>Product Review Report</h1>
                
                <h2>Executive Summary</h2>
                <p>{{ parsed_dict['Executive Summary'] }}</p>
                
                <h2>Product Information</h2>
                <ul>
                    {% for line in parsed_dict['Product Information'].split('\n') %}
                    <li>{{ line }}</li>
                    {% endfor %}
                </ul>
                
                <h2>Review Summary</h2>
                <ul>
                    {% for line in parsed_dict['Review Summary'].split('\n') %}
                    <li>{{ line }}</li>
                    {% endfor %}
                </ul>
                
                <h2>Sentiment Analysis</h2>
                <ul>
                    {% for line in parsed_dict['Sentiment Analysis'].split('\n') %}
                    <li>{{ line }}</li>
                    {% endfor %}
                </ul>
                
                <h2>Geographical Distribution</h2>
                <ul>
                    {% for line in parsed_dict['Geographical Distribution'].split('\n') %}
                    <li>{{ line }}</li>
                    {% endfor %}
                </ul>
                
                <h2>Pros and Cons</h2>
                <h3>Pros</h3>
                <ul>
                    {% set pros_section = parsed_dict['Pros and Cons'].split('**b. Cons:**')[0] %}
                    {% for line in pros_section.split('\n') %}
                    {% if line %}
                    <li>{{ line }}</li>
                    {% endif %}
                    {% endfor %}
                </ul>
                <h3>Cons</h3>
                <ul>
                    {% set cons_section = parsed_dict['Pros and Cons'].split('**b. Cons:**')[1] if '**b. Cons:**' in parsed_dict['Pros and Cons'] else '' %}
                    {% for line in cons_section.split('\n') %}
                    {% if line %}
                    <li>{{ line }}</li>
                    {% endif %}
                    {% endfor %}
                </ul>
                
                <h2>Detailed Analysis</h2>
                <h3>Top Keywords in Positive Reviews</h3>
                <ul>
                    {% set positive_keywords = parsed_dict['Detailed Analysis'].split('**b. Top Keywords in Negative Reviews:**')[0] %}
                    {% for line in positive_keywords.split('\n') %}
                    {% if line %}
                    <li>{{ line }}</li>
                    {% endif %}
                    {% endfor %}
                </ul>
                <h3>Top Keywords in Negative Reviews</h3>
                <ul>
                    {% set negative_keywords = parsed_dict['Detailed Analysis'].split('**b. Top Keywords in Negative Reviews:**')[1].split('**c. Excerpt from a Helpful Positive Review:**')[0] if '**b. Top Keywords in Negative Reviews:**' in parsed_dict['Detailed Analysis'] else '' %}
                    {% for line in negative_keywords.split('\n') %}
                    {% if line %}
                    <li>{{ line }}</li>
                    {% endif %}
                    {% endfor %}
                </ul>
                <h3>Excerpt from a Helpful Positive Review</h3>
                <p>{{ parsed_dict['Detailed Analysis'].split('**c. Excerpt from a Helpful Positive Review:**')[1].split('**d. Excerpt from a Helpful Negative Review:**')[0].strip() if '**c. Excerpt from a Helpful Positive Review:**' in parsed_dict['Detailed Analysis'] else '' }}</p>
                
                <h3>Excerpt from a Helpful Negative Review</h3>
                <p>{{ parsed_dict['Detailed Analysis'].split('**d. Excerpt from a Helpful Negative Review:**')[1].strip() if '**d. Excerpt from a Helpful Negative Review:**' in parsed_dict['Detailed Analysis'] else '' }}</p>
                
                <h2>Customer Feedback Trends</h2>
                <p>{{ parsed_dict['Customer Feedback Trends'] }}</p>
                
                <h2>Actionable Insights and Recommendations</h2>
                <h3>Product Improvements</h3>
                <ul>
                    {% set improvements = parsed_dict['Actionable Insights and Recommendations'].split('**b. Feature Enhancements:**')[0] %}
                    {% for line in improvements.split('\n') %}
                    {% if line %}
                    <li>{{ line }}</li>
                    {% endif %}
                    {% endfor %}
                </ul>
                
                <h3>Feature Enhancements</h3>
                <ul>
                    {% set enhancements = parsed_dict['Actionable Insights and Recommendations'].split('**b. Feature Enhancements:**')[1].split('**c. Marketing Strategies:**')[0] if '**b. Feature Enhancements:**' in parsed_dict['Actionable Insights and Recommendations'] else '' %}
                    {% for line in enhancements.split('\n') %}
                    {% if line %}
                    <li>{{ line }}</li>
                    {% endif %}
                    {% endfor %}
                </ul>
                
                <h3>Marketing Strategies</h3>
                <ul>
                    {% set marketing = parsed_dict['Actionable Insights and Recommendations'].split('**c. Marketing Strategies:**')[1] if '**c. Marketing Strategies:**' in parsed_dict['Actionable Insights and Recommendations'] else '' %}
                    {% for line in marketing.split('\n') %}
                    {% if line %}
                    <li>{{ line }}</li>
                    {% endif %}
                    {% endfor %}
                </ul>
            </body>
            </html>
            """
        config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
        template = Template(html_template)
        html_out = template.render(parsed_dict=parsed_dict)
        print(html_out)
        pdf = pdfkit.from_string(html_out, False, configuration=config)
        print(pdf)
        st.download_button(
            label="Download Full Report as PDF",
            data=pdf,
            file_name=f"{selected_product}_Review_Report.pdf",
            mime='application/pdf'
        )

        if st.session_state.show_raw_data:
            st.write("**Raw Data:**")
            st.dataframe(data)

    if st.session_state.generate_clicked:
        if st.button("Show Raw Data"):
            st.session_state.show_raw_data = not st.session_state.show_raw_data
            if st.session_state.show_raw_data:
                data = show_data(selected_product)
                st.write("**Raw Data:**")
                st.dataframe(data)
    else:
        st.write("Please click 'Generate' to see the raw data.")

if __name__ == "__main__":
    main()
