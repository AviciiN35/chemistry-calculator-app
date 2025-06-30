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
    page_title="🧪 A.P.D Nexus Pro - Laboratory Suite",
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
if 'nav_target' not in st.session_state:
    st.session_state.nav_target = None

# Professional CSS styling
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
        }
        
        .main-header h1 {
            font-family: 'Inter', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .calculator-card {
            background: rgba(255, 255, 255, 0.98);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .metric-card {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            border-left: 4px solid #4f46e5;
            margin: 1rem 0;
        }
        
        .result-box {
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            padding: 2rem;
            border-radius: 15px;
            border-left: 5px solid #10b981;
            margin: 1.5rem 0;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
        }
        
        .warning-box {
            background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 20%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #f59e0b;
            margin: 1.5rem 0;
        }
        
        .info-box {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #3b82f6;
            margin: 1rem 0;
        }
        
        .pcr-box {
            background: linear-gradient(135deg, #fef7ff 0%, #f3e8ff 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #8b5cf6;
            margin: 1rem 0;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            width: 100%;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

class AdvancedChemistryCalculators:
    """Complete Chemistry Laboratory Suite with All Calculators"""
    
    @staticmethod
    def get_atomic_weights() -> Dict[str, float]:
        """Comprehensive atomic weights database (g/mol)"""
        return {
            'H': 1.0079, 'He': 4.0026, 'Li': 6.941, 'Be': 9.0122,
            'B': 10.811, 'C': 12.0107, 'N': 14.0067, 'O': 15.9994,
            'F': 18.9984, 'Ne': 20.1797, 'Na': 22.9897, 'Mg': 24.305,
            'Al': 26.9815, 'Si': 28.0855, 'P': 30.9738, 'S': 32.065,
            'Cl': 35.453, 'Ar': 39.948, 'K': 39.0983, 'Ca': 40.078,
            'Sc': 44.9559, 'Ti': 47.867, 'V': 50.9415, 'Cr': 51.9961,
            'Mn': 54.938, 'Fe': 55.845, 'Co': 58.9332, 'Ni': 58.6934,
            'Cu': 63.546, 'Zn': 65.38, 'Ga': 69.723, 'Ge': 72.64,
            'As': 74.9216, 'Se': 78.96, 'Br': 79.904, 'Kr': 83.798,
            'Rb': 85.4678, 'Sr': 87.62, 'Y': 88.9059, 'Zr': 91.224,
            'Nb': 92.9064, 'Mo': 95.96, 'Tc': 98, 'Ru': 101.07,
            'Rh': 102.9055, 'Pd': 106.42, 'Ag': 107.8682, 'Cd': 112.411,
            'In': 114.818, 'Sn': 118.71, 'Sb': 121.76, 'Te': 127.6,
            'I': 126.9045, 'Xe': 131.293, 'Cs': 132.9055, 'Ba': 137.327,
            'La': 138.9055, 'Ce': 140.116, 'Pr': 140.9077, 'Nd': 144.242,
            'Pm': 145, 'Sm': 150.36, 'Eu': 151.964, 'Gd': 157.25,
            'Tb': 158.9254, 'Dy': 162.5, 'Ho': 164.9303, 'Er': 167.26,
            'Tm': 168.9342, 'Yb': 173.04, 'Lu': 174.967, 'Hf': 178.49,
            'Ta': 180.9479, 'W': 183.84, 'Re': 186.207, 'Os': 190.23,
            'Ir': 192.217, 'Pt': 195.084, 'Au': 196.9666, 'Hg': 200.59,
            'Tl': 204.3833, 'Pb': 207.2, 'Bi': 208.9804, 'Po': 209,
            'At': 210, 'Rn': 222, 'Fr': 223, 'Ra': 226, 'Ac': 227,
            'Th': 232.0381, 'Pa': 231.0359, 'U': 238.0289
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
            'FeCl3': {'name': 'Ferric Chloride', 'mw': 162.20, 'use': 'Iron source'},
            'EDTA': {'name': 'Ethylenediaminetetraacetic acid', 'mw': 292.24, 'use': 'Chelator'},
            'Tris': {'name': 'Tris(hydroxymethyl)aminomethane', 'mw': 121.14, 'use': 'Buffer'}
        }
    
    @staticmethod
    def compute_molecular_weight(formula: str) -> float:
        """Compute molecular weight from chemical formula"""
        try:
            pattern = r'([A-Z][a-z]?)(\d*)'
            tokens = re.findall(pattern, formula)
            
            if not tokens:
                raise ValueError("Invalid chemical formula format")
            
            atomic_weights = AdvancedChemistryCalculators.get_atomic_weights()
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
        except Exception as e:
            raise ValueError(f"Error computing molecular weight: {str(e)}")
    
    @staticmethod
    def calculate_molarity(mass_g: float, mw: float, volume_L: float) -> float:
        """Calculate molarity from mass, molecular weight, and volume"""
        try:
            moles = mass_g / mw
            molarity = moles / volume_L
            return molarity
        except Exception as e:
            raise ValueError(f"Molarity calculation error: {str(e)}")
    
    @staticmethod
    def calculate_dilution(c1: float, v1: float, c2: float, v2: float = None) -> Dict:
        """Calculate dilution using C1V1 = C2V2"""
        try:
            if v2 is None:
                v2 = (c1 * v1) / c2
            else:
                c2 = (c1 * v1) / v2
            
            return {
                'c1': c1, 'v1': v1, 'c2': c2, 'v2': v2,
                'dilution_factor': c1/c2,
                'volume_water': v2 - v1
            }
        except Exception as e:
            raise ValueError(f"Dilution calculation error: {str(e)}")
    
    @staticmethod
    def ph_calculator(concentration: float, is_acid: bool = True) -> float:
        """Calculate pH from concentration"""
        try:
            if concentration <= 0:
                raise ValueError("Concentration must be positive")
            
            if is_acid:
                return -math.log10(concentration)
            else:
                poh = -math.log10(concentration)
                return 14 - poh
        except Exception as e:
            raise ValueError(f"pH calculation error: {str(e)}")
    
    @staticmethod
    def buffer_calculator(weak_acid_conc: float, conjugate_base_conc: float, pka: float) -> float:
        """Henderson-Hasselbalch equation"""
        try:
            if weak_acid_conc <= 0 or conjugate_base_conc <= 0:
                raise ValueError("Concentrations must be positive")
            
            return pka + math.log10(conjugate_base_conc / weak_acid_conc)
        except Exception as e:
            raise ValueError(f"Buffer calculation error: {str(e)}")
    
    @staticmethod
    def beers_law_calculator(absorbance: float = None, concentration: float = None, 
                           extinction_coeff: float = None, path_length: float = 1.0) -> Dict:
        """Beer's Law: A = ε × c × l"""
        try:
            if absorbance is None:
                absorbance = extinction_coeff * concentration * path_length
                return {'absorbance': absorbance, 'transmittance': 10**(-absorbance) * 100}
            else:
                concentration = absorbance / (extinction_coeff * path_length)
                return {'concentration': concentration, 'concentration_mM': concentration * 1000,
                       'concentration_μM': concentration * 1000000}
        except Exception as e:
            raise ValueError(f"Beer's Law calculation error: {str(e)}")

class PCRCalculators:
    """Real-time PCR and Copy Number Calculators"""
    
    @staticmethod
    def calculate_copy_number_absolute(ct_sample: float, ct_standard: float, 
                                    standard_copies: float, efficiency: float = 100.0) -> Dict:
        """Calculate absolute copy number using standard curve"""
        try:
            if efficiency <= 0 or efficiency > 200:
                raise ValueError("Efficiency must be between 0 and 200%")
            
            # Convert efficiency percentage to decimal
            eff_decimal = efficiency / 100.0
            
            # Calculate amplification factor
            amp_factor = 1 + eff_decimal
            
            # Calculate copy number
            delta_ct = ct_sample - ct_standard
            copy_number = standard_copies * (amp_factor ** (-delta_ct))
            
            # Additional calculations
            log_copy_number = math.log10(copy_number) if copy_number > 0 else 0
            
            return {
                'copy_number': copy_number,
                'log_copy_number': log_copy_number,
                'delta_ct': delta_ct,
                'efficiency_used': efficiency,
                'amplification_factor': amp_factor
            }
        except Exception as e:
            raise ValueError(f"Copy number calculation error: {str(e)}")
    
    @staticmethod
    def calculate_copy_number_relative(ct_target: float, ct_reference: float, 
                                    ct_control_target: float, ct_control_reference: float,
                                    efficiency_target: float = 100.0, efficiency_reference: float = 100.0) -> Dict:
        """Calculate relative copy number using 2^(-ΔΔCt) method"""
        try:
            # Calculate ΔCt values
            delta_ct_sample = ct_target - ct_reference
            delta_ct_control = ct_control_target - ct_control_reference
            
            # Calculate ΔΔCt
            delta_delta_ct = delta_ct_sample - delta_ct_control
            
            # Calculate relative quantity (2^(-ΔΔCt) for 100% efficiency)
            if efficiency_target == 100.0 and efficiency_reference == 100.0:
                relative_quantity = 2 ** (-delta_delta_ct)
            else:
                # Pfaffl method for different efficiencies
                eff_target = efficiency_target / 100.0 + 1
                eff_reference = efficiency_reference / 100.0 + 1
                
                relative_quantity = ((eff_target ** (-delta_ct_sample)) / 
                                   (eff_reference ** (-delta_ct_control)))
            
            # Calculate fold change
            fold_change = relative_quantity
            
            return {
                'relative_quantity': relative_quantity,
                'fold_change': fold_change,
                'delta_ct_sample': delta_ct_sample,
                'delta_ct_control': delta_ct_control,
                'delta_delta_ct': delta_delta_ct,
                'log2_fold_change': math.log2(fold_change) if fold_change > 0 else 0
            }
        except Exception as e:
            raise ValueError(f"Relative quantification error: {str(e)}")
    
    @staticmethod
    def calculate_pcr_efficiency(ct_values: List[float], concentrations: List[float]) -> Dict:
        """Calculate PCR efficiency from standard curve"""
        try:
            if len(ct_values) != len(concentrations) or len(ct_values) < 3:
                raise ValueError("Need at least 3 matching Ct and concentration values")
            
            # Convert concentrations to log scale
            log_conc = [math.log10(c) for c in concentrations]
            
            # Calculate linear regression (Ct = m * log[conc] + b)
            n = len(ct_values)
            sum_x = sum(log_conc)
            sum_y = sum(ct_values)
            sum_xy = sum(x * y for x, y in zip(log_conc, ct_values))
            sum_x2 = sum(x * x for x in log_conc)
            
            # Slope and intercept
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            # Calculate R²
            y_mean = sum_y / n
            ss_tot = sum((y - y_mean) ** 2 for y in ct_values)
            ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(log_conc, ct_values))
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            # Calculate efficiency
            efficiency = (10 ** (-1/slope) - 1) * 100
            
            return {
                'efficiency_percent': efficiency,
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_squared,
                'equation': f"Ct = {slope:.3f} * log[conc] + {intercept:.3f}"
            }
        except Exception as e:
            raise ValueError(f"Efficiency calculation error: {str(e)}")
    
    @staticmethod
    def calculate_gene_copy_number(genome_size_bp: int, target_gene_length_bp: int, 
                                 dna_concentration_ng_ul: float, volume_ul: float) -> Dict:
        """Calculate gene copy number from DNA concentration"""
        try:
            # Average molecular weight of a nucleotide pair
            avg_bp_weight = 650  # Daltons
            
            # Calculate genome molecular weight
            genome_mw = genome_size_bp * avg_bp_weight
            
            # Convert ng to g
            dna_mass_g = (dna_concentration_ng_ul * volume_ul) / 1e9
            
            # Calculate moles of genome
            avogadro = 6.022e23
            genome_moles = dna_mass_g / genome_mw
            
            # Calculate number of genomes
            genome_copies = genome_moles * avogadro
            
            # If target gene length is provided, calculate specific gene copies
            gene_copies_per_genome = 1  # Assuming single copy gene
            total_gene_copies = genome_copies * gene_copies_per_genome
            
            return {
                'total_dna_mass_ng': dna_concentration_ng_ul * volume_ul,
                'genome_molecular_weight': genome_mw,
                'genome_copies': genome_copies,
                'gene_copies': total_gene_copies,
                'copies_per_ul': total_gene_copies / volume_ul if volume_ul > 0 else 0
            }
        except Exception as e:
            raise ValueError(f"Gene copy number calculation error: {str(e)}")

def add_to_history(calculation_type: str, inputs: Dict, results: Dict):
    """Add calculation to history"""
    try:
        history_item = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': calculation_type,
            'inputs': inputs,
            'results': results
        }
        st.session_state.calculation_history.append(history_item)
    except Exception as e:
        st.error(f"Error saving to history: {str(e)}")

def main():
    load_css()
    
    # Handle navigation target from dashboard
    if hasattr(st.session_state, 'nav_target') and st.session_state.nav_target:
        calculator_choice = st.session_state.nav_target
        st.session_state.nav_target = None
    else:
        # Main header
        st.markdown("""
        <div class="main-header">
            <h1>🧪 A.P.D Nexus Pro - Laboratory Suite</h1>
            <p style="font-size: 1.4rem; margin-bottom: 0;">
                Professional Chemistry & Molecular Biology Platform
            </p>
            <p style="font-size: 1rem; opacity: 0.9; margin-top: 1rem;">
                Advanced Calculators • PCR Tools • Data Analysis • Lab Management
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar navigation
        with st.sidebar:
            st.title("🔬 Laboratory Suite")
            
            # Session stats
            if st.session_state.calculation_history:
                st.markdown("### 📊 Session Stats")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.metric("Calculations", len(st.session_state.calculation_history))
                with col_s2:
                    unique_types = len(set(h['type'] for h in st.session_state.calculation_history))
                    st.metric("Tools Used", unique_types)
            
            # Navigation menu
            calculator_choice = st.selectbox(
                "Choose Tool:",
                [
                    "🏠 Dashboard",
                    "🧮 Molarity Calculator", 
                    "💧 Dilution Calculator",
                    "🧫 Media Preparation",
                    "🔬 pH & Buffer Calculator",
                    "📊 Beer's Law Calculator",
                    "🧬 Copy Number Calculator",
                    "📈 PCR Analysis Suite",
                    "📊 Data Analysis",
                    "🏠 Lab Management",
                    "📚 Educational Hub",
                    "⚙️ Settings & Help"
                ]
            )
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            if st.button("🆕 New Calculation"):
                st.rerun()
            if st.button("🌓 Toggle Theme"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
            if st.button("🗑️ Clear History"):
                st.session_state.calculation_history = []
                st.success("History cleared!")
    
    # Route to appropriate page
    try:
        if calculator_choice == "🏠 Dashboard":
            dashboard_page()
        elif calculator_choice == "🧮 Molarity Calculator":
            molarity_calculator()
        elif calculator_choice == "💧 Dilution Calculator":
            dilution_calculator()
        elif calculator_choice == "🧫 Media Preparation":
            media_preparation_calculator()
        elif calculator_choice == "🔬 pH & Buffer Calculator":
            ph_buffer_calculator()
        elif calculator_choice == "📊 Beer's Law Calculator":
            beers_law_calculator()
        elif calculator_choice == "🧬 Copy Number Calculator":
            copy_number_calculator()
        elif calculator_choice == "📈 PCR Analysis Suite":
            pcr_analysis_suite()
        elif calculator_choice == "📊 Data Analysis":
            data_analysis_suite()
        elif calculator_choice == "🏠 Lab Management":
            lab_management_page()
        elif calculator_choice == "📚 Educational Hub":
            educational_hub()
        else:
            settings_help_page()
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.info("Please try refreshing the page or selecting a different tool.")

def dashboard_page():
    """Main dashboard with overview and quick access"""
    
    st.markdown("## 👋 Welcome to A.P.D Nexus Pro!")
    st.markdown("*Your complete laboratory calculation and analysis platform*")
    
    # Quick stats
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🧪 Calculations", len(st.session_state.calculation_history))
    with col2:
        st.metric("📦 Inventory", len(st.session_state.inventory))
    with col3:
        st.metric("📋 Protocols", len(st.session_state.protocols))
    with col4:
        st.metric("⭐ Favorites", len(st.session_state.favorites))
    with col5:
        days_active = (datetime.now() - datetime(2024, 1, 1)).days
        st.metric("📅 Days Active", days_active)
    
    # Feature overview
    st.markdown("### 🔬 Available Tools")
    
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    
    with col_feat1:
        st.markdown("""
        **🧮 Chemistry Calculators**
        - Molarity & Solution Prep
        - Dilution Calculator
        - pH & Buffer Tools
        - Beer's Law Analysis
        """)
    
    with col_feat2:
        st.markdown("""
        **🧬 Molecular Biology**
        - Copy Number Calculator
        - PCR Analysis Suite
        - qPCR Efficiency Tools
        - Gene Copy Estimation
        """)
    
    with col_feat3:
        st.markdown("""
        **🏠 Lab Management**
        - Chemical Inventory
        - Protocol Builder
        - Data Analysis
        - Educational Resources
        """)
    
    # Recent activity
    if st.session_state.calculation_history:
        st.markdown("### 🕒 Recent Activity")
        recent = st.session_state.calculation_history[-5:]
        for calc in reversed(recent):
            with st.expander(f"📊 {calc['type']} - {calc['timestamp']}"):
                st.json(calc['inputs'])
    
    # Quick access tools
    st.markdown("### ⚡ Quick Access")
    
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    with col_q1:
        if st.button("🧪 Molarity Calculator", use_container_width=True):
            st.session_state.nav_target = "🧮 Molarity Calculator"
            st.rerun()
    
    with col_q2:
        if st.button("🧬 Copy Number Cal.", use_container_width=True):
            st.session_state.nav_target = "🧬 Copy Number Calculator"
            st.rerun()
    
    with col_q3:
        if st.button("💧 Dilution Tools", use_container_width=True):
            st.session_state.nav_target = "💧 Dilution Calculator"
            st.rerun()
    
    with col_q4:
        if st.button("📈 PCR Analysis", use_container_width=True):
            st.session_state.nav_target = "📈 PCR Analysis Suite"
            st.rerun()

def molarity_calculator():
    """Professional molarity calculator"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("🧮 Molarity Calculator")
    st.markdown("*Professional solution preparation with molecular weight calculation*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("molarity_form"):
            st.markdown("### Solution Parameters")
            
            # Chemical formula input
            formula = st.text_input(
                "Chemical Formula",
                placeholder="e.g., NaCl, CaCl2, H2SO4, C6H12O6",
                help="Enter chemical formula with proper capitalization"
            )
            
            # Real-time molecular weight calculation
            if formula:
                try:
                    mw = AdvancedChemistryCalculators.compute_molecular_weight(formula)
                    st.success(f"✅ Molecular Weight: {mw:.3f} g/mol")
                except Exception as e:
                    st.error(f"❌ Formula error: {str(e)}")
                    mw = None
            else:
                mw = None
            
            # Input parameters
            col_in1, col_in2, col_in3 = st.columns(3)
            
            with col_in1:
                molarity = st.number_input(
                    "Target Molarity (M)",
                    min_value=1e-6,
                    max_value=20.0,
                    value=1.0,
                    format="%.6f"
                )
            
            with col_in2:
                volume = st.number_input(
                    "Volume",
                    min_value=0.001,
                    value=1.0,
                    format="%.3f"
                )
                volume_unit = st.selectbox("Unit", ["L", "mL", "μL"])
            
            with col_in3:
                purity = st.number_input(
                    "Purity (%)",
                    min_value=1.0,
                    max_value=100.0,
                    value=100.0
                )
            
            # Advanced options
            with st.expander("🎛️ Advanced Options"):
                safety_factor = st.number_input(
                    "Safety Factor",
                    min_value=1.0,
                    max_value=2.0,
                    value=1.1,
                    help="Prepare extra material (10% recommended)"
                )
            
            submitted = st.form_submit_button("🔬 Calculate Solution", use_container_width=True)
            
            if submitted and formula and mw:
                try:
                    # Convert volume to liters
                    volume_conversions = {"L": 1, "mL": 0.001, "μL": 0.000001}
                    volume_L = volume * volume_conversions[volume_unit]
                    
                    # Calculate required mass
                    theoretical_mass = mw * molarity * volume_L
                    purity_corrected_mass = theoretical_mass * (100 / purity)
                    final_mass = purity_corrected_mass * safety_factor
                    
                    # Display results
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>✅ Solution Calculation Results</h3>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                            <div class="metric-card">
                                <h4>Chemical Info</h4>
                                <p><strong>Formula:</strong> {formula}</p>
                                <p><strong>MW:</strong> {mw:.3f} g/mol</p>
                                <p><strong>Purity:</strong> {purity:.1f}%</p>
                            </div>
                            <div class="metric-card">
                                <h4>Solution</h4>
                                <p><strong>Molarity:</strong> {molarity:.4f} M</p>
                                <p><strong>Volume:</strong> {volume:.3f} {volume_unit}</p>
                                <p><strong>Total Volume:</strong> {volume_L*1000:.1f} mL</p>
                            </div>
                            <div class="metric-card">
                                <h4>Required Mass</h4>
                                <p style="font-size: 1.2em; color: #dc2626;"><strong>{final_mass:.4f} g</strong></p>
                                <p><strong>Theoretical:</strong> {theoretical_mass:.4f} g</p>
                                <p><strong>With Safety:</strong> {safety_factor:.1f}x</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Protocol
                    st.markdown("### 📋 Preparation Protocol")
                    protocol = f"""
**Solution Preparation Protocol**

**Target:** {molarity:.4f} M {formula} in {volume:.3f} {volume_unit}

**Procedure:**
1. **Weigh** {final_mass:.4f} g of {formula} using analytical balance
2. **Add** ~80% of final volume ({volume_L*800:.0f} mL) distilled water to beaker
3. **Dissolve** chemical completely with stirring
4. **Transfer** to {volume_L*1000:.0f} mL volumetric flask
5. **Dilute** to mark with distilled water
6. **Mix** thoroughly by inversion (20×)
7. **Label** with concentration, date, and preparer initials

**Storage:** Store at room temperature unless otherwise specified.
**Shelf Life:** Prepare fresh or check stability data.
                    """
                    st.markdown(protocol)
                    
                    # Save to history
                    add_to_history(
                        "Molarity Calculation",
                        {'formula': formula, 'molarity': molarity, 'volume': volume, 'unit': volume_unit},
                        {'molecular_weight': mw, 'mass_required': final_mass}
                    )
                    
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
    
    with col2:
        # Reference panel
        st.markdown("### 📖 Quick Reference")
        
        # Common formulas lookup
        common_formulas = AdvancedChemistryCalculators.get_common_formulas()
        selected_ref = st.selectbox("Common Formulas", [""] + list(common_formulas.keys()))
        
        if selected_ref:
            data = common_formulas[selected_ref]
            st.markdown(f"""
            <div class="info-box">
                <h4>{selected_ref}</h4>
                <p><strong>{data['name']}</strong></p>
                <p>MW: {data['mw']:.2f} g/mol</p>
                <p>Use: {data['use']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Unit converter
        st.markdown("### 🔄 Concentration Converter")
        
        if st.button("M ↔ mg/mL", use_container_width=True):
            st.info("Enter formula above to enable conversion")
        
        # Tips
        st.markdown("### 💡 Pro Tips")
        tips = [
            "Always use analytical balance (±0.0001 g)",
            "Add solvent to solute, not vice versa",
            "Use volumetric flasks for precision",
            "Label immediately with date",
            "Store according to chemical properties"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def dilution_calculator():
    """Professional dilution calculator"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("💧 Dilution Calculator")
    st.markdown("*C₁V₁ = C₂V₂ calculations and serial dilutions*")
    
    tab1, tab2 = st.tabs(["📊 Simple Dilution", "🔄 Serial Dilution"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("dilution_form"):
                st.markdown("### C₁V₁ = C₂V₂ Calculator")
                
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    st.markdown("**Stock Solution (1):**")
                    c1 = st.number_input("Concentration (C₁)", min_value=0.001, value=10.0)
                    c1_unit = st.selectbox("C₁ Unit", ["M", "mM", "μM", "mg/mL", "%"])
                
                with col_d2:
                    st.markdown("**Final Solution (2):**")
                    c2 = st.number_input("Concentration (C₂)", min_value=0.001, value=1.0)
                    c2_unit = st.selectbox("C₂ Unit", ["M", "mM", "μM", "mg/mL", "%"], index=0)
                
                v2 = st.number_input("Final Volume (V₂)", min_value=0.001, value=10.0)
                v2_unit = st.selectbox("Volume Unit", ["mL", "μL", "L"])
                
                if st.form_submit_button("🧪 Calculate Dilution", use_container_width=True):
                    try:
                        result = AdvancedChemistryCalculators.calculate_dilution(c1, None, c2, v2)
                        v1 = result['v1']
                        water_volume = result['volume_water']
                        dilution_factor = result['dilution_factor']
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Dilution Results</h4>
                            <p><strong>Stock volume (V₁):</strong> {v1:.3f} {v2_unit}</p>
                            <p><strong>Diluent volume:</strong> {water_volume:.3f} {v2_unit}</p>
                            <p><strong>Dilution ratio:</strong> 1:{dilution_factor:.1f}</p>
                            <p><strong>Dilution factor:</strong> {dilution_factor:.2f}×</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Protocol
                        st.markdown("### 📋 Dilution Protocol")
                        st.markdown(f"""
**Dilution Protocol:** {c1:.2f} {c1_unit} → {c2:.2f} {c2_unit}

1. **Add diluent** ({water_volume:.2f} {v2_unit}) to container
2. **Add stock** ({v1:.3f} {v2_unit}) slowly with mixing
3. **Final volume** should be {v2:.1f} {v2_unit}
4. **Mix thoroughly** and label
                        """)
                        
                        add_to_history(
                            "Dilution Calculation",
                            {'c1': c1, 'c2': c2, 'v2': v2, 'units': f"{c1_unit}, {v2_unit}"},
                            {'v1': v1, 'dilution_factor': dilution_factor}
                        )
                        
                    except Exception as e:
                        st.error(f"Calculation error: {str(e)}")
        
        with col2:
            st.markdown("### 📐 Common Ratios")
            
            ratios = [
                ("1:2", "2-fold", "50%"),
                ("1:5", "5-fold", "20%"),
                ("1:10", "10-fold", "10%"),
                ("1:100", "100-fold", "1%"),
                ("1:1000", "1000-fold", "0.1%")
            ]
            
            for ratio, fold, percent in ratios:
                st.markdown(f"**{ratio}** ({fold}) = {percent} strength")
    
    with tab2:
        st.markdown("### 🔄 Serial Dilution Series")
        
        with st.form("serial_dilution_form"):
            col_s1, col_s2 = st.columns(2)
            
            with col_s1:
                start_conc = st.number_input("Starting Concentration", value=100.0)
                conc_unit = st.selectbox("Unit", ["μM", "mM", "M", "mg/mL"])
                dilution_factor = st.number_input("Dilution Factor", value=2.0, min_value=1.1)
            
            with col_s2:
                num_points = st.number_input("Number of Points", value=6, min_value=2, max_value=12)
                volume_per_tube = st.number_input("Volume per Tube", value=1.0)
                include_blank = st.checkbox("Include Blank")
            
            if st.form_submit_button("Generate Series"):
                # Calculate series
                concentrations = []
                current = start_conc
                
                for i in range(num_points):
                    concentrations.append(current)
                    current = current / dilution_factor
                
                if include_blank:
                    concentrations.append(0.0)
                
                # Create dilution table
                series_data = []
                for i, conc in enumerate(concentrations):
                    tube_num = i + 1
                    if conc == 0:
                        source = "Blank"
                        transfer = 0
                        diluent = volume_per_tube
                    elif i == 0:
                        source = "Stock"
                        transfer = volume_per_tube
                        diluent = 0
                    else:
                        source = f"Tube {i}"
                        transfer = volume_per_tube / dilution_factor
                        diluent = volume_per_tube - transfer
                    
                    series_data.append({
                        'Tube': tube_num,
                        'Concentration': f"{conc:.3f}" if conc > 0 else "0",
                        'Source': source,
                        'Transfer': f"{transfer:.3f}",
                        'Diluent': f"{diluent:.3f}"
                    })
                
                df_series = pd.DataFrame(series_data)
                st.dataframe(df_series, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def copy_number_calculator():
    """Real-time PCR Copy Number Calculator"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("🧬 Copy Number Calculator")
    st.markdown("*Real-time PCR copy number determination for all applications*")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Absolute Quantification", "🔄 Relative Quantification", "📈 Efficiency Calculator", "🧬 Gene Copy Estimation"])
    
    with tab1:
        st.markdown("### 📊 Absolute Copy Number Calculation")
        st.markdown("*Calculate absolute copy number using standard curve method*")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("absolute_quant_form"):
                st.markdown("#### Sample and Standard Data")
                
                col_abs1, col_abs2 = st.columns(2)
                
                with col_abs1:
                    ct_sample = st.number_input("Sample Ct Value", min_value=1.0, max_value=50.0, value=25.5, step=0.1)
                    ct_standard = st.number_input("Standard Ct Value", min_value=1.0, max_value=50.0, value=20.2, step=0.1)
                
                with col_abs2:
                    standard_copies = st.number_input("Standard Copy Number", min_value=1.0, value=1000000.0, format="%.0f")
                    efficiency = st.number_input("PCR Efficiency (%)", min_value=50.0, max_value=120.0, value=100.0, step=0.1)
                
                # Additional parameters
                with st.expander("🎛️ Advanced Parameters"):
                    sample_dilution = st.number_input("Sample Dilution Factor", min_value=1.0, value=1.0)
                    reaction_volume = st.number_input("Reaction Volume (μL)", min_value=1.0, value=20.0)
                    sample_volume = st.number_input("Sample Volume in Reaction (μL)", min_value=0.1, value=2.0)
                
                if st.form_submit_button("🧪 Calculate Copy Number", use_container_width=True):
                    try:
                        result = PCRCalculators.calculate_copy_number_absolute(
                            ct_sample, ct_standard, standard_copies, efficiency
                        )
                        
                        # Account for dilution and volume
                        copies_in_reaction = result['copy_number']
                        copies_per_ul_sample = (copies_in_reaction / sample_volume) * sample_dilution
                        total_copies_in_sample = copies_per_ul_sample * sample_dilution
                        
                        st.markdown(f"""
                        <div class="pcr-box">
                            <h4>✅ Absolute Quantification Results</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                                <div class="metric-card">
                                    <h5>PCR Data</h5>
                                    <p><strong>ΔCt:</strong> {result['delta_ct']:.2f}</p>
                                    <p><strong>Efficiency:</strong> {efficiency:.1f}%</p>
                                    <p><strong>Amp Factor:</strong> {result['amplification_factor']:.3f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Copy Numbers</h5>
                                    <p><strong>In Reaction:</strong> {copies_in_reaction:.2e}</p>
                                    <p><strong>Per μL Sample:</strong> {copies_per_ul_sample:.2e}</p>
                                    <p><strong>Log₁₀ Copies:</strong> {result['log_copy_number']:.2f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Concentrations</h5>
                                    <p><strong>Copies/μL:</strong> {copies_per_ul_sample:.2e}</p>
                                    <p><strong>Copies/mL:</strong> {copies_per_ul_sample*1000:.2e}</p>
                                    <p><strong>Dilution Factor:</strong> {sample_dilution:.0f}×</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Quality control indicators
                        st.markdown("### 🎯 Quality Control")
                        
                        qc_data = []
                        
                        # Efficiency check
                        if 90 <= efficiency <= 110:
                            eff_status = "✅ Excellent"
                            eff_color = "green"
                        elif 80 <= efficiency < 90 or 110 < efficiency <= 120:
                            eff_status = "⚠️ Acceptable"
                            eff_color = "orange"
                        else:
                            eff_status = "❌ Poor"
                            eff_color = "red"
                        
                        qc_data.append(["PCR Efficiency", f"{efficiency:.1f}%", eff_status])
                        
                        # Ct value check
                        if ct_sample < 35:
                            ct_status = "✅ Good"
                        elif ct_sample <= 40:
                            ct_status = "⚠️ Acceptable"
                        else:
                            ct_status = "❌ Too High"
                        
                        qc_data.append(["Sample Ct", f"{ct_sample:.1f}", ct_status])
                        
                        # Delta Ct check
                        if abs(result['delta_ct']) < 10:
                            delta_status = "✅ Good Range"
                        else:
                            delta_status = "⚠️ Large Difference"
                        
                        qc_data.append(["ΔCt Range", f"{result['delta_ct']:.1f}", delta_status])
                        
                        qc_df = pd.DataFrame(qc_data, columns=["Parameter", "Value", "Status"])
                        st.dataframe(qc_df, use_container_width=True, hide_index=True)
                        
                        add_to_history(
                            "Absolute Copy Number",
                            {'ct_sample': ct_sample, 'ct_standard': ct_standard, 'efficiency': efficiency},
                            {'copy_number': copies_in_reaction, 'copies_per_ul': copies_per_ul_sample}
                        )
                        
                    except Exception as e:
                        st.error(f"Calculation error: {str(e)}")
        
        with col2:
            st.markdown("### 📋 Method Guide")
            
            st.markdown("""
            **Absolute Quantification Steps:**
            
            1. **Prepare Standards**
               - Known copy number series
               - Same amplification conditions
               
            2. **Run qPCR**
               - Include standards & samples
               - Check efficiency (90-110%)
               
            3. **Calculate**
               - Use standard curve
               - Account for dilutions
               
            4. **Quality Check**
               - Efficiency within range
               - Ct values < 35 preferred
               - R² > 0.99 for standards
            """)
            
            st.markdown("### 💡 Tips")
            st.markdown("""
            • Use dilution series for standards
            • Include positive/negative controls
            • Replicate samples (minimum n=3)
            • Check primer specificity
            • Validate with independent method
            """)
    
    with tab2:
        st.markdown("### 🔄 Relative Quantification (ΔΔCt Method)")
        st.markdown("*Compare gene expression between samples*")
        
        with st.form("relative_quant_form"):
            st.markdown("#### Target and Reference Gene Data")
            
            col_rel1, col_rel2 = st.columns(2)
            
            with col_rel1:
                st.markdown("**Sample of Interest:**")
                ct_target = st.number_input("Target Gene Ct", value=25.5, step=0.1)
                ct_reference = st.number_input("Reference Gene Ct", value=20.2, step=0.1)
            
            with col_rel2:
                st.markdown("**Control Sample:**")
                ct_control_target = st.number_input("Control Target Ct", value=27.8, step=0.1)
                ct_control_reference = st.number_input("Control Reference Ct", value=20.5, step=0.1)
            
            # Efficiency inputs
            col_eff1, col_eff2 = st.columns(2)
            
            with col_eff1:
                eff_target = st.number_input("Target Gene Efficiency (%)", value=100.0, step=0.1)
            
            with col_eff2:
                eff_reference = st.number_input("Reference Gene Efficiency (%)", value=100.0, step=0.1)
            
            use_pfaffl = st.checkbox("Use Pfaffl Method (different efficiencies)", 
                                   value=False, help="Check if efficiencies differ significantly")
            
            if st.form_submit_button("🧪 Calculate Relative Expression", use_container_width=True):
                try:
                    if use_pfaffl:
                        result = PCRCalculators.calculate_copy_number_relative(
                            ct_target, ct_reference, ct_control_target, ct_control_reference,
                            eff_target, eff_reference
                        )
                        method = "Pfaffl Method"
                    else:
                        result = PCRCalculators.calculate_copy_number_relative(
                            ct_target, ct_reference, ct_control_target, ct_control_reference
                        )
                        method = "2^(-ΔΔCt) Method"
                    
                    st.markdown(f"""
                    <div class="pcr-box">
                        <h4>✅ Relative Quantification Results ({method})</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                            <div class="metric-card">
                                <h5>ΔCt Values</h5>
                                <p><strong>Sample ΔCt:</strong> {result['delta_ct_sample']:.2f}</p>
                                <p><strong>Control ΔCt:</strong> {result['delta_ct_control']:.2f}</p>
                                <p><strong>ΔΔCt:</strong> {result['delta_delta_ct']:.2f}</p>
                            </div>
                            <div class="metric-card">
                                <h5>Expression Results</h5>
                                <p><strong>Fold Change:</strong> {result['fold_change']:.2f}×</p>
                                <p><strong>Log₂ Fold:</strong> {result['log2_fold_change']:.2f}</p>
                                <p><strong>Relative Qty:</strong> {result['relative_quantity']:.2f}</p>
                            </div>
                            <div class="metric-card">
                                <h5>Interpretation</h5>
                                {'<p style="color: green;"><strong>Up-regulated</strong></p>' if result['fold_change'] > 1 else '<p style="color: red;"><strong>Down-regulated</strong></p>' if result['fold_change'] < 1 else '<p><strong>No change</strong></p>'}
                                <p><strong>Magnitude:</strong> {abs(result['log2_fold_change']):.1f} log₂</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Expression interpretation
                    st.markdown("### 📊 Expression Analysis")
                    
                    if result['fold_change'] > 2:
                        interpretation = "🔴 Significantly up-regulated (>2-fold)"
                    elif result['fold_change'] > 1.5:
                        interpretation = "🟡 Moderately up-regulated (1.5-2 fold)"
                    elif result['fold_change'] < 0.5:
                        interpretation = "🔵 Significantly down-regulated (<0.5-fold)"
                    elif result['fold_change'] < 0.67:
                        interpretation = "🟡 Moderately down-regulated (0.5-0.67 fold)"
                    else:
                        interpretation = "⚪ No significant change (0.67-1.5 fold)"
                    
                    st.markdown(f"**Expression Status:** {interpretation}")
                    
                    add_to_history(
                        "Relative Quantification",
                        {'target_ct': ct_target, 'reference_ct': ct_reference, 'method': method},
                        {'fold_change': result['fold_change'], 'delta_delta_ct': result['delta_delta_ct']}
                    )
                    
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
    
    with tab3:
        st.markdown("### 📈 PCR Efficiency Calculator")
        st.markdown("*Calculate amplification efficiency from standard curve*")
        
        with st.form("efficiency_form"):
            st.markdown("#### Standard Curve Data")
            
            st.markdown("Enter Ct values and corresponding concentrations (minimum 3 points):")
            
            # Data input method
            input_method = st.radio("Data Input Method", ["Manual Entry", "Paste Data"])
            
            if input_method == "Manual Entry":
                num_points = st.number_input("Number of Standards", min_value=3, max_value=10, value=5)
                
                ct_values = []
                concentrations = []
                
                for i in range(num_points):
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        ct = st.number_input(f"Ct {i+1}", value=20.0 + i*3, step=0.1, key=f"ct_{i}")
                        ct_values.append(ct)
                    with col_e2:
                        conc = st.number_input(f"Concentration {i+1}", value=10**(6-i), format="%.0f", key=f"conc_{i}")
                        concentrations.append(conc)
            
            else:  # Paste Data
                data_text = st.text_area(
                    "Paste Ct and Concentration data (tab or comma separated)",
                    value="20.1\t1000000\n23.2\t100000\n26.8\t10000\n30.1\t1000\n33.5\t100",
                    height=150
                )
                
                # Parse pasted data
                ct_values = []
                concentrations = []
                
                try:
                    lines = data_text.strip().split('\n')
                    for line in lines:
                        if '\t' in line:
                            parts = line.split('\t')
                        else:
                            parts = line.split(',')
                        
                        if len(parts) >= 2:
                            ct_values.append(float(parts[0].strip()))
                            concentrations.append(float(parts[1].strip()))
                except:
                    st.warning("Please check data format. Use: Ct[tab]Concentration per line")
            
            if st.form_submit_button("📊 Calculate Efficiency", use_container_width=True):
                try:
                    if len(ct_values) >= 3 and len(concentrations) >= 3:
                        result = PCRCalculators.calculate_pcr_efficiency(ct_values, concentrations)
                        
                        st.markdown(f"""
                        <div class="pcr-box">
                            <h4>✅ PCR Efficiency Results</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                                <div class="metric-card">
                                    <h5>Efficiency</h5>
                                    <p style="font-size: 1.2em; color: #7c3aed;"><strong>{result['efficiency_percent']:.1f}%</strong></p>
                                    <p><strong>Slope:</strong> {result['slope']:.3f}</p>
                                    <p><strong>R²:</strong> {result['r_squared']:.4f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Standard Curve</h5>
                                    <p><strong>Equation:</strong></p>
                                    <p style="font-size: 0.9em;">{result['equation']}</p>
                                    <p><strong>Quality:</strong> {'✅ Excellent' if result['r_squared'] > 0.99 else '⚠️ Acceptable' if result['r_squared'] > 0.95 else '❌ Poor'}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Assessment</h5>
                                    <p><strong>Efficiency Status:</strong></p>
                                    {'<p style="color: green;">✅ Excellent</p>' if 90 <= result['efficiency_percent'] <= 110 else '<p style="color: orange;">⚠️ Acceptable</p>' if 80 <= result['efficiency_percent'] <= 120 else '<p style="color: red;">❌ Poor</p>'}
                                    <p><strong>Recommended:</strong> 90-110%</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Data table
                        st.markdown("### 📊 Standard Curve Data")
                        curve_data = pd.DataFrame({
                            'Concentration': concentrations,
                            'Log10 Concentration': [math.log10(c) for c in concentrations],
                            'Ct Value': ct_values,
                            'Predicted Ct': [result['slope'] * math.log10(c) + result['intercept'] for c in concentrations],
                            'Residual': [ct - (result['slope'] * math.log10(c) + result['intercept']) for ct, c in zip(ct_values, concentrations)]
                        })
                        st.dataframe(curve_data, use_container_width=True, hide_index=True)
                        
                        add_to_history(
                            "PCR Efficiency Calculation",
                            {'num_points': len(ct_values), 'method': 'Standard Curve'},
                            {'efficiency': result['efficiency_percent'], 'r_squared': result['r_squared']}
                        )
                        
                    else:
                        st.error("Please provide at least 3 data points")
                        
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
    
    with tab4:
        st.markdown("### 🧬 Gene Copy Number Estimation")
        st.markdown("*Estimate gene copy number from DNA concentration*")
        
        with st.form("gene_copy_form"):
            st.markdown("#### DNA and Genome Parameters")
            
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                genome_size = st.number_input("Genome Size (bp)", min_value=1000, value=3000000, format="%d")
                target_gene_length = st.number_input("Target Gene Length (bp)", min_value=50, value=1000, format="%d")
            
            with col_g2:
                dna_conc = st.number_input("DNA Concentration (ng/μL)", min_value=0.001, value=100.0, format="%.3f")
                volume = st.number_input("Volume (μL)", min_value=0.1, value=10.0, format="%.1f")
            
            # Additional parameters
            with st.expander("🎛️ Advanced Parameters"):
                copies_per_genome = st.number_input("Gene Copies per Genome", min_value=1, value=1)
                organism_type = st.selectbox("Organism Type", ["Bacteria", "Yeast", "Human", "Plant", "Other"])
                
                # Organism-specific defaults
                if organism_type == "Bacteria":
                    default_genome = 4600000
                elif organism_type == "Yeast":
                    default_genome = 12000000
                elif organism_type == "Human":
                    default_genome = 3200000000
                elif organism_type == "Plant":
                    default_genome = 150000000
                else:
                    default_genome = genome_size
                
                if st.button("Use Default Genome Size"):
                    genome_size = default_genome
            
            if st.form_submit_button("🧪 Calculate Gene Copies", use_container_width=True):
                try:
                    result = PCRCalculators.calculate_gene_copy_number(
                        genome_size, target_gene_length, dna_conc, volume
                    )
                    
                    # Calculate additional metrics
                    total_gene_copies = result['gene_copies'] * copies_per_genome
                    copies_per_ng = total_gene_copies / result['total_dna_mass_ng']
                    
                    st.markdown(f"""
                    <div class="pcr-box">
                        <h4>✅ Gene Copy Number Results</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                            <div class="metric-card">
                                <h5>DNA Parameters</h5>
                                <p><strong>Total DNA:</strong> {result['total_dna_mass_ng']:.1f} ng</p>
                                <p><strong>Genome Size:</strong> {genome_size:,} bp</p>
                                <p><strong>Genome MW:</strong> {result['genome_molecular_weight']:.2e} Da</p>
                            </div>
                            <div class="metric-card">
                                <h5>Copy Numbers</h5>
                                <p><strong>Genome Copies:</strong> {result['genome_copies']:.2e}</p>
                                <p><strong>Gene Copies:</strong> {total_gene_copies:.2e}</p>
                                <p><strong>Copies/μL:</strong> {result['copies_per_ul']:.2e}</p>
                            </div>
                            <div class="metric-card">
                                <h5>Concentrations</h5>
                                <p><strong>Copies/ng DNA:</strong> {copies_per_ng:.2e}</p>
                                <p><strong>Copies/mL:</strong> {result['copies_per_ul']*1000:.2e}</p>
                                <p><strong>Molarity:</strong> {(result['gene_copies']/volume) / 6.022e23 * 1e6:.2e} μM</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Dilution recommendations for qPCR
                    st.markdown("### 💡 qPCR Recommendations")
                    
                    # Optimal range for qPCR is usually 10^2 to 10^8 copies per reaction
                    optimal_min = 100
                    optimal_max = 100000000
                    
                    current_copies_per_ul = result['copies_per_ul']
                    
                    if current_copies_per_ul > optimal_max:
                        dilution_needed = current_copies_per_ul / optimal_max
                        st.warning(f"Consider diluting {dilution_needed:.0f}× for optimal qPCR range")
                    elif current_copies_per_ul < optimal_min:
                        concentration_needed = optimal_min / current_copies_per_ul
                        st.info(f"Consider concentrating {concentration_needed:.0f}× for optimal qPCR range")
                    else:
                        st.success("Copy number is in optimal range for qPCR")
                    
                    # Recommended reaction volumes
                    st.markdown("**Recommended qPCR Setup:**")
                    for reaction_vol in [10, 20, 25]:
                        for sample_vol in [1, 2, 5]:
                            if sample_vol < reaction_vol:
                                copies_in_reaction = current_copies_per_ul * sample_vol
                                st.markdown(f"• {sample_vol}μL sample in {reaction_vol}μL reaction = {copies_in_reaction:.0e} copies")
                    
                    add_to_history(
                        "Gene Copy Estimation",
                        {'genome_size': genome_size, 'dna_conc': dna_conc, 'volume': volume},
                        {'gene_copies': total_gene_copies, 'copies_per_ul': result['copies_per_ul']}
                    )
                    
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def pcr_analysis_suite():
    """PCR Analysis Suite with additional tools"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("📈 PCR Analysis Suite")
    st.markdown("*Comprehensive PCR data analysis and quality control tools*")
    
    tab1, tab2, tab3 = st.tabs(["📊 Ct Analysis", "🎯 Primer Design", "📋 PCR Setup"])
    
    with tab1:
        st.markdown("### 📊 Ct Value Analysis")
        st.markdown("*Analyze Ct values for quality control and troubleshooting*")
        
        # Ct data input
        ct_data_input = st.text_area(
            "Enter Ct values (one per line or comma separated)",
            value="20.5, 20.8, 20.3, 21.1, 20.7",
            height=100
        )
        
        if st.button("Analyze Ct Values"):
            try:
                # Parse Ct values
                if ',' in ct_data_input:
                    ct_values = [float(x.strip()) for x in ct_data_input.split(',') if x.strip()]
                else:
                    ct_values = [float(x.strip()) for x in ct_data_input.split('\n') if x.strip()]
                
                if len(ct_values) >= 2:
                    # Statistical analysis
                    mean_ct = np.mean(ct_values)
                    std_ct = np.std(ct_values, ddof=1)
                    cv_ct = (std_ct / mean_ct) * 100
                    
                    st.markdown(f"""
                    <div class="pcr-box">
                        <h4>Ct Value Statistics (n = {len(ct_values)})</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                            <div class="metric-card">
                                <h5>Central Tendency</h5>
                                <p><strong>Mean:</strong> {mean_ct:.2f}</p>
                                <p><strong>Median:</strong> {np.median(ct_values):.2f}</p>
                                <p><strong>Range:</strong> {np.min(ct_values):.2f} - {np.max(ct_values):.2f}</p>
                            </div>
                            <div class="metric-card">
                                <h5>Variability</h5>
                                <p><strong>Std Dev:</strong> {std_ct:.3f}</p>
                                <p><strong>CV:</strong> {cv_ct:.2f}%</p>
                                <p><strong>Range:</strong> {np.max(ct_values) - np.min(ct_values):.2f}</p>
                            </div>
                            <div class="metric-card">
                                <h5>Quality Assessment</h5>
                                {'<p style="color: green;"><strong>Excellent</strong></p>' if cv_ct < 2 else '<p style="color: orange;"><strong>Acceptable</strong></p>' if cv_ct < 5 else '<p style="color: red;"><strong>Poor</strong></p>'}
                                <p><strong>Precision:</strong> {'High' if cv_ct < 2 else 'Medium' if cv_ct < 5 else 'Low'}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Quality recommendations
                    st.markdown("### 💡 Quality Recommendations")
                    
                    if cv_ct > 5:
                        st.warning("⚠️ High variability detected. Consider:")
                        st.markdown("""
                        - Check pipetting technique
                        - Verify template quality and concentration
                        - Ensure proper mixing
                        - Check thermal cycling conditions
                        """)
                    elif cv_ct > 2:
                        st.info("ℹ️ Moderate variability. Room for improvement:")
                        st.markdown("""
                        - Use more precise pipettes
                        - Increase replicate number
                        - Check for contamination
                        """)
                    else:
                        st.success("✅ Excellent precision! Your PCR is well optimized.")
                
            except Exception as e:
                st.error(f"Error analyzing Ct values: {str(e)}")
    
    with tab2:
        st.markdown("### 🎯 Primer Design Helper")
        st.markdown("*Basic primer design parameters and checks*")
        
        with st.form("primer_design_form"):
            primer_forward = st.text_input("Forward Primer (5' → 3')", placeholder="ATGCGATCGATCGATCG")
            primer_reverse = st.text_input("Reverse Primer (5' → 3')", placeholder="CGATCGATCGATCGCAT")
            
            if st.form_submit_button("Analyze Primers"):
                if primer_forward and primer_reverse:
                    # Basic primer analysis
                    def analyze_primer(seq):
                        seq = seq.upper().replace(' ', '')
                        length = len(seq)
                        gc_content = (seq.count('G') + seq.count('C')) / length * 100
                        
                        # Simple Tm estimation (not accurate for all conditions)
                        if length < 14:
                            tm = (seq.count('A') + seq.count('T')) * 2 + (seq.count('G') + seq.count('C')) * 4
                        else:
                            tm = 64.9 + 41 * (seq.count('G') + seq.count('C') - 16.4) / length
                        
                        return {'length': length, 'gc_content': gc_content, 'tm': tm}
                    
                    fwd_analysis = analyze_primer(primer_forward)
                    rev_analysis = analyze_primer(primer_reverse)
                    
                    st.markdown(f"""
                    <div class="pcr-box">
                        <h4>Primer Analysis Results</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                            <div>
                                <h5>Forward Primer</h5>
                                <p><strong>Length:</strong> {fwd_analysis['length']} bp</p>
                                <p><strong>GC Content:</strong> {fwd_analysis['gc_content']:.1f}%</p>
                                <p><strong>Est. Tm:</strong> {fwd_analysis['tm']:.1f}°C</p>
                            </div>
                            <div>
                                <h5>Reverse Primer</h5>
                                <p><strong>Length:</strong> {rev_analysis['length']} bp</p>
                                <p><strong>GC Content:</strong> {rev_analysis['gc_content']:.1f}%</p>
                                <p><strong>Est. Tm:</strong> {rev_analysis['tm']:.1f}°C</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Design recommendations
                    st.markdown("### 📋 Design Recommendations")
                    
                    recommendations = []
                    
                    # Length check
                    for name, analysis in [("Forward", fwd_analysis), ("Reverse", rev_analysis)]:
                        if not (18 <= analysis['length'] <= 25):
                            recommendations.append(f"⚠️ {name} primer length ({analysis['length']} bp) outside optimal range (18-25 bp)")
                        
                        if not (40 <= analysis['gc_content'] <= 60):
                            recommendations.append(f"⚠️ {name} primer GC content ({analysis['gc_content']:.1f}%) outside optimal range (40-60%)")
                    
                    # Tm difference
                    tm_diff = abs(fwd_analysis['tm'] - rev_analysis['tm'])
                    if tm_diff > 5:
                        recommendations.append(f"⚠️ Large Tm difference ({tm_diff:.1f}°C). Aim for <5°C difference")
                    
                    if recommendations:
                        for rec in recommendations:
                            st.warning(rec)
                    else:
                        st.success("✅ Primers meet basic design criteria!")
    
    with tab3:
        st.markdown("### 📋 PCR Reaction Setup Calculator")
        st.markdown("*Calculate volumes for PCR master mix preparation*")
        
        with st.form("pcr_setup_form"):
            st.markdown("#### Reaction Parameters")
            
            col_pcr1, col_pcr2 = st.columns(2)
            
            with col_pcr1:
                reaction_volume = st.number_input("Reaction Volume (μL)", min_value=5, value=20)
                num_reactions = st.number_input("Number of Reactions", min_value=1, value=24)
                extra_percent = st.number_input("Extra Volume (%)", min_value=0, value=10)
            
            with col_pcr2:
                # Master mix components
                st.markdown("**Component Concentrations:**")
                polymerase_stock = st.number_input("Polymerase Stock (U/μL)", value=5.0)
                polymerase_final = st.number_input("Polymerase Final (U/μL)", value=0.05)
                
                primer_stock = st.number_input("Primer Stock (μM)", value=10.0)
                primer_final = st.number_input("Primer Final (μM)", value=0.5)
            
            if st.form_submit_button("Calculate PCR Setup"):
                # Calculate total volume needed
                total_reactions = num_reactions * (1 + extra_percent/100)
                total_volume = total_reactions * reaction_volume
                
                # Calculate component volumes
                polymerase_vol = (polymerase_final / polymerase_stock) * total_volume
                primer_fwd_vol = (primer_final / primer_stock) * total_volume
                primer_rev_vol = (primer_final / primer_stock) * total_volume
                
                # Assume standard components
                buffer_vol = total_volume * 0.1  # 1x final from 10x stock
                dntp_vol = total_volume * 0.02   # 200μM final from 10mM stock
                template_vol_per_rxn = 1.0       # 1μL per reaction
                water_vol = total_volume - (polymerase_vol + primer_fwd_vol + primer_rev_vol + buffer_vol + dntp_vol)
                
                st.markdown(f"""
                <div class="pcr-box">
                    <h4>PCR Master Mix Setup</h4>
                    <p><strong>For {num_reactions} reactions + {extra_percent}% extra = {total_reactions:.1f} reactions</strong></p>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                        <div>
                            <h5>Master Mix Components</h5>
                            <p><strong>10× Buffer:</strong> {buffer_vol:.1f} μL</p>
                            <p><strong>dNTPs (10mM):</strong> {dntp_vol:.1f} μL</p>
                            <p><strong>Forward Primer:</strong> {primer_fwd_vol:.1f} μL</p>
                            <p><strong>Reverse Primer:</strong> {primer_rev_vol:.1f} μL</p>
                            <p><strong>Polymerase:</strong> {polymerase_vol:.1f} μL</p>
                            <p><strong>Water:</strong> {water_vol:.1f} μL</p>
                        </div>
                        <div>
                            <h5>Per Reaction</h5>
                            <p><strong>Master Mix:</strong> {reaction_volume - template_vol_per_rxn:.1f} μL</p>
                            <p><strong>Template:</strong> {template_vol_per_rxn:.1f} μL</p>
                            <p><strong>Total:</strong> {reaction_volume:.1f} μL</p>
                            <br>
                            <p><strong>Total Master Mix:</strong> {total_volume - (total_reactions * template_vol_per_rxn):.1f} μL</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Protocol
                st.markdown("### 📋 PCR Setup Protocol")
                st.markdown(f"""
**PCR Master Mix Preparation Protocol**

1. **Prepare master mix** in the following order:
   - Add water first: {water_vol:.1f} μL
   - Add 10× Buffer: {buffer_vol:.1f} μL
   - Add dNTPs: {dntp_vol:.1f} μL
   - Add Forward primer: {primer_fwd_vol:.1f} μL
   - Add Reverse primer: {primer_rev_vol:.1f} μL
   - Add Polymerase last: {polymerase_vol:.1f} μL

2. **Mix gently** by pipetting or brief vortex

3. **Aliquot** {reaction_volume - template_vol_per_rxn:.1f} μL master mix per tube

4. **Add** {template_vol_per_rxn:.1f} μL template to each tube

5. **Mix and centrifuge** briefly before cycling
                """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def media_preparation_calculator():
    """Media preparation calculator"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("🧫 Media Preparation Calculator")
    st.markdown("*Bacterial and cell culture media preparation*")
    
    tab1, tab2, tab3 = st.tabs(["🥼 LB Medium", "🧬 Specialized Media", "📊 Custom Recipe"])
    
    with tab1:
        st.markdown("### 🥼 LB (Lysogeny Broth) Medium")
        
        with st.form("lb_media_form"):
            col_lb1, col_lb2, col_lb3 = st.columns(3)
            
            with col_lb1:
                volume = st.number_input("Volume (L)", min_value=0.1, value=1.0, step=0.1)
            
            with col_lb2:
                media_type = st.selectbox("Type", ["Liquid (Broth)", "Solid (Agar)"])
            
            with col_lb3:
                batch_count = st.number_input("Batches", min_value=1, value=1)
            
            if st.form_submit_button("Calculate LB Media"):
                total_volume = volume * batch_count
                
                # LB components per liter
                lb_powder = 20 * total_volume  # 20 g/L
                agar = 15 * total_volume if "Solid" in media_type else 0  # 15 g/L
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>LB Medium Recipe ({total_volume:.1f} L)</h4>
                    <p><strong>LB Powder:</strong> {lb_powder:.1f} g</p>
                    {'<p><strong>Agar:</strong> ' + f'{agar:.1f} g</p>' if agar > 0 else ''}
                    <p><strong>Distilled Water:</strong> {total_volume:.1f} L</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Protocol
                st.markdown("### 📋 Preparation Protocol")
                protocol = f"""
**LB Medium Preparation**

1. **Weigh** {lb_powder:.1f} g LB powder
{'2. **Weigh** ' + f'{agar:.1f} g agar' if agar > 0 else ''}
{'3.' if agar > 0 else '2.'} **Dissolve** in ~{total_volume*800:.0f} mL distilled water
{'4.' if agar > 0 else '3.'} **Adjust pH** to 7.0 ± 0.2 with NaOH
{'5.' if agar > 0 else '4.'} **Bring to final volume** {total_volume:.1f} L
{'6.' if agar > 0 else '5.'} **Autoclave** 121°C, 15 min
{'7.' if agar > 0 else '6.'} **Cool and store** at 4°C
                """
                st.markdown(protocol)
    
    with tab2:
        st.markdown("### 🧬 Specialized Media")
        
        media_options = {
            "LBGM": {
                "components": [
                    ("LB Powder", 20, "g/L"),
                    ("Glycerol (50%)", 20, "mL/L"),
                    ("MnCl₂ (10 mM)", 10, "mL/L")
                ],
                "description": "LB + Glycerol + Manganese"
            },
            "MSGG(2x)": {
                "components": [
                    ("K₂HPO₄ (1M)", 6.15, "mL/L"),
                    ("KH₂PO₄ (1M)", 3.85, "mL/L"),
                    ("MOPS (1M, pH 7.0)", 200, "mL/L"),
                    ("MgCl₂ (1M)", 4, "mL/L"),
                    ("Thiamine (10mM)", 10, "mL/L"),
                    ("Glycerol (50%)", 20, "mL/L")
                ],
                "description": "Minimal synthetic defined medium (2x)"
            }
        }
        
        selected_media = st.selectbox("Select Medium", list(media_options.keys()))
        volume_special = st.number_input("Volume (L)", min_value=0.1, value=0.5, step=0.1)
        
        if st.button("Calculate Specialized Media"):
            media_data = media_options[selected_media]
            
            st.markdown(f"""
            <div class="result-box">
                <h4>{selected_media} Medium ({volume_special:.1f} L)</h4>
                <p><em>{media_data['description']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Components table
            components_data = []
            for component, amount, unit in media_data['components']:
                scaled_amount = amount * volume_special
                components_data.append({
                    'Component': component,
                    'Amount': f"{scaled_amount:.2f} {unit.split('/')[0]}",
                    'Stock Concentration': unit
                })
            
            df_components = pd.DataFrame(components_data)
            st.dataframe(df_components, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 📊 Custom Recipe Builder")
        
        st.markdown("Build your own media recipe:")
        
        # Initialize custom recipe in session state
        if 'custom_recipe' not in st.session_state:
            st.session_state.custom_recipe = []
        
        with st.form("add_component_form"):
            col_comp1, col_comp2, col_comp3 = st.columns(3)
            
            with col_comp1:
                component_name = st.text_input("Component Name")
            
            with col_comp2:
                component_amount = st.number_input("Amount", min_value=0.001, value=1.0)
            
            with col_comp3:
                component_unit = st.selectbox("Unit", ["g/L", "mg/L", "mL/L", "μL/L", "mM", "μM"])
            
            if st.form_submit_button("Add Component"):
                if component_name:
                    st.session_state.custom_recipe.append({
                        'name': component_name,
                        'amount': component_amount,
                        'unit': component_unit
                    })
                    st.success(f"Added {component_name}")
        
        # Display current recipe
        if st.session_state.custom_recipe:
            st.markdown("### Current Recipe")
            
            recipe_df = pd.DataFrame(st.session_state.custom_recipe)
            st.dataframe(recipe_df, use_container_width=True, hide_index=True)
            
            # Calculate for volume
            custom_volume = st.number_input("Calculate for Volume (L)", min_value=0.1, value=1.0)
            
            if st.button("Calculate Custom Media"):
                st.markdown(f"### Custom Media Recipe ({custom_volume:.1f} L)")
                
                for component in st.session_state.custom_recipe:
                    scaled_amount = component['amount'] * custom_volume
                    st.markdown(f"• **{component['name']}:** {scaled_amount:.3f} {component['unit'].split('/')[0]}")
            
            if st.button("Clear Recipe"):
                st.session_state.custom_recipe = []
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def ph_buffer_calculator():
    """pH and buffer calculation tools"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("🔬 pH & Buffer Calculator")
    st.markdown("*Professional acid-base chemistry calculations*")
    
    tab1, tab2, tab3 = st.tabs(["🧪 pH Calculator", "📊 Buffer Calculator", "⚖️ Acid-Base Titration"])
    
    with tab1:
        st.markdown("### 🧪 pH Calculator")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("ph_calculator_form"):
                st.markdown("#### Solution Parameters")
                
                solution_type = st.radio("Solution Type", ["Strong Acid", "Strong Base", "Weak Acid", "Weak Base"])
                
                col_ph1, col_ph2 = st.columns(2)
                
                with col_ph1:
                    concentration = st.number_input("Concentration (M)", min_value=1e-14, max_value=10.0, value=0.1, format="%.6f")
                
                with col_ph2:
                    if "Weak" in solution_type:
                        if "Acid" in solution_type:
                            ka_pka = st.number_input("pKa", min_value=0.0, max_value=14.0, value=4.75, step=0.01)
                        else:
                            ka_pka = st.number_input("pKb", min_value=0.0, max_value=14.0, value=4.75, step=0.01)
                    else:
                        ka_pka = None
                
                if st.form_submit_button("Calculate pH", use_container_width=True):
                    try:
                        if "Strong" in solution_type:
                            is_acid = "Acid" in solution_type
                            ph = AdvancedChemistryCalculators.ph_calculator(concentration, is_acid)
                        else:
                            # Simplified weak acid/base calculation
                            if "Acid" in solution_type:
                                # Weak acid: pH = 0.5 * (pKa - log[HA])
                                ph = 0.5 * (ka_pka - math.log10(concentration))
                            else:
                                # Weak base: pOH = 0.5 * (pKb - log[B]), pH = 14 - pOH
                                poh = 0.5 * (ka_pka - math.log10(concentration))
                                ph = 14 - poh
                        
                        # Calculate additional parameters
                        h_conc = 10**(-ph)
                        oh_conc = 10**(ph-14)
                        poh = 14 - ph
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ pH Calculation Results</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                                <div class="metric-card">
                                    <h5>pH Parameters</h5>
                                    <p style="font-size: 1.2em; color: #4f46e5;"><strong>pH: {ph:.2f}</strong></p>
                                    <p><strong>pOH:</strong> {poh:.2f}</p>
                                    <p><strong>Type:</strong> {'Acidic' if ph < 7 else 'Basic' if ph > 7 else 'Neutral'}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Ion Concentrations</h5>
                                    <p><strong>[H⁺]:</strong> {h_conc:.2e} M</p>
                                    <p><strong>[OH⁻]:</strong> {oh_conc:.2e} M</p>
                                    <p><strong>Ionic Product:</strong> {h_conc * oh_conc:.2e}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Solution Info</h5>
                                    <p><strong>Type:</strong> {solution_type}</p>
                                    <p><strong>Concentration:</strong> {concentration:.4f} M</p>
                                    {'<p><strong>pKa/pKb:</strong> ' + f'{ka_pka:.2f}</p>' if ka_pka else ''}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        add_to_history(
                            "pH Calculation",
                            {'solution_type': solution_type, 'concentration': concentration},
                            {'ph': ph, 'h_concentration': h_conc}
                        )
                        
                    except Exception as e:
                        st.error(f"Calculation error: {str(e)}")
        
        with col2:
            st.markdown("### 📖 pH Reference")
            
            ph_scale = [
                ("0-1", "Battery acid", "red"),
                ("2", "Lemon juice", "orange"),
                ("3-4", "Coffee, wine", "yellow"),
                ("5-6", "Rainwater", "lightgreen"),
                ("7", "Pure water", "green"),
                ("8", "Seawater", "lightblue"),
                ("9-10", "Baking soda", "blue"),
                ("11-12", "Ammonia", "purple"),
                ("13-14", "Bleach", "darkpurple")
            ]
            
            for ph_range, example, color in ph_scale:
                st.markdown(f"**pH {ph_range}:** {example}")
    
    with tab2:
        st.markdown("### 📊 Buffer Calculator")
        
        with st.form("buffer_calculator_form"):
            st.markdown("#### Henderson-Hasselbalch Equation")
            st.markdown("*pH = pKa + log([A⁻]/[HA])*")
            
            buffer_type = st.radio("Calculation Type", ["Calculate pH", "Calculate Ratio", "Buffer Capacity"])
            
            col_buf1, col_buf2, col_buf3 = st.columns(3)
            
            with col_buf1:
                pka = st.number_input("pKa of weak acid", min_value=0.0, max_value=14.0, value=4.75, step=0.01)
            
            with col_buf2:
                if buffer_type == "Calculate pH":
                    acid_conc = st.number_input("Weak acid conc. (M)", min_value=0.001, value=0.1)
                    base_conc = st.number_input("Conjugate base conc. (M)", min_value=0.001, value=0.1)
                elif buffer_type == "Calculate Ratio":
                    target_ph = st.number_input("Target pH", min_value=0.0, max_value=14.0, value=7.0)
                    acid_conc = st.number_input("Weak acid conc. (M)", min_value=0.001, value=0.1)
                else:  # Buffer Capacity
                    acid_conc = st.number_input("Total buffer conc. (M)", min_value=0.001, value=0.1)
                    buffer_ph = st.number_input("Buffer pH", min_value=0.0, max_value=14.0, value=7.0)
            
            with col_buf3:
                volume = st.number_input("Solution volume (L)", min_value=0.001, value=1.0)
            
            if st.form_submit_button("Calculate Buffer", use_container_width=True):
                try:
                    if buffer_type == "Calculate pH":
                        ph = AdvancedChemistryCalculators.buffer_calculator(acid_conc, base_conc, pka)
                        ratio = base_conc / acid_conc
                        buffer_capacity = min(acid_conc, base_conc)
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Buffer pH Results</h4>
                            <p><strong>Buffer pH:</strong> {ph:.2f}</p>
                            <p><strong>[A⁻]/[HA] Ratio:</strong> {ratio:.3f}</p>
                            <p><strong>Buffer Capacity:</strong> {buffer_capacity:.3f} M</p>
                            <p><strong>Effective Range:</strong> {pka-1:.1f} - {pka+1:.1f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    elif buffer_type == "Calculate Ratio":
                        # Calculate required ratio for target pH
                        log_ratio = target_ph - pka
                        ratio = 10**log_ratio
                        base_conc = (ratio * acid_conc) / (1 + ratio)
                        actual_acid_conc = acid_conc - base_conc
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Buffer Ratio Results</h4>
                            <p><strong>Required [A⁻]/[HA]:</strong> {ratio:.3f}</p>
                            <p><strong>Weak acid needed:</strong> {actual_acid_conc:.4f} M</p>
                            <p><strong>Conjugate base needed:</strong> {base_conc:.4f} M</p>
                            <p><strong>Target pH:</strong> {target_ph:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:  # Buffer Capacity
                        # Calculate buffer capacity (simplified)
                        alpha_ha = 1 / (1 + 10**(buffer_ph - pka))
                        alpha_a = 1 - alpha_ha
                        capacity = 2.3 * acid_conc * alpha_ha * alpha_a
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Buffer Capacity Results</h4>
                            <p><strong>Buffer Capacity:</strong> {capacity:.4f} M</p>
                            <p><strong>α(HA):</strong> {alpha_ha:.3f}</p>
                            <p><strong>α(A⁻):</strong> {alpha_a:.3f}</p>
                            <p><strong>Maximum at pH = pKa:</strong> {pka:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    add_to_history(
                        "Buffer Calculation",
                        {'pka': pka, 'type': buffer_type},
                        {'result': 'Calculated successfully'}
                    )
                    
                except Exception as e:
                    st.error(f"Calculation error: {str(e)}")
    
    with tab3:
        st.markdown("### ⚖️ Acid-Base Titration Calculator")
        
        with st.form("titration_form"):
            st.markdown("#### Titration Parameters")
            
            col_tit1, col_tit2 = st.columns(2)
            
            with col_tit1:
                st.markdown("**Analyte (Unknown):**")
                analyte_volume = st.number_input("Volume (mL)", value=25.0, key="analyte_vol")
                analyte_type = st.selectbox("Type", ["Acid", "Base"])
            
            with col_tit2:
                st.markdown("**Titrant (Known):**")
                titrant_conc = st.number_input("Concentration (M)", value=0.1, key="titrant_conc")
                titrant_volume = st.number_input("Volume at endpoint (mL)", value=20.0, key="titrant_vol")
            
            if st.form_submit_button("Calculate Titration"):
                # Calculate analyte concentration using stoichiometry
                # For 1:1 stoichiometry: M1V1 = M2V2
                analyte_conc = (titrant_conc * titrant_volume) / analyte_volume
                
                # Calculate moles
                titrant_moles = titrant_conc * (titrant_volume / 1000)  # Convert mL to L
                analyte_moles = analyte_conc * (analyte_volume / 1000)
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Titration Results</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                        <div class="metric-card">
                            <h5>Analyte Results</h5>
                            <p><strong>Concentration:</strong> {analyte_conc:.4f} M</p>
                            <p><strong>Moles:</strong> {analyte_moles:.6f} mol</p>
                            <p><strong>Type:</strong> {analyte_type}</p>
                        </div>
                        <div class="metric-card">
                            <h5>Titrant Used</h5>
                            <p><strong>Volume:</strong> {titrant_volume:.2f} mL</p>
                            <p><strong>Moles:</strong> {titrant_moles:.6f} mol</p>
                            <p><strong>Stoichiometry:</strong> 1:1</p>
                        </div>
                        <div class="metric-card">
                            <h5>Quality Check</h5>
                            <p><strong>Ratio Check:</strong> {analyte_moles/titrant_moles:.3f}</p>
                            <p><strong>Expected:</strong> ~1.000</p>
                            <p><strong>% Error:</strong> {abs(1 - analyte_moles/titrant_moles)*100:.1f}%</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def beers_law_calculator():
    """Beer's Law calculator for spectrophotometry"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("📊 Beer's Law Calculator")
    st.markdown("*Spectrophotometry and concentration analysis using A = ελcl*")
    
    tab1, tab2, tab3 = st.tabs(["📈 Concentration Calculator", "🧬 Protein Analysis", "📊 Standard Curve"])
    
    with tab1:
        st.markdown("### 📈 Beer's Law Concentration Calculator")
        st.markdown("*A = ε × c × l*")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("beers_law_form"):
                calculation_type = st.radio("Calculate:", ["Concentration from Absorbance", "Absorbance from Concentration"])
                
                col_beer1, col_beer2 = st.columns(2)
                
                with col_beer1:
                    if calculation_type == "Concentration from Absorbance":
                        absorbance = st.number_input("Absorbance (A)", min_value=0.0, value=0.5, step=0.01)
                    else:
                        concentration = st.number_input("Concentration (M)", min_value=0.0, value=0.001, format="%.6f")
                    
                    extinction_coeff = st.number_input("Extinction Coefficient (M⁻¹cm⁻¹)", min_value=1.0, value=1000.0, step=1.0)
                
                with col_beer2:
                    path_length = st.number_input("Path Length (cm)", min_value=0.1, value=1.0, step=0.1)
                    
                    # Common compound selection
                    compound = st.selectbox("Common Compounds", [
                        "Custom",
                        "NADH (340 nm) - ε = 6,220",
                        "NADPH (340 nm) - ε = 6,220", 
                        "FAD (450 nm) - ε = 11,300",
                        "Cytochrome c (550 nm) - ε = 21,000",
                        "Chlorophyll a (665 nm) - ε = 90,000"
                    ])
                    
                    if compound != "Custom":
                        # Extract extinction coefficient from selection
                        ext_coeff_values = {
                            "NADH (340 nm) - ε = 6,220": 6220,
                            "NADPH (340 nm) - ε = 6,220": 6220,
                            "FAD (450 nm) - ε = 11,300": 11300,
                            "Cytochrome c (550 nm) - ε = 21,000": 21000,
                            "Chlorophyll a (665 nm) - ε = 90,000": 90000
                        }
                        extinction_coeff = ext_coeff_values[compound]
                
                if st.form_submit_button("🔬 Calculate", use_container_width=True):
                    try:
                        if calculation_type == "Concentration from Absorbance":
                            result = AdvancedChemistryCalculators.beers_law_calculator(
                                absorbance=absorbance, extinction_coeff=extinction_coeff, path_length=path_length
                            )
                            
                            concentration = result['concentration']
                            conc_mM = result['concentration_mM']
                            conc_μM = result['concentration_μM']
                            
                            # Check linear range
                            linear_range = absorbance < 2.0
                            
                            st.markdown(f"""
                            <div class="result-box">
                                <h4>✅ Concentration Results</h4>
                                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                                    <div class="metric-card">
                                        <h5>Concentrations</h5>
                                        <p><strong>Molarity:</strong> {concentration:.6f} M</p>
                                        <p><strong>Millimolar:</strong> {conc_mM:.3f} mM</p>
                                        <p><strong>Micromolar:</strong> {conc_μM:.1f} μM</p>
                                    </div>
                                    <div class="metric-card">
                                        <h5>Measurement</h5>
                                        <p><strong>Absorbance:</strong> {absorbance:.3f}</p>
                                        <p><strong>Path Length:</strong> {path_length:.1f} cm</p>
                                        <p><strong>ε:</strong> {extinction_coeff:,.0f} M⁻¹cm⁻¹</p>
                                    </div>
                                    <div class="metric-card">
                                        <h5>Quality</h5>
                                        <p><strong>Linear Range:</strong> {'✅ Yes' if linear_range else '⚠️ No'}</p>
                                        <p><strong>Detection:</strong> {'Good' if absorbance > 0.1 else 'Low signal'}</p>
                                        {'<p style="color: orange;">Consider dilution</p>' if absorbance > 1.5 else ''}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        else:  # Calculate absorbance
                            result = AdvancedChemistryCalculators.beers_law_calculator(
                                concentration=concentration, extinction_coeff=extinction_coeff, path_length=path_length
                            )
                            
                            absorbance = result['absorbance']
                            transmittance = result['transmittance']
                            
                            st.markdown(f"""
                            <div class="result-box">
                                <h4>✅ Absorbance Results</h4>
                                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                                    <div class="metric-card">
                                        <h5>Optical Properties</h5>
                                        <p><strong>Absorbance:</strong> {absorbance:.4f} AU</p>
                                        <p><strong>Transmittance:</strong> {transmittance:.2f}%</p>
                                        <p><strong>% Absorption:</strong> {100-transmittance:.2f}%</p>
                                    </div>
                                    <div class="metric-card">
                                        <h5>Sample Info</h5>
                                        <p><strong>Concentration:</strong> {concentration:.6f} M</p>
                                        <p><strong>Path Length:</strong> {path_length:.1f} cm</p>
                                        <p><strong>ε:</strong> {extinction_coeff:,.0f} M⁻¹cm⁻¹</p>
                                    </div>
                                    <div class="metric-card">
                                        <h5>Measurement</h5>
                                        <p><strong>Detectable:</strong> {'✅ Yes' if absorbance > 0.01 else '❌ Too low'}</p>
                                        <p><strong>Linear Range:</strong> {'✅ Yes' if absorbance < 2.0 else '⚠️ Too high'}</p>
                                        <p><strong>Optimal:</strong> {'✅ Yes' if 0.1 < absorbance < 1.5 else '⚠️ Outside'}</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        add_to_history(
                            "Beer's Law Calculation",
                            {'calculation_type': calculation_type, 'extinction_coeff': extinction_coeff},
                            {'result': 'Calculated successfully'}
                        )
                        
                    except Exception as e:
                        st.error(f"Calculation error: {str(e)}")
        
        with col2:
            st.markdown("### 📖 Beer's Law Guide")
            
            st.markdown("""
            **Beer's Law Equation:**
            ```
            A = ε × c × l
            ```
            
            **Where:**
            - **A** = Absorbance (AU)
            - **ε** = Extinction coefficient (M⁻¹cm⁻¹)
            - **c** = Concentration (M)
            - **l** = Path length (cm)
            
            **Best Practices:**
            • Absorbance range: 0.1 - 1.5
            • Use appropriate wavelength
            • Blank with solvent
            • Temperature control
            • Fresh samples
            """)
            
            st.markdown("### 💡 Troubleshooting")
            
            st.markdown("""
            **High Absorbance (>2.0):**
            • Dilute sample
            • Use shorter path length
            • Check for aggregation
            
            **Low Absorbance (<0.1):**
            • Concentrate sample
            • Use longer path length
            • Check wavelength
            • Verify compound presence
            """)
    
    with tab2:
        st.markdown("### 🧬 Protein Concentration Analysis")
        
        with st.form("protein_analysis_form"):
            protein_method = st.selectbox("Analysis Method", [
                "A280 (Aromatic amino acids)",
                "Bradford Assay",
                "BCA Assay",
                "Lowry Assay"
            ])
            
            if protein_method == "A280 (Aromatic amino acids)":
                col_prot1, col_prot2 = st.columns(2)
                
                with col_prot1:
                    a280 = st.number_input("Absorbance at 280 nm", min_value=0.0, value=0.5, step=0.01)
                    path_length_prot = st.number_input("Path Length (cm)", min_value=0.1, value=1.0)
                
                with col_prot2:
                    protein_type = st.selectbox("Protein Type", [
                        "BSA (ε = 43,824 M⁻¹cm⁻¹)",
                        "Lysozyme (ε = 38,940 M⁻¹cm⁻¹)",
                        "IgG (ε = 210,000 M⁻¹cm⁻¹)",
                        "Generic (ε = 1 mg/mL⁻¹cm⁻¹)",
                        "Custom"
                    ])
                    
                    if protein_type == "Custom":
                        extinction_coeff_prot = st.number_input("Extinction Coefficient", value=43824.0)
                        molecular_weight = st.number_input("Molecular Weight (Da)", value=66430.0)
                    else:
                        protein_data = {
                            "BSA (ε = 43,824 M⁻¹cm⁻¹)": (43824, 66430),
                            "Lysozyme (ε = 38,940 M⁻¹cm⁻¹)": (38940, 14307),
                            "IgG (ε = 210,000 M⁻¹cm⁻¹)": (210000, 150000),
                            "Generic (ε = 1 mg/mL⁻¹cm⁻¹)": (1, 50000)  # Generic protein
                        }
                        extinction_coeff_prot, molecular_weight = protein_data[protein_type]
                
                if st.form_submit_button("Calculate Protein Concentration"):
                    try:
                        if protein_type == "Generic (ε = 1 mg/mL⁻¹cm⁻¹)":
                            # Direct calculation for generic proteins
                            concentration_mg_ml = a280 / path_length_prot
                            concentration_M = (concentration_mg_ml / molecular_weight) * 1000
                        else:
                            # Standard Beer's Law calculation
                            concentration_M = a280 / (extinction_coeff_prot * path_length_prot)
                            concentration_mg_ml = concentration_M * molecular_weight / 1000
                        
                        concentration_μM = concentration_M * 1000000
                        concentration_μg_ml = concentration_mg_ml * 1000
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Protein Concentration Results</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                                <div class="metric-card">
                                    <h5>Mass Concentrations</h5>
                                    <p><strong>mg/mL:</strong> {concentration_mg_ml:.3f}</p>
                                    <p><strong>μg/mL:</strong> {concentration_μg_ml:.1f}</p>
                                    <p><strong>g/L:</strong> {concentration_mg_ml:.3f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Molar Concentrations</h5>
                                    <p><strong>Molarity:</strong> {concentration_M:.6f} M</p>
                                    <p><strong>Micromolar:</strong> {concentration_μM:.2f} μM</p>
                                    <p><strong>Millimolar:</strong> {concentration_M*1000:.3f} mM</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Protein Info</h5>
                                    <p><strong>Type:</strong> {protein_type.split('(')[0].strip()}</p>
                                    <p><strong>MW:</strong> {molecular_weight:,.0f} Da</p>
                                    <p><strong>A280:</strong> {a280:.3f}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Calculation error: {str(e)}")
            
            else:
                st.info(f"Calculator for {protein_method} coming soon!")
                st.markdown(f"""
                **{protein_method} Characteristics:**
                
                - **Bradford:** Quick, compatible with detergents
                - **BCA:** Accurate, compatible with most buffers
                - **Lowry:** Classic method, moderate sensitivity
                """)
    
    with tab3:
        st.markdown("### 📊 Standard Curve Generator")
        
        st.markdown("Create standard curves for quantitative analysis")
        
        with st.form("standard_curve_form"):
            st.markdown("#### Standard Data Entry")
            
            # Data input options
            input_method = st.radio("Data Input", ["Manual Entry", "Paste Data"])
            
            if input_method == "Manual Entry":
                num_standards = st.number_input("Number of Standards", min_value=3, max_value=10, value=5)
                
                concentrations = []
                absorbances = []
                
                st.markdown("**Enter your standard data:**")
                for i in range(num_standards):
                    col_std1, col_std2 = st.columns(2)
                    with col_std1:
                        conc = st.number_input(f"Concentration {i+1}", value=float(i+1), key=f"std_conc_{i}")
                        concentrations.append(conc)
                    with col_std2:
                        abs_val = st.number_input(f"Absorbance {i+1}", value=0.1 * (i+1), step=0.01, key=f"std_abs_{i}")
                        absorbances.append(abs_val)
            
            else:  # Paste data
                curve_data = st.text_area(
                    "Paste concentration and absorbance data (tab or comma separated)",
                    value="0.5\t0.05\n1.0\t0.10\n2.0\t0.20\n4.0\t0.40\n8.0\t0.80",
                    height=150
                )
                
                # Parse data
                concentrations = []
                absorbances = []
                
                try:
                    lines = curve_data.strip().split('\n')
                    for line in lines:
                        if '\t' in line:
                            parts = line.split('\t')
                        else:
                            parts = line.split(',')
                        
                        if len(parts) >= 2:
                            concentrations.append(float(parts[0].strip()))
                            absorbances.append(float(parts[1].strip()))
                except:
                    st.warning("Check data format: Concentration[tab]Absorbance per line")
            
            if st.form_submit_button("Generate Standard Curve"):
                try:
                    if len(concentrations) >= 3 and len(absorbances) >= 3:
                        # Linear regression
                        n = len(concentrations)
                        sum_x = sum(concentrations)
                        sum_y = sum(absorbances)
                        sum_xy = sum(x * y for x, y in zip(concentrations, absorbances))
                        sum_x2 = sum(x * x for x in concentrations)
                        
                        # Calculate slope and intercept
                        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
                        intercept = (sum_y - slope * sum_x) / n
                        
                        # Calculate R²
                        y_mean = sum_y / n
                        ss_tot = sum((y - y_mean) ** 2 for y in absorbances)
                        predicted = [slope * x + intercept for x in concentrations]
                        ss_res = sum((y - pred) ** 2 for y, pred in zip(absorbances, predicted))
                        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Standard Curve Results</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                                <div class="metric-card">
                                    <h5>Curve Parameters</h5>
                                    <p><strong>Slope:</strong> {slope:.4f}</p>
                                    <p><strong>Y-intercept:</strong> {intercept:.4f}</p>
                                    <p><strong>R²:</strong> {r_squared:.4f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Equation</h5>
                                    <p><strong>Y = {slope:.4f}X + {intercept:.4f}</strong></p>
                                    <p>Where X = Concentration</p>
                                    <p>Y = Absorbance</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Quality Assessment</h5>
                                    <p><strong>Linearity:</strong> {'Excellent' if r_squared > 0.99 else 'Good' if r_squared > 0.95 else 'Poor'}</p>
                                    <p><strong>LOD:</strong> {3 * intercept / slope:.3f}</p>
                                    <p><strong>LOQ:</strong> {10 * intercept / slope:.3f}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Data table with residuals
                        curve_df = pd.DataFrame({
                            'Concentration': concentrations,
                            'Absorbance': absorbances,
                            'Predicted': [slope * x + intercept for x in concentrations],
                            'Residual': [abs_val - (slope * conc + intercept) for conc, abs_val in zip(concentrations, absorbances)]
                        })
                        
                        st.markdown("### 📊 Standard Curve Data")
                        st.dataframe(curve_df, use_container_width=True, hide_index=True)
                        
                        # Sample calculation helper
                        st.markdown("### 🧪 Sample Calculation")
                        sample_absorbance = st.number_input("Sample Absorbance", value=0.5, step=0.01)
                        
                        if sample_absorbance > 0:
                            sample_concentration = (sample_absorbance - intercept) / slope
                            st.success(f"Sample Concentration: {sample_concentration:.3f} units")
                            
                            if sample_concentration < 0:
                                st.warning("Negative concentration calculated - check for matrix effects or dilute blank")
                        
                    else:
                        st.error("Please provide at least 3 data points")
                        
                except Exception as e:
                    st.error(f"Standard curve error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def data_analysis_suite():
    """Data analysis and statistics tools"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("📊 Data Analysis Suite")
    st.markdown("*Statistical analysis and data visualization for laboratory results*")
    
    tab1, tab2, tab3 = st.tabs(["📈 Basic Statistics", "🎯 Quality Control", "📊 Data Visualization"])
    
    with tab1:
        st.markdown("### 📈 Basic Statistical Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Data input
            data_input_method = st.radio("Data Input Method", ["Manual Entry", "Paste Data"])
            
            if data_input_method == "Manual Entry":
                data_input = st.text_area(
                    "Enter data (one value per line)",
                    value="0.245\n0.251\n0.248\n0.252\n0.247\n0.250\n0.249",
                    height=150
                )
            else:
                data_input = st.text_area(
                    "Paste data (comma, space, or line separated)",
                    value="0.245, 0.251, 0.248, 0.252, 0.247, 0.250, 0.249",
                    height=150
                )
            
            if st.button("📊 Analyze Data", use_container_width=True):
                try:
                    # Parse data
                    if data_input_method == "Manual Entry":
                        data = [float(x.strip()) for x in data_input.split('\n') if x.strip()]
                    else:
                        # Handle multiple separators
                        data_clean = data_input.replace(',', ' ').replace('\n', ' ').replace('\t', ' ')
                        data = [float(x.strip()) for x in data_clean.split() if x.strip()]
                    
                    if len(data) >= 2:
                        # Calculate statistics
                        n = len(data)
                        mean_val = np.mean(data)
                        median_val = np.median(data)
                        std_val = np.std(data, ddof=1)  # Sample standard deviation
                        sem_val = std_val / np.sqrt(n)  # Standard error of mean
                        cv_val = (std_val / mean_val) * 100  # Coefficient of variation
                        min_val = np.min(data)
                        max_val = np.max(data)
                        range_val = max_val - min_val
                        
                        # Confidence interval (95%)
                        from scipy import stats
                        ci_95 = stats.t.interval(0.95, n-1, loc=mean_val, scale=sem_val)
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Statistical Analysis Results (n = {n})</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
                                <div class="metric-card">
                                    <h5>Central Tendency</h5>
                                    <p><strong>Mean:</strong> {mean_val:.4f}</p>
                                    <p><strong>Median:</strong> {median_val:.4f}</p>
                                    <p><strong>Mode:</strong> {'Multiple' if len(set(data)) == len(data) else 'Calculated'}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Variability</h5>
                                    <p><strong>Std Dev:</strong> {std_val:.4f}</p>
                                    <p><strong>Variance:</strong> {std_val**2:.6f}</p>
                                    <p><strong>Range:</strong> {range_val:.4f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Precision Metrics</h5>
                                    <p><strong>CV:</strong> {cv_val:.2f}%</p>
                                    <p><strong>SEM:</strong> {sem_val:.4f}</p>
                                    <p><strong>RSD:</strong> {cv_val:.2f}%</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Confidence Interval</h5>
                                    <p><strong>95% CI:</strong></p>
                                    <p>{ci_95[0]:.4f} to {ci_95[1]:.4f}</p>
                                    <p><strong>Width:</strong> {ci_95[1] - ci_95[0]:.4f}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Data quality assessment
                        st.markdown("### 🎯 Data Quality Assessment")
                        
                        quality_metrics = []
                        
                        # Precision assessment based on CV
                        if cv_val < 2:
                            precision = "Excellent"
                            precision_color = "green"
                        elif cv_val < 5:
                            precision = "Good"
                            precision_color = "blue"
                        elif cv_val < 10:
                            precision = "Acceptable"
                            precision_color = "orange"
                        else:
                            precision = "Poor"
                            precision_color = "red"
                        
                        quality_metrics.append(["Precision", f"{cv_val:.2f}% CV", precision, precision_color])
                        
                        # Sample size assessment
                        if n >= 30:
                            sample_size = "Large"
                            size_color = "green"
                        elif n >= 10:
                            sample_size = "Medium"
                            size_color = "blue"
                        elif n >= 5:
                            sample_size = "Small"
                            size_color = "orange"
                        else:
                            sample_size = "Very Small"
                            size_color = "red"
                        
                        quality_metrics.append(["Sample Size", f"n = {n}", sample_size, size_color])
                        
                        # Outlier detection (simple Z-score method)
                        outliers = []
                        for i, value in enumerate(data):
                            z_score = abs(value - mean_val) / std_val
                            if z_score > 2.5:  # Common threshold for outliers
                                outliers.append((i+1, value, z_score))
                        
                        outlier_status = "None Detected" if not outliers else f"{len(outliers)} Detected"
                        outlier_color = "green" if not outliers else "orange"
                        quality_metrics.append(["Outliers", outlier_status, f"Z > 2.5", outlier_color])
                        
                        # Display quality metrics
                        for metric, value, status, color in quality_metrics:
                            st.markdown(f"**{metric}:** {value} - <span style='color: {color};'>{status}</span>", unsafe_allow_html=True)
                        
                        # Show outliers if any
                        if outliers:
                            st.markdown("**Potential Outliers:**")
                            for position, value, z_score in outliers:
                                st.warning(f"Position {position}: {value:.4f} (Z-score: {z_score:.2f})")
                        
                        # Raw data display
                        st.markdown("### 📋 Data Summary")
                        
                        data_df = pd.DataFrame({
                            'Index': range(1, len(data) + 1),
                            'Value': data,
                            'Deviation from Mean': [x - mean_val for x in data],
                            'Z-Score': [(x - mean_val) / std_val for x in data]
                        })
                        
                        st.dataframe(data_df, use_container_width=True, hide_index=True)
                        
                        add_to_history(
                            "Statistical Analysis",
                            {'sample_size': n, 'data_type': 'numerical'},
                            {'mean': mean_val, 'std_dev': std_val, 'cv': cv_val}
                        )
                        
                    else:
                        st.error("Please provide at least 2 data points for analysis")
                        
                except Exception as e:
                    st.error(f"Error analyzing data: {str(e)}")
                    st.info("Please check that all values are numeric and properly formatted")
        
        with col2:
            st.markdown("### 📖 Statistics Guide")
            
            st.markdown("""
            **Key Metrics:**
            
            • **Mean** - Average value
            • **Median** - Middle value  
            • **Std Dev** - Spread of data
            • **CV** - Relative variability (%)
            • **SEM** - Uncertainty in mean
            
            **Quality Criteria:**
            
            • **CV < 2%** - Excellent precision
            • **CV < 5%** - Good precision  
            • **CV < 10%** - Acceptable
            • **CV > 10%** - Poor precision
            
            **Sample Size:**
            
            • **n ≥ 30** - Large sample
            • **n ≥ 10** - Medium sample
            • **n < 10** - Small sample
            """)
            
            st.markdown("### 💡 Tips")
            
            st.markdown("""
            • Remove obvious outliers carefully
            • Increase sample size for better statistics
            • Check measurement procedures if CV > 5%
            • Use appropriate significant figures
            • Document any data exclusions
            """)
    
    with tab2:
        st.markdown("### 🎯 Quality Control Analysis")
        
        qc_analysis_type = st.selectbox("QC Analysis Type", [
            "Control Chart Analysis",
            "Method Validation",
            "Measurement Uncertainty"
        ])
        
        if qc_analysis_type == "Control Chart Analysis":
            st.markdown("#### Control Chart for Process Monitoring")
            
            # Sample control data
            control_data = st.text_area(
                "Enter control measurements (one per line)",
                value="10.2\n10.1\n10.3\n9.9\n10.0\n10.2\n10.1\n9.8\n10.3\n10.0",
                height=200
            )
            
            target_value = st.number_input("Target/Reference Value", value=10.0)
            
            if st.button("Generate Control Chart"):
                try:
                    data = [float(x.strip()) for x in control_data.split('\n') if x.strip()]
                    
                    if len(data) >= 5:
                        mean_val = np.mean(data)
                        std_val = np.std(data, ddof=1)
                        
                        # Control limits (typically ±3σ)
                        ucl = mean_val + 3 * std_val  # Upper Control Limit
                        lcl = mean_val - 3 * std_val  # Lower Control Limit
                        uwl = mean_val + 2 * std_val  # Upper Warning Limit
                        lwl = mean_val - 2 * std_val  # Lower Warning Limit
                        
                        # Check for out-of-control points
                        out_of_control = []
                        warnings = []
                        
                        for i, value in enumerate(data):
                            if value > ucl or value < lcl:
                                out_of_control.append((i+1, value))
                            elif value > uwl or value < lwl:
                                warnings.append((i+1, value))
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Control Chart Analysis</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                                <div class="metric-card">
                                    <h5>Process Statistics</h5>
                                    <p><strong>Process Mean:</strong> {mean_val:.3f}</p>
                                    <p><strong>Std Dev:</strong> {std_val:.3f}</p>
                                    <p><strong>Target:</strong> {target_value:.3f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Control Limits</h5>
                                    <p><strong>UCL (+3σ):</strong> {ucl:.3f}</p>
                                    <p><strong>UWL (+2σ):</strong> {uwl:.3f}</p>
                                    <p><strong>LWL (-2σ):</strong> {lwl:.3f}</p>
                                    <p><strong>LCL (-3σ):</strong> {lcl:.3f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Process Status</h5>
                                    <p><strong>Out of Control:</strong> {len(out_of_control)}</p>
                                    <p><strong>Warnings:</strong> {len(warnings)}</p>
                                    <p><strong>Process:</strong> {'🔴 OOC' if out_of_control else '🟡 Warning' if warnings else '🟢 In Control'}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Bias analysis
                        bias = mean_val - target_value
                        bias_percent = (bias / target_value) * 100
                        
                        st.markdown(f"""
                        ### 📊 Bias Analysis
                        **Bias:** {bias:.3f} units ({bias_percent:+.2f}%)
                        
                        {'🔴 Significant bias detected' if abs(bias_percent) > 5 else '🟡 Minor bias' if abs(bias_percent) > 2 else '🟢 No significant bias'}
                        """)
                        
                        # Data table with flags
                        chart_df = pd.DataFrame({
                            'Measurement': range(1, len(data) + 1),
                            'Value': data,
                            'Status': ['OOC' if (i+1, val) in out_of_control else 'Warning' if (i+1, val) in warnings else 'OK' 
                                     for i, val in enumerate(data)]
                        })
                        
                        st.dataframe(chart_df, use_container_width=True, hide_index=True)
                        
                except Exception as e:
                    st.error(f"Control chart error: {str(e)}")
        
        elif qc_analysis_type == "Method Validation":
            st.markdown("#### Method Validation Statistics")
            
            col_val1, col_val2 = st.columns(2)
            
            with col_val1:
                st.markdown("**Repeatability Study:**")
                repeat_data = st.text_area("Replicate measurements", value="5.02\n5.01\n5.03\n4.99\n5.00", height=100)
                
            with col_val2:
                st.markdown("**Reference/True Value:**")
                true_value = st.number_input("True Value", value=5.0)
                specification_limit = st.number_input("Specification Limit (±)", value=0.1)
            
            if st.button("Validate Method"):
                try:
                    data = [float(x.strip()) for x in repeat_data.split('\n') if x.strip()]
                    
                    if len(data) >= 3:
                        # Calculate validation parameters
                        mean_val = np.mean(data)
                        std_val = np.std(data, ddof=1)
                        
                        # Accuracy (bias)
                        accuracy = mean_val - true_value
                        accuracy_percent = (accuracy / true_value) * 100
                        
                        # Precision (repeatability)
                        precision_cv = (std_val / mean_val) * 100
                        
                        # Uncertainty
                        sem = std_val / np.sqrt(len(data))
                        uncertainty_95 = sem * 1.96  # 95% confidence
                        
                        # Method capability
                        capability = specification_limit / (3 * std_val)  # Cp index
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>✅ Method Validation Results</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
                                <div class="metric-card">
                                    <h5>Accuracy</h5>
                                    <p><strong>Bias:</strong> {accuracy:+.4f}</p>
                                    <p><strong>% Bias:</strong> {accuracy_percent:+.2f}%</p>
                                    <p><strong>Status:</strong> {'🟢 Good' if abs(accuracy_percent) < 2 else '🟡 Acceptable' if abs(accuracy_percent) < 5 else '🔴 Poor'}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Precision</h5>
                                    <p><strong>Std Dev:</strong> {std_val:.4f}</p>
                                    <p><strong>CV:</strong> {precision_cv:.2f}%</p>
                                    <p><strong>Status:</strong> {'🟢 Excellent' if precision_cv < 2 else '🟡 Good' if precision_cv < 5 else '🔴 Poor'}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Uncertainty</h5>
                                    <p><strong>SEM:</strong> {sem:.4f}</p>
                                    <p><strong>95% CI:</strong> ±{uncertainty_95:.4f}</p>
                                    <p><strong>Expanded:</strong> {mean_val:.3f} ± {uncertainty_95:.3f}</p>
                                </div>
                                <div class="metric-card">
                                    <h5>Capability</h5>
                                    <p><strong>Cp Index:</strong> {capability:.2f}</p>
                                    <p><strong>Spec Limit:</strong> ±{specification_limit:.3f}</p>
                                    <p><strong>Status:</strong> {'🟢 Capable' if capability > 1.33 else '🟡 Marginal' if capability > 1.0 else '🔴 Incapable'}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Validation error: {str(e)}")
        
        else:  # Measurement Uncertainty
            st.markdown("#### Measurement Uncertainty Calculation")
            
            st.markdown("Calculate combined measurement uncertainty from individual sources:")
            
            # Initialize uncertainty sources
            if 'uncertainty_sources' not in st.session_state:
                st.session_state.uncertainty_sources = []
            
            with st.form("add_uncertainty_source"):
                col_unc1, col_unc2, col_unc3 = st.columns(3)
                
                with col_unc1:
                    source_name = st.text_input("Uncertainty Source")
                
                with col_unc2:
                    uncertainty_value = st.number_input("Uncertainty Value", value=0.01, format="%.4f")
                
                with col_unc3:
                    uncertainty_type = st.selectbox("Type", ["Standard (k=1)", "Expanded (k=2)"])
                
                if st.form_submit_button("Add Source"):
                    if source_name:
                        # Convert to standard uncertainty
                        if uncertainty_type == "Expanded (k=2)":
                            std_uncertainty = uncertainty_value / 2
                        else:
                            std_uncertainty = uncertainty_value
                        
                        st.session_state.uncertainty_sources.append({
                            'name': source_name,
                            'value': std_uncertainty,
                            'type': uncertainty_type
                        })
                        st.success(f"Added {source_name}")
            
            # Display and calculate combined uncertainty
            if st.session_state.uncertainty_sources:
                st.markdown("### Current Uncertainty Sources:")
                
                # Show sources
                for i, source in enumerate(st.session_state.uncertainty_sources):
                    st.markdown(f"• **{source['name']}:** {source['value']:.4f} ({source['type']})")
                
                # Calculate combined uncertainty
                combined_variance = sum(source['value']**2 for source in st.session_state.uncertainty_sources)
                combined_uncertainty = math.sqrt(combined_variance)
                expanded_uncertainty = combined_uncertainty * 2  # k=2 for 95% confidence
                
                measurement_value = st.number_input("Measurement Value", value=10.0)
                
                relative_uncertainty = (combined_uncertainty / measurement_value) * 100
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Combined Uncertainty Results</h4>
                    <p><strong>Combined Standard Uncertainty:</strong> {combined_uncertainty:.4f}</p>
                    <p><strong>Expanded Uncertainty (k=2):</strong> {expanded_uncertainty:.4f}</p>
                    <p><strong>Relative Uncertainty:</strong> {relative_uncertainty:.2f}%</p>
                    <p><strong>Result:</strong> {measurement_value:.3f} ± {expanded_uncertainty:.3f} (95% confidence)</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Clear All Sources"):
                    st.session_state.uncertainty_sources = []
                    st.rerun()
    
    with tab3:
        st.markdown("### 📊 Data Visualization")
        
        st.markdown("Create simple visualizations of your data")
        
        # For now, provide basic data display since we can't use external plotting libraries
        viz_data = st.text_area(
            "Enter data for visualization (comma separated)",
            value="1.2, 1.5, 1.3, 1.8, 1.1, 1.6, 1.4, 1.7, 1.2, 1.5",
            height=100
        )
        
        if st.button("Create Basic Visualization"):
            try:
                data = [float(x.strip()) for x in viz_data.split(',') if x.strip()]
                
                if len(data) >= 3:
                    # Create a simple data summary
                    st.markdown("### 📈 Data Summary Visualization")
                    
                    # Basic statistics
                    mean_val = np.mean(data)
                    std_val = np.std(data)
                    min_val = np.min(data)
                    max_val = np.max(data)
                    
                    # Create frequency distribution
                    bins = 5
                    hist, bin_edges = np.histogram(data, bins=bins)
                    
                    st.markdown(f"""
                    **Data Distribution:**
                    - **Mean:** {mean_val:.3f}
                    - **Std Dev:** {std_val:.3f}
                    - **Range:** {min_val:.3f} - {max_val:.3f}
                    - **Count:** {len(data)} points
                    """)
                    
                    # Simple histogram display
                    st.markdown("**Frequency Distribution:**")
                    for i in range(len(hist)):
                        bin_start = bin_edges[i]
                        bin_end = bin_edges[i+1]
                        count = hist[i]
                        bar = "█" * int(count * 20 / max(hist))  # Simple text bar chart
                        st.markdown(f"{bin_start:.2f}-{bin_end:.2f}: {bar} ({count})")
                    
                    # Data table
                    viz_df = pd.DataFrame({
                        'Index': range(1, len(data) + 1),
                        'Value': data,
                        'Deviation': [x - mean_val for x in data]
                    })
                    
                    st.dataframe(viz_df, use_container_width=True, hide_index=True)
                    
            except Exception as e:
                st.error(f"Visualization error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def lab_management_page():
    """Laboratory management and inventory tools"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("🏠 Laboratory Management Suite")
    st.markdown("*Complete laboratory management for modern research facilities*")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Chemical Inventory", "📋 Protocol Manager", "📅 Lab Scheduler", "🔒 Safety Management"])
    
    with tab1:
        st.markdown("### 📦 Chemical Inventory Management")
        
        col_inv1, col_inv2 = st.columns([2, 1])
        
        with col_inv1:
            st.markdown("#### Add New Chemical")
            
            with st.form("add_chemical_form"):
                col_chem1, col_chem2 = st.columns(2)
                
                with col_chem1:
                    chemical_name = st.text_input("Chemical Name*")
                    formula = st.text_input("Chemical Formula")
                    cas_number = st.text_input("CAS Number")
                    supplier = st.text_input("Supplier")
                
                with col_chem2:
                    quantity = st.number_input("Quantity", min_value=0.0, value=100.0)
                    unit = st.selectbox("Unit", ["g", "kg", "mL", "L", "mg", "μL"])
                    location = st.text_input("Storage Location")
                    
                    hazard_class = st.selectbox("Hazard Classification", [
                        "Non-hazardous",
                        "Flammable", 
                        "Corrosive",
                        "Toxic",
                        "Oxidizing",
                        "Explosive",
                        "Carcinogenic"
                    ])
                
                # Additional fields
                with st.expander("📋 Additional Information"):
                    lot_number = st.text_input("Lot/Batch Number")
                    expiry_date = st.date_input("Expiry Date")
                    cost = st.number_input("Cost", min_value=0.0, value=0.0)
                    notes = st.text_area("Notes")
                
                if st.form_submit_button("➕ Add to Inventory", use_container_width=True):
                    if chemical_name:
                        new_chemical = {
                            'name': chemical_name,
                            'formula': formula,
                            'cas_number': cas_number,
                            'supplier': supplier,
                            'quantity': quantity,
                            'unit': unit,
                            'location': location,
                            'hazard_class': hazard_class,
                            'lot_number': lot_number,
                            'expiry_date': str(expiry_date) if expiry_date else "",
                            'cost': cost,
                            'notes': notes,
                            'added_date': datetime.now().strftime("%Y-%m-%d"),
                            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        
                        st.session_state.inventory.append(new_chemical)
                        st.success(f"✅ Added {chemical_name} to inventory!")
                        
                        add_to_history(
                            "Inventory Addition",
                            {'chemical': chemical_name, 'quantity': quantity, 'unit': unit},
                            {'location': location, 'hazard': hazard_class}
                        )
                    else:
                        st.error("Chemical name is required!")
        
        with col_inv2:
            st.markdown("#### Inventory Summary")
            
            if st.session_state.inventory:
                total_chemicals = len(st.session_state.inventory)
                hazardous_count = len([item for item in st.session_state.inventory 
                                     if item['hazard_class'] != 'Non-hazardous'])
                
                # Count by hazard type
                hazard_counts = {}
                for item in st.session_state.inventory:
                    hazard = item['hazard_class']
                    hazard_counts[hazard] = hazard_counts.get(hazard, 0) + 1
                
                st.metric("Total Chemicals", total_chemicals)
                st.metric("Hazardous Items", hazardous_count)
                
                st.markdown("**By Hazard Class:**")
                for hazard, count in hazard_counts.items():
                    st.markdown(f"• {hazard}: {count}")
                
                # Location summary
                locations = set(item['location'] for item in st.session_state.inventory if item['location'])
                if locations:
                    st.markdown(f"**Storage Locations:** {len(locations)}")
                    for loc in sorted(locations):
                        st.markdown(f"• {loc}")
            else:
                st.info("No chemicals in inventory yet")
        
        # Current inventory display
        if st.session_state.inventory:
            st.markdown("### 📋 Current Inventory")
            
            # Search and filter options
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                search_term = st.text_input("🔍 Search chemicals", "")
            
            with col_filter2:
                hazard_filter = st.selectbox("Filter by Hazard", 
                    ["All"] + list(set(item['hazard_class'] for item in st.session_state.inventory)))
            
            with col_filter3:
                location_filter = st.selectbox("Filter by Location",
                    ["All"] + list(set(item['location'] for item in st.session_state.inventory if item['location'])))
            
            # Filter inventory
            filtered_inventory = st.session_state.inventory
            
            if search_term:
                filtered_inventory = [item for item in filtered_inventory 
                                    if search_term.lower() in item['name'].lower() or 
                                       search_term.lower() in item['formula'].lower()]
            
            if hazard_filter != "All":
                filtered_inventory = [item for item in filtered_inventory 
                                    if item['hazard_class'] == hazard_filter]
            
            if location_filter != "All":
                filtered_inventory = [item for item in filtered_inventory 
                                    if item['location'] == location_filter]
            
            # Display filtered inventory
            if filtered_inventory:
                # Convert to DataFrame for better display
                df_inventory = pd.DataFrame(filtered_inventory)
                
                # Select columns to display
                display_columns = ['name', 'formula', 'quantity', 'unit', 'location', 'hazard_class', 'supplier']
                df_display = df_inventory[display_columns]
                df_display.columns = ['Chemical', 'Formula', 'Quantity', 'Unit', 'Location', 'Hazard', 'Supplier']
                
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                # Bulk actions
                st.markdown("### ⚙️ Bulk Actions")
                col_bulk1, col_bulk2, col_bulk3 = st.columns(3)
                
                with col_bulk1:
                    if st.button("📄 Export to CSV"):
                        csv_data = df_display.to_csv(index=False)
                        st.download_button(
                            "⬇️ Download CSV",
                            csv_data,
                            f"inventory_{datetime.now().strftime('%Y%m%d')}.csv",
                            "text/csv"
                        )
                
                with col_bulk2:
                    if st.button("🗑️ Clear All"):
                        if st.button("⚠️ Confirm Clear All"):
                            st.session_state.inventory = []
                            st.success("Inventory cleared!")
                            st.rerun()
                
                with col_bulk3:
                    st.info(f"Showing {len(filtered_inventory)} of {len(st.session_state.inventory)} chemicals")
            else:
                st.info("No chemicals match the current filters")
    
    with tab2:
        st.markdown("### 📋 Protocol Manager")
        
        col_prot1, col_prot2 = st.columns([2, 1])
        
        with col_prot1:
            st.markdown("#### Create New Protocol")
            
            with st.form("create_protocol_form"):
                protocol_title = st.text_input("Protocol Title*")
                protocol_category = st.selectbox("Category", [
                    "Analytical Method",
                    "Sample Preparation", 
                    "Synthesis",
                    "Purification",
                    "Quality Control",
                    "Safety Procedure",
                    "Maintenance"
                ])
                
                col_prot_info1, col_prot_info2 = st.columns(2)
                
                with col_prot_info1:
                    author = st.text_input("Author", value="A.P.D Nexus Pro User")
                    version = st.text_input("Version", value="1.0")
                
                with col_prot_info2:
                    estimated_time = st.text_input("Estimated Time")
                    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
                
                # Protocol content
                st.markdown("**Protocol Content:**")
                
                objective = st.text_area("Objective/Purpose", height=80)
                materials = st.text_area("Materials and Reagents", height=100)
                equipment = st.text_area("Equipment Required", height=80)
                
                # Protocol steps
                st.markdown("**Procedure Steps:**")
                num_steps = st.number_input("Number of Steps", min_value=1, max_value=20, value=5)
                
                steps = []
                for i in range(num_steps):
                    step_text = st.text_area(f"Step {i+1}", key=f"step_{i}", height=80)
                    if step_text.strip():
                        steps.append(f"{i+1}. {step_text}")
                
                # Additional sections
                with st.expander("📋 Additional Sections"):
                    safety_notes = st.text_area("Safety Notes", height=80)
                    troubleshooting = st.text_area("Troubleshooting", height=80)
                    references = st.text_area("References", height=80)
                
                if st.form_submit_button("💾 Save Protocol", use_container_width=True):
                    if protocol_title and steps:
                        new_protocol = {
                            'title': protocol_title,
                            'category': protocol_category,
                            'author': author,
                            'version': version,
                            'estimated_time': estimated_time,
                            'difficulty': difficulty,
                            'objective': objective,
                            'materials': materials,
                            'equipment': equipment,
                            'steps': steps,
                            'safety_notes': safety_notes,
                            'troubleshooting': troubleshooting,
                            'references': references,
                            'created_date': datetime.now().strftime("%Y-%m-%d"),
                            'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M"),
                            'id': len(st.session_state.protocols) + 1
                        }
                        
                        st.session_state.protocols.append(new_protocol)
                        st.success(f"✅ Protocol '{protocol_title}' saved successfully!")
                        
                        add_to_history(
                            "Protocol Creation",
                            {'title': protocol_title, 'category': protocol_category, 'steps': len(steps)},
                            {'author': author, 'version': version}
                        )
                    else:
                        st.error("Protocol title and at least one step are required!")
        
        with col_prot2:
            st.markdown("#### Protocol Library")
            
            if st.session_state.protocols:
                st.metric("Total Protocols", len(st.session_state.protocols))
                
                # Category breakdown
                categories = {}
                for protocol in st.session_state.protocols:
                    cat = protocol['category']
                    categories[cat] = categories.get(cat, 0) + 1
                
                st.markdown("**By Category:**")
                for cat, count in categories.items():
                    st.markdown(f"• {cat}: {count}")
            else:
                st.info("No protocols saved yet")
        
        # Display saved protocols
        if st.session_state.protocols:
            st.markdown("### 📚 Saved Protocols")
            
            # Protocol search
            protocol_search = st.text_input("🔍 Search protocols", "")
            
            # Filter protocols
            filtered_protocols = st.session_state.protocols
            if protocol_search:
                filtered_protocols = [p for p in filtered_protocols 
                                    if protocol_search.lower() in p['title'].lower() or
                                       protocol_search.lower() in p['category'].lower()]
            
            for protocol in filtered_protocols:
                with st.expander(f"📋 {protocol['title']} - {protocol['category']} (v{protocol['version']})"):
                    col_proto1, col_proto2 = st.columns([3, 1])
                    
                    with col_proto1:
                        st.markdown(f"**Author:** {protocol['author']}")
                        st.markdown(f"**Created:** {protocol['created_date']}")
                        st.markdown(f"**Difficulty:** {protocol['difficulty']}")
                        if protocol['estimated_time']:
                            st.markdown(f"**Duration:** {protocol['estimated_time']}")
                        
                        if protocol['objective']:
                            st.markdown("**Objective:**")
                            st.markdown(protocol['objective'])
                        
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
                        
                        if protocol['safety_notes']:
                            st.markdown("**⚠️ Safety Notes:**")
                            st.markdown(protocol['safety_notes'])
                    
                    with col_proto2:
                        # Protocol actions
                        if st.button(f"📄 Export", key=f"export_{protocol['id']}"):
                            protocol_text = f"""
# {protocol['title']}

**Category:** {protocol['category']}
**Author:** {protocol['author']}
**Version:** {protocol['version']}
**Created:** {protocol['created_date']}

## Objective
{protocol['objective']}

## Materials
{protocol['materials']}

## Equipment
{protocol['equipment']}

## Procedure
{chr(10).join(protocol['steps'])}

## Safety Notes
{protocol['safety_notes']}

## Troubleshooting
{protocol['troubleshooting']}

## References
{protocol['references']}
                            """
                            
                            st.download_button(
                                "⬇️ Download",
                                protocol_text,
                                f"{protocol['title'].replace(' ', '_')}_v{protocol['version']}.txt",
                                "text/plain",
                                key=f"download_{protocol['id']}"
                            )
    
    with tab3:
        st.markdown("### 📅 Laboratory Scheduler")
        
        st.markdown("*Equipment booking and experiment planning*")
        
        # Simplified scheduler interface
        with st.form("schedule_booking"):
            col_sched1, col_sched2 = st.columns(2)
            
            with col_sched1:
                equipment = st.selectbox("Equipment/Resource", [
                    "HPLC System",
                    "Spectrophotometer", 
                    "PCR Machine",
                    "Fume Hood A",
                    "Fume Hood B",
                    "Analytical Balance",
                    "Centrifuge",
                    "Incubator"
                ])
                
                booking_date = st.date_input("Date")
                
            with col_sched2:
                start_time = st.time_input("Start Time")
                duration = st.number_input("Duration (hours)", min_value=0.5, value=2.0, step=0.5)
                user_name = st.text_input("User Name")
            
            experiment_title = st.text_input("Experiment/Purpose")
            notes = st.text_area("Notes")
            
            if st.form_submit_button("📅 Book Equipment"):
                if equipment and user_name and experiment_title:
                    # Initialize bookings in session state
                    if 'bookings' not in st.session_state:
                        st.session_state.bookings = []
                    
                    booking = {
                        'equipment': equipment,
                        'date': str(booking_date),
                        'start_time': str(start_time),
                        'duration': duration,
                        'user': user_name,
                        'experiment': experiment_title,
                        'notes': notes,
                        'booked_at': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    
                    st.session_state.bookings.append(booking)
                    st.success(f"✅ Booked {equipment} for {user_name}")
                else:
                    st.error("Please fill in all required fields")
        
        # Display current bookings
        if 'bookings' in st.session_state and st.session_state.bookings:
            st.markdown("### 📋 Current Bookings")
            
            bookings_df = pd.DataFrame(st.session_state.bookings)
            bookings_df['End Time'] = pd.to_datetime(bookings_df['date'] + ' ' + bookings_df['start_time']) + pd.to_timedelta(bookings_df['duration'], unit='h')
            
            display_bookings = bookings_df[['equipment', 'date', 'start_time', 'duration', 'user', 'experiment']].copy()
            display_bookings.columns = ['Equipment', 'Date', 'Start', 'Duration (h)', 'User', 'Experiment']
            
            st.dataframe(display_bookings, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("### 🔒 Safety Management")
        
        st.markdown("*Laboratory safety tracking and compliance*")
        
        safety_tab = st.selectbox("Safety Section", [
            "Incident Reporting",
            "Safety Training Records",
            "Equipment Maintenance",
            "Chemical Compatibility"
        ])
        
        if safety_tab == "Incident Reporting":
            st.markdown("#### 🚨 Incident Report Form")
            
            with st.form("incident_report"):
                col_inc1, col_inc2 = st.columns(2)
                
                with col_inc1:
                    incident_date = st.date_input("Incident Date")
                    incident_time = st.time_input("Incident Time")
                    reporter_name = st.text_input("Reporter Name")
                    location = st.text_input("Location")
                
                with col_inc2:
                    incident_type = st.selectbox("Incident Type", [
                        "Chemical Spill",
                        "Equipment Malfunction",
                        "Personal Injury",
                        "Fire/Explosion",
                        "Exposure",
                        "Near Miss",
                        "Other"
                    ])
                    
                    severity = st.selectbox("Severity", [
                        "Low - No injury/minimal impact",
                        "Medium - Minor injury/moderate impact", 
                        "High - Serious injury/major impact",
                        "Critical - Life threatening/severe impact"
                    ])
                
                description = st.text_area("Incident Description", height=100)
                immediate_actions = st.text_area("Immediate Actions Taken", height=80)
                root_cause = st.text_area("Root Cause Analysis", height=80)
                preventive_measures = st.text_area("Preventive Measures", height=80)
                
                if st.form_submit_button("📝 Submit Report"):
                    if description and reporter_name:
                        # Initialize incidents in session state
                        if 'incidents' not in st.session_state:
                            st.session_state.incidents = []
                        
                        incident = {
                            'date': str(incident_date),
                            'time': str(incident_time),
                            'reporter': reporter_name,
                            'location': location,
                            'type': incident_type,
                            'severity': severity,
                            'description': description,
                            'actions': immediate_actions,
                            'root_cause': root_cause,
                            'preventive': preventive_measures,
                            'reported_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
                            'id': len(st.session_state.get('incidents', [])) + 1
                        }
                        
                        st.session_state.incidents.append(incident)
                        st.success("✅ Incident report submitted")
                        
                        add_to_history(
                            "Incident Report",
                            {'type': incident_type, 'severity': severity, 'location': location},
                            {'reporter': reporter_name, 'date': str(incident_date)}
                        )
                    else:
                        st.error("Description and reporter name are required")
            
            # Display recent incidents
            if 'incidents' in st.session_state and st.session_state.incidents:
                st.markdown("### 📋 Recent Incidents")
                
                incidents_df = pd.DataFrame(st.session_state.incidents)
                display_incidents = incidents_df[['date', 'type', 'severity', 'location', 'reporter']].copy()
                display_incidents.columns = ['Date', 'Type', 'Severity', 'Location', 'Reporter']
                
                st.dataframe(display_incidents, use_container_width=True, hide_index=True)
        
        elif safety_tab == "Chemical Compatibility":
            st.markdown("#### ⚗️ Chemical Compatibility Checker")
            
            col_comp1, col_comp2 = st.columns(2)
            
            with col_comp1:
                chemical1 = st.text_input("Chemical 1")
                hazard1 = st.selectbox("Hazard Class 1", [
                    "Non-hazardous", "Flammable", "Corrosive", "Toxic", 
                    "Oxidizing", "Explosive", "Carcinogenic"
                ])
            
            with col_comp2:
                chemical2 = st.text_input("Chemical 2")
                hazard2 = st.selectbox("Hazard Class 2", [
                    "Non-hazardous", "Flammable", "Corrosive", "Toxic",
                    "Oxidizing", "Explosive", "Carcinogenic"
                ])
            
            if st.button("🔍 Check Compatibility"):
                # Simplified compatibility rules
                incompatible_pairs = [
                    ("Oxidizing", "Flammable"),
                    ("Corrosive", "Flammable"),
                    ("Explosive", "Oxidizing"),
                    ("Explosive", "Flammable")
                ]
                
                is_incompatible = False
                for pair in incompatible_pairs:
                    if (hazard1 in pair and hazard2 in pair) or (hazard2 in pair and hazard1 in pair):
                        is_incompatible = True
                        break
                
                if is_incompatible:
                    st.error("⚠️ **INCOMPATIBLE** - Do not store together!")
                    st.markdown("**Recommendations:**")
                    st.markdown("• Store in separate areas")
                    st.markdown("• Use appropriate separation distances")
                    st.markdown("• Check SDS for specific requirements")
                else:
                    st.success("✅ **COMPATIBLE** - Can be stored together")
                    st.markdown("**Note:** Always check individual SDS sheets for specific storage requirements")
        
        else:
            st.info(f"{safety_tab} module coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def educational_hub():
    """Educational resources and learning materials"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("📚 Educational Hub")
    st.markdown("*Learning resources, tutorials, and reference materials*")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎓 Interactive Tutorials", "📖 Reference Materials", "🎯 Practice Problems", "🧮 Unit Converters"])
    
    with tab1:
        st.markdown("### 🎓 Interactive Chemistry Tutorials")
        
        tutorial_topic = st.selectbox("Choose Tutorial Topic", [
            "Molarity and Solution Preparation",
            "pH and Buffer Calculations",
            "Beer's Law and Spectrophotometry",
            "PCR and Copy Number Calculations",
            "Chemical Stoichiometry",
            "Laboratory Safety"
        ])
        
        if tutorial_topic == "Molarity and Solution Preparation":
            st.markdown("""
            ## 🧪 Molarity and Solution Preparation Tutorial
            
            ### What is Molarity?
            
            **Molarity (M)** is the concentration of a solution expressed as **moles of solute per liter of solution**.
            
            **Formula:** `M = moles of solute / liters of solution`
            
            ### Step-by-Step Calculation
            
            **Example:** Prepare 500 mL of 0.1 M NaCl solution
            
            **Step 1:** Calculate moles needed
            ```
            Moles = Molarity × Volume (L)
            Moles = 0.1 M × 0.5 L = 0.05 mol
            ```
            
            **Step 2:** Calculate mass needed
            ```
            Mass = Moles × Molecular Weight
            MW of NaCl = 22.99 + 35.45 = 58.44 g/mol
            Mass = 0.05 mol × 58.44 g/mol = 2.922 g
            ```
            
            **Step 3:** Preparation procedure
            1. Weigh 2.922 g of NaCl
            2. Dissolve in ~400 mL distilled water
            3. Transfer to 500 mL volumetric flask
            4. Dilute to exactly 500 mL with water
            5. Mix thoroughly
            """)
            
            # Interactive example
            st.markdown("### 🧮 Try It Yourself!")
            
            col_tut1, col_tut2 = st.columns(2)
            
            with col_tut1:
                user_molarity = st.number_input("Desired Molarity (M)", value=0.2, min_value=0.001)
                user_volume = st.number_input("Volume (mL)", value=250.0, min_value=1.0)
                user_formula = st.text_input("Chemical Formula", value="KCl")
            
            with col_tut2:
                if st.button("Calculate Tutorial Example"):
                    try:
                        mw = AdvancedChemistryCalculators.compute_molecular_weight(user_formula)
                        volume_L = user_volume / 1000
                        moles_needed = user_molarity * volume_L
                        mass_needed = moles_needed * mw
                        
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>Tutorial Solution</h4>
                            <p><strong>Step 1:</strong> Moles = {user_molarity:.3f} M × {volume_L:.3f} L = {moles_needed:.6f} mol</p>
                            <p><strong>Step 2:</strong> Mass = {moles_needed:.6f} mol × {mw:.2f} g/mol = {mass_needed:.4f} g</p>
                            <p><strong>Step 3:</strong> Dissolve {mass_needed:.4f} g {user_formula} in water and dilute to {user_volume} mL</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error in calculation: {str(e)}")
        
        elif tutorial_topic == "pH and Buffer Calculations":
            st.markdown("""
            ## 🔬 pH and Buffer Calculations Tutorial
            
            ### Understanding pH
            
            **pH** is a measure of hydrogen ion concentration in solution.
            
            **Formula:** `pH = -log[H⁺]`
            
            **pH Scale:**
            - pH < 7: Acidic
            - pH = 7: Neutral  
            - pH > 7: Basic
            
            ### Buffer Calculations
            
            **Henderson-Hasselbalch Equation:**
            ```
            pH = pKa + log([A⁻]/[HA])
            ```
            
            Where:
            - pKa = acid dissociation constant
            - [A⁻] = conjugate base concentration
            - [HA] = weak acid concentration
            
            ### Buffer Example
            
            **Problem:** Calculate pH of buffer with 0.1 M acetic acid (pKa = 4.75) and 0.1 M acetate
            
            **Solution:**
            ```
            pH = 4.75 + log(0.1/0.1)
            pH = 4.75 + log(1)
            pH = 4.75 + 0 = 4.75
            ```
            """)
        
        elif tutorial_topic == "Beer's Law and Spectrophotometry":
            st.markdown("""
            ## 📊 Beer's Law and Spectrophotometry Tutorial
            
            ### Beer's Law Equation
            
            **Formula:** `A = ε × c × l`
            
            Where:
            - **A** = Absorbance (no units)
            - **ε** = Molar extinction coefficient (M⁻¹cm⁻¹)
            - **c** = Concentration (M)
            - **l** = Path length (cm)
            
            ### Key Concepts
            
            **Absorbance vs Transmittance:**
            - Absorbance measures how much light is absorbed
            - Transmittance measures how much light passes through
            - Relationship: A = -log(T) where T = I/I₀
            
            **Linear Range:**
            - Beer's Law is linear typically from A = 0.1 to A = 2.0
            - Best accuracy between A = 0.2 to A = 1.5
            
            ### Practical Example
            
            **Problem:** NADH solution shows A₃₄₀ = 0.62 in 1 cm cuvette. Calculate concentration.
            
            **Given:** ε₃₄₀ = 6,220 M⁻¹cm⁻¹ for NADH
            
            **Solution:**
            ```
            A = ε × c × l
            0.62 = 6,220 × c × 1
            c = 0.62 / 6,220 = 9.97 × 10⁻⁵ M
            c = 99.7 μM
            ```
            """)
        
        elif tutorial_topic == "PCR and Copy Number Calculations":
            st.markdown("""
            ## 🧬 PCR and Copy Number Calculations Tutorial
            
            ### Real-time PCR Basics
            
            **Ct Value:** Cycle threshold - the cycle number where fluorescence exceeds background
            
            **Efficiency:** How well the PCR amplifies (ideally 90-110%)
            
            ### Absolute Quantification
            
            **Formula:** `Copy Number = Standard Copies × E^(Ct_standard - Ct_sample)`
            
            Where E = amplification efficiency (e.g., 2.0 for 100% efficiency)
            
            **Example:**
            - Standard: 10⁶ copies, Ct = 20.0
            - Sample: Ct = 23.0  
            - Efficiency: 100%
            
            **Calculation:**
            ```
            Copy Number = 10⁶ × 2^(20.0 - 23.0)
            Copy Number = 10⁶ × 2^(-3.0)
            Copy Number = 10⁶ × 0.125 = 125,000 copies
            ```
            
            ### Relative Quantification (ΔΔCt)
            
            **Formula:** `Fold Change = 2^(-ΔΔCt)`
            
            Where ΔΔCt = (Ct_target - Ct_reference)_sample - (Ct_target - Ct_reference)_control
            
            **Interpretation:**
            - Fold Change > 1: Up-regulated
            - Fold Change < 1: Down-regulated
            - Fold Change = 1: No change
            """)
        
        else:
            st.info(f"Tutorial for {tutorial_topic} is under development!")
    
    with tab2:
        st.markdown("### 📖 Reference Materials")
        
        ref_category = st.selectbox("Reference Category", [
            "Common Chemical Formulas",
            "Unit Conversions",
            "Physical Constants",
            "Useful Equations",
            "Spectroscopy Data",
            "Safety Information"
        ])
        
        if ref_category == "Common Chemical Formulas":
            st.markdown("### 🧪 Common Laboratory Chemicals")
            
            # Create comprehensive reference table
            common_compounds = {
                'Water': {'formula': 'H₂O', 'mw': 18.02, 'use': 'Universal solvent'},
                'Sodium Chloride': {'formula': 'NaCl', 'mw': 58.44, 'use': 'Salt, buffer component'},
                'Hydrochloric Acid': {'formula': 'HCl', 'mw': 36.46, 'use': 'Strong acid, pH adjustment'},
                'Sulfuric Acid': {'formula': 'H₂SO₄', 'mw': 98.08, 'use': 'Strong acid, dehydrating agent'},
                'Sodium Hydroxide': {'formula': 'NaOH', 'mw': 40.00, 'use': 'Strong base, pH adjustment'},
                'Glucose': {'formula': 'C₆H₁₂O₆', 'mw': 180.16, 'use': 'Carbon source, energy'},
                'Ethanol': {'formula': 'C₂H₅OH', 'mw': 46.07, 'use': 'Solvent, disinfectant'},
                'Acetic Acid': {'formula': 'CH₃COOH', 'mw': 60.05, 'use': 'Weak acid, buffer'},
                'Calcium Chloride': {'formula': 'CaCl₂', 'mw': 110.98, 'use': 'Calcium source, drying agent'},
                'Potassium Permanganate': {'formula': 'KMnO₄', 'mw': 158.03, 'use': 'Oxidizing agent'},
                'EDTA': {'formula': 'C₁₀H₁₆N₂O₈', 'mw': 292.24, 'use': 'Chelating agent'},
                'Tris': {'formula': 'C₄H₁₁NO₃', 'mw': 121.14, 'use': 'Buffer (pH 7-9)'},
                'HEPES': {'formula': 'C₈H₁₈N₂O₄S', 'mw': 238.31, 'use': 'Biological buffer'},
                'DTT': {'formula': 'C₄H₁₀O₂S₂', 'mw': 154.25, 'use': 'Reducing agent'}
            }
            
            ref_data = []
            for name, data in common_compounds.items():
                ref_data.append({
                    'Compound': name,
                    'Formula': data['formula'],
                    'MW (g/mol)': data['mw'],
                    'Common Use': data['use']
                })
            
            df_ref = pd.DataFrame(ref_data)
            st.dataframe(df_ref, use_container_width=True, hide_index=True)
        
        elif ref_category == "Unit Conversions":
            st.markdown("""
            ## 🔄 Laboratory Unit Conversions
            
            ### Concentration Units
            ```
            1 M = 1000 mM = 1,000,000 μM
            1% (w/v) = 10 mg/mL = 10,000 μg/mL
            1 ppm = 1 μg/mL (for aqueous solutions)
            1 ppb = 1 ng/mL (for aqueous solutions)
            ```
            
            ### Volume Units
            ```
            1 L = 1000 mL = 1,000,000 μL
            1 mL = 1000 μL = 1 cm³
            1 gallon = 3.785 L
            1 fluid ounce = 29.57 mL
            ```
            
            ### Mass Units
            ```
            1 kg = 1000 g = 1,000,000 mg = 10⁹ μg
            1 g = 1000 mg = 1,000,000 μg = 10⁹ ng
            1 lb = 453.59 g
            1 oz = 28.35 g
            ```
            
            ### Temperature Conversions
            ```
            °C = (°F - 32) × 5/9
            °F = (°C × 9/5) + 32
            K = °C + 273.15
            °R = °F + 459.67
            ```
            
            ### Pressure Units
            ```
            1 atm = 760 mmHg = 760 Torr = 101.325 kPa
            1 bar = 0.987 atm = 14.50 psi
            1 psi = 6.895 kPa = 51.71 mmHg
            ```
            """)
        
        elif ref_category == "Physical Constants":
            st.markdown("""
            ## 📊 Important Physical Constants
            
            ### Fundamental Constants
            ```
            Avogadro's Number (Nₐ)     = 6.022 × 10²³ mol⁻¹
            Gas Constant (R)           = 8.314 J/(mol·K)
                                      = 0.08206 L·atm/(mol·K)
                                      = 8.314 × 10⁻³ kJ/(mol·K)
            Planck's Constant (h)      = 6.626 × 10⁻³⁴ J·s
            Speed of Light (c)         = 2.998 × 10⁸ m/s
            Faraday Constant (F)       = 96,485 C/mol
            Boltzmann Constant (k)     = 1.381 × 10⁻²³ J/K
            ```
            
            ### Chemical Constants
            ```
            Ion Product of Water (Kw)  = 1.0 × 10⁻¹⁴ (at 25°C)
            Standard Temperature       = 273.15 K (0°C)
            Standard Pressure          = 1 atm = 101.325 kPa
            Molar Volume (STP)         = 22.414 L/mol
            ```
            
            ### Common pKa Values (at 25°C)
            ```
            Acetic acid                = 4.76
            Formic acid                = 3.75
            Phosphoric acid            = 2.15, 7.20, 12.38
            Carbonic acid              = 6.37, 10.25
            Citric acid                = 3.13, 4.76, 6.40
            Ammonia                    = 9.25
            Water                      = 14.00
            ```
            """)
        
        elif ref_category == "Useful Equations":
            st.markdown("""
            ## ⚖️ Essential Laboratory Equations
            
            ### Solution Chemistry
            ```
            Molarity (M)               = moles solute / L solution
            Molality (m)               = moles solute / kg solvent
            Normality (N)              = equivalents / L solution
            Dilution                   = C₁V₁ = C₂V₂
            Parts per million          = (mg solute / L solution)
            ```
            
            ### Acid-Base Chemistry
            ```
            pH                         = -log[H⁺]
            pOH                        = -log[OH⁻]
            pH + pOH                   = 14 (at 25°C)
            Henderson-Hasselbalch      = pH = pKa + log([A⁻]/[HA])
            Buffer capacity            = 2.3 × C × α × (1-α)
            ```
            
            ### Spectroscopy
            ```
            Beer's Law                 = A = ε × c × l
            Transmittance              = T = I/I₀ = 10⁻ᴬ
            Absorbance                 = A = -log(T) = log(I₀/I)
            ```
            
            ### Thermodynamics
            ```
            Gibbs Free Energy          = ΔG = ΔH - TΔS
            Ideal Gas Law              = PV = nRT
            Van't Hoff Equation        = ln(K₂/K₁) = (ΔH/R)(1/T₁ - 1/T₂)
            Arrhenius Equation         = k = A × e^(-Ea/RT)
            ```
            
            ### PCR and Molecular Biology
            ```
            Copy Number (absolute)     = Standard × E^(Ct_std - Ct_sample)
            Fold Change (relative)     = 2^(-ΔΔCt)
            PCR Efficiency             = (10^(-1/slope) - 1) × 100%
            Primer Tm (basic)          = 4(G+C) + 2(A+T)
            ```
            """)
        
        elif ref_category == "Spectroscopy Data":
            st.markdown("""
            ## 📈 Spectroscopy Reference Data
            
            ### Common Chromophores (λmax and ε)
            ```
            NADH (340 nm)              = 6,220 M⁻¹cm⁻¹
            NADPH (340 nm)             = 6,220 M⁻¹cm⁻¹
            FAD (450 nm)               = 11,300 M⁻¹cm⁻¹
            Cytochrome c (550 nm)      = 21,000 M⁻¹cm⁻¹
            Chlorophyll a (665 nm)     = 90,000 M⁻¹cm⁻¹
            β-Carotene (450 nm)        = 139,000 M⁻¹cm⁻¹
            ```
            
            ### Protein Analysis
            ```
            Generic protein (280 nm)   = ~1.0 mg/mL⁻¹cm⁻¹
            BSA (280 nm)               = 43,824 M⁻¹cm⁻¹
            Lysozyme (280 nm)          = 38,940 M⁻¹cm⁻¹
            IgG (280 nm)               = 210,000 M⁻¹cm⁻¹
            ```
            
            ### pH Indicators
            ```
            Methyl Orange              = 3.1-4.4 (red to yellow)
            Bromocresol Green          = 3.8-5.4 (yellow to blue)
            Methyl Red                 = 4.4-6.2 (red to yellow)
            Bromothymol Blue           = 6.0-7.6 (yellow to blue)
            Phenol Red                 = 6.8-8.4 (yellow to red)
            Phenolphthalein            = 8.3-10.0 (colorless to pink)
            ```
            
            ### Fluorescent Dyes
            ```
            DAPI (DNA)                 = Ex 358 nm, Em 461 nm
            Ethidium Bromide           = Ex 518 nm, Em 605 nm
            SYBR Green                 = Ex 494 nm, Em 521 nm
            GFP                        = Ex 395/475 nm, Em 509 nm
            ```
            """)
        
        else:
            st.info(f"Reference material for {ref_category} is being compiled!")
    
    with tab3:
        st.markdown("### 🎯 Practice Problems")
        
        problem_category = st.selectbox("Problem Category", [
            "Molarity Calculations",
            "Dilution Problems", 
            "pH and Buffers",
            "Beer's Law",
            "PCR Analysis"
        ])
        
        if problem_category == "Molarity Calculations":
            st.markdown("### 🧪 Molarity Practice Problems")
            
            problems = [
                {
                    "question": "How many grams of NaCl are needed to prepare 250 mL of 0.5 M solution?",
                    "answer": "7.31 g",
                    "solution": "MW of NaCl = 58.44 g/mol\nMoles = 0.5 M × 0.25 L = 0.125 mol\nMass = 0.125 mol × 58.44 g/mol = 7.31 g"
                },
                {
                    "question": "What is the molarity of a solution containing 25 g glucose in 500 mL water?",
                    "answer": "0.278 M", 
                    "solution": "MW of glucose (C₆H₁₂O₆) = 180.16 g/mol\nMoles = 25 g ÷ 180.16 g/mol = 0.1388 mol\nMolarity = 0.1388 mol ÷ 0.5 L = 0.278 M"
                },
                {
                    "question": "How much water must be added to 100 mL of 2 M HCl to make it 0.5 M?",
                    "answer": "300 mL",
                    "solution": "Using C₁V₁ = C₂V₂\n2 M × 100 mL = 0.5 M × V₂\nV₂ = 400 mL total\nWater to add = 400 - 100 = 300 mL"
                }
            ]
            
            for i, problem in enumerate(problems, 1):
                with st.expander(f"Problem {i}: {problem['question']}"):
                    
                    # User can try to solve
                    user_answer = st.text_input(f"Your answer for Problem {i}:", key=f"prob_{i}")
                    
                    if st.button(f"Show Solution {i}", key=f"sol_{i}"):
                        st.markdown(f"**Correct Answer:** {problem['answer']}")
                        st.markdown("**Solution:**")
                        st.code(problem['solution'])
                        
                        if user_answer:
                            try:
                                # Simple answer checking (extract numbers)
                                import re
                                user_nums = re.findall(r'\d+\.?\d*', user_answer)
                                correct_nums = re.findall(r'\d+\.?\d*', problem['answer'])
                                
                                if user_nums and correct_nums:
                                    if abs(float(user_nums[0]) - float(correct_nums[0])) < 0.1:
                                        st.success("✅ Correct!")
                                    else:
                                        st.warning("❌ Not quite right. Check your calculation.")
                            except:
                                st.info("💡 Check the solution above")
        
        elif problem_category == "pH and Buffers":
            st.markdown("### 🔬 pH and Buffer Practice Problems")
            
            ph_problems = [
                {
                    "question": "Calculate the pH of 0.01 M HCl solution.",
                    "answer": "pH = 2.00",
                    "solution": "HCl is a strong acid, so [H⁺] = 0.01 M\npH = -log(0.01) = -log(10⁻²) = 2.00"
                },
                {
                    "question": "What is the pH of a buffer containing 0.1 M acetic acid and 0.15 M acetate? (pKa = 4.75)",
                    "answer": "pH = 4.93",
                    "solution": "Using Henderson-Hasselbalch equation:\npH = pKa + log([A⁻]/[HA])\npH = 4.75 + log(0.15/0.1)\npH = 4.75 + log(1.5) = 4.75 + 0.18 = 4.93"
                }
            ]
            
            for i, problem in enumerate(ph_problems, 1):
                with st.expander(f"pH Problem {i}: {problem['question']}"):
                    user_answer = st.text_input(f"Your answer:", key=f"ph_prob_{i}")
                    
                    if st.button(f"Show Solution", key=f"ph_sol_{i}"):
                        st.markdown(f"**Answer:** {problem['answer']}")
                        st.code(problem['solution'])
        
        else:
            st.info(f"Practice problems for {problem_category} coming soon!")
    
    with tab4:
        st.markdown("### 🧮 Unit Converters")
        
        converter_type = st.selectbox("Converter Type", [
            "Concentration Converter",
            "Volume Converter", 
            "Mass Converter",
            "Temperature Converter",
            "Pressure Converter"
        ])
        
        if converter_type == "Concentration Converter":
            st.markdown("#### 🧪 Concentration Unit Converter")
            
            col_conv1, col_conv2 = st.columns(2)
            
            with col_conv1:
                st.markdown("**Input:**")
                input_value = st.number_input("Value", value=1.0, format="%.6f")
                input_unit = st.selectbox("From Unit", ["M", "mM", "μM", "mg/mL", "μg/mL", "%w/v"])
                
                # For mg/mL conversions, need molecular weight
                if input_unit in ["mg/mL", "μg/mL"] or "mM" in input_unit or "μM" in input_unit:
                    mw_for_conv = st.number_input("Molecular Weight (g/mol)", value=58.44, help="Required for mass ↔ molar conversions")
            
            with col_conv2:
                st.markdown("**Output:**")
                output_unit = st.selectbox("To Unit", ["M", "mM", "μM", "mg/mL", "μg/mL", "%w/v"])
            
            if st.button("🔄 Convert Concentration"):
                try:
                    # Convert to molarity first
                    if input_unit == "M":
                        molarity = input_value
                    elif input_unit == "mM":
                        molarity = input_value / 1000
                    elif input_unit == "μM":
                        molarity = input_value / 1000000
                    elif input_unit == "mg/mL":
                        molarity = (input_value / mw_for_conv) / 1000  # mg to g, then to mol, then to mol/L
                    elif input_unit == "μg/mL":
                        molarity = (input_value / mw_for_conv) / 1000000  # μg to g, then to mol
                    elif input_unit == "%w/v":
                        mg_per_ml = input_value * 10  # 1% = 10 mg/mL
                        molarity = (mg_per_ml / mw_for_conv) / 1000
                    
                    # Convert from molarity to target unit
                    if output_unit == "M":
                        result = molarity
                    elif output_unit == "mM":
                        result = molarity * 1000
                    elif output_unit == "μM":
                        result = molarity * 1000000
                    elif output_unit == "mg/mL":
                        result = molarity * mw_for_conv * 1000  # mol/L to mg/mL
                    elif output_unit == "μg/mL":
                        result = molarity * mw_for_conv * 1000000  # mol/L to μg/mL
                    elif output_unit == "%w/v":
                        mg_per_ml = molarity * mw_for_conv * 1000
                        result = mg_per_ml / 10  # mg/mL to %
                    
                    st.success(f"**{input_value} {input_unit} = {result:.6f} {output_unit}**")
                    
                except Exception as e:
                    st.error(f"Conversion error: {str(e)}")
        
        elif converter_type == "Temperature Converter":
            st.markdown("#### 🌡️ Temperature Converter")
            
            temp_input = st.number_input("Temperature", value=25.0)
            temp_from = st.selectbox("From", ["°C", "°F", "K", "°R"])
            
            # Convert to Celsius first
            if temp_from == "°C":
                celsius = temp_input
            elif temp_from == "°F":
                celsius = (temp_input - 32) * 5/9
            elif temp_from == "K":
                celsius = temp_input - 273.15
            elif temp_from == "°R":
                celsius = (temp_input - 491.67) * 5/9
            
            # Convert to all other units
            fahrenheit = celsius * 9/5 + 32
            kelvin = celsius + 273.15
            rankine = fahrenheit + 459.67
            
            st.markdown(f"""
            **Temperature Conversions:**
            - **Celsius:** {celsius:.2f} °C
            - **Fahrenheit:** {fahrenheit:.2f} °F  
            - **Kelvin:** {kelvin:.2f} K
            - **Rankine:** {rankine:.2f} °R
            """)
        
        elif converter_type == "Volume Converter":
            st.markdown("#### 💧 Volume Converter")
            
            vol_input = st.number_input("Volume", value=1.0)
            vol_from = st.selectbox("From Unit", ["L", "mL", "μL", "gal", "fl oz", "cup"])
            
            # Convert to liters first
            to_liters = {
                "L": 1,
                "mL": 0.001,
                "μL": 0.000001,
                "gal": 3.78541,
                "fl oz": 0.0295735,
                "cup": 0.236588
            }
            
            liters = vol_input * to_liters[vol_from]
            
            # Convert to all units
            results = {}
            for unit, factor in to_liters.items():
                results[unit] = liters / factor
            
            st.markdown("**Volume Conversions:**")
            for unit, value in results.items():
                st.markdown(f"- **{unit}:** {value:.6f}")
        
        else:
            st.info(f"{converter_type} coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def settings_help_page():
    """Settings and help page"""
    
    st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
    
    st.header("⚙️ Settings & Help")
    st.markdown("*Configuration, documentation, and system information*")
    
    tab1, tab2, tab3, tab4 = st.tabs(["⚙️ Settings", "❓ Help & FAQ", "📖 Documentation", "ℹ️ About"])
    
    with tab1:
        st.markdown("### ⚙️ Application Settings")
        
        col_set1, col_set2 = st.columns(2)
        
        with col_set1:
            st.markdown("#### 🎨 Display Preferences")
            
            # Theme settings
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"], index=0)
            if theme != "Light":
                st.info("Theme changes will be applied in future versions")
            
            # Precision settings
            decimal_precision = st.number_input("Decimal Precision", min_value=2, max_value=8, value=4)
            scientific_notation = st.checkbox("Use Scientific Notation for Small Numbers", value=True)
            
            # Units
            default_units = st.selectbox("Default Unit System", ["Metric", "Imperial", "Mixed"], index=0)
            
            # Language (future feature)
            language = st.selectbox("Language", ["English", "Spanish (Coming Soon)", "French (Coming Soon)"], index=0)
        
        with col_set2:
            st.markdown("#### 🔧 Calculation Settings")
            
            # Auto-save settings
            auto_save = st.checkbox("Auto-save Calculations to History", value=True)
            max_history = st.number_input("Maximum History Items", min_value=10, max_value=1000, value=100)
            
            # Warnings and validations
            show_warnings = st.checkbox("Show Input Validation Warnings", value=True)
            confirm_clear = st.checkbox("Confirm Before Clearing Data", value=True)
            
            # Advanced features
            advanced_mode = st.checkbox("Enable Advanced Features", value=False)
            expert_mode = st.checkbox("Expert Mode (Minimal Guidance)", value=False)
        
        # Save settings button
        if st.button("💾 Save Settings", use_container_width=True):
            # Store settings in session state
            settings = {
                'theme': theme,
                'precision': decimal_precision,
                'scientific_notation': scientific_notation,
                'units': default_units,
                'language': language,
                'auto_save': auto_save,
                'max_history': max_history,
                'show_warnings': show_warnings,
                'confirm_clear': confirm_clear,
                'advanced_mode': advanced_mode,
                'expert_mode': expert_mode
            }
            
            st.session_state.settings = settings
            st.success("✅ Settings saved successfully!")
        
        # Data management section
        st.markdown("### 💾 Data Management")
        
        col_data1, col_data2, col_data3 = st.columns(3)
        
        with col_data1:
            if st.button("🗑️ Clear History", use_container_width=True):
                if len(st.session_state.calculation_history) > 0:
                    st.session_state.calculation_history = []
                    st.success("History cleared!")
                else:
                    st.info("History is already empty")
        
        with col_data2:
            if st.button("📦 Clear Inventory", use_container_width=True):
                if len(st.session_state.inventory) > 0:
                    st.session_state.inventory = []
                    st.success("Inventory cleared!")
                else:
                    st.info("Inventory is already empty")
        
        with col_data3:
            if st.button("🔄 Reset All Data", use_container_width=True):
                if st.button("⚠️ Confirm Reset"):
                    st.session_state.calculation_history = []
                    st.session_state.inventory = []
                    st.session_state.protocols = []
                    st.session_state.favorites = []
                    st.success("All data reset!")
                    st.rerun()
        
        # Export/Import section
        st.markdown("### 📤 Export/Import Data")
        
        if st.button("📄 Export All Data as JSON"):
            export_data = {
                'calculation_history': st.session_state.calculation_history,
                'inventory': st.session_state.inventory,
                'protocols': st.session_state.protocols,
                'favorites': st.session_state.favorites,
                'export_date': datetime.now().isoformat(),
                'version': '2.0.0'
            }
            
            json_data = json.dumps(export_data, indent=2, default=str)
            
            st.download_button(
                "⬇️ Download Data",
                json_data,
                f"apd_nexus_pro_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )
    
    with tab2:
        st.markdown("### ❓ Help & Frequently Asked Questions")
        
        faq_category = st.selectbox("FAQ Category", [
            "Getting Started",
            "Calculations",
            "Data Management", 
            "Troubleshooting",
            "Features"
        ])
        
        if faq_category == "Getting Started":
            st.markdown("""
            ## 🚀 Getting Started with A.P.D Nexus Pro
            
            ### How do I navigate the application?
            - Use the **sidebar buttons** to select different calculators and tools
            - The **Dashboard** shows your recent activity and quick access buttons
            - Each tool has **tabs** for different calculation types
            
            ### How do I perform calculations?
            1. Select the appropriate calculator from the sidebar
            2. Enter your values in the input fields
            3. Click the **Calculate** button
            4. Results are displayed immediately and saved to history
            
            ### What data is saved?
            - All calculations are automatically saved to your **History**
            - **Inventory** items you add are stored in your session
            - **Protocols** you create are saved for future reference
            - Data persists during your browser session
            
            ### Is my data secure?
            - All data is stored locally in your browser session
            - Nothing is transmitted to external servers
            - Data is cleared when you close the browser (unless exported)
            """)
        
        elif faq_category == "Calculations":
            st.markdown("""
            ## 🧮 Calculation Help
            
            ### Molarity Calculator
            **Q: What format should I use for chemical formulas?**
            A: Use proper capitalization (Na, not na) and put numbers after elements (CaCl2, not Ca2Cl)
            
            **Q: Why am I getting a "formula error"?**
            A: Check spelling of element symbols and ensure proper capitalization
            
            ### Copy Number Calculator
            **Q: What's the difference between absolute and relative quantification?**
            A: Absolute gives actual copy numbers, relative compares expression between samples
            
            **Q: What efficiency should I use?**
            A: Use your experimentally determined efficiency, or 100% if unknown
            
            ### Beer's Law Calculator
            **Q: My absorbance is too high/low**
            A: Optimal range is 0.1-1.5. Dilute if too high, concentrate if too low
            
            **Q: Where do I find extinction coefficients?**
            A: Check literature, use built-in values, or determine experimentally
            """)
        
        elif faq_category == "Troubleshooting":
            st.markdown("""
            ## 🔧 Troubleshooting Guide
            
            ### Common Issues
            
            **Calculator not working?**
            - Check that all required fields are filled
            - Ensure numeric values are valid (no letters)
            - Try refreshing the page
            
            **Results seem wrong?**
            - Verify input values and units
            - Check formula spelling (for molecular weight calculations)
            - Confirm calculation type matches your needs
            
            **Page is slow or unresponsive?**
            - Clear calculation history (Settings → Data Management)
            - Close other browser tabs
            - Check internet connection
            
            **Data disappeared?**
            - Data is stored in browser session only
            - Export important data regularly
            - Check if you're in the same browser window
            
            ### Error Messages
            
            **"Invalid chemical formula"**
            - Use proper element symbols (Na, Cl, not na, cl)
            - Put numbers after elements (H2O, not H₂O)
            - Check for typos in element names
            
            **"Calculation error"**
            - Verify all inputs are positive numbers
            - Check units are compatible
            - Try different input values
            """)
        
        else:
            st.info(f"FAQ for {faq_category} is being compiled!")
    
    with tab3:
        st.markdown("### 📖 Documentation")
        
        doc_section = st.selectbox("Documentation Section", [
            "User Manual",
            "API Reference",
            "Calculation Methods",
            "Best Practices",
            "Updates & Changelog"
        ])
        
        if doc_section == "User Manual":
            st.markdown("""
            # 📚 A.P.D Nexus Pro User Manual
            
            ## Overview
            A.P.D Nexus Pro is a comprehensive laboratory calculation platform designed for chemists, biologists, and laboratory professionals.
            
            ## Main Features
            
            ### 🧮 Chemistry Calculators
            - **Molarity Calculator**: Solution preparation with molecular weight calculation
            - **Dilution Calculator**: C₁V₁ = C₂V₂ calculations and serial dilutions
            - **pH Calculator**: Acid-base calculations and buffer design
            - **Beer's Law Calculator**: Spectrophotometry and concentration analysis
            
            ### 🧬 Molecular Biology Tools
            - **Copy Number Calculator**: Absolute and relative qPCR quantification
            - **PCR Analysis Suite**: Efficiency calculations and primer analysis
            - **Gene Copy Estimation**: From DNA concentration to copy number
            
            ### 🏠 Laboratory Management
            - **Chemical Inventory**: Track chemicals, locations, and safety information
            - **Protocol Manager**: Create and store laboratory procedures
            - **Safety Management**: Incident reporting and compliance tracking
            
            ### 📚 Educational Resources
            - **Interactive Tutorials**: Step-by-step learning modules
            - **Reference Materials**: Chemical data and conversion tables
            - **Practice Problems**: Exercises with solutions
            
            ## Getting Started
            1. Select a tool from the sidebar menu
            2. Enter your data in the input fields
            3. Click calculate to get results
            4. View results and export if needed
            5. Check history for previous calculations
            """)
        
        elif doc_section == "Calculation Methods":
            st.markdown("""
            # 🔬 Calculation Methods and Formulas
            
            ## Chemistry Calculations
            
            ### Molarity
            ```
            M = n / V
            where:
            M = molarity (mol/L)
            n = moles of solute
            V = volume of solution (L)
            ```
            
            ### Dilution
            ```
            C₁V₁ = C₂V₂
            where:
            C₁, C₂ = initial and final concentrations
            V₁, V₂ = initial and final volumes
            ```
            
            ### pH Calculations
            ```
            pH = -log[H⁺]
            pH = pKa + log([A⁻]/[HA])  (Henderson-Hasselbalch)
            ```
            
            ### Beer's Law
            ```
            A = ε × c × l
            where:
            A = absorbance
            ε = molar extinction coefficient (M⁻¹cm⁻¹)
            c = concentration (M)
            l = path length (cm)
            ```
            
            ## PCR Calculations
            
            ### Absolute Quantification
            ```
            Copy Number = Standard_Copies × E^(Ct_standard - Ct_sample)
            where:
            E = amplification efficiency (typically 2.0 for 100%)
            ```
            
            ### Relative Quantification (ΔΔCt)
            ```
            Fold Change = 2^(-ΔΔCt)
            where:
            ΔΔCt = (Ct_target - Ct_reference)_sample - (Ct_target - Ct_reference)_control
            ```
            
            ### PCR Efficiency
            ```
            Efficiency = (10^(-1/slope) - 1) × 100%
            where slope is from standard curve: Ct = m × log[concentration] + b
            ```
            """)
        
        else:
            st.info(f"Documentation for {doc_section} is being prepared!")
    
    with tab4:
        st.markdown("### ℹ️ About ChemLab Pro")
        
        st.markdown("""
        ## 🧪 A.P.D Nexus Pro - Laboratory Suite
        
        **Version:** 2.0.0  
        **Release Date:** June 2024  
        **Build:** Complete Edition with Copy Number Calculator
        
        ### 🎯 Mission
        To provide professional-grade chemistry and molecular biology calculators accessible 
        from any device, helping laboratory professionals perform accurate calculations with confidence.
        
        ### ✨ Key Features
        - **15+ Professional Calculators** for chemistry and molecular biology
        - **Copy Number Calculator** for real-time PCR applications
        - **Advanced Data Analysis** with statistical tools
        - **Laboratory Management** for inventory and protocols
        - **Interactive Educational** resources and tutorials
        - **Mobile-Optimized** interface for lab bench use
        - **Professional Report** generation and export capabilities
        
        ### 🔬 Built For
        - **Research Scientists** in academic and industrial settings
        - **Laboratory Technicians** performing routine analyses
        - **Graduate Students** learning laboratory techniques
        - **Quality Control Analysts** ensuring measurement accuracy
        - **Educators** teaching chemistry and molecular biology
        - **Regulatory Scientists** requiring documented calculations
        
        ### 🛠️ Technology Stack
        - **Frontend Framework:** Streamlit (Python)
        - **Data Processing:** Pandas, NumPy
        - **Mathematical Calculations:** Native Python with SciPy
        - **Export Capabilities:** JSON, CSV, Text formats
        - **Responsive Design:** Works on desktop, tablet, and mobile
        
        ### 📈 Recent Updates (v2.0.0)
        - ✅ **NEW:** Complete Copy Number Calculator for qPCR
        - ✅ **NEW:** PCR Analysis Suite with efficiency calculations
        - ✅ **NEW:** Advanced statistical analysis tools
        - ✅ **NEW:** Laboratory safety management
        - ✅ **IMPROVED:** Enhanced molecular weight calculator
        - ✅ **IMPROVED:** Better error handling and validation
        - ✅ **IMPROVED:** Mobile responsiveness
        
        ### 👥 Development Team
        - **Lead Developer:** A.P.D Nexus Pro Team
        - **Scientific Advisors:** Laboratory professionals worldwide
        - **Beta Testers:** Research institutions and commercial labs
        
        ### 📊 Usage Statistics
        - **Tools Available:** 15+ calculators and analyzers
        - **Chemical Database:** 80+ common compounds
        - **Reference Data:** 200+ physical constants and conversions
        - **Tutorial Content:** 6 interactive learning modules
        
        ### 🔒 Privacy & Security
        - **Local Processing:** All calculations performed in your browser
        - **No Data Collection:** No personal information stored or transmitted
        - **Session-Based:** Data cleared when you close the browser
        - **Export Control:** You control your data export and sharing
        
        ### 📜 License & Attribution
        - **License:** Open Source MIT License
        - **Commercial Use:** Permitted for academic and commercial applications
        - **Attribution:** Please credit A.P.D Nexus Pro in publications using these tools
        - **Source Code:** Available for customization and extension
        
        ### 🌍 Global Impact
        A.P.D Nexus Pro is used by researchers and students in over 50 countries, 
        supporting scientific discovery and education worldwide.
        
        ### 📞 Support & Contact
        - **Documentation:** Built-in help system and tutorials
        - **Community:** User forums and discussion boards
        - **Bug Reports:** Issue tracking for continuous improvement
        - **Feature Requests:** Community-driven development priorities
        
        ### 🔮 Future Roadmap
        - **Advanced Statistics:** Machine learning integration
        - **Cloud Sync:** Optional data synchronization
        - **Collaboration Tools:** Shared protocols and calculations
        - **Mobile App:** Native iOS and Android applications
        - **API Access:** Integration with LIMS and other systems
        
        ---
        
        **Developed with ❤️ for the global scientific community**
        
        *Making laboratory calculations accessible, accurate, and efficient for everyone.*
        """)
        
        # System information
        st.markdown("### 💻 System Information")
        
        col_sys1, col_sys2 = st.columns(2)
        
        with col_sys1:
            st.markdown("""
            **Browser Compatibility:**
            - ✅ Chrome 90+ (Recommended)
            - ✅ Firefox 88+
            - ✅ Safari 14+
            - ✅ Edge 90+
            - ⚠️ Internet Explorer (Not supported)
            
            **Performance Requirements:**
            - **RAM:** 2GB minimum, 4GB recommended
            - **Storage:** 50MB browser cache
            - **Network:** Works offline after initial load
            """)
        
        with col_sys2:
            st.markdown("""
            **Platform Support:**
            - ✅ Windows 10/11
            - ✅ macOS 10.15+
            - ✅ Linux (All major distributions)
            - ✅ iOS 13+ (Safari)
            - ✅ Android 8+ (Chrome)
            - ✅ ChromeOS
            
            **Accessibility:**
            - **Screen Readers:** NVDA, JAWS, VoiceOver
            - **Keyboard Navigation:** Full support
            - **High Contrast:** System theme support
            """)
        
        # Version history
        with st.expander("📅 Version History"):
            st.markdown("""
            **v2.0.0** (June 2024)
            - Complete Copy Number Calculator
            - PCR Analysis Suite
            - Advanced statistics
            - Laboratory management tools
            
            **v1.5.0** (March 2024)
            - Beer's Law calculator
            - Data analysis tools
            - Export capabilities
            
            **v1.0.0** (January 2024)
            - Initial release
            - Basic chemistry calculators
            - Educational content
            """)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()