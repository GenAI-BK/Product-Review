from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import  PromptTemplate
from langchain.chains import LLMChain
import os
import re
import streamlit as st
from query import query_data
GOOGLE_API_KEY=st.secrets["GOOGLE_API_KEY"]
llm=ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)
# data=query_data('realme_Buds_2_Wired_Headset')
def response(data):
    template2="""Output format:1.Executive Summary: <executive summary>\n\n
                               2.Product Information: <product information>\n\n
                               3.Review Summary: <review summary>\n\n
                               4.Sentiment Analysis: <sentiment analysis>\n\n
                               5.Geographical Distribution: <geographical distribution>\n\n
                               6.Pros and Cons: <pros and cons>\n\n
                                      a.Pros:<pros>\n\n
                                      b.Cons:<cons>\n\n
                               7.Detailed Analysis: <detailed analysis>
                                      a.Top Keywords in Positive Reviews:<top keywords in positive reviews>\n\n
                                      b.Top Keywords in Negative Reviews<top keywords in negative reviews>\n\n
                                      c.Excerpt from a Helpful Positive Review:<excerpt from a helpful positive review>\n\n
                                      d.Excerpt from a Helpful Negative Review:<excerpt from a helpful negative review>\n\n
                               8.Customer Feedback Trends: <customer feedback trends>\n\n
                               9.Actionable Insights and Recommendations: <actionable insights and recommendations>
                                      a.Product Improvements:<Product Improvements>\n\n
                                      b.Feature Enhancements:<feature enhancements>\n\n
                                      c.Marketing Strategies:<marketing strategies>\n\n
                               
                             """
    template1="""Generate a comprehensive product review report for a product and use the {data} to generate the report. The report should include the following sections:

                1. Executive Summary:
                    Provide a brief overview of the product's performance based on customer reviews.
                    Highlight the main findings such as overall sentiment, common themes, and critical areas of improvement.
                2. Product Information:
                    Include the product name, product ID, category, and the reporting period.
                3. Review Summary:
                    Summarize the total number of reviews, the average rating, and the distribution of ratings across 1 to 5 stars.
                4. Sentiment Analysis:
                    Analyze the overall sentiment of the reviews (positive, negative, neutral).
                    Break down the sentiment percentages and identify common positive and negative themes.
                5. Geographical Distribution:
                    Identify the top regions or countries by the number of reviews.
                    Provide insights into any patterns or trends observed in different regions.
                6. Pros and Cons:
                    List the most frequently mentioned pros and cons of the product based on the reviews.
                7. Detailed Analysis:
                    Identify the top keywords and phrases used in positive and negative reviews.
                    Include excerpts from the most helpful or insightful reviews.
                8. Customer Feedback Trends:
                    Provide monthly or quarterly trends in review volume and average rating.
                    Identify any seasonal patterns or changes during specific events.
                9. Actionable Insights and Recommendations:
                    Product Improvements: Suggest product improvements based on common issues or negative feedback.
                    Feature Enhancements: Propose feature enhancements based on positive feedback.
                    Marketing Strategies: Recommend marketing strategies based on geographical and sentiment analysis.
                  """
    template=template1 +" "+ template2
    prompt_template=PromptTemplate(
    template= template,
    input_variables=["data"]
    )
    chain=LLMChain(llm=llm,prompt=prompt_template)
    answer=chain.run({"data":data})
    return answer




