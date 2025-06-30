import streamlit as st
import re
import pandas as pd
from typing import Dict, Tuple

# Page configuration
st.set_page_config(
    page_title="Chemistry Lab Calculators",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for amazing styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .calculator-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #4f46e5;
    }
    
    .result-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0ea5e9;
        margin-top: 1rem;
    }
    
    .success-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #22c55e;
        margin-top: 1rem;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin-top: 1rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 3px solid #4f46e5;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.3);
    }
    
    .sidebar .stButton > button {
        background: linear-gradient(135deg, #06b6d4, #0891b2);
    }
</style>
""", unsafe_allow_html=True)

class ChemistryCalculators:
    """Chemistry Calculators Class with all calculation methods"""
    
    @staticmethod
    def get_atomic_weights() -> Dict[str, float]:
        """Comprehensive atomic weights database (g/mol)"""
        return {
            # Main group elements
            'H': 1.0079, 'He': 4.0026, 'Li': 6.941, 'Be': 9.0122,
            'B': 10.811, 'C': 12.0107, 'N': 14.0067, 'O': 15.9994,
            'F': 18.9984, 'Ne': 20.1797, 'Na': 22.9897, 'Mg': 24.305,
            'Al': 26.9815, 'Si': 28.0855, 'P': 30.9738, 'S': 32.065,
            'Cl': 35.453, 'Ar': 39.948, 'K': 39.0983, 'Ca': 40.078,
            
            # Transition metals (common ones)
            'Sc': 44.9559, 'Ti': 47.867, 'V': 50.9415, 'Cr': 51.9961,
            'Mn': 54.938, 'Fe': 55.845, 'Co': 58.9332, 'Ni': 58.6934,
            'Cu': 63.546, 'Zn': 65.38, 'Ga': 69.723, 'Ge': 72.64,
            'As': 74.9216, 'Se': 78.96, 'Br': 79.904, 'Kr': 83.798,
            'Rb': 85.4678, 'Sr': 87.62, 'Y': 88.9059, 'Zr': 91.224,
            'Nb': 92.9064, 'Mo': 95.96, 'Tc': 98, 'Ru': 101.07,
            'Rh': 102.9055, 'Pd': 106.42, 'Ag': 107.8682, 'Cd': 112.411,
            'In': 114.818, 'Sn': 118.71, 'Sb': 121.76, 'Te': 127.6,
            'I': 126.9045, 'Xe': 131.293, 'Cs': 132.9055, 'Ba': 137.327,
            
            # Additional elements
            'La': 138.9055, 'Ce': 140.116, 'Pr': 140.9077, 'Nd': 144.242,
            'Pm': 145, 'Sm': 150.36, 'Eu': 151.964, 'Gd': 157.25,
            'Th': 232.0381, 'Pa': 231.0359, 'U': 238.0289, 'Np': 237,
            'Pu': 244, 'Am': 243, 'Cm': 247,
            'Hf': 178.49, 'Ta': 180.9479, 'W': 183.84, 'Re': 186.207,
            'Os': 190.23, 'Ir': 192.217, 'Pt': 195.084, 'Au': 196.9666,
            'Hg': 200.59, 'Tl': 204.3833, 'Pb': 207.2, 'Bi': 208.9804,
            'Po': 209, 'At': 210, 'Rn': 222
        }
    
    @staticmethod
    def compute_molecular_weight(formula: str) -> float:
        """Compute molecular weight from chemical formula"""
        pattern = r'([A-Z][a-z]?)(\d*)'
        tokens = re.findall(pattern, formula)
        
        if not tokens:
            raise ValueError("Invalid chemical formula format")
        
        atomic_weights = ChemistryCalculators.get_atomic_weights()
        mw = 0.0
        
        for element, count_str in tokens:
            count = 1 if not count_str else int(count_str)
            if count <= 0:
                raise ValueError(f"Invalid element count for {element}")
            if element in atomic_weights:
                mw += atomic_weights[element] * count
            else:
                raise ValueError(f"Unknown element '{element}'")
        
        return mw

def main():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🧪 Chemistry Laboratory Calculators</h1>
        <p>Professional tools for accurate chemical calculations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🔬 Navigation")
    calculator_choice = st.sidebar.selectbox(
        "Choose Calculator:",
        ["🧮 Molarity Calculator", "🧫 Media Preparation Calculator", "📊 About"]
    )
    
    if calculator_choice == "🧮 Molarity Calculator":
        molarity_calculator()
    elif calculator_choice == "🧫 Media Preparation Calculator":
        media_preparation_calculator()
    else:
        about_page()

def molarity_calculator():
    """Molarity Calculator Interface"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🧮 Molarity Calculator")
        st.markdown("*Calculate the exact mass needed for your target molarity*")
        
        # Input form
        with st.form("molarity_form"):
            formula = st.text_input(
                "Chemical Formula",
                placeholder="e.g., NaCl, CaCl2, H2SO4, C6H12O6",
                help="Enter the chemical formula using proper capitalization"
            )
            
            col_input1, col_input2 = st.columns(2)
            with col_input1:
                molarity = st.number_input(
                    "Desired Molarity (mol/L)",
                    min_value=0.0001,
                    max_value=20.0,
                    value=1.0,
                    step=0.01,
                    format="%.4f"
                )
            
            with col_input2:
                volume = st.number_input(
                    "Volume (L)",
                    min_value=0.001,
                    max_value=100.0,
                    value=1.0,
                    step=0.01,
                    format="%.3f"
                )
            
            submitted = st.form_submit_button("🔬 Calculate Mass", use_container_width=True)
            
            if submitted:
                if formula:
                    try:
                        mw = ChemistryCalculators.compute_molecular_weight(formula)
                        grams = mw * molarity * volume
                        
                        # Success result
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>✅ Calculation Results</h3>
                            <p><strong>Formula:</strong> {formula}</p>
                            <p><strong>Molecular Weight:</strong> {mw:.3f} g/mol</p>
                            <p><strong>Mass needed:</strong> <span style="font-size: 1.2em; color: #059669;"><strong>{grams:.4f} g</strong></span></p>
                            <p><strong>Mass needed:</strong> <span style="color: #059669;">{grams * 1000:.2f} mg</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Additional metrics
                        col_m1, col_m2, col_m3 = st.columns(3)
                        with col_m1:
                            st.metric("Molecular Weight", f"{mw:.3f} g/mol")
                        with col_m2:
                            st.metric("Mass (g)", f"{grams:.4f}")
                        with col_m3:
                            st.metric("Mass (mg)", f"{grams * 1000:.2f}")
                            
                    except Exception as e:
                        st.markdown(f"""
                        <div class="warning-box">
                            <h3>⚠️ Error in Formula</h3>
                            <p>{str(e)}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Please enter a chemical formula")
    
    with col2:
        st.markdown("### 📖 Quick Reference")
        
        # Common formulas reference
        reference_data = {
            "Formula": ["NaCl", "CaCl₂", "H₂SO₄", "C₆H₁₂O₆", "KMnO₄"],
            "MW (g/mol)": ["58.44", "110.98", "98.08", "180.16", "158.03"],
            "Common Use": ["Salt", "Calcium", "Acid", "Glucose", "Oxidizer"]
        }
        
        df = pd.DataFrame(reference_data)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### 💡 Tips")
        st.info("""
        • Use proper capitalization (Na, not na)
        • Numbers come after elements (CaCl2)
        • Check formula spelling carefully
        • Common prefixes: mono-, di-, tri-
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def media_preparation_calculator():
    """Media Preparation Calculator Interface"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("🧫 Media Preparation Calculator")
    st.markdown("*Prepare bacterial growth media with precision*")
    
    # Media selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        media_type = st.selectbox(
            "Select Media Type:",
            ["LB Medium", "LBGM Medium", "MSGG(2x) Medium"],
            help="Choose the type of bacterial growth medium"
        )
        
        include_agar = st.radio(
            "Agar Option:",
            ["Without Agar (Liquid)", "With Agar (Solid)"],
            horizontal=True
        )
        
        volume = st.number_input(
            "Volume (L):",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1,
            format="%.1f"
        )
        
        if st.button("🧪 Calculate Media Components", use_container_width=True):
            agar_flag = "With Agar" in include_agar
            
            if media_type == "LB Medium":
                calculate_lb_media(volume, agar_flag)
            elif media_type == "LBGM Medium":
                calculate_lbgm_media(volume, agar_flag)
            elif media_type == "MSGG(2x) Medium":
                calculate_msgg_media(volume, agar_flag)
    
    with col2:
        st.markdown("### 📋 Media Information")
        
        if media_type == "LB Medium":
            st.info("""
            **LB (Lysogeny Broth)**
            - General purpose medium
            - Rich nutrient content
            - Supports most E. coli strains
            - pH: ~7.0
            """)
        elif media_type == "LBGM Medium":
            st.info("""
            **LBGM Medium**
            - LB + Glycerol + MnCl₂
            - Enhanced for specific applications
            - Glycerol as carbon source
            - Mn²⁺ cofactor support
            """)
        else:
            st.info("""
            **MSGG(2x) Medium**
            - Minimal synthetic defined medium
            - 2x concentrated
            - 14+ individual components
            - Precise nutritional control
            """)
        
        st.markdown("### ⚗️ Preparation Tips")
        st.success("""
        • Autoclave at 121°C, 15 psi, 15-20 min
        • Cool to ~50°C before adding heat-sensitive components
        • Store at 4°C for up to 1 month
        • Check pH before use
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def calculate_lb_media(volume: float, include_agar: bool):
    """Calculate LB media components"""
    
    grams_lb = 20 * volume
    
    if include_agar:
        grams_agar = 15 * volume
        components = [
            ("LB powder", f"{grams_lb:.2f} g"),
            ("Agar", f"{grams_agar:.2f} g")
        ]
        title = f"LB-Agar Medium ({volume:.1f} L)"
    else:
        components = [
            ("LB powder", f"{grams_lb:.2f} g")
        ]
        title = f"LB Medium ({volume:.1f} L)"
    
    display_media_results(title, components)

def calculate_lbgm_media(volume: float, include_agar: bool):
    """Calculate LBGM media components"""
    
    grams_lb = 20 * volume
    ml_glycerol = 20 * volume
    ml_mncl2 = 10 * volume
    
    components = [
        ("LB powder", f"{grams_lb:.2f} g"),
        ("Glycerol (50%)", f"{ml_glycerol:.2f} mL"),
        ("MnCl₂ (10 mM)", f"{ml_mncl2:.2f} mL")
    ]
    
    if include_agar:
        grams_agar = 15 * volume
        components.append(("Agar", f"{grams_agar:.2f} g"))
        title = f"LBGM-Agar Medium ({volume:.1f} L)"
    else:
        title = f"LBGM Medium ({volume:.1f} L)"
    
    components.append(("DDW (to final volume)", f"{volume:.1f} L"))
    
    display_media_results(title, components)

def calculate_msgg_media(volume: float, include_agar: bool):
    """Calculate MSGG(2x) media components"""
    
    scale_factor = volume / 0.5  # Reference is for 0.5L
    
    components = [
        ("1M K₂HPO₄", f"{3.075 * scale_factor:.3f} mL"),
        ("1M KH₂PO₄", f"{1.925 * scale_factor:.3f} mL"),
        ("1M MOPS", f"{100 * scale_factor:.1f} mL (filter fresh, pH 7.0)"),
        ("1M MgCl₂", f"{2 * scale_factor:.1f} mL"),
        ("10mM MnCl₂", f"{5 * scale_factor:.1f} mL"),
        ("10mM ZnCl₂", f"{0.1 * scale_factor:.2f} mL"),
        ("1M CaCl₂", f"{0.7 * scale_factor:.1f} mL"),
        ("10mM Thiamine", f"{5 * scale_factor:.1f} mL"),
        ("10mg/ml Phenylalanine", f"{5 * scale_factor:.1f} mL (filter fresh)"),
        ("10mg/ml Tryptophan", f"{5 * scale_factor:.1f} mL (filter fresh)"),
        ("50% Glycerol", f"{10 * scale_factor:.1f} mL"),
        ("10% Glutamic acid", f"{50 * scale_factor:.1f} mL (filter fresh)"),
        ("10mg/ml Threonine", f"{5 * scale_factor:.1f} mL (filter fresh)")
    ]
    
    if include_agar:
        grams_agar = 15 * volume
        ml_fecl3 = 12.5 * scale_factor
        components.extend([
            ("5mM FeCl₃", f"{ml_fecl3:.1f} mL (add when using)"),
            ("Agar", f"{grams_agar:.2f} g")
        ])
        title = f"MSGG(2x)-Agar Medium ({volume:.1f} L)"
    else:
        ml_fecl3 = 10 * scale_factor
        components.append(("5mM FeCl₃", f"{ml_fecl3:.1f} mL (add when using)"))
        title = f"MSGG(2x) Medium ({volume:.1f} L)"
    
    components.append(("DDW", f"{302 * scale_factor:.1f} mL"))
    
    display_media_results(title, components, is_complex=True)

def display_media_results(title: str, components: list, is_complex: bool = False):
    """Display media preparation results in a beautiful format"""
    
    st.markdown(f"""
    <div class="success-box">
        <h3>✅ {title}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create DataFrame for better display
    df = pd.DataFrame(components, columns=["Component", "Amount"])
    
    # Split into columns if it's a complex medium
    if is_complex and len(components) > 8:
        mid = len(components) // 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Primary Components:**")
            df1 = pd.DataFrame(components[:mid], columns=["Component", "Amount"])
            st.dataframe(df1, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**Secondary Components:**")
            df2 = pd.DataFrame(components[mid:], columns=["Component", "Amount"])
            st.dataframe(df2, use_container_width=True, hide_index=True)
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Preparation notes for complex media
    if is_complex:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Important Notes:</h4>
            <ul>
                <li>Filter sterilize components marked as "filter fresh"</li>
                <li>Add FeCl₃ separately when using the medium</li>
                <li>Adjust MOPS to pH 7.0 with 1N NaOH before use</li>
                <li>Store components separately if not using immediately</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def about_page():
    """About page with information"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("📊 About Chemistry Lab Calculators")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Purpose
        This web application provides professional-grade calculators for chemistry laboratory work, 
        specifically designed for accurate preparation of solutions and bacterial growth media.
        
        ### 🧮 Molarity Calculator
        - Calculate exact mass needed for target molarity solutions
        - Supports complex chemical formulas
        - Comprehensive atomic weights database (100+ elements)
        - Precise calculations for research-grade accuracy
        
        ### 🧫 Media Preparation Calculator
        - **LB Medium**: General purpose bacterial growth medium
        - **LBGM Medium**: Enhanced medium with glycerol and manganese
        - **MSGG(2x)**: Minimal synthetic defined medium with 14+ components
        - Automatic scaling for any volume
        - Agar/liquid options for all media types
        
        ### 🔬 Features
        - **Responsive Design**: Works on desktop, tablet, and mobile devices
        - **Real-time Calculations**: Instant results as you type
        - **Professional Accuracy**: Research-grade precision
        - **User-friendly Interface**: Intuitive design for laboratory use
        """)
        
    with col2:
        st.markdown("### 📱 Access Information")
        st.info("""
        **Local Access:**
        - Run on your computer
        - Access via localhost
        - Share via local network
        
        **Online Deployment:**
        - Deploy to Streamlit Cloud (free)
        - Access from any device
        - Share via URL
        
        **Mobile Optimized:**
        - Works on phones/tablets
        - Touch-friendly interface
        - Responsive layout
        """)
        
        st.markdown("### 🛠️ Technical Details")
        st.code("""
        Framework: Streamlit
        Language: Python 3.7+
        Dependencies: streamlit, pandas
        Deployment: Streamlit Cloud
        """)
        
        st.markdown("### 📞 Support")
        st.success("""
        For technical support or feature requests, 
        contact your system administrator or 
        the development team.
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()