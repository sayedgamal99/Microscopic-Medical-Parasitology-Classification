from utils import *

def main():
    image = None
    st.set_page_config(page_title="Parasitology Image Classifier", page_icon="🔬", layout="wide")
    
    with st.sidebar:
        st.title("Settings & Information")
        show_debug = st.checkbox("Show Debug Info", value=False)
        st.markdown("---")
    
    # Load model
    model = load_model_safely()
    if model is None:
        st.error("Could not load the model. Please check the model file.")
        return

    st.title("Parasitology Image Classifier")

    # Image selection option
    input_choice = st.radio("Choose image source", ["Upload Image", "Use Camera", "Sample Images"])

    # Handle uploaded file
    if input_choice == "Upload Image":
        uploaded_file = st.file_uploader("Upload a microscopic image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
    
    # Handle camera input
    elif input_choice == "Use Camera":
        camera_input = st.camera_input("Take a picture")
        if camera_input is not None:
            image = Image.open(camera_input)
    
    # Handle sample images
    elif input_choice == "Sample Images":
        st.markdown("### Sample Images")
        sample_images = load_sample_images(NUM_DISPLAYED)
        n = len(sample_images)
        if n == 0:
            st.warning("No sample images available.")
            return
        
        # Display sample images in a grid layout
        sample_cols = st.columns(n, gap="small")
        selected_image = None

        for idx, (img_name, sample_image) in enumerate(sample_images):
            with sample_cols[idx % n]:
                st.image(sample_image, caption=img_name, width=90, use_container_width=True)
                if st.button('Choose', key=img_name):
                    selected_image = sample_image

        if selected_image:
            image = selected_image
            st.image(image, caption="Selected Sample Image", use_container_width=False)

    # Continue only if an image is loaded
    if image:
        with st.spinner("Processing image..."):
            img_array, preprocess_error = preprocess_image(image)
            if preprocess_error:
                st.error(preprocess_error)
                return
            
            predicted_class, confidence_scores, prediction_error = predict_image(model, img_array)
            if prediction_error:
                st.error(prediction_error)
                return
            
            # Display predictions
            top_predictions = get_top_predictions(confidence_scores)
            st.success("Analysis Complete!")
            col1, col2 = st.columns(2)
            with col1:
                primary_prediction = top_predictions[0]
                st.markdown(f"### Primary Detection\n**{primary_prediction[0]}** ({primary_prediction[1]*100:.1f}%)")
            with col2:
                st.markdown("### Alternative Possibilities")
                for parasite, conf in top_predictions[1:]:
                    st.markdown(f"- {parasite}: {conf*100:.1f}%")
            
            # Display information about predicted parasite
            st.markdown("### Parasite Information")
            display_parasite_info(primary_prediction[0])

            if st.button("Save Results"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                results_dict = {
                    "timestamp": timestamp,
                    "primary_prediction": primary_prediction[0],
                    "confidence": primary_prediction[1],
                    "image_name": uploaded_file.name if input_choice == "Upload Image" else img_name
                }
                df = pd.DataFrame([results_dict])
                df.to_csv(f"prediction_results_{timestamp}.csv", index=False)
                st.success("Results saved successfully!")

            # Debug information
            if show_debug:
                st.json({"Image Properties": {"Size": f"{image.size}", "Mode": image.mode}})

if __name__ == "__main__":
    main()
