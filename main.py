import re
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from langchain_experimental.agents import create_pandas_dataframe_agent
from logger_helper import get_logger
from data_loader import load_csv_data
from llm_config import initialize_llm
import time 

logger = get_logger()
 
# Configure page
st.set_page_config(
    page_title="DF Chat", 
    page_icon="📊", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load data
df = load_csv_data("Titanic-Dataset.csv")

# Configure LLM
llm = initialize_llm()

agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=False,
    allow_dangerous_code=True, # The allow_dangerous_code=True is necessary for the agent to work, but you should implement additional security layers around it
    agent_executor_kwargs={"handle_parsing_errors": True}
)

# Working CSS Animation 
st.markdown("""
<style>
/* Main container background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Animated title */
@keyframes wave {
    0%, 100% { 
        transform: translateY(0px) scale(1) rotate(0deg); 
        opacity: 1;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
    }
    25% { 
        transform: translateY(-15px) scale(1.1) rotate(5deg); 
        opacity: 0.8;
        color: #ffeb3b;
        text-shadow: 0 0 30px rgba(255,235,59,0.8);
    }
    50% { 
        transform: translateY(-10px) scale(1.2) rotate(-5deg); 
        opacity: 1;
        color: #00bcd4;
        text-shadow: 0 0 25px rgba(0,188,212,0.6);
    }
    75% { 
        transform: translateY(-5px) scale(1.1) rotate(3deg); 
        opacity: 0.9;
        color: #e91e63;
        text-shadow: 0 0 20px rgba(233,30,99,0.7);
    }
}

.dancing-letter {
    display: inline-block;
    margin: 0 2px;
    font-size: 2.5rem;
    font-weight: bold;
    animation: wave 3s ease-in-out infinite;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

.dancing-letter:hover {
    transform: scale(1.5) rotate(360deg);
    color: #ff5722 !important;
}

/* Staggered animation delays */
.dancing-letter:nth-child(1) { animation-delay: 0.0s; }
.dancing-letter:nth-child(2) { animation-delay: 0.1s; }
.dancing-letter:nth-child(3) { animation-delay: 0.2s; }
.dancing-letter:nth-child(4) { animation-delay: 0.3s; }
.dancing-letter:nth-child(5) { animation-delay: 0.4s; }
.dancing-letter:nth-child(6) { animation-delay: 0.5s; }
.dancing-letter:nth-child(7) { animation-delay: 0.6s; }
.dancing-letter:nth-child(8) { animation-delay: 0.7s; }
.dancing-letter:nth-child(9) { animation-delay: 0.8s; }
.dancing-letter:nth-child(10) { animation-delay: 0.9s; }

/* Floating particles */
@keyframes float {
    0%, 100% { 
        transform: translateY(0px) translateX(0px) rotate(0deg); 
        opacity: 0.7; 
    }
    33% { 
        transform: translateY(-20px) translateX(10px) rotate(120deg); 
        opacity: 1; 
    }
    66% { 
        transform: translateY(-10px) translateX(-10px) rotate(240deg); 
        opacity: 0.8; 
    }
}

.floating-particle {
    position: fixed;
    width: 8px;
    height: 8px;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
    pointer-events: none;
    z-index: 1;
}

.particle-1 { top: 10%; left: 10%; animation-delay: 0s; animation-duration: 4s; }
.particle-2 { top: 20%; left: 80%; animation-delay: 1s; animation-duration: 5s; }
.particle-3 { top: 60%; left: 20%; animation-delay: 2s; animation-duration: 6s; }
.particle-4 { top: 80%; left: 70%; animation-delay: 0.5s; animation-duration: 4.5s; }
.particle-5 { top: 30%; left: 50%; animation-delay: 1.5s; animation-duration: 5.5s; }

/* Response box animation */
.response-box {
    background: rgba(255, 255, 255, 0.95);
    border-left: 5px solid #00bcd4;
    padding: 2rem;
    border-radius: 15px;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    animation: slideInUp 0.8s ease-out;
    backdrop-filter: blur(10px);
}

@keyframes slideInUp {
    0% {
        transform: translateY(50px);
        opacity: 0;
    }
    100% {
        transform: translateY(0);
        opacity: 1;
    }
}

/* Chat input styling */
.stChatInput input {
    border-radius: 25px !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    padding: 15px 20px !important;
    font-size: 16px !important;
    backdrop-filter: blur(10px) !important;
}

.stChatInput input::placeholder {
    color: rgba(255,255,255,0.7) !important;
}

.stChatInput input:focus {
    border-color: #00bcd4 !important;
    box-shadow: 0 0 20px rgba(0,188,212,0.5) !important;
    background: rgba(255,255,255,0.2) !important;
}
</style>

<!-- Floating particles -->
<div class="floating-particle particle-1"></div>
<div class="floating-particle particle-2"></div>
<div class="floating-particle particle-3"></div>
<div class="floating-particle particle-4"></div>
<div class="floating-particle particle-5"></div>

<!-- Animated title -->
<div style="text-align: center; margin: 40px 0; padding: 30px;">
    <span class="dancing-letter">📊</span>
    <span class="dancing-letter">D</span>
    <span class="dancing-letter">a</span>
    <span class="dancing-letter">t</span>
    <span class="dancing-letter">a</span>
    <span class="dancing-letter">F</span>
    <span class="dancing-letter">r</span>
    <span class="dancing-letter">a</span>
    <span class="dancing-letter">m</span>
    <span class="dancing-letter">e</span>
</div>

<div style="text-align: center; color: rgba(255,255,255,0.8); margin-bottom: 30px;">
    <p style="font-size: 1.2rem; margin: 0;">✨ AI-Powered DataFrame Analysis with Graphs ✨</p>
    <p style="font-size: 1rem; margin: 10px 0 0 0; opacity: 0.8;">Try: "Create a bar chart of passenger class vs survival rate" or "Show age distribution"</p>
</div>
""", unsafe_allow_html=True)

