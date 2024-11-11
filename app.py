import streamlit as st
from utils import *
from datetime import datetime
from PIL import Image
import pandas as pd

def create_about_section():
    st.sidebar.markdown("## About Project")
    with st.sidebar.expander("ℹ️ Project Information", expanded=True):
        st.markdown("""
        ### Medical Parasitology Classifier
        
        This tool uses advanced deep learning to assist medical professionals in 
        identifying parasites from microscopic images.
        
        #### Key Features:
        - 15 distinct parasite classifications
        - Real-time analysis
        - Detailed parasite information
        - Geographic distribution tracking
        
        #### Important Note:
        This tool is designed to assist, not replace, professional medical diagnosis.
        """)


def create_interactive_image_upload():
    st.markdown("## Image Analysis")

    # Initialize session state for active tab and camera state if they don't exist
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "upload"
    if "camera_active" not in st.session_state:
        st.session_state.camera_active = False  # Camera starts off by default
    
    # Create the tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload", "📸 Camera", "🔍 Samples"])
    
    image = None
    source = None
    
    # Tab 1: Upload Image
    with tab1:
        # Set active tab to "upload"
        if st.session_state.active_tab != "upload":
            st.session_state.active_tab = "upload"
        
        uploaded_file = st.file_uploader(
            "Upload Microscopic Image",
            type=["png", "jpg", "jpeg"],
            help="Support formats: PNG, JPG, JPEG"
        )
        if uploaded_file:
            image = Image.open(uploaded_file)
            source = "upload"
        st.markdown("""
            ### Guidelines
            ✅ Clear focus
            ✅ Good lighting
            ✅ Proper magnification
            ❌ Avoid blurry images
            ❌ No digital modifications
        """)
    
    # Tab 2: Camera Capture
    with tab2:
        # Set active tab to "camera"
        if st.session_state.active_tab != "camera":
            st.session_state.active_tab = "camera"
        
        # Create an empty container for the camera
        camera_container = st.empty()
        
        # Show start and stop buttons only if we're on the Camera tab
        if st.session_state.active_tab == "camera":
            if st.button("Start Camera"):
                st.session_state.camera_active = True  # Activate the camera
            if st.button("Stop Camera"):
                st.session_state.camera_active = False  # Deactivate the camera
        
            # Display camera input if camera is active
            if st.session_state.camera_active:
                camera_input = camera_container.camera_input("Capture from Microscope")
                if camera_input:
                    image = Image.open(camera_input)
                    source = "camera"
            else:
                # Clear the camera when not active
                camera_container.empty()
    
    # Tab 3: Sample Images
    with tab3:
        # Set active tab to "samples"
        if st.session_state.active_tab != "samples":
            st.session_state.active_tab = "samples"
        
        st.markdown("### Sample Images")
        sample_images = load_sample_images(NUM_DISPLAYED)
        if sample_images:
            cols = st.columns(len(sample_images))
            for idx, (name, img) in enumerate(sample_images):
                with cols[idx]:
                    st.image(img, caption=name, use_container_width=True)
                    if st.button('Select', key=f'sample_{name}'):
                        image = img
                        source = "sample"
    
    return image, source



def display_parasite_details(parasite_name):
    if parasite_name in PARASITE_INFO:
        info = PARASITE_INFO[parasite_name]
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            ### {parasite_name}
            **Scientific Name:** {info['scientific_name']}
            
            {info['description']}
            
            #### Health Effects:
            """)
            for effect in info['health_effects']:
                st.markdown(f"- {effect}")
                
        with col2:
            st.markdown("#### Geographic Distribution")
            for region in info['prevalence']:
                st.markdown(f"- {region}")
            
            st.markdown(f"""
            **Risk Level:** {info['risk_level']}
            
            **Diagnosis Method:**
            {info['diagnosis']}
            """)

        # Place the expander outside of the columns
        st.markdown("### Prevention Methods")
        with st.expander("Click to view prevention methods", expanded=False):
            for method in info['prevention']:
                st.markdown(f"- {method}")

def display_analysis_results(model, image):
    if not image:
        return
    
    with st.spinner("🔬 Analyzing image..."):
        try:
            img_array, _ = preprocess_image(image)
            predicted_class, confidence_scores, _ = predict_image(model, img_array)
            
            # Get top predictions (primary and 2 alternatives)
            predictions = get_top_predictions(confidence_scores, top_k=3)
            
            if not predictions:
                st.warning("No predictions meet the confidence threshold.")
                return
            
            # Display primary prediction and alternatives side by side
            col1, col2 = st.columns(2)
            
            # Primary Prediction
            primary = predictions[0]
            col1.markdown(
                f"""
                <div style='padding: 20px; border-radius: 10px; background-color: #f0f2f6;'>
                    <h2>Primary Detection</h2>
                    <h3 style='color: #1f77b4;'>{primary[0]}</h3>
                    <h4>Confidence: {primary[1]*100:.1f}%</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Alternative Predictions
            col2.markdown("### Alternative Possibilities")
            for parasite, conf in predictions[1:3]:  # Show top 2 alternatives
                col2.progress(float(conf))  # Ensure progress bar accepts float
                col2.markdown(f"**{parasite}** ({conf*100:.1f}%)")
            
            # Display detailed information without nesting expander within columns
            st.markdown("📋 **Detailed Information**")
            display_parasite_details(primary[0])
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")


def main():
    st.set_page_config(
        page_title="Parasitology Image Classifier",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🔬 Parasitology Image Classifier")
    st.markdown("""
    Welcome to the Medical Parasitology Image Classification System. 
    This tool assists medical professionals in identifying parasites through microscopic image analysis.
    """)
    
    # Initialize components
    create_about_section()
    
    # Load model
    model = load_model_safely()
    if model is None:
        st.error("❌ Model loading failed. Please contact technical support.")
        return
    
    # Main interface
    image, source = create_interactive_image_upload()
    
    if image:
        # Display selected image
        st.image(image, caption="Selected Image", use_container_width=False)
        
        # Analysis and results
        display_analysis_results(model, image)
        
        # Export options
        if st.button("📥 Export Results"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            try:
                # Save results
                results_path = f"results/analysis_{timestamp}"
                export_results(results_path, image, predictions, confidence_scores)
                st.success("✅ Results exported successfully!")
                st.download_button(
                    "Download Report",
                    results_path,
                    file_name=f"parasite_analysis_{timestamp}.pdf"
                )
            except Exception as e:
                st.error(f"Export failed: {str(e)}")

if __name__ == "__main__":
    main()
