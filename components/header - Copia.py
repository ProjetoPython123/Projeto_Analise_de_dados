import streamlit as st
from PIL import Image
import os

def render_header():
    """Render the application header with university logo and student information"""
    
    # Create header layout with logo and info
    col1, col2, col3 = st.columns([1.5, 2, 2])
    
    with col1:
        # Display logo if it exists
        if os.path.exists("logo_estacio.png"):
            try:
                logo = Image.open("logo_estacio.png")
                # Center the logo and text properly
                st.markdown("<div style='display: flex; flex-direction: column; align-items: center;'>", unsafe_allow_html=True)
                st.image(logo, width=150)
                st.markdown("<p style='text-align: center; font-weight: bold; font-size: 16px; margin-top: 5px; margin-bottom: 0;'>SUPERCAMPUS MARACANÃ</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown("<div style='text-align: center;'><strong>SUPERCAMPUS MARACANÃ</strong></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center;'><strong>SUPERCAMPUS MARACANÃ</strong></div>", unsafe_allow_html=True)
    
    with col2:
        # Empty space for title area
        pass
    
    with col3:
        # Student and faculty information with better formatting
        st.markdown("""
        <div style='text-align: right; font-size: 11px; line-height: 1.4;'>
        <strong>DISCENTES:</strong><br>
        Kézia Casemiro Rodrigues<br>
        202402437097<br><br>
        Mateus Musqueira Machado<br>
        202402429353<br><br>
        Leonardo Braga Nogueira Santos<br>
        202403520621<br><br>
        Renan Cristiano Soares da Silva<br>
        202402435541<br><br>
        Eduardo Henrique Aires Campos<br>
        202402303988<br><br><br>
        <strong>DOCENTE:</strong><br>
        Antonio Candido Oliveira Filho
        </div>
        """, unsafe_allow_html=True)
    
    # Add some spacing after header
    st.markdown("<br>", unsafe_allow_html=True)