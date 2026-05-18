import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem.Draw import MolDraw2DCairo
import io
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Organic Chemistry Reaction Visualizer",
    page_icon="🧪",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .reaction-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .compound-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def mol_to_image(mol, width=300, height=200):
    """Convert RDKit molecule to PIL Image"""
    if mol is None:
        return None
    drawer = MolDraw2DCairo(width, height)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    png_data = drawer.GetDrawingText()
    return Image.open(io.BytesIO(png_data))

def display_compound(comp_name, smiles, description=""):
    """Display compound with name, structure, and description"""
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        img = mol_to_image(mol)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(img, caption=comp_name, use_column_width=True)
        with col2:
            st.write(f"{comp_name}")
            st.write(f"SMILES: {smiles}")
            if description:
                st.write(description)
    else:
        st.error(f"Invalid SMILES for {comp_name}: {smiles}")

def show_reaction_example(reaction_name, reaction_data, compound_name, compound_smiles):
    """Display a specific reaction example"""
    with st.expander(f"🎯 {reaction_name}"):
        st.write(f"*Description:* {reaction_data.get('description', '')}")
        st.write(f"*Reagents:* {reaction_data['reagents']}")
        st.write(f"*Conditions:* {reaction_data['conditions']}")
        
        if "wikipedia" in reaction_data:
            st.markdown(f"[📚 Wikipedia Article]({reaction_data['wikipedia']})")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            display_compound("Reactant", compound_smiles, compound_name)
        
        with col2:
            st.markdown("<h3 style='text-align: center;'>→</h3>", unsafe_allow_html=True)
            st.write("*Reaction*")
        
        with col3:
            if "product_smiles" in reaction_data:
                display_compound("Product", reaction_data["product_smiles"], "Example Product")
            else:
                st.info("Product prediction not available for this compound")

def show_oxidation_reactions(compound_name, smiles):
    """Display oxidation reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    oxidation_reactions = {
        "Alcohol to Aldehyde": {
            "product_smiles": "CC=O",
            "reagents": "PCC, CrO₃, or KMnO₄",
            "conditions": "Mild oxidation, anhydrous conditions",
            "description": "Oxidation of primary alcohols to aldehydes"
        },
        "Alcohol to Carboxylic Acid": {
            "product_smiles": "CC(=O)O",
            "reagents": "KMnO₄, K₂Cr₂O₇/H₂SO₄",
            "conditions": "Strong oxidation, acidic conditions",
            "description": "Oxidation of primary alcohols to carboxylic acids"
        },
        "Aldehyde to Carboxylic Acid": {
            "product_smiles": "CC(=O)O",
            "reagents": "Tollens' reagent, KMnO₄",
            "conditions": "Mild conditions",
            "description": "Oxidation of aldehydes to carboxylic acids"
        }
    }
    
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        alcohol_pattern = Chem.MolFromSmarts("[OX2H]")
        aldehyde_pattern = Chem.MolFromSmarts("[CX3H1](=O)[#6]")
        
        if mol.HasSubstructMatch(alcohol_pattern):
            st.success("🔍 Compound A contains alcohol functional group")
            show_reaction_example("Alcohol to Aldehyde", oxidation_reactions["Alcohol to Aldehyde"], 
                                 compound_name, smiles)
            show_reaction_example("Alcohol to Carboxylic Acid", oxidation_reactions["Alcohol to Carboxylic Acid"],
                                 compound_name, smiles)
        
        elif mol.HasSubstructMatch(aldehyde_pattern):
            st.success("🔍 Compound A contains aldehyde functional group")
            show_reaction_example("Aldehyde to Carboxylic Acid", oxidation_reactions["Aldehyde to Carboxylic Acid"],
                                 compound_name, smiles)
        else:
            st.info("💡 Try compounds like ethanol (CCO) or acetaldehyde (CC=O) for oxidation examples")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_reduction_reactions(compound_name, smiles):
    """Display reduction reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    reduction_reactions = {
        "Aldehyde to Primary Alcohol": {
            "product_smiles": "CCO",
            "reagents": "NaBH₄, LiAlH₄",
            "conditions": "Room temperature",
            "description": "Reduction of aldehydes to primary alcohols"
        },
        "Ketone to Secondary Alcohol": {
            "product_smiles": "CC(O)C",
            "reagents": "NaBH₄, LiAlH₄",
            "conditions": "Room temperature",
            "description": "Reduction of ketones to secondary alcohols"
        },
        "Carboxylic Acid to Alcohol": {
            "product_smiles": "CCO",
            "reagents": "LiAlH₄",
            "conditions": "Anhydrous conditions",
            "description": "Reduction of carboxylic acids to primary alcohols"
        }
    }
    
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        aldehyde_pattern = Chem.MolFromSmarts("[CX3H1](=O)[#6]")
        ketone_pattern = Chem.MolFromSmarts("[CX3](=O)[#6]")
        acid_pattern = Chem.MolFromSmarts("C(=O)O")
        
        if mol.HasSubstructMatch(aldehyde_pattern):
            st.success("🔍 Compound A contains aldehyde functional group")
            show_reaction_example("Aldehyde to Primary Alcohol", reduction_reactions["Aldehyde to Primary Alcohol"],
                                 compound_name, smiles)
        
        elif mol.HasSubstructMatch(ketone_pattern):
            st.success("🔍 Compound A contains ketone functional group")
            show_reaction_example("Ketone to Secondary Alcohol", reduction_reactions["Ketone to Secondary Alcohol"],
                                 compound_name, smiles)
        
        elif mol.HasSubstructMatch(acid_pattern):
            st.success("🔍 Compound A contains carboxylic acid functional group")
            show_reaction_example("Carboxylic Acid to Alcohol", reduction_reactions["Carboxylic Acid to Alcohol"],
                                 compound_name, smiles)
        else:
            st.info("💡 Try compounds like acetaldehyde (CC=O) or acetone (CC(=O)C) for reduction examples")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_rearrangement_reactions(compound_name, smiles):
    """Display rearrangement reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    rearrangement_examples = {
        "Pinacol Rearrangement": {
            "reactant_smiles": "CC(C)(C)C(C)(C)O",
            "product_smiles": "CC(C)(C)C(=O)C",
            "reagents": "H₂SO₄, H₃O⁺",
            "conditions": "Acid-catalyzed",
            "description": "Rearrangement of 1,2-diols to carbonyl compounds"
        },
        "Beckmann Rearrangement": {
            "reactant_smiles": "CC(=NOH)C",
            "product_smiles": "CC(=O)NC",
            "reagents": "Acid catalyst",
            "conditions": "Acidic conditions",
            "description": "Rearrangement of oximes to amides"
        },
        "Hofmann Rearrangement": {
            "reactant_smiles": "CC(=O)N",
            "product_smiles": "CNC=O",
            "reagents": "Br₂, NaOH",
            "conditions": "Basic conditions",
            "description": "Conversion of primary amides to amines with one less carbon"
        }
    }
    
    st.subheader("Common Rearrangement Reactions")
    
    for reaction_name, data in rearrangement_examples.items():
        with st.expander(f"🎯 {reaction_name}"):
            st.write(f"*Description:* {data['description']}")
            st.write(f"*Reagents:* {data['reagents']}")
            st.write(f"*Conditions:* {data['conditions']}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                display_compound("Reactant", data["reactant_smiles"])
            with col2:
                st.markdown("<h3 style='text-align: center;'>→</h3>", unsafe_allow_html=True)
                st.write("*Rearrangement*")
            with col3:
                display_compound("Product", data["product_smiles"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_substitution_reactions(compound_name, smiles):
    """Display substitution reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    substitution_examples = {
        "SN2 Reaction": {
            "reactant_smiles": "CCl",
            "product_smiles": "CI",
            "reagents": "NaI in acetone",
            "conditions": "Polar aprotic solvent",
            "description": "Bimolecular nucleophilic substitution"
        },
        "SN1 Reaction": {
            "reactant_smiles": "C(C)(C)Cl",
            "product_smiles": "C(C)(C)O",
            "reagents": "H₂O",
            "conditions": "Polar protic solvent",
            "description": "Unimolecular nucleophilic substitution"
        }
    }
    
    st.subheader("Substitution Reactions")
    st.info("SN1 and SN2 mechanisms")
    
    for reaction_name, data in substitution_examples.items():
        with st.expander(f"🎯 {reaction_name}"):
            st.write(f"*Description:* {data['description']}")
            st.write(f"*Reagents:* {data['reagents']}")
            st.write(f"*Conditions:* {data['conditions']}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                display_compound("Reactant", data["reactant_smiles"])
            with col2:
                st.markdown("<h3 style='text-align: center;'>→</h3>", unsafe_allow_html=True)
                st.write("*Substitution*")
            with col3:
                display_compound("Product", data["product_smiles"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_elimination_reactions(compound_name, smiles):
    """Display elimination reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    elimination_examples = {
        "E2 Elimination": {
            "reactant_smiles": "CCCCl",
            "product_smiles": "C=C",
            "reagents": "KOH, ethanol",
            "conditions": "Strong base, heat",
            "description": "Bimolecular elimination"
        },
        "E1 Elimination": {
            "reactant_smiles": "CC(C)(C)Cl",
            "product_smiles": "C=C(C)C",
            "reagents": "H₂O, heat",
            "conditions": "Weak base, thermal",
            "description": "Unimolecular elimination"
        }
    }
    
    st.subheader("Elimination Reactions")
    st.info("E1 and E2 mechanisms forming alkenes")
    
    for reaction_name, data in elimination_examples.items():
        with st.expander(f"🎯 {reaction_name}"):
            st.write(f"*Description:* {data['description']}")
            st.write(f"*Reagents:* {data['reagents']}")
            st.write(f"*Conditions:* {data['conditions']}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                display_compound("Reactant", data["reactant_smiles"])
            with col2:
                st.markdown("<h3 style='text-align: center;'>→</h3>", unsafe_allow_html=True)
                st.write("*Elimination*")
            with col3:
                display_compound("Product", data["product_smiles"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_addition_reactions(compound_name, smiles):
    """Display addition reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    addition_examples = {
        "Hydrogenation": {
            "reactant_smiles": "C=C",
            "product_smiles": "CC",
            "reagents": "H₂, Pt/Pd/Ni catalyst",
            "conditions": "Room temperature, pressure",
            "description": "Addition of hydrogen to alkenes/alkynes"
        },
        "Halogen Addition": {
            "reactant_smiles": "C=C",
            "product_smiles": "CC(Br)Br",
            "reagents": "Br₂ in CCl₄",
            "conditions": "Room temperature",
            "description": "Anti addition of halogens"
        }
    }
    
    st.subheader("Addition Reactions")
    st.info("Electrophilic and nucleophilic addition to multiple bonds")
    
    for reaction_name, data in addition_examples.items():
        with st.expander(f"🎯 {reaction_name}"):
            st.write(f"*Description:* {data['description']}")
            st.write(f"*Reagents:* {data['reagents']}")
            st.write(f"*Conditions:* {data['conditions']}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                display_compound("Reactant", data["reactant_smiles"])
            with col2:
                st.markdown("<h3 style='text-align: center;'>→</h3>", unsafe_allow_html=True)
                st.write("*Addition*")
            with col3:
                display_compound("Product", data["product_smiles"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_named_reactions(compound_name, smiles):
    """Display famous named reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    named_reactions = {
        "Diels-Alder Reaction": {
            "reactant_smiles": "C=CC=C.C=C(C=O)",
            "product_smiles": "C1C=CC(C=O)C1",
            "reagents": "Heat",
            "conditions": "Thermal, concerted mechanism",
            "description": "[4+2] cycloaddition between diene and dienophile",
            "wikipedia": "https://en.wikipedia.org/wiki/Diels–Alder_reaction"
        },
        "Wittig Reaction": {
            "reactant_smiles": "C=O",
            "product_smiles": "C=C",
            "reagents": "Ph₃P=CH₂",
            "conditions": "Basic conditions",
            "description": "Conversion of carbonyls to alkenes using phosphonium ylides",
            "wikipedia": "https://en.wikipedia.org/wiki/Wittig_reaction"
        },
        "Grignard Reaction": {
            "reactant_smiles": "C=O",
            "product_smiles": "CO",
            "reagents": "RMgBr",
            "conditions": "Anhydrous conditions",
            "description": "Addition of organomagnesium compounds to carbonyls",
            "wikipedia": "https://en.wikipedia.org/wiki/Grignard_reaction"
        },
        "Aldol Condensation": {
            "reactant_smiles": "CC=O",
            "product_smiles": "CC(=O)CC=O",
            "reagents": "NaOH",
            "conditions": "Basic conditions",
            "description": "Formation of β-hydroxy carbonyl compounds",
            "wikipedia": "https://en.wikipedia.org/wiki/Aldol_reaction"
        }
    }
    
    st.subheader("Famous Named Reactions")
    st.info("Classic organic reactions with historical significance")
    
    for reaction_name, data in named_reactions.items():
        with st.expander(f"🏆 {reaction_name}"):
            st.write(f"*Description:* {data['description']}")
            st.write(f"*Reagents:* {data['reagents']}")
            st.write(f"*Conditions:* {data['conditions']}")
            
            if "wikipedia" in data:
                st.markdown(f"[📚 Wikipedia Article]({data['wikipedia']})")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                display_compound("Reactant(s)", data["reactant_smiles"])
            with col2:
                st.markdown("<h3 style='text-align: center;'>→</h3>", unsafe_allow_html=True)
                st.write("*Named Reaction*")
            with col3:
                display_compound("Product", data["product_smiles"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_coupling_reactions(compound_name, smiles):
    """Display modern coupling reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    coupling_reactions = {
        "Suzuki Coupling": {
            "reactant_smiles": "Brc1ccccc1.B(O)(O)c1ccccc1",
            "product_smiles": "c1ccc(cc1)-c2ccccc2",
            "reagents": "Pd(PPh₃)₄, Base",
            "conditions": "Mild conditions",
            "description": "Palladium-catalyzed cross-coupling of boronic acids with halides",
            "wikipedia": "https://en.wikipedia.org/wiki/Suzuki_reaction"
        },
        "Heck Reaction": {
            "reactant_smiles": "Brc1ccccc1.C=C",
            "product_smiles": "C=Cc1ccccc1",
            "reagents": "Pd(OAc)₂, Base",
            "conditions": "Palladium catalysis",
            "description": "Coupling of alkenes with aryl/vinyl halides",
            "wikipedia": "https://en.wikipedia.org/wiki/Heck_reaction"
        }
    }
    
    st.subheader("Modern Coupling Reactions")
    st.info("Palladium-catalyzed cross-coupling reactions (Nobel Prize 2010)")
    
    for reaction_name, data in coupling_reactions.items():
        with st.expander(f"🔗 {reaction_name}"):
            st.write(f"*Description:* {data['description']}")
            st.write(f"*Reagents:* {data['reagents']}")
            st.write(f"*Conditions:* {data['conditions']}")
            
            if "wikipedia" in data:
                st.markdown(f"[📚 Wikipedia Article]({data['wikipedia']})")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                display_compound("Reactants", data["reactant_smiles"])
            with col2:
                st.markdown("<h3 style='text-align: center;'>→</h3>", unsafe_allow_html=True)
                st.write("*Coupling*")
            with col3:
                display_compound("Product", data["product_smiles"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_carbonyl_reactions(compound_name, smiles):
    """Display carbonyl chemistry reactions"""
    st.markdown('<div class="reaction-section">', unsafe_allow_html=True)
    
    carbonyl_reactions = {
        "Knoevenagel Condensation": {
            "reactant_smiles": "O=CC=O",
            "product_smiles": "C=C(C=O)C=O",
            "reagents": "Amine catalyst",
            "conditions": "Basic conditions",
            "description": "Condensation of carbonyls with active methylene compounds",
            "wikipedia": "https://en.wikipedia.org/wiki/Knoevenagel_condensation"
        },
        "Michael Addition": {
            "reactant_smiles": "C=C(C=O)C",
            "product_smiles": "CC(C=O)CC=O",
            "reagents": "Base catalyst",
            "conditions": "Mild conditions",
            "description": "Conjugate addition to α,β-unsaturated carbonyls",
            "wikipedia": "https://en.wikipedia.org/wiki/Michael_reaction"
        }
    }
    
    st.subheader("Carbonyl Chemistry Reactions")
    st.info("Reactions involving carbonyl functional groups")
    
    for reaction_name, data in carbonyl_reactions.items():
        with st.expander(f"🎯 {reaction_name}"):
            st.write(f"*Description:* {data['description']}")
            st.write(f"*Reagents:* {data['reagents']}")
            st.write(f"*Conditions:* {data['conditions']}")
            
            if "wikipedia" in data:
                st.markdown(f"[📚 Wikipedia Article]({data['wikipedia']})")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                display_compound("Reactant", data["reactant_smiles"])
            with col2:
                st.markdown("<h3 style='text-align: center;'>→</h3>", unsafe_allow_html=True)
                st.write("*Carbonyl Reaction*")
            with col3:
                display_compound("Product", data["product_smiles"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🧪 Organic Chemistry Reaction Visualizer</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    reaction_type = st.sidebar.selectbox(
        "Select Reaction Type",
        ["Oxidation", "Reduction", "Rearrangement", "Substitution", "Elimination", "Addition", 
         "Named Reactions", "Coupling Reactions", "Carbonyl Chemistry"]
    )
    
    # Compound A input
    st.sidebar.header("Compound A Input")
    custom_mode = st.sidebar.checkbox("Use custom compound")
    
    if custom_mode:
        compound_a_smiles = st.sidebar.text_input("Enter SMILES for Compound A", "CCO")
        compound_a_name = st.sidebar.text_input("Compound A Name", "Ethanol")
    else:
        predefined_compounds = {
            "Ethanol": "CCO",
            "Methanol": "CO",
            "Acetaldehyde": "CC=O",
            "Acetic Acid": "CC(=O)O",
            "Cyclohexanol": "C1CCC(CC1)O",
            "Benzaldehyde": "c1ccc(cc1)C=O",
            "2-Propanol": "CC(O)C",
            "1-Butanol": "CCCCO",
            "Acetone": "CC(=O)C",
            "Benzene": "c1ccccc1",
            "Ethene": "C=C",
            "Acetylene": "C#C"
        }
        selected_compound = st.sidebar.selectbox("Select Compound A", list(predefined_compounds.keys()))
        compound_a_name = selected_compound
        compound_a_smiles = predefined_compounds[selected_compound]
    
    # Main content area
    st.header(f"{reaction_type} Reactions")
    
    # Display Compound A
    st.subheader("Starting Compound")
    display_compound(compound_a_name, compound_a_smiles)
    
    # Reaction examples based on selected type
    if reaction_type == "Oxidation":
        show_oxidation_reactions(compound_a_name, compound_a_smiles)
    elif reaction_type == "Reduction":
        show_reduction_reactions(compound_a_name, compound_a_smiles)
    elif reaction_type == "Rearrangement":
        show_rearrangement_reactions(compound_a_name, compound_a_smiles)
    elif reaction_type == "Substitution":
        show_substitution_reactions(compound_a_name, compound_a_smiles)
    elif reaction_type == "Elimination":
        show_elimination_reactions(compound_a_name, compound_a_smiles)
    elif reaction_type == "Addition":
        show_addition_reactions(compound_a_name, compound_a_smiles)
    elif reaction_type == "Named Reactions":
        show_named_reactions(compound_a_name, compound_a_smiles)
    elif reaction_type == "Coupling Reactions":
        show_coupling_reactions(compound_a_name, compound_a_smiles)
    elif reaction_type == "Carbonyl Chemistry":
        show_carbonyl_reactions(compound_a_name, compound_a_smiles)

# Add information section
def add_info_section():
    st.sidebar.markdown("---")
    st.sidebar.header("About")
    st.sidebar.info("""
    This application demonstrates organic chemistry reactions using RDKit for structure visualization.
    
    *Features:*
    - View compound structures
    - Explore different reaction types
    - See reaction conditions and reagents
    - Custom compound input via SMILES
    - Wikipedia links for named reactions
    
    *New Categories Added:*
    - Named Reactions (Diels-Alder, Wittig, Grignard, etc.)
    - Coupling Reactions (Suzuki, Heck, Sonogashira, etc.)
    - Carbonyl Chemistry (Knoevenagel, Michael, Mannich, etc.)
    """)

if __name__ == "__main__":
    add_info_section()
    main()
