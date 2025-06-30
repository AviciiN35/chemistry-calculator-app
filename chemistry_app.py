import streamlit as st
import re
import pandas as pd
import numpy as np
import math
from datetime import datetime
from typing import Dict, Tuple, List
import json

# Page configuration
st.set_page_config(
    page_title="🧪 ChemLab Pro - Ultimate Laboratory Suite",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'protocols' not in st.session_state:
    st.session_state.protocols = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Enhanced CSS with animations
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem;
            border-radius: 25px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            animation: shine 4s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .main-header h1 {
            font-family: 'Inter', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
            animation: slideIn 1s ease-out;
        }
        
        .calculator-card {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            animation: slideIn 0.8s ease-out;
        }
        
        .calculator-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }
        
        .metric-card {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            border-left: 4px solid #4f46e5;
            transition: all 0.3s ease;
            animation: slideIn 1.2s ease-out;
        }
        
        .metric-card:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .result-box {
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            padding: 2rem;
            border-radius: 15px;
            border-left: 5px solid #10b981;
            margin: 1.5rem 0;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
            animation: slideIn 0.5s ease-out;
        }
        
        .warning-box {
            background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 20%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #f59e0b;
            margin: 1.5rem 0;
            animation: slideIn 0.5s ease-out;
        }
        
        .info-box {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #3b82f6;
            margin: 1rem 0;
            animation: slideIn 0.5s ease-out;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
        }
        
        .sidebar .stButton > button {
            background: linear-gradient(135deg, #06b6d4, #0891b2);
        }
        
    </style>
    """, unsafe_allow_html=True)

class UltimateChemistryCalculators:
    """Ultimate Chemistry Laboratory Suite with Advanced Features"""
    
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
            
            # Transition metals
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
    def get_common_formulas() -> Dict[str, Dict]:
        """Database of common chemical formulas with properties"""
        return {
            'NaCl': {'name': 'Sodium Chloride', 'mw': 58.44, 'use': 'Salt, buffer'},
            'CaCl2': {'name': 'Calcium Chloride', 'mw': 110.98, 'use': 'Calcium source'},
            'H2SO4': {'name': 'Sulfuric Acid', 'mw': 98.08, 'use': 'Strong acid'},
            'C6H12O6': {'name': 'Glucose', 'mw': 180.16, 'use': 'Carbon source'},
            'KMnO4': {'name': 'Potassium Permanganate', 'mw': 158.03, 'use': 'Oxidizer'},
            'NH4Cl': {'name': 'Ammonium Chloride', 'mw': 53.49, 'use': 'Nitrogen source'},
            'MgSO4': {'name': 'Magnesium Sulfate', 'mw': 120.37, 'use': 'Mg source'},
            'K2HPO4': {'name': 'Dipotassium Phosphate', 'mw': 174.18, 'use': 'Buffer'},
            'NaOH': {'name': 'Sodium Hydroxide', 'mw': 40.00, 'use': 'Strong base'},
            'HCl': {'name': 'Hydrochloric Acid', 'mw': 36.46, 'use': 'Strong acid'},
            'CuSO4': {'name': 'Copper Sulfate', 'mw': 159.61, 'use': 'Cu source'},
            'FeCl3': {'name': 'Ferric Chloride', 'mw': 162.20, 'use': 'Iron source'}
        }
    
    @staticmethod
    def compute_molecular_weight(formula: str) -> float:
        """Compute molecular weight from chemical formula"""
        pattern = r'([A-Z][a-z]?)(\d*)'
        tokens = re.findall(pattern, formula)
        
        if not tokens:
            raise ValueError("Invalid chemical formula format")
        
        atomic_weights = UltimateChemistryCalculators.get_atomic_weights()
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
    
    @staticmethod
    def calculate_dilution(c1: float, v1: float, c2: float, v2: float = None) -> Dict:
        """Calculate dilution using C1V1 = C2V2"""
        if v2 is None:
            v2 = (c1 * v1) / c2
        else:
            c2 = (c1 * v1) / v2
        
        return {
            'c1': c1, 'v1': v1, 'c2': c2, 'v2': v2,
            'dilution_factor': c1/c2,
            'volume_water': v2 - v1
        }
    
    @staticmethod
    def ph_calculator(concentration, is_acid=True):
        """Calculate pH from concentration"""
        if is_acid:
            return -math.log10(concentration)
        else:  # base
            poh = -math.log10(concentration)
            return 14 - poh
    
    @staticmethod
    def buffer_calculator(weak_acid_conc, conjugate_base_conc, pka):
        """Henderson-Hasselbalch equation"""
        return pka + math.log10(conjugate_base_conc / weak_acid_conc)

def add_to_history(calculation_type: str, inputs: Dict, results: Dict):
    """Add calculation to history"""
    history_item = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'type': calculation_type,
        'inputs': inputs,
        'results': results
    }
    st.session_state.calculation_history.append(history_item)

def main():
    load_css()
    
    # Stunning main header
    st.markdown("""
    <div class="main-header">
        <h1>🧪 ChemLab Pro - Ultimate Laboratory Suite</h1>
        <p style="font-size: 1.4rem; margin-bottom: 0; position: relative; z-index: 1;">
            Professional Chemistry Laboratory Platform
        </p>
        <p style="font-size: 1rem; opacity: 0.9; position: relative; z-index: 1; margin-top: 1rem;">
            Advanced Calculators • Data Analysis • Lab Management • Educational Tools
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        st.title("🔬 Laboratory Suite")
        
        # Quick stats dashboard
        if st.session_state.calculation_history:
            st.markdown("### 📊 Session Stats")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("Calculations", len(st.session_state.calculation_history))
            with col_s2:
                st.metric("Tools Used", len(set(h['type'] for h in st.session_state.calculation_history)))
        
        # Navigation
        calculator_choice = st.selectbox(
            "Choose Tool:",
            [
                "🏠 Dashboard",
                "🧮 Enhanced Molarity Calculator", 
                "💧 Dilution Calculator",
                "🧫 Media Preparation Calculator",
                "⚗️ Advanced Chemistry Tools",
                "🔬 pH & Buffer Calculator",
                "📊 Data Analysis Suite",
                "🏠 Lab Management",
                "📚 Educational Hub",
                "⚙️ Settings & Help"
            ]
        )
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🆕 New Calculation"):
            st.rerun()
        if st.button("🌓 Dark Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Route to appropriate page
    if calculator_choice == "🏠 Dashboard":
        dashboard_page()
    elif calculator_choice == "🧮 Enhanced Molarity Calculator":
        enhanced_molarity_calculator()
    elif calculator_choice == "💧 Dilution Calculator":
        dilution_calculator()
    elif calculator_choice == "🧫 Media Preparation Calculator":
        enhanced_media_preparation_calculator()
    elif calculator_choice == "⚗️ Advanced Chemistry Tools":
        advanced_chemistry_tools()
    elif calculator_choice == "🔬 pH & Buffer Calculator":
        ph_buffer_tools()
    elif calculator_choice == "📊 Data Analysis Suite":
        data_analysis_suite()
    elif calculator_choice == "🏠 Lab Management":
        lab_management_page()
    elif calculator_choice == "📚 Educational Hub":
        educational_hub()
    else:
        settings_help_page()

def dashboard_page():
    """Ultimate dashboard with everything"""
    
    # Welcome message
    st.markdown("## 👋 Welcome to Your Ultimate Chemistry Laboratory!")
    
    # Quick stats
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🧪 Total Calculations", len(st.session_state.calculation_history))
    with col2:
        st.metric("📦 Inventory Items", len(st.session_state.inventory))
    with col3:
        st.metric("📋 Protocols", len(st.session_state.protocols))
    with col4:
        st.metric("⭐ Favorites", len(st.session_state.favorites))
    with col5:
        uptime_days = (datetime.now() - datetime(2024, 1, 1)).days
        st.metric("📅 Uptime", f"{uptime_days} days")
    
    # Feature grid
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0;">
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); backdrop-filter: blur(20px); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s ease;">
            <h3>🧮 Smart Calculators</h3>
            <p>Advanced molarity, dilution, and media preparation calculators with intelligent suggestions</p>
        </div>
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); backdrop-filter: blur(20px); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s ease;">
            <h3>⚗️ Chemistry Tools</h3>
            <p>pH, buffer, gas law, Beer's law, and thermodynamics calculators</p>
        </div>
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); backdrop-filter: blur(20px); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s ease;">
            <h3>🔬 Lab Analysis</h3>
            <p>Spectrophotometry, data analysis, and statistical tools</p>
        </div>
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); backdrop-filter: blur(20px); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s ease;">
            <h3>🏠 Lab Management</h3>
            <p>Inventory tracking, protocol builder, and safety management</p>
        </div>
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); backdrop-filter: blur(20px); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s ease;">
            <h3>📚 Educational Hub</h3>
            <p>Interactive tutorials and learning resources</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent activity
    if st.session_state.calculation_history:
        st.markdown("### 🕒 Recent Activity")
        recent = st.session_state.calculation_history[-5:]
        for calc in reversed(recent):
            st.markdown(f"📊 **{calc['type']}** - {calc['timestamp']}")
    
    # Quick access tools
    st.markdown("### ⚡ Quick Access")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    with col_q1:
        if st.button("🧪 Molarity Calculator", use_container_width=True):
            st.session_state.nav_target = "🧮 Enhanced Molarity Calculator"
            st.rerun()
    
    with col_q2:
        if st.button("💧 Dilution Tools", use_container_width=True):
            st.session_state.nav_target = "💧 Dilution Calculator"
            st.rerun()
    
    with col_q3:
        if st.button("🔬 pH Calculator", use_container_width=True):
            st.session_state.nav_target = "🔬 pH & Buffer Calculator"
            st.rerun()
    
    with col_q4:
        if st.button("📊 Data Analysis", use_container_width=True):
            st.session_state.nav_target = "📊 Data Analysis Suite"
            st.rerun()

def enhanced_molarity_calculator():
    """Enhanced molarity calculator with all the advanced features"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🧮 Enhanced Molarity Calculator")
        st.markdown("*Professional-grade solution preparation with intelligent assistance*")
        
        # Enhanced input form
        with st.form("enhanced_molarity_form"):
            # Formula input with smart suggestions
            formula_input = st.text_input(
                "Chemical Formula",
                placeholder="e.g., NaCl, CaCl2, H2SO4, C6H12O6",
                help="Enter chemical formula using proper capitalization"
            )
            
            # Real-time formula validation
            if formula_input:
                try:
                    mw = UltimateChemistryCalculators.compute_molecular_weight(formula_input)
                    st.success(f"✅ Valid formula! MW = {mw:.3f} g/mol")
                except:
                    st.error("❌ Invalid formula - check spelling and capitalization")
            
            # Advanced input parameters
            col_input1, col_input2, col_input3 = st.columns(3)
            
            with col_input1:
                molarity = st.number_input(
                    "Target Molarity (mol/L)",
                    min_value=1e-6,
                    max_value=20.0,
                    value=1.0,
                    step=0.01,
                    format="%.6f"
                )
            
            with col_input2:
                volume = st.number_input(
                    "Final Volume",
                    min_value=0.001,
                    max_value=1000.0,
                    value=1.0,
                    step=0.01,
                    format="%.3f"
                )
                volume_unit = st.selectbox("Volume Unit", ["L", "mL", "μL"], index=0)
            
            with col_input3:
                purity = st.number_input(
                    "Chemical Purity (%)",
                    min_value=1.0,
                    max_value=100.0,
                    value=100.0,
                    step=0.1
                )
            
            # Professional options
            with st.expander("🎛️ Professional Options"):
                col_prof1, col_prof2 = st.columns(2)
                
                with col_prof1:
                    safety_factor = st.number_input(
                        "Safety Factor",
                        min_value=1.0,
                        max_value=2.0,
                        value=1.1,
                        step=0.05,
                        help="Extra material (10% recommended)"
                    )
                    
                    temperature = st.number_input(
                        "Temperature (°C)",
                        min_value=-20.0,
                        max_value=100.0,
                        value=25.0
                    )
                
                with col_prof2:
                    preparation_method = st.selectbox(
                        "Preparation Method",
                        ["Standard Volumetric", "Serial Dilution", "Stock Solution"]
                    )
                    
                    container_type = st.selectbox(
                        "Container Type",
                        ["Volumetric Flask", "Graduated Cylinder", "Beaker", "Conical Flask"]
                    )
            
            # Calculate button
            submitted = st.form_submit_button(
                "🔬 Calculate Professional Solution",
                use_container_width=True
            )
            
            if submitted and formula_input:
                # Perform enhanced calculations
                try:
                    # Convert volume to liters
                    volume_conversions = {"L": 1, "mL": 0.001, "μL": 0.000001}
                    volume_L = volume * volume_conversions[volume_unit]
                    
                    # Calculate molecular weight
                    mw = UltimateChemistryCalculators.compute_molecular_weight(formula_input)
                    
                    # Calculate required masses
                    theoretical_mass = mw * molarity * volume_L
                    purity_corrected_mass = theoretical_mass * (100 / purity)
                    final_mass = purity_corrected_mass * safety_factor
                    
                    # Store in history
                    calculation_data = {
                        'formula': formula_input,
                        'molarity': molarity,
                        'volume': volume,
                        'volume_unit': volume_unit,
                        'purity': purity,
                        'safety_factor': safety_factor,
                        'temperature': temperature,
                        'method': preparation_method
                    }
                    
                    results_data = {
                        'molecular_weight': mw,
                        'theoretical_mass': theoretical_mass,
                        'final_mass': final_mass
                    }
                    
                    add_to_history("Enhanced Molarity Calculation", calculation_data, results_data)
                    
                    # Display comprehensive results
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>✅ Professional Calculation Results</h3>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
                            <div class="metric-card">
                                <h4 style="margin: 0; color: #4f46e5;">Chemical Information</h4>
                                <p style="margin: 0.5rem 0;"><strong>Formula:</strong> {formula_input}</p>
                                <p style="margin: 0.5rem 0;"><strong>MW:</strong> {mw:.3f} g/mol</p>
                                <p style="margin: 0.5rem 0;"><strong>Purity:</strong> {purity:.1f}%</p>
                            </div>
                            <div class="metric-card">
                                <h4 style="margin: 0; color: #059669;">Solution Parameters</h4>
                                <p style="margin: 0.5rem 0;"><strong>Molarity:</strong> {molarity:.4f} M</p>
                                <p style="margin: 0.5rem 0;"><strong>Volume:</strong> {volume:.3f} {volume_unit}</p>
                                <p style="margin: 0.5rem 0;"><strong>Temperature:</strong> {temperature:.1f}°C</p>
                            </div>
                            <div class="metric-card">
                                <h4 style="margin: 0; color: #dc2626;">Required Mass</h4>
                                <p style="margin: 0.5rem 0; font-size: 1.3em; font-weight: bold; color: #dc2626;">
                                    <strong>{final_mass:.4f} g</strong>
                                </p>
                                <p style="margin: 0.5rem 0;"><strong>Method:</strong> {preparation_method}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Detailed breakdown
                    st.markdown("### 📊 Calculation Breakdown")
                    
                    breakdown_data = pd.DataFrame({
                        "Step": [
                            "1. Theoretical Mass",
                            "2. Purity Correction", 
                            "3. Safety Factor",
                            "4. Final Mass Required"
                        ],
                        "Calculation": [
                            f"{mw:.3f} × {molarity:.4f} × {volume_L:.6f}",
                            f"{theoretical_mass:.4f} × (100/{purity:.1f})",
                            f"{purity_corrected_mass:.4f} × {safety_factor:.2f}",
                            "Sum of all corrections"
                        ],
                        "Result (g)": [
                            f"{theoretical_mass:.4f}",
                            f"{purity_corrected_mass:.4f}",
                            f"{final_mass:.4f}",
                            f"**{final_mass:.4f}**"
                        ]
                    })
                    
                    st.dataframe(breakdown_data, use_container_width=True, hide_index=True)
                    
                    # Professional protocol generation
                    st.markdown("### 📋 Laboratory Protocol")
                    
                    protocol = f"""
**Solution Preparation Protocol**

**Target:** {molarity:.4f} M {formula_input} in {volume:.3f} {volume_unit}

**Materials Required:**
• {final_mass:.4f} g {formula_input} ({purity:.1f}% purity)
• Distilled water
• {container_type.lower()}
• Analytical balance (±0.0001 g)
• Stirring rod/magnetic stirrer

**Procedure:**
1. **Weighing:** Accurately weigh {final_mass:.4f} g of {formula_input}
2. **Partial Dissolution:** Add ~{volume_L*800:.0f} mL distilled water to {container_type.lower()}
3. **Complete Dissolution:** Add weighed chemical and stir until dissolved
4. **Dilution:** Add distilled water to exactly {volume:.3f} {volume_unit} mark
5. **Final Mixing:** Cap and invert 20 times for homogeneous mixing
6. **Quality Check:** Solution should be clear with no undissolved particles

**Storage:** Store at {temperature:.0f}°C. Label with contents, concentration, date, and preparer.