# Function to extract and execute Python code for graphs
def extract_and_execute_code(response_text):
    """Extract Python code from response and execute it to display graphs"""
    # Pattern to find Python code blocks
    code_pattern = r'``````'
    code_blocks = re.findall(code_pattern, response_text, re.DOTALL)
    
    if code_blocks:
        for code_block in code_blocks:
            try:
                # Create execution context with necessary variables
                exec_context = {
                    'df': df,
                    'pd': pd,
                    'px': px,
                    'go': go,
                    'st': st,
                    'plt': None  
                }
                
                # Replace fig.show() with st.plotly_chart(fig) for Plotly
                modified_code = code_block.replace('fig.show()', 'st.plotly_chart(fig, use_container_width=True)')
                
                # Replace plt.show() with st.pyplot() for matplotlib
                if 'matplotlib' in modified_code or 'plt.' in modified_code:
                    import matplotlib.pyplot as plt
                    exec_context['plt'] = plt
                    modified_code = modified_code.replace('plt.show()', 'st.pyplot()')
                
                # Execute the code
                exec(modified_code, exec_context)
                
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
    
    return len(code_blocks) > 0

# Function to create sample graphs for common questions
def create_sample_visualization(question, answer):
    """Create visualizations for common data analysis questions"""
    question_lower = question.lower()
    
    if 'survival' in question_lower and 'class' in question_lower:
        # Survival by passenger class
        survival_by_class = df.groupby('Pclass')['Survived'].agg(['count', 'sum']).reset_index()
        survival_by_class['survival_rate'] = survival_by_class['sum'] / survival_by_class['count']
        
        fig = px.bar(
            survival_by_class, 
            x='Pclass', 
            y='survival_rate',
            title='Survival Rate by Passenger Class',
            labels={'Pclass': 'Passenger Class', 'survival_rate': 'Survival Rate'},
            color='survival_rate',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
        return True
        
    elif 'age' in question_lower and ('distribution' in question_lower or 'histogram' in question_lower):
        # Age distribution
        fig = px.histogram(
            df.dropna(subset=['Age']), 
            x='Age', 
            nbins=30,
            title='Age Distribution of Passengers',
            labels={'Age': 'Age', 'count': 'Number of Passengers'}
        )
        st.plotly_chart(fig, use_container_width=True)
        return True
        
    elif 'fare' in question_lower and ('class' in question_lower or 'pclass' in question_lower):
        # Fare by class
        fig = px.box(
            df, 
            x='Pclass', 
            y='Fare',
            title='Fare Distribution by Passenger Class',
            labels={'Pclass': 'Passenger Class', 'Fare': 'Fare'}
        )
        st.plotly_chart(fig, use_container_width=True)
        return True
        
    elif 'gender' in question_lower or 'sex' in question_lower:
        # Survival by gender
        survival_by_gender = df.groupby('Sex')['Survived'].agg(['count', 'sum']).reset_index()
        survival_by_gender['survival_rate'] = survival_by_gender['sum'] / survival_by_gender['count']
        
        fig = px.bar(
            survival_by_gender,
            x='Sex',
            y='survival_rate',
            title='Survival Rate by Gender',
            labels={'Sex': 'Gender', 'survival_rate': 'Survival Rate'},
            color='survival_rate',
            color_continuous_scale='plasma'
        )
        st.plotly_chart(fig, use_container_width=True)
        return True
    
    return False

# Chat interface
prompt = st.chat_input("Ask about the Titanic DataFrame...")
if prompt:
    logger.info(f"User query received: {prompt}")
    with st.container():
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.8); margin: 20px;">
            <p style="margin: 0;">🤔 Analyzing your question...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get the response from the agent
        start_time = time.time()
        logger.info("Starting agent processing...")
        try:
            logger.debug("Invoking agent with user query")
            response = agent.invoke({"input": prompt})
            processing_time = time.time() - start_time
            logger.info(f"Agent processing completed in {processing_time:.2f} seconds")
            answer = response.get("output", "No response generated.")
            logger.info("Agent response generated successfully")
            logger.debug(f"Agent response preview: {answer[:100]}...")  # Log first 100 chars
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            
            # Log the error with details
            logger.error(f"Agent processing failed after {processing_time:.2f} seconds")
            logger.exception(f"Agent error details: {error_msg}")
            logger.error(f"Failed query: {prompt}")
            
            answer = f"An error occurred: {error_msg}"
    
    # Clear the loading indicator
    st.empty()
    
    # Try to extract and execute any code for graphs
    has_code = extract_and_execute_code(answer)
    
    if not has_code:
        has_visualization = create_sample_visualization(prompt, answer)
    else:
        has_visualization = True
    
    # Display response with animated entrance
    st.markdown(f"""
    <div class="response-box">
        <h4 style="color: #333; margin-bottom: 1rem; font-size: 1.3rem;">
            {'📊 Analysis Result:' if has_visualization else '📈 Analysis Result:'}
        </h4>
        <p style="color: #555; line-height: 1.8; font-size: 1.1rem;">{answer}</p>
    </div>
    """, unsafe_allow_html=True)
    total_time = time.time() - start_time
    logger.info(f"Complete interaction finished in {total_time:.2f} seconds")
    logger.info("="*50)

# Add some helpful suggestions
with st.expander("💡 Example Questions to Try", expanded=False):
    st.markdown("""
    **Text Analysis Questions:**
    - How many passengers survived?
    - What's the average age of passengers?
    - How many passengers were in each class?
    
    **Graph-Generating Questions:**
    - Create a bar chart showing survival rate by passenger class
    - Show me the age distribution of passengers
    - Display fare distribution by passenger class
    - Create a chart showing survival rate by gender
    - Plot the relationship between age and fare
    """)