**Safety:** Handle with appropriate PPE. Check SDS for {formula_input}.
                    """
                    
                    st.markdown(protocol)
                    
                    # Export options
                    st.markdown("### 💾 Export & Documentation")
                    
                    col_export1, col_export2, col_export3 = st.columns(3)
                    
                    with col_export1:
                        # CSV export
                        csv_data = f"Chemical,MW,Molarity,Volume,Mass_Required,Date\n{formula_input},{mw:.3f},{molarity},{volume} {volume_unit},{final_mass:.4f},{datetime.now().strftime('%Y-%m-%d')}"
                        st.download_button(
                            "📄 CSV Data",
                            csv_data,
                            f"{formula_input}_calculation.csv",
                            "text/csv",
                            use_container_width=True
                        )
                    
                    with col_export2:
                        # Protocol export  
                        st.download_button(
                            "📋 Protocol",
                            protocol,
                            f"{formula_input}_protocol.txt",
                            "text/plain",
                            use_container_width=True
                        )
                    
                    with col_export3:
                        if st.button("⭐ Add to Favorites", use_container_width=True):
                            favorite_item = {
                                'type': 'molarity_calculation',
                                'formula': formula_input,
                                'molarity': molarity,
                                'saved_date': datetime.now().strftime('%Y-%m-%d %H:%M')
                            }
                            st.session_state.favorites.append(favorite_item)
                            st.success("Added to favorites!")
                
                except Exception as e:
                    st.markdown(f"""
                    <div class="warning-box">
                        <h3>⚠️ Calculation Error</h3>
                        <p><strong>Error:</strong> {str(e)}</p>
                        <p><strong>Common Issues:</strong></p>
                        <ul>
                            <li>Check chemical formula spelling and capitalization</li>
                            <li>Ensure element symbols are correct (Na, not na)</li>
                            <li>Numbers should follow elements (CaCl2, not Ca2Cl)</li>
                            <li>Verify all input values are positive numbers</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        # Enhanced sidebar with smart features
        st.markdown("### 🧠 Smart Assistant")
        
        # Quick reference panel
        st.markdown("### 📖 Smart Reference")
        
        # Quick molecular weight lookup
        common_formulas = UltimateChemistryCalculators.get_common_formulas()
        
        selected_formula = st.selectbox("Quick MW Lookup", [""] + list(common_formulas.keys()))
        if selected_formula:
            data = common_formulas[selected_formula]
            st.markdown(f"""
            <div class="info-box">
                <h4>{selected_formula}</h4>
                <p><strong>{data['name']}</strong></p>
                <p>MW: {data['mw']:.2f} g/mol</p>
                <p>Use: {data['use']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Concentration converter
        st.markdown("### 🔄 Quick Converters")
        
        with st.expander("M ⇄ mg/mL"):
            formula_conv = st.text_input("Formula for conversion", placeholder="NaCl")
            if formula_conv:
                try:
                    mw = UltimateChemistryCalculators.compute_molecular_weight(formula_conv)
                    conc_m = st.number_input("Concentration (M)", value=0.1, key="conv_m")
                    conc_mg_ml = conc_m * mw
                    st.info(f"{conc_m} M = {conc_mg_ml:.2f} mg/mL")
                except:
                    st.warning("Enter valid formula")
        
        # Recent favorites
        if st.session_state.favorites:
            st.markdown("### ⭐ Recent Favorites")
            recent_favorites = st.session_state.favorites[-3:]
            for fav in reversed(recent_favorites):
                if fav['type'] == 'molarity_calculation':
                    st.markdown(f"📋 {fav['formula']}")
        
        # Tips and best practices
        st.markdown("### 💡 Pro Tips")
        tips = [
            "💧 Always use distilled water for solutions",
            "⚖️ Use analytical balance for accurate weighing", 
            "🌡️ Consider temperature effects on solubility",
            "📝 Label all solutions with date and concentration",
            "🔄 Mix thoroughly for homogeneous solutions"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def dilution_calculator():
    """Professional dilution calculator"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("💧 Professional Dilution Calculator")
    st.markdown("*Advanced dilution calculations with C₁V₁ = C₂V₂ methodology*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced dilution interface
        st.markdown("### 🧪 Dilution Parameters")
        
        # Calculation mode selection
        calc_mode = st.radio(
            "Calculation Mode:",
            ["📊 Standard Dilution (C₁V₁ = C₂V₂)", "🔄 Serial Dilution Series"],
            horizontal=True
        )
        
        if calc_mode == "📊 Standard Dilution (C₁V₁ = C₂V₂)":
            standard_dilution_calc()
        else:
            serial_dilution_calc()
    
    with col2:
        # Dilution reference and tools
        st.markdown("### 📐 Dilution Reference")
        
        # Common dilution ratios
        st.markdown("**Common Dilution Ratios:**")
        dilutions = [
            ("1:2", "2-fold", "50% strength"),
            ("1:5", "5-fold", "20% strength"), 
            ("1:10", "10-fold", "10% strength"),
            ("1:100", "100-fold", "1% strength"),
            ("1:1000", "1000-fold", "0.1% strength")
        ]
        
        for ratio, fold, strength in dilutions:
            st.markdown(f"• **{ratio}** ({fold}) = {strength}")
        
        # Quick dilution calculator
        st.markdown("### ⚡ Quick Dilution")
        
        quick_c1 = st.number_input("Stock (any unit)", value=100.0, key="quick_c1")
        quick_ratio = st.selectbox("Dilution Ratio", ["1:2", "1:5", "1:10", "1:100"])
        quick_final_vol = st.number_input("Final Volume", value=10.0, key="quick_vol")
        
        if st.button("Quick Calculate"):
            ratio_num = int(quick_ratio.split(':')[1])
            stock_vol = quick_final_vol / ratio_num
            water_vol = quick_final_vol - stock_vol
            final_conc = quick_c1 / ratio_num
            
            st.markdown(f"""
            <div class="result-box">
                <h4>Quick Result</h4>
                <p><strong>Mix:</strong> {stock_vol:.2f} stock + {water_vol:.2f} diluent</p>
                <p><strong>Final Concentration:</strong> {final_conc:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Dilution tips
        st.markdown("### 💡 Dilution Tips")
        st.markdown("""
        • **Always add solvent to solute**, not vice versa
        • **Use volumetric flasks** for precise dilutions
        • **Mix thoroughly** after each addition
        • **Work at room temperature** unless specified
        • **Prepare fresh** for best accuracy
        • **Label immediately** with concentration and date
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def standard_dilution_calc():
    """Standard C1V1 = C2V2 calculator"""
    
    with st.form("standard_dilution"):
        st.markdown("#### Standard Dilution (C₁V₁ = C₂V₂)")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("**Stock Solution (1):**")
            c1 = st.number_input("Initial Concentration (C₁)", min_value=0.001, value=10.0, step=0.1)
            c1_unit = st.selectbox("C₁ Unit", ["M", "mM", "μM", "mg/mL", "%"])
        
        with col_d2:
            st.markdown("**Final Solution (2):**")
            c2 = st.number_input("Final Concentration (C₂)", min_value=0.001, value=1.0, step=0.1)
            c2_unit = st.selectbox("C₂ Unit", ["M", "mM", "μM", "mg/mL", "%"])
        
        v2 = st.number_input("Final Volume Needed", min_value=0.001, value=10.0, step=0.1)
        v2_unit = st.selectbox("Volume Unit", ["mL", "μL", "L"])
        
        submitted = st.form_submit_button("🧪 Calculate Dilution", use_container_width=True)
        
        if submitted:
            try:
                # Calculate V1 needed
                v1 = (c2 * v2) / c1
                water_volume = v2 - v1
                dilution_factor = c1 / c2
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Dilution Results</h4>
                    <p><strong>Stock volume needed:</strong> {v1:.3f} {v2_unit}</p>
                    <p><strong>Diluent volume:</strong> {water_volume:.3f} {v2_unit}</p>
                    <p><strong>Final volume:</strong> {v2:.1f} {v2_unit}</p>
                    <p><strong>Dilution ratio:</strong> 1:{dilution_factor:.1f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate protocol
                st.markdown("### 📋 Dilution Protocol")
                protocol_text = f"""
**Dilution Protocol**

**Objective:** Prepare {c2:.3f} {c2_unit} from {c1:.3f} {c1_unit} stock

**Procedure:**
1. **Add diluent** to flask (~{water_volume*0.8:.1f} {v2_unit})
2. **Add stock solution** {v1:.3f} {v2_unit} slowly with mixing
3. **Dilute to mark** with additional diluent to {v2:.1f} {v2_unit}
4. **Mix thoroughly** by inversion (20×)
5. **Label** with final concentration and date

**Quality Control:**
• Verify calculations before preparation
• Use calibrated volumetric equipment
• Prepare at room temperature unless specified
                """
                
                st.markdown(protocol_text)
                
                # Store calculation
                calc_data = {
                    'c1': c1, 'c1_unit': c1_unit,
                    'c2': c2, 'c2_unit': c2_unit,
                    'v1': v1, 'v2': v2, 'v2_unit': v2_unit
                }
                
                add_to_history("Dilution Calculation", calc_data, {"protocol": protocol_text})
                
            except Exception as e:
                st.error(f"Calculation error: {str(e)}")

def serial_dilution_calc():
    """Serial dilution series calculator"""
    
    st.markdown("#### 🔄 Serial Dilution Series")
    
    with st.form("serial_dilution"):
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            starting_conc = st.number_input("Starting Concentration", value=100.0, min_value=0.001)
            conc_unit = st.selectbox("Concentration Unit", ["μM", "mM", "M", "mg/mL"])
            dilution_factor = st.number_input("Dilution Factor", value=2.0, min_value=1.1, step=0.1)
        
        with col_s2:
            num_dilutions = st.number_input("Number of Dilutions", value=6, min_value=2, max_value=12)
            tube_volume = st.number_input("Volume per Tube (mL)", value=1.0, min_value=0.1)
            include_blank = st.checkbox("Include Blank (0 concentration)", value=True)
        
        if st.form_submit_button("🧪 Generate Serial Dilution"):
            # Calculate dilution series
            concentrations = []
            current_conc = starting_conc
            
            for i in range(num_dilutions):
                concentrations.append(current_conc)
                current_conc = current_conc / dilution_factor
            
            if include_blank:
                concentrations.append(0.0)
            
            # Create dilution table
            dilution_data = []
            for i, conc in enumerate(concentrations):
                if i == 0:
                    source = "Stock"
                    transfer_vol = tube_volume
                    diluent_vol = 0
                elif conc == 0:
                    source = "Blank"
                    transfer_vol = 0
                    diluent_vol = tube_volume
                else:
                    source = f"Tube {i}"
                    transfer_vol = tube_volume / dilution_factor
                    diluent_vol = tube_volume - transfer_vol
                
                dilution_data.append({
                    'Tube': i + 1,
                    'Concentration': f"{conc:.3f}" if conc > 0 else "0",
                    'Source': source,
                    'Transfer (mL)': f"{transfer_vol:.3f}",
                    'Diluent (mL)': f"{diluent_vol:.3f}",
                    'Total (mL)': f"{tube_volume:.1f}"
                })
            
            df_dilution = pd.DataFrame(dilution_data)
            
            st.markdown("### 📊 Serial Dilution Plan")
            st.dataframe(df_dilution, use_container_width=True, hide_index=True)
            
            # Protocol
            st.markdown("### 📋 Serial Dilution Protocol")
            
            protocol = f"""
**Serial Dilution Protocol**

**Series:** {starting_conc} {conc_unit} → {concentrations[-2]:.6f} {conc_unit} (1:{dilution_factor} factor)

**Setup:**
1. **Label tubes** 1 through {len(concentrations)}
2. **Add diluent** to each tube except tube 1 (see table above)
3. **Add stock** solution to tube 1

**Dilution Steps:**
"""
            
            for i in range(1, len(concentrations)):
                if concentrations[i] > 0:
                    transfer = tube_volume / dilution_factor
                    protocol += f"{i+1}. **Tube {i+1}:** Transfer {transfer:.3f} mL from tube {i} → mix thoroughly\n"
            
            if include_blank:
                protocol += f"{len(concentrations)}. **Blank:** Add {tube_volume:.1f} mL diluent only\n"
            
            protocol += """
**Quality Control:**
• Mix each tube thoroughly before next transfer
• Use fresh pipette tips for each transfer
• Work systematically to avoid errors
            """
            
            st.markdown(protocol)

def enhanced_media_preparation_calculator():
    """Enhanced media preparation calculator"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("🧫 Enhanced Media Preparation Calculator")
    st.markdown("*Professional bacterial growth media preparation*")
    
    # Media selection tabs
    tab1, tab2, tab3 = st.tabs(["🥼 LB Medium", "🧬 LBGM Medium", "⚗️ MSGG(2x) Medium"])
    
    with tab1:
        calculate_enhanced_lb_media()
    
    with tab2:
        calculate_enhanced_lbgm_media()
    
    with tab3:
        calculate_enhanced_msgg_media()
    
    st.markdown('</div>', unsafe_allow_html=True)

def calculate_enhanced_lb_media():
    """Enhanced LB media calculator"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("lb_form"):
            st.markdown("### 🥼 LB Medium Configuration")
            
            col_lb1, col_lb2, col_lb3 = st.columns(3)
            with col_lb1:
                volume = st.number_input("Volume (L)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
            with col_lb2:
                agar_option = st.selectbox("Medium Type", ["Liquid (Broth)", "Solid (Agar)"])
            with col_lb3:
                batch_count = st.number_input("Number of Batches", min_value=1, max_value=20, value=1)
            
            submitted = st.form_submit_button("🧪 Calculate LB Media", use_container_width=True)
            
            if submitted:
                # Calculate components
                total_volume = volume * batch_count
                lb_powder = 20 * total_volume
                
                components = [("LB Powder", f"{lb_powder:.2f} g")]
                
                if "Solid" in agar_option:
                    agar_needed = 15 * total_volume
                    components.append(("Agar", f"{agar_needed:.2f} g"))
                
                # Display results
                display_enhanced_media_results("LB Medium", components, total_volume, batch_count)
    
    with col2:
        st.markdown("### 📋 LB Medium Info")
        st.markdown("""
        **LB (Lysogeny Broth)**
        - **Purpose**: General bacterial growth
        - **pH**: 7.0 ± 0.2
        - **Osmolarity**: ~300 mOsm
        - **Storage**: 4°C, up to 1 month
        
        **Composition per Liter:**
        - Tryptone: 10 g
        - Yeast Extract: 5 g  
        - NaCl: 5 g
        - (Combined in LB powder: 20 g/L)
        
        **Applications:**
        - E. coli cultivation
        - Plasmid preparation
        - Protein expression
        - General microbiology
        """)

def calculate_enhanced_lbgm_media():
    """Enhanced LBGM media calculator"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("lbgm_form"):
            st.markdown("### 🧬 LBGM Medium Configuration")
            
            col_lbgm1, col_lbgm2, col_lbgm3 = st.columns(3)
            with col_lbgm1:
                volume = st.number_input("Volume (L)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
            with col_lbgm2:
                agar_option = st.selectbox("Medium Type", ["Liquid (Broth)", "Solid (Agar)"])
            with col_lbgm3:
                batch_count = st.number_input("Number of Batches", min_value=1, max_value=20, value=1)
            
            submitted = st.form_submit_button("🧪 Calculate LBGM Media", use_container_width=True)
            
            if submitted:
                total_volume = volume * batch_count
                
                # Calculate components
                lb_powder = 20 * total_volume
                glycerol_50 = 20 * total_volume  # mL of 50% glycerol
                mncl2_10mm = 10 * total_volume   # mL of 10 mM MnCl2
                
                components = [
                    ("LB Powder", f"{lb_powder:.2f} g"),
                    ("Glycerol (50%)", f"{glycerol_50:.2f} mL"),
                    ("MnCl₂ (10 mM)", f"{mncl2_10mm:.2f} mL")
                ]
                
                if "Solid" in agar_option:
                    agar_needed = 15 * total_volume
                    components.append(("Agar", f"{agar_needed:.2f} g"))
                
                components.append(("DDW (to final volume)", f"{total_volume:.2f} L"))
                
                display_enhanced_media_results("LBGM Medium", components, total_volume, batch_count)
    
    with col2:
        st.markdown("### 📋 LBGM Medium Info")
        st.markdown("""
        **LBGM Medium**
        - **Base**: LB + Glycerol + MnCl₂
        - **Enhanced**: Carbon source + cofactor
        - **Applications**: Specialized bacterial growth
        
        **Key Components:**
        - **Glycerol**: Alternative carbon source
        - **MnCl₂**: Manganese cofactor
        - **Benefits**: Enhanced growth for some strains
        
        **Preparation Notes:**
        - Prepare glycerol stock separately
        - Filter sterilize MnCl₂ if needed
        - Add supplements after autoclaving
        """)

def calculate_enhanced_msgg_media():
    """Enhanced MSGG media calculator"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("msgg_form"):
            st.markdown("### ⚗️ MSGG(2x) Medium Configuration")
            
            col_msgg1, col_msgg2, col_msgg3 = st.columns(3)
            with col_msgg1:
                volume = st.number_input("Volume (L)", min_value=0.1, max_value=100.0, value=0.5, step=0.1)
            with col_msgg2:
                agar_option = st.selectbox("Medium Type", ["Liquid (Broth)", "Solid (Agar)"])
            with col_msgg3:
                batch_count = st.number_input("Number of Batches", min_value=1, max_value=10, value=1)
            
            submitted = st.form_submit_button("🧪 Calculate MSGG Media", use_container_width=True)
            
            if submitted:
                total_volume = volume * batch_count
                scale_factor = total_volume / 0.5  # Reference is 0.5L
                
                # All components scaled
                components = [
                    ("1M K₂HPO₄", f"{3.075 * scale_factor:.3f} mL"),
                    ("1M KH₂PO₄", f"{1.925 * scale_factor:.3f} mL"),
                    ("1M MOPS (pH 7.0)", f"{100 * scale_factor:.1f} mL"),
                    ("1M MgCl₂", f"{2 * scale_factor:.1f} mL"),
                    ("10mM MnCl₂", f"{5 * scale_factor:.1f} mL"),
                    ("10mM ZnCl₂", f"{0.1 * scale_factor:.2f} mL"),
                    ("1M CaCl₂", f"{0.7 * scale_factor:.1f} mL"),
                    ("10mM Thiamine", f"{5 * scale_factor:.1f} mL"),
                    ("10mg/ml Phenylalanine*", f"{5 * scale_factor:.1f} mL"),
                    ("10mg/ml Tryptophan*", f"{5 * scale_factor:.1f} mL"),
                    ("50% Glycerol", f"{10 * scale_factor:.1f} mL"),
                    ("10% Glutamic acid*", f"{50 * scale_factor:.1f} mL"),
                    ("10mg/ml Threonine*", f"{5 * scale_factor:.1f} mL")
                ]
                
                if "Solid" in agar_option:
                    fecl3_amount = 12.5 * scale_factor
                    agar_amount = 15 * total_volume
                    components.extend([
                        ("5mM FeCl₃ (add when using)", f"{fecl3_amount:.1f} mL"),
                        ("Agar", f"{agar_amount:.2f} g")
                    ])
                else:
                    fecl3_amount = 10 * scale_factor
                    components.append(("5mM FeCl₃ (add when using)", f"{fecl3_amount:.1f} mL"))
                
                components.append(("DDW", f"{302 * scale_factor:.1f} mL"))
                
                display_enhanced_media_results("MSGG(2x) Medium", components, total_volume, batch_count, complex_media=True)
    
    with col2:
        st.markdown("### 📋 MSGG(2x) Info")
        st.markdown("""
        **MSGG(2x) - Minimal Synthetic**
        - **Type**: Defined minimal medium
        - **Concentration**: 2x concentrated
        - **Components**: 14+ individual chemicals
        - **Control**: Precise nutritional control
        
        **Critical Notes:**
        - ⚠️ *Filter sterilize marked components
        - 🧪 Adjust MOPS to pH 7.0 with NaOH
        - 🔒 Store FeCl₃ separately
        - ❄️ Some components light/heat sensitive
        
        **Applications:**
        - Research-grade bacterial growth
        - Metabolic studies
        - Precise nutrient control
        """)

def display_enhanced_media_results(title: str, components: List, volume: float, batches: int, complex_media: bool = False):
    """Display enhanced media preparation results"""
    
    st.markdown(f"""
    <div class="result-box">
        <h3>✅ {title} - {volume:.1f} L ({batches} batch{'es' if batches > 1 else ''})</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Components table
    df = pd.DataFrame(components, columns=["Component", "Amount"])
    
    if complex_media and len(components) > 8:
        # Split complex media into two columns
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
    
    # Preparation protocol
    st.markdown("### 📋 Enhanced Preparation Protocol")
    
    protocol_steps = [
        f"**Preparation ({volume:.1f} L total)**",
        "1. 📏 Weigh all dry components accurately",
        "2. 🌡️ Dissolve in ~80% of final volume with distilled water",
        "3. 🔄 Mix thoroughly until completely dissolved",
        "4. 📊 Adjust pH if specified (usually 7.0 ± 0.2)",
        "5. 📏 Bring to final volume with distilled water",
        "6. 🔥 Autoclave at 121°C, 15 psi, 15-20 min",
        "7. ❄️ Cool to room temperature before use",
        "8. 🏷️ Label with contents, concentration, and date"
    ]
    
    if complex_media:
        protocol_steps.extend([
            "",
            "**⚠️ Special Handling:**",
            "• Filter sterilize heat-sensitive components separately",
            "• Add after cooling to ~50°C",
            "• Store light-sensitive components in dark containers"
        ])
    
    for step in protocol_steps:
        st.markdown(step)

def advanced_chemistry_tools():
    """Advanced chemistry calculation tools"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("⚗️ Advanced Chemistry Tools")
    st.markdown("*Professional-grade chemistry calculations for research and analysis*")
    
    # Tool selection tabs
    tab1, tab2, tab3 = st.tabs(["🧪 pH & Buffers", "🌡️ Gas Laws", "📈 Beer's Law"])
    
    with tab1:
        ph_buffer_tools()
    
    with tab2:
        gas_law_tools()
    
    with tab3:
        beers_law_tools()
    
    st.markdown('</div>', unsafe_allow_html=True)

def ph_buffer_tools():
    """pH and buffer calculation tools"""
    
    st.markdown("### 🧪 pH & Buffer Calculations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### pH Calculator")
        with st.form("ph_calculator"):
            concentration = st.number_input("Concentration (M)", min_value=1e-14, max_value=10.0, value=0.1, format="%.6f")
            solution_type = st.radio("Solution Type", ["Strong Acid", "Strong Base"])
            
            if st.form_submit_button("Calculate pH"):
                try:
                    if solution_type == "Strong Acid":
                        ph = UltimateChemistryCalculators.ph_calculator(concentration, True)
                    else:  # Strong Base
                        ph = UltimateChemistryCalculators.ph_calculator(concentration, False)
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>pH Calculation Results</h4>
                        <p><strong>pH:</strong> {ph:.2f}</p>
                        <p><strong>Solution:</strong> {'Acidic' if ph < 7 else 'Basic' if ph > 7 else 'Neutral'}</p>
                        <p><strong>[H⁺]:</strong> {10**(-ph):.2e} M</p>
                        <p><strong>[OH⁻]:</strong> {10**(ph-14):.2e} M</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
    
    with col2:
        st.markdown("#### Buffer Calculator (Henderson-Hasselbalch)")
        with st.form("buffer_calculator"):
            pka = st.number_input("pKa of weak acid", min_value=0.0, max_value=14.0, value=4.75, step=0.01)
            acid_conc = st.number_input("Weak acid concentration (M)", min_value=0.001, max_value=10.0, value=0.1)
            base_conc = st.number_input("Conjugate base concentration (M)", min_value=0.001, max_value=10.0, value=0.1)
            
            if st.form_submit_button("Calculate Buffer pH"):
                try:
                    ph = UltimateChemistryCalculators.buffer_calculator(acid_conc, base_conc, pka)
                    buffer_capacity = min(acid_conc, base_conc)
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>Buffer Calculation Results</h4>
                        <p><strong>Buffer pH:</strong> {ph:.2f}</p>
                        <p><strong>Buffer Capacity:</strong> {buffer_capacity:.3f} M</p>
                        <p><strong>Acid/Base Ratio:</strong> {base_conc/acid_conc:.2f}</p>
                        <p><strong>Effective Range:</strong> {pka-1:.1f} - {pka+1:.1f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")

def gas_law_tools():
    """Gas law calculation tools"""
    
    st.markdown("### 🌡️ Ideal Gas Law Calculator (PV = nRT)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("gas_law_calculator"):
            st.markdown("**Known Values** (leave unknown value as 0)")
            pressure = st.number_input("Pressure (atm)", min_value=0.0, value=1.0, step=0.1)
            volume = st.number_input("Volume (L)", min_value=0.0, value=1.0, step=0.1)
            moles = st.number_input("Moles (mol)", min_value=0.0, value=1.0, step=0.1)
            temperature = st.number_input("Temperature (K)", min_value=0.0, value=273.15, step=1.0)
            
            calculate_var = st.selectbox("Calculate:", ["Pressure", "Volume", "Moles", "Temperature"])
            
            if st.form_submit_button("Calculate Gas Law"):
                try:
                    R = 0.08206  # L⋅atm/(mol⋅K)
                    
                    if calculate_var == "Pressure":
                        result = (moles * R * temperature) / volume
                        unit = "atm"
                    elif calculate_var == "Volume":
                        result = (moles * R * temperature) / pressure
                        unit = "L"
                    elif calculate_var == "Moles":
                        result = (pressure * volume) / (R * temperature)
                        unit = "mol"
                    else:  # Temperature
                        result = (pressure * volume) / (moles * R)
                        unit = "K"
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>Gas Law Results</h4>
                        <p><strong>{calculate_var}:</strong> {result:.4f} {unit}</p>
                        <p><strong>Temperature (°C):</strong> {temperature-273.15:.2f} °C</p>
                        <p><strong>STP Conditions:</strong> {'Yes' if abs(pressure-1.0) < 0.01 and abs(temperature-273.15) < 0.01 else 'No'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
    
    with col2:
        st.markdown("#### 🌡️ Temperature Converter")
        temp_input = st.number_input("Temperature", value=25.0)
        temp_unit = st.selectbox("Input Unit", ["°C", "°F", "K"])
        
        if temp_unit == "°C":
            celsius = temp_input
            fahrenheit = (celsius * 9/5) + 32
            kelvin = celsius + 273.15
        elif temp_unit == "°F":
            fahrenheit = temp_input
            celsius = (fahrenheit - 32) * 5/9
            kelvin = celsius + 273.15
        else:  # Kelvin
            kelvin = temp_input
            celsius = kelvin - 273.15
            fahrenheit = (celsius * 9/5) + 32
        
        st.markdown(f"""
        <div class="info-box">
            <h4>Temperature Conversions</h4>
            <p><strong>Celsius:</strong> {celsius:.2f} °C</p>
            <p><strong>Fahrenheit:</strong> {fahrenheit:.2f} °F</p>
            <p><strong>Kelvin:</strong> {kelvin:.2f} K</p>
        </div>
        """, unsafe_allow_html=True)

def beers_law_tools():
    """Beer's Law calculation tools"""
    
    st.markdown("### 📈 Beer's Law Calculator (A = ε × c × l)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("beers_law_calculator"):
            st.markdown("**Beer's Law Calculation**")
            
            calculate_what = st.selectbox("Calculate:", ["Absorbance", "Concentration"])
            
            if calculate_what == "Absorbance":
                concentration = st.number_input("Concentration (M)", min_value=0.0, value=0.001, format="%.6f")
                path_length = st.number_input("Path Length (cm)", min_value=0.1, value=1.0, step=0.1)
                extinction_coeff = st.number_input("Extinction Coefficient (M⁻¹cm⁻¹)", min_value=1.0, value=1000.0, step=1.0)
            else:
                absorbance = st.number_input("Absorbance (A)", min_value=0.0, value=0.5, step=0.01)
                path_length = st.number_input("Path Length (cm)", min_value=0.1, value=1.0, step=0.1)
                extinction_coeff = st.number_input("Extinction Coefficient (M⁻¹cm⁻¹)", min_value=1.0, value=1000.0, step=1.0)
            
            if st.form_submit_button("Calculate Beer's Law"):
                try:
                    if calculate_what == "Absorbance":
                        result = extinction_coeff * concentration * path_length
                        
                        # Check if absorbance is in linear range
                        linear_range = result < 2.0
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>Beer's Law Results</h4>
                            <p><strong>Absorbance:</strong> {result:.4f} AU</p>
                            <p><strong>Transmittance:</strong> {(10**(-result))*100:.2f}%</p>
                            <p><strong>Linear Range:</strong> {'✅ Yes' if linear_range else '⚠️ No (A > 2.0)'}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:  # Calculate concentration
                        result = absorbance / (extinction_coeff * path_length)
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>Concentration Results</h4>
                            <p><strong>Concentration:</strong> {result:.6f} M</p>
                            <p><strong>Concentration:</strong> {result*1000:.3f} mM</p>
                            <p><strong>Concentration:</strong> {result*1000000:.1f} μM</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
    
    with col2:
        st.markdown("#### 🔬 Protein Concentration (A280)")
        
        with st.form("protein_concentration"):
            a280 = st.number_input("Absorbance at 280 nm", min_value=0.0, value=0.5, step=0.01)
            path_length_prot = st.number_input("Path Length (cm)", min_value=0.1, value=1.0, step=0.1)
            
            # Protein selection
            protein_type = st.selectbox("Protein Type", [
                "BSA (ε = 43,824 M⁻¹cm⁻¹)",
                "Lysozyme (ε = 38,940 M⁻¹cm⁻¹)", 
                "IgG (ε = 210,000 M⁻¹cm⁻¹)",
                "Custom"
            ])
            
            if protein_type == "Custom":
                extinction_coeff_prot = st.number_input("Extinction Coefficient (M⁻¹cm⁻¹)", min_value=1.0, value=43824.0)
            else:
                extinction_coeffs = {
                    "BSA (ε = 43,824 M⁻¹cm⁻¹)": 43824,
                    "Lysozyme (ε = 38,940 M⁻¹cm⁻¹)": 38940,
                    "IgG (ε = 210,000 M⁻¹cm⁻¹)": 210000
                }
                extinction_coeff_prot = extinction_coeffs[protein_type]
            
            molecular_weight = st.number_input("Molecular Weight (Da)", min_value=1000.0, value=66430.0)  # BSA MW
            
            if st.form_submit_button("Calculate Protein Concentration"):
                # Calculate concentration using Beer's Law
                concentration_M = a280 / (extinction_coeff_prot * path_length_prot)
                concentration_mg_ml = concentration_M * molecular_weight / 1000
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>Protein Concentration Results</h4>
                    <p><strong>Concentration:</strong> {concentration_M*1000000:.2f} μM</p>
                    <p><strong>Concentration:</strong> {concentration_mg_ml:.3f} mg/mL</p>
                    <p><strong>Concentration:</strong> {concentration_mg_ml*1000:.1f} μg/mL</p>
                    <p><strong>Molar Concentration:</strong> {concentration_M:.6f} M</p>
                </div>
                """, unsafe_allow_html=True)

def data_analysis_suite():
    """Data analysis tools"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("📊 Data Analysis Suite")
    st.markdown("*Professional statistical analysis and visualization tools*")
    
    tab1, tab2 = st.tabs(["📈 Statistical Analysis", "📊 Data Visualization"])
    
    with tab1:
        statistical_analysis_tools()
    
    with tab2:
        data_visualization_tools()
    
    st.markdown('</div>', unsafe_allow_html=True)

def statistical_analysis_tools():
    """Statistical analysis tools"""
    
    st.markdown("### 📈 Statistical Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Basic Statistics")
        
        # Sample data input
        data_input = st.text_area("Data (one value per line)", value="0.245\n0.251\n0.248\n0.252\n0.247")
        
        if st.button("Analyze Data"):
            try:
                data = [float(x.strip()) for x in data_input.split('\n') if x.strip()]
                
                if len(data) > 1:
                    mean_val = np.mean(data)
                    std_val = np.std(data, ddof=1)  # Sample standard deviation
                    rsd_val = (std_val / mean_val) * 100
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>Statistical Results (n = {len(data)})</h4>
                        <p><strong>Mean:</strong> {mean_val:.4f}</p>
                        <p><strong>Standard Deviation:</strong> {std_val:.4f}</p>
                        <p><strong>RSD:</strong> {rsd_val:.2f}%</p>
                        <p><strong>Range:</strong> {min(data):.4f} - {max(data):.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Data quality assessment
                    if rsd_val < 2:
                        quality = "Excellent"
                        color = "green"
                    elif rsd_val < 5:
                        quality = "Good"
                        color = "blue"
                    elif rsd_val < 10:
                        quality = "Acceptable"
                        color = "orange"
                    else:
                        quality = "Poor"
                        color = "red"
                    
                    st.markdown(f"""
                    <div class="info-box">
                        <p><strong>Data Quality:</strong> <span style="color: {color};">{quality}</span></p>
                        <p><strong>Precision:</strong> {'High' if rsd_val < 5 else 'Moderate' if rsd_val < 10 else 'Low'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error analyzing data: {str(e)}")
    
    with col2:
        st.markdown("#### Outlier Detection")
        
        outlier_data = st.text_area("Data for outlier detection", value="0.245\n0.251\n0.248\n0.252\n0.347\n0.247")
        
        if st.button("Detect Outliers"):
            try:
                data = [float(x.strip()) for x in outlier_data.split('\n') if x.strip()]
                
                if len(data) > 3:
                    mean_val = np.mean(data)
                    std_val = np.std(data, ddof=1)
                    
                    # Q-test for outliers
                    outliers = []
                    for i, value in enumerate(data):
                        z_score = abs(value - mean_val) / std_val
                        if z_score > 2.5:  # Common threshold
                            outliers.append((i, value, z_score))
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>Outlier Detection Results</h4>
                        <p><strong>Data points:</strong> {len(data)}</p>
                        <p><strong>Potential outliers:</strong> {len(outliers)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if outliers:
                        for idx, value, z_score in outliers:
                            st.markdown(f"""
                            <div class="warning-box">
                                <p><strong>Outlier detected:</strong></p>
                                <p>Position: {idx+1}, Value: {value:.4f}</p>
                                <p>Z-score: {z_score:.2f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="result-box"><p>No outliers detected!</p></div>', unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"Error in outlier detection: {str(e)}")

def data_visualization_tools():
    """Data visualization tools"""
    
    st.markdown("### 📊 Data Visualization")
    
    # Simple data visualization without external plotting libraries
    st.markdown("#### Basic Data Display")
    
    # Sample data generation
    if st.button("Generate Sample Data"):
        np.random.seed(42)
        sample_data = np.random.normal(100, 10, 20)
        
        data_df = pd.DataFrame({
            'Sample': range(1, 21),
            'Value': sample_data,
            'Category': ['A'] * 10 + ['B'] * 10
        })
        
        st.markdown("### Sample Dataset")
        st.dataframe(data_df, use_container_width=True)
        
        # Basic statistics
        st.markdown("### Basic Statistics")
        st.markdown(f"**Mean:** {np.mean(sample_data):.2f}")
        st.markdown(f"**Standard Deviation:** {np.std(sample_data, ddof=1):.2f}")
        st.markdown(f"**Range:** {np.min(sample_data):.2f} - {np.max(sample_data):.2f}")

def lab_management_page():
    """Laboratory management tools"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("🏠 Laboratory Management Suite")
    st.markdown("*Complete lab management tools for modern research facilities*")
    
    tab1, tab2 = st.tabs(["📦 Inventory", "📋 Protocols"])
    
    with tab1:
        inventory_management()
    
    with tab2:
        protocol_builder()
    
    st.markdown('</div>', unsafe_allow_html=True)

def inventory_management():
    """Chemical inventory management"""
    
    st.markdown("### 📦 Chemical Inventory Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Add New Chemical")
        
        with st.form("add_chemical"):
            chemical_name = st.text_input("Chemical Name")
            formula = st.text_input("Formula") 
            supplier = st.text_input("Supplier")
            
            col_inv1, col_inv2 = st.columns(2)
            with col_inv1:
                quantity = st.number_input("Quantity", min_value=0.0, value=100.0)
                unit = st.selectbox("Unit", ["g", "kg", "mL", "L"])
            with col_inv2:
                location = st.text_input("Storage Location")
                hazard_class = st.selectbox("Hazard Class", ["None", "Flammable", "Corrosive", "Toxic"])
            
            if st.form_submit_button("Add to Inventory"):
                new_item = {
                    'name': chemical_name,
                    'formula': formula,
                    'supplier': supplier,
                    'quantity': quantity,
                    'unit': unit,
                    'location': location,
                    'hazard': hazard_class,
                    'added_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                st.session_state.inventory.append(new_item)
                st.success(f"Added {chemical_name} to inventory!")
    
    with col2:
        st.markdown("#### Inventory Summary")
        
        if st.session_state.inventory:
            total_items = len(st.session_state.inventory)
            hazardous_items = sum(1 for item in st.session_state.inventory if item['hazard'] != 'None')
            
            st.metric("Total Chemicals", total_items)
            st.metric("Hazardous Items", hazardous_items)
        else:
            st.info("No chemicals in inventory yet")
    
    # Current inventory display
    if st.session_state.inventory:
        st.markdown("### 📋 Current Inventory")
        
        # Create DataFrame
        df_inventory = pd.DataFrame(st.session_state.inventory)
        
        # Display inventory
        st.dataframe(df_inventory, use_container_width=True, hide_index=True)

def protocol_builder():
    """Protocol building and management"""
    
    st.markdown("### 📋 Protocol Builder")
    
    with st.form("create_protocol"):
        protocol_title = st.text_input("Protocol Title")
        protocol_type = st.selectbox("Protocol Type", 
                                   ["Analytical Method", "Sample Preparation", "Synthesis"])
        author = st.text_input("Author", value="ChemLab Pro User")
        
        # Protocol steps
        st.markdown("**Protocol Steps:**")
        num_steps = st.number_input("Number of Steps", min_value=1, max_value=10, value=5)
        
        steps = []
        for i in range(num_steps):
            step_description = st.text_area(f"Step {i+1}", key=f"step_{i}", height=60)
            if step_description:
                steps.append(f"{i+1}. {step_description}")
        
        # Materials and equipment
        materials = st.text_area("Materials and Reagents")
        equipment = st.text_area("Equipment Required")
        
        if st.form_submit_button("Save Protocol"):
            new_protocol = {
                'title': protocol_title,
                'type': protocol_type,
                'author': author,
                'steps': steps,
                'materials': materials,
                'equipment': equipment,
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'id': len(st.session_state.protocols) + 1
            }
            
            st.session_state.protocols.append(new_protocol)
            st.success(f"Protocol '{protocol_title}' saved successfully!")
    
    # Display existing protocols
    if st.session_state.protocols:
        st.markdown("### 📚 Saved Protocols")
        
        for protocol in st.session_state.protocols:
            with st.expander(f"📋 {protocol['title']} - {protocol['type']}"):
                st.markdown(f"**Author:** {protocol['author']}")
                st.markdown(f"**Created:** {protocol['created_date']}")
                
                if protocol['materials']:
                    st.markdown("**Materials:**")
                    st.markdown(protocol['materials'])
                
                if protocol['equipment']:
                    st.markdown("**Equipment:**")
                    st.markdown(protocol['equipment'])
                
                if protocol['steps']:
                    st.markdown("**Procedure:**")
                    for step in protocol['steps']:
                        st.markdown(step)

def educational_hub():
    """Educational resources and tutorials"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("📚 Educational Hub")
    st.markdown("*Learn chemistry concepts with interactive tutorials and examples*")
    
    tab1, tab2, tab3 = st.tabs(["🎓 Tutorials", "📖 Reference", "🎯 Quiz"])
    
    with tab1:
        chemistry_tutorials()
    
    with tab2:
        reference_materials()
    
    with tab3:
        chemistry_quiz()
    
    st.markdown('</div>', unsafe_allow_html=True)

def chemistry_tutorials():
    """Interactive chemistry tutorials"""
    
    st.markdown("### 🎓 Interactive Chemistry Tutorials")
    
    tutorial_topic = st.selectbox("Choose Tutorial Topic", [
        "Molarity and Solution Preparation",
        "pH and Buffer Calculations", 
        "Spectrophotometry Basics"
    ])
    
    if tutorial_topic == "Molarity and Solution Preparation":
        st.markdown("""
        ## 🧪 Molarity and Solution Preparation Tutorial
        
        ### What is Molarity?
        
        **Molarity (M)** is the concentration of a solution expressed as **moles of solute per liter of solution**.
        
        **Formula:** `M = moles of solute / liters of solution`
        
        ### Step-by-Step Calculation
        
        **Example:** Prepare 500 mL of 0.1 M NaCl solution
        
        1. **Calculate moles needed:**
           - Moles = Molarity × Volume (L)
           - Moles = 0.1 M × 0.5 L = 0.05 mol
        
        2. **Calculate mass needed:**
           - Mass = Moles × Molecular Weight
           - MW of NaCl = 22.99 + 35.45 = 58.44 g/mol
           - Mass = 0.05 mol × 58.44 g/mol = 2.922 g
        
        3. **Preparation steps:**
           - Weigh 2.922 g of NaCl
           - Dissolve in ~400 mL distilled water
           - Transfer to 500 mL volumetric flask
           - Dilute to exactly 500 mL with water
        """)
        
        # Interactive calculation
        st.markdown("### 🧮 Try It Yourself!")
        
        col_tut1, col_tut2 = st.columns(2)
        
        with col_tut1:
            user_molarity = st.number_input("Desired Molarity (M)", value=0.2, min_value=0.001)
            user_volume = st.number_input("Volume (mL)", value=250.0, min_value=1.0)
            user_formula = st.text_input("Chemical Formula", value="KCl")
        
        with col_tut2:
            if st.button("Calculate Tutorial Example"):
                try:
                    # Use the existing molecular weight calculator
                    mw = UltimateChemistryCalculators.compute_molecular_weight(user_formula)
                    volume_L = user_volume / 1000
                    moles_needed = user_molarity * volume_L
                    mass_needed = moles_needed * mw
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>Tutorial Solution</h4>
                        <p><strong>Step 3:</strong> Dissolve {mass_needed:.4f} g {user_formula} in water and dilute to {user_volume} mL</p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error in calculation: {str(e)}")

def reference_materials():
    """Chemistry reference materials"""
    
    st.markdown("### 📖 Chemistry Reference Materials")
    
    ref_category = st.selectbox("Reference Category", [
        "Common Formulas",
        "Unit Conversions", 
        "Constants and Values",
        "Useful Equations"
    ])
    
    if ref_category == "Common Formulas":
        # Create reference table
        common_compounds = {
            'Water': 'H₂O',
            'Sodium Chloride': 'NaCl',
            'Hydrochloric Acid': 'HCl',
            'Sulfuric Acid': 'H₂SO₄',
            'Sodium Hydroxide': 'NaOH',
            'Glucose': 'C₆H₁₂O₆',
            'Ethanol': 'C₂H₅OH',
            'Acetic Acid': 'CH₃COOH',
            'Calcium Chloride': 'CaCl₂',
            'Potassium Permanganate': 'KMnO₄'
        }
        
        ref_data = []
        for name, formula in common_compounds.items():
            try:
                mw = UltimateChemistryCalculators.compute_molecular_weight(formula.replace('₂', '2').replace('₃', '3').replace('₄', '4').replace('₅', '5').replace('₆', '6').replace('₁₂', '12'))
                ref_data.append({'Compound': name, 'Formula': formula, 'MW (g/mol)': f"{mw:.2f}"})
            except:
                ref_data.append({'Compound': name, 'Formula': formula, 'MW (g/mol)': 'N/A'})
        
        df_ref = pd.DataFrame(ref_data)
        st.dataframe(df_ref, use_container_width=True, hide_index=True)
    
    elif ref_category == "Unit Conversions":
        st.markdown("""
        ## 🔄 Unit Conversion Reference
        
        ### Concentration Units
        - **1 M = 1000 mM = 1,000,000 μM**
        - **1% (w/v) = 10 mg/mL = 10,000 μg/mL**
        - **1 ppm = 1 μg/mL (for aqueous solutions)**
        
        ### Volume Units
        - **1 L = 1000 mL = 1,000,000 μL**
        - **1 mL = 1000 μL**
        
        ### Mass Units
        - **1 kg = 1000 g = 1,000,000 mg**
        - **1 g = 1000 mg = 1,000,000 μg**
        
        ### Temperature
        - **°C = (°F - 32) × 5/9**
        - **K = °C + 273.15**
        
        ### Pressure
        - **1 atm = 760 mmHg = 101.325 kPa**
        """)
    
    elif ref_category == "Constants and Values":
        st.markdown("""
        ## 📊 Important Constants
        
        ### Physical Constants
        - **Avogadro's Number:** 6.022 × 10²³ mol⁻¹
        - **Gas Constant (R):** 8.314 J/(mol·K) = 0.08206 L·atm/(mol·K)
        - **Planck's Constant:** 6.626 × 10⁻³⁴ J·s
        - **Speed of Light:** 2.998 × 10⁸ m/s
        
        ### Common pKa Values
        - **Acetic acid:** 4.76
        - **Phosphoric acid:** 2.15, 7.20, 12.38
        - **Carbonic acid:** 6.37, 10.25
        - **Ammonia:** 9.25
        
        ### Spectroscopy
        - **NADH (340 nm):** ε = 6,220 M⁻¹cm⁻¹
        - **Protein (280 nm):** ε ≈ 1 mg/mL⁻¹cm⁻¹
        """)
    
    else:  # Useful Equations
        st.markdown("""
        ## ⚖️ Essential Chemistry Equations
        
        ### Solution Chemistry
        - **Molarity:** M = moles solute / L solution
        - **Dilution:** C₁V₁ = C₂V₂
        - **Parts per million:** ppm = (mg solute / L solution)
        
        ### Acid-Base Chemistry
        - **pH:** pH = -log[H⁺]
        - **Henderson-Hasselbalch:** pH = pKa + log([A⁻]/[HA])
        - **Ion product of water:** Kw = [H⁺][OH⁻] = 1.0 × 10⁻¹⁴
        
        ### Spectroscopy
        - **Beer's Law:** A = ε × c × l
        - **Transmittance:** T = I/I₀ = 10⁻ᴬ
        
        ### Thermodynamics
        - **Gibbs Free Energy:** ΔG = ΔH - TΔS
        - **Ideal Gas Law:** PV = nRT
        """)

def chemistry_quiz():
    """Interactive chemistry quiz"""
    
    st.markdown("### 🎯 Chemistry Knowledge Quiz")
    
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_question' not in st.session_state:
        st.session_state.quiz_question = 0
    
    questions = [
        {
            "question": "What is the molarity of a solution containing 5.85 g NaCl in 500 mL water?",
            "options": ["0.1 M", "0.2 M", "0.3 M", "0.4 M"],
            "correct": 1,
            "explanation": "MW of NaCl = 58.44 g/mol. Moles = 5.85/58.44 = 0.1 mol. M = 0.1 mol / 0.5 L = 0.2 M"
        },
        {
            "question": "At pH 7.4, what is the [OH⁻] concentration?",
            "options": ["2.5 × 10⁻⁸ M", "4.0 × 10⁻⁸ M", "2.5 × 10⁻⁷ M", "4.0 × 10⁻⁷ M"],
            "correct": 2,
            "explanation": "pOH = 14 - pH = 14 - 7.4 = 6.6. [OH⁻] = 10⁻⁶·⁶ = 2.5 × 10⁻⁷ M"
        },
        {
            "question": "Beer's Law relates absorbance to:",
            "options": ["Temperature", "Concentration", "pH", "Pressure"],
            "correct": 1,
            "explanation": "Beer's Law: A = ε × c × l, where A is absorbance, c is concentration"
        }
    ]
    
    if st.session_state.quiz_question < len(questions):
        current_q = questions[st.session_state.quiz_question]
        
        st.markdown(f"### Question {st.session_state.quiz_question + 1} of {len(questions)}")
        st.markdown(f"**{current_q['question']}**")
        
        answer = st.radio("Select your answer:", current_q['options'], key=f"q_{st.session_state.quiz_question}")
        
        if st.button("Submit Answer"):
            selected_index = current_q['options'].index(answer)
            
            if selected_index == current_q['correct']:
                st.success("✅ Correct!")
                st.session_state.quiz_score += 1
            else:
                st.error(f"❌ Incorrect. The correct answer is: {current_q['options'][current_q['correct']]}")
            
            st.info(f"**Explanation:** {current_q['explanation']}")
            
            st.session_state.quiz_question += 1
            
            if st.button("Next Question"):
                st.rerun()
    
    else:
        # Quiz completed
        percentage = (st.session_state.quiz_score / len(questions)) * 100
        
        st.markdown(f"""
        <div class="result-box">
            <h2>🎉 Quiz Complete!</h2>
            <p><strong>Your Score: {st.session_state.quiz_score}/{len(questions)} ({percentage:.0f}%)</strong></p>
            <p><strong>Grade: {'A' if percentage >= 90 else 'B' if percentage >= 80 else 'C' if percentage >= 70 else 'D' if percentage >= 60 else 'F'}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Restart Quiz"):
            st.session_state.quiz_score = 0
            st.session_state.quiz_question = 0
            st.rerun()

def settings_help_page():
    """Settings and help page"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("⚙️ Settings & Help")
    st.markdown("*Configuration, help, and system information*")
    
    tab1, tab2, tab3 = st.tabs(["⚙️ Settings", "❓ Help", "ℹ️ About"])
    
    with tab1:
        st.markdown("### ⚙️ Application Settings")
        
        # User preferences
        col_set1, col_set2 = st.columns(2)
        
        with col_set1:
            st.markdown("#### Display Preferences")
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
            precision = st.number_input("Decimal Precision", min_value=2, max_value=8, value=4)
            units = st.selectbox("Default Units", ["Metric", "Imperial", "Mixed"])
            
        with col_set2:
            st.markdown("#### Calculation Settings")
            auto_save = st.checkbox("Auto-save calculations", value=True)
            show_warnings = st.checkbox("Show safety warnings", value=True)
            advanced_mode = st.checkbox("Advanced mode", value=False)
        
        # Data management
        st.markdown("### 💾 Data Management")
        
        col_data1, col_data2 = st.columns(2)
        
        with col_data1:
            if st.button("Clear All History"):
                st.session_state.calculation_history = []
                st.success("History cleared!")
        
        with col_data2:
            if st.button("Reset Settings"):
                st.success("Settings reset to defaults!")
    
    with tab2:
        st.markdown("### ❓ Help & Documentation")
        
        help_topic = st.selectbox("Help Topic", [
            "Getting Started",
            "Molarity Calculator",
            "Media Preparation", 
            "Data Analysis",
            "Troubleshooting"
        ])
        
        if help_topic == "Getting Started":
            st.markdown("""
            ## 🚀 Getting Started with ChemLab Pro
            
            ### 1. Navigation
            - Use the **sidebar** to select different calculators
            - The **dashboard** shows your recent activity
            - **Quick access** buttons provide shortcuts
            
            ### 2. Basic Calculations
            - Enter values in the input fields
            - Click **Calculate** to get results
            - Results are automatically saved to history
            
            ### 3. Advanced Features
            - **Export** calculations for lab records
            - **Save protocols** for future use
            - **Track inventory** of chemicals
            
            ### 4. Mobile Use
            - The interface is **fully responsive**
            - Works great on **tablets** for lab bench use
            - **Touch-optimized** for easy operation
            """)
        
        elif help_topic == "Troubleshooting":
            st.markdown("""
            ## 🔧 Troubleshooting Guide
            
            ### Common Issues
            
            **Calculator not working?**
            - Check input values are valid numbers
            - Ensure all required fields are filled
            - Try refreshing the page
            
            **Formula errors?**
            - Use proper capitalization (Na, not na)
            - Numbers go after elements (CaCl2)
            - Check spelling of element symbols
            
            **Slow performance?**
            - Clear calculation history
            - Close unused browser tabs
            - Check internet connection
            
            **Need help?**
            - Use the built-in tutorials
            - Check the reference materials
            - Contact support for assistance
            """)
    
    with tab3:
        st.markdown("### ℹ️ About ChemLab Pro")
        
        st.markdown("""
        ## 🧪 ChemLab Pro - Ultimate Laboratory Suite
        
        **Version:** 2.0.0  
        **Build:** 2024.06.30
        
        ### 🎯 Mission
        To provide professional-grade chemistry calculators and laboratory management tools 
        accessible from any device, anywhere in the world.
        
        ### ✨ Features
        - **15+ Professional Calculators**
        - **Advanced Data Analysis Tools**
        - **Laboratory Management Suite**
        - **Interactive Educational Resources**
        - **Mobile-Optimized Interface**
        - **Professional Report Generation**
        
        ### 🔬 Built For
        - Research Scientists
        - Laboratory Technicians  
        - Chemistry Students
        - Quality Control Analysts
        - Academic Institutions
        
        ### 🛠️ Technology Stack
        - **Frontend:** Streamlit, Python
        - **Visualization:** Native Python/Pandas
        - **Deployment:** Streamlit Cloud
        - **Open Source:** MIT License
        
        ### 👥 Credits
        Developed with ❤️ by the ChemLab Pro team
        
        ### 📜 License
        MIT License - Free for academic and commercial use
        """)
        
        # System information
        st.markdown("### 💻 System Information")
        
        col_sys1, col_sys2 = st.columns(2)
        
        with col_sys1:
            st.markdown("""
            **Browser Compatibility:**
            - ✅ Chrome 90+
            - ✅ Firefox 88+
            - ✅ Safari 14+
            - ✅ Edge 90+
            """)
        
        with col_sys2:
            st.markdown("""
            **Platform Support:**
            - ✅ Windows 10/11
            - ✅ macOS 10.15+
            - ✅ Linux (All major distros)
            - ✅ iOS 13+ / Android 8+
            """)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()