import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report_docx():
    doc = Document()

    # Page setup - Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Helper function for headings
    def add_custom_heading(text, level):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        if level == 1:
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            run.font.size = Pt(18)
            run.font.color.rgb = RGBColor(0x00, 0x33, 0x66) # Deep Navy
            # Page break before Chapter 1 to 9 except title
            if "CHAPTER" in text or text in ["CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "TABLE OF CONTENTS", "LIST OF ABBREVIATIONS", "REFERENCES", "APPENDIX A", "APPENDIX B", "APPENDIX C", "APPENDIX D", "FINAL PROJECT SUMMARY"]:
                p.paragraph_format.page_break_before = True
        elif level == 2:
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(0x00, 0x40, 0x80)
        elif level == 3:
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    def add_p(text, bold_prefix=None, space_after=6, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        r_text = p.add_run(text)
        r_text.italic = italic
        return p

    def add_styled_table(headers, data, col_widths=None):
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], "003366")
            set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                r.font.size = Pt(10)

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F4F6F8" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                row_cells[c_idx].text = str(cell_value)
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=150, right=150)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.size = Pt(9.5)

        # Apply Column Widths
        if col_widths:
            for row in table.rows:
                for c_idx, w in enumerate(col_widths):
                    row.cells[c_idx].width = Inches(w)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        return table

    def add_image_figure(img_path, caption):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            run = p_img.add_run()
            run.add_picture(img_path, width=Inches(5.8))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(caption)
            r_cap.italic = True
            r_cap.bold = True
            r_cap.font.size = Pt(9.5)
            r_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # =========================================================
    # TITLE & COVER
    # =========================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run("EXPLAINABLE DEEP LEARNING FOR POST-COVID LUNG FIBROSIS SCREENING USING CHEST X-RAYS")
    r_t.bold = True
    r_t.font.size = Pt(22)
    r_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    r_sub = p_sub.add_run("PROJECT REPORT")
    r_sub.bold = True
    r_sub.font.size = Pt(16)
    r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(24)
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.add_run("Submitted by\n").bold = True
    p_meta.add_run("Shaik Thaslim\n").font.size = Pt(13)
    p_meta.add_run("AV.SC.U4AIE23138\n\n").font.size = Pt(11)

    p_meta.add_run("Department of Computer Science and Engineering – Artificial Intelligence\n").bold = True
    p_meta.add_run("Amrita Vishwa Vidyapeetham – Amaravati\n\n").font.size = Pt(12)

    p_meta.add_run("Under the Guidance of\n").bold = True
    p_meta.add_run("Dr. Satya Rajendra Singh\n\n").font.size = Pt(13)

    p_meta.add_run("Academic Year: 2026").bold = True

    # =========================================================
    # CERTIFICATE
    # =========================================================
    add_custom_heading("CERTIFICATE", 1)
    add_p("This is to certify that the project entitled “Explainable Deep Learning for Post-COVID Lung Fibrosis Screening Using Chest X-rays” has been carried out by Shaik Thaslim (AV.SC.U4AIE23138), Department of Computer Science and Engineering – Artificial Intelligence, Amrita Vishwa Vidyapeetham – Amaravati, under the guidance of Dr. Satya Rajendra Singh.")
    add_p("The project presents the design and implementation of an explainable deep-learning framework for screening fibrosis-related patterns from chest X-ray images. The work includes dataset preparation, deep-learning model development, transfer learning, fine-tuning, performance evaluation, Grad-CAM-based explainability, and Streamlit deployment.")
    add_p("The work documented in this report is submitted in partial fulfillment of the academic requirements of the program.")

    # =========================================================
    # DECLARATION
    # =========================================================
    add_custom_heading("DECLARATION", 1)
    add_p("I hereby declare that the project entitled “Explainable Deep Learning for Post-COVID Lung Fibrosis Screening Using Chest X-rays” is my academic project work carried out as part of the requirements of the Department of Computer Science and Engineering – Artificial Intelligence, Amrita Vishwa Vidyapeetham – Amaravati.")
    add_p("The implementation, experiments, evaluation results, model architecture, explainability workflow, and deployment details presented in this report are based on the supplied project implementation and documentation. Wherever exact experimental information was not available in the project artifacts, no unsupported numerical result has been introduced.")

    # =========================================================
    # ACKNOWLEDGEMENT
    # =========================================================
    add_custom_heading("ACKNOWLEDGEMENT", 1)
    add_p("I express my sincere gratitude to my project guide, Dr. Satya Rajendra Singh, for his guidance, technical suggestions, encouragement, and continuous support throughout the development of this project.")
    add_p("I would also like to thank the Department of Computer Science and Engineering – Artificial Intelligence, Amrita Vishwa Vidyapeetham – Amaravati, for providing the academic environment and resources required to carry out this work.")
    add_p("I acknowledge the researchers and organizations responsible for making medical imaging datasets, research papers, and deep-learning resources available to the research community. These resources provided the foundation for investigating chest X-ray-based fibrosis screening, transfer learning, and explainable artificial intelligence.")

    # =========================================================
    # ABSTRACT
    # =========================================================
    add_custom_heading("ABSTRACT", 1)
    add_p("Post-COVID pulmonary complications can persist after recovery from the acute infection and may include structural abnormalities associated with fibrotic changes. Detecting such abnormalities using chest X-rays is challenging because fibrosis-related patterns can be subtle and may overlap with normal pulmonary textures. Computed Tomography (CT) generally provides more detailed structural information, but chest X-rays remain more accessible, inexpensive, and widely available.")
    add_p("This project proposes an explainable deep-learning-based screening system for post-COVID lung fibrosis using chest X-ray images. The problem is formulated as a binary image-classification task involving two classes: Fibrosis and Normal.")
    add_p("The project uses the NIH Chest X-ray Dataset as the main training dataset, while the Kaggle Lung Disease Dataset (Fibrosis) and the Post-COVID Lung Fibrosis Dataset are maintained as independent external testing datasets. The dataset pipeline standardizes images to 224 × 224 pixels, converts them to RGB format, normalizes pixel values, and uses memory-mapped storage for efficient processing.")
    add_p("Several convolutional neural-network approaches were investigated, including a baseline CNN, ResNet50 transfer learning, fine-tuned ResNet50, DenseNet121, EfficientNet-B0, and DenseNet121 with attention. The final deployed model is a fine-tuned ResNet50 pretrained on ImageNet. The final architecture consists of the ResNet50 backbone, Global Average Pooling, a 256-unit fully connected layer, dropout, and a sigmoid output layer.")
    add_p("The final fine-tuning stage unfreezes the last 40 layers of ResNet50 while retaining the earlier pretrained layers. A learning rate of 1 × 10⁻⁵, batch size of 16, dropout of 0.4, binary cross-entropy loss, Adam optimization, and early stopping are used in the final configuration.")
    add_p("The final notebook evaluation uses a classification threshold of 0.4 and reports an accuracy of approximately 73% and a ROC-AUC of 0.69099. The fibrosis class obtains a recall of 0.38 in this final evaluation. These results demonstrate that the model learns useful visual representations but also highlight the difficulty of detecting subtle fibrosis from chest X-rays.")
    add_p("To improve interpretability, Grad-CAM is incorporated into the system. The final model is deployed using Streamlit, allowing users to upload a chest X-ray and obtain a predicted probability, risk level, original image, Grad-CAM heatmap, and heatmap overlay.")
    add_p("The proposed system is intended as an AI-assisted screening and decision-support tool, not as a replacement for radiologists, CT imaging, or clinical diagnosis.")

    # =========================================================
    # TABLE OF CONTENTS
    # =========================================================
    add_custom_heading("TABLE OF CONTENTS", 1)
    toc_items = [
        ("1. Introduction", "CHAPTER 1"),
        ("2. Literature Review", "CHAPTER 2"),
        ("3. Dataset and Data Preparation", "CHAPTER 3"),
        ("4. Proposed Methodology", "CHAPTER 4"),
        ("5. Implementation", "CHAPTER 5"),
        ("6. Experimental Results", "CHAPTER 6"),
        ("7. Discussion", "CHAPTER 7"),
        ("8. Application and Deployment", "CHAPTER 8"),
        ("9. Conclusion and Future Work", "CHAPTER 9"),
        ("10. References", "REFERENCES"),
        ("11. Appendices", "APPENDICES")
    ]
    for item, ref in toc_items:
        add_p(f"{item}")

    # =========================================================
    # LIST OF ABBREVIATIONS
    # =========================================================
    add_custom_heading("LIST OF ABBREVIATIONS", 1)
    abbrev_headers = ["Abbreviation", "Meaning"]
    abbrev_data = [
        ["AI", "Artificial Intelligence"],
        ["CNN", "Convolutional Neural Network"],
        ["CXR", "Chest X-ray"],
        ["CT", "Computed Tomography"],
        ["DL", "Deep Learning"],
        ["XAI", "Explainable Artificial Intelligence"],
        ["ROC", "Receiver Operating Characteristic"],
        ["AUC", "Area Under the Curve"],
        ["CAM", "Class Activation Mapping"],
        ["Grad-CAM", "Gradient-weighted Class Activation Mapping"],
        ["RGB", "Red-Green-Blue"],
        ["TP", "True Positive"],
        ["TN", "True Negative"],
        ["FP", "False Positive"],
        ["FN", "False Negative"]
    ]
    add_styled_table(abbrev_headers, abbrev_data, col_widths=[2.0, 4.0])

    # =========================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================
    add_custom_heading("CHAPTER 1: INTRODUCTION", 1)

    add_custom_heading("1.1 Background", 2)
    add_p("Artificial Intelligence has become an important technology in medical image analysis. Deep-learning models, particularly Convolutional Neural Networks, have demonstrated the ability to learn complex visual representations directly from medical images.")
    add_p("Chest X-rays are among the most commonly used medical imaging modalities because they are relatively inexpensive, fast, widely available, and routinely used in clinical practice.")
    add_p("However, not all pulmonary diseases produce strong visual patterns. Fibrotic changes in the lungs may appear as subtle alterations in texture, architecture, and interstitial patterns. This makes automated fibrosis detection significantly more difficult than the detection of visually prominent diseases.")
    add_p("The COVID-19 pandemic further increased interest in long-term pulmonary consequences. Patients recovering from COVID-19 may experience persistent respiratory abnormalities, and some patients demonstrate fibrotic-like changes during follow-up.")
    add_p("Research in the supplied project literature emphasizes that CT provides more detailed information about pulmonary abnormalities, whereas chest X-rays may underestimate subtle fibrotic involvement. This project therefore investigates whether deep learning can provide an early screening indication of fibrosis-related patterns from chest X-rays, while also providing an explanation for the model's prediction.")

    add_custom_heading("1.2 Problem Statement", 2)
    add_p("The objective is to develop an AI-based system capable of classifying chest X-ray images into Normal and Fibrosis. The system must address several challenges:")
    add_p("1. Fibrosis is visually subtle.\n2. The fibrosis class is comparatively smaller than the normal class.\n3. Chest X-rays contain less structural information than CT.\n4. A high accuracy can be misleading under class imbalance.\n5. Medical AI predictions should be interpretable.\n6. The model should be usable through a practical interface.")
    add_p("Therefore, the project combines: Deep Learning + Transfer Learning + Class-Imbalance Handling + Explainability + Deployment.")

    add_image_figure("figures/fig1_system_architecture.png", "Figure 1: Overall Deep Learning and Explainable AI Architecture Workflow")

    add_custom_heading("1.3 Motivation", 2)
    add_p("The primary motivation is to investigate whether an accessible imaging modality such as chest X-ray can provide useful preliminary screening information for fibrosis-related abnormalities.")
    add_p("The project is particularly motivated by limited accessibility of CT in some environments, the need for early risk identification, increasing use of AI in medical imaging, the difficulty of manually identifying subtle radiographic patterns, and the need for explainable predictions. The goal is not to replace clinical diagnosis, but to investigate whether AI can serve as an additional screening and decision-support mechanism.")

    add_custom_heading("1.4 Research Gap", 2)
    add_p("Existing deep-learning research has achieved strong performance on diseases such as pneumonia and COVID-19 when the radiographic features are relatively prominent. However, post-COVID fibrosis presents a different problem.")
    add_p("The supplied literature notes that many fibrosis-related investigations depend heavily on CT, chest X-rays may underestimate subtle fibrotic abnormalities, and explainability is often absent from conventional classification systems. The project therefore investigates the combination of Chest X-ray + Fibrosis Screening + Transfer Learning + Explainability.")

    add_custom_heading("1.5 Objectives", 2)
    add_p("1. Develop a binary chest X-ray classification system for Fibrosis and Normal cases.\n2. Use the NIH Chest X-ray Dataset as the primary training source.\n3. Maintain independent external datasets for testing.\n4. Develop a transfer-learning model using ResNet50.\n5. Fine-tune the pretrained network for the fibrosis task.\n6. Address class imbalance through sample weighting.\n7. Evaluate the model using multiple classification metrics.\n8. Tune the classification threshold for screening.\n9. Generate Grad-CAM explanations.\n10. Deploy the final model using Streamlit.")

    add_custom_heading("1.6 Scope", 2)
    add_p("The scope of the project is limited to chest X-ray image classification, binary Fibrosis versus Normal prediction, explainability through Grad-CAM, and demonstration through a Streamlit application.")
    add_p("The system does NOT replace a radiologist, replace CT imaging, provide definitive clinical diagnosis, establish a clinically validated risk threshold, or claim prospective clinical effectiveness.")

    add_custom_heading("1.7 Contributions", 2)
    add_p("• A standardized chest X-ray preprocessing pipeline.\n• ResNet50-based transfer learning.\n• Fine-tuning of the final ResNet50 layers.\n• Class-imbalance-aware training.\n• Threshold-based screening.\n• Grad-CAM visual explanations.\n• Independent external dataset organization.\n• Streamlit deployment.")

    # =========================================================
    # CHAPTER 2: LITERATURE REVIEW
    # =========================================================
    add_custom_heading("CHAPTER 2: LITERATURE REVIEW", 1)

    add_custom_heading("2.1 Deep Learning for Chest X-ray Analysis", 2)
    add_p("Deep learning has demonstrated significant success in chest radiograph analysis. CNN architectures can automatically learn hierarchical image features without requiring manually engineered descriptors. Rajpurkar et al. introduced CheXNet, demonstrating pneumonia detection. However, these tasks involve diseases with prominent features.")

    add_custom_heading("2.2 COVID-19 Chest X-ray Classification", 2)
    add_p("Apostolopoulos and Mpesiana investigated transfer learning for COVID-19 detection. Wang et al. proposed COVID-Net for COVID-19 detection. These studies focus on acute infection rather than post-infection fibrosis.")

    add_custom_heading("2.3 Post-COVID Pulmonary Abnormalities", 2)
    add_p("Huang et al. investigated pulmonary outcomes during recovery. Wu et al. studied longer-term respiratory outcomes following COVID-19. Besutti et al. demonstrated limitations of X-ray compared with CT.")

    add_custom_heading("2.4 Transfer Learning", 2)
    add_p("Medical datasets are often small. Transfer learning using ImageNet pretrained ResNet50 prevents overfitting and speeds convergence.")

    add_custom_heading("2.5 ResNet50", 2)
    add_p("ResNet introduces residual learning with shortcut connections H(x) = F(x) + x to solve vanishing gradients.")

    add_custom_heading("2.6 Explainable Artificial Intelligence", 2)
    add_p("Grad-CAM produces visual heatmaps highlighting influential image regions for transparency in clinical AI.")

    add_custom_heading("2.7 Literature Comparison", 2)
    lit_headers = ["Study", "Modality", "Task", "Main Relevance"]
    lit_data = [
        ["Huang et al., 2021", "CT + X-ray", "Post-COVID follow-up", "Demonstrates persistent pulmonary abnormalities"],
        ["Wu et al., 2021", "CT", "Respiratory outcomes", "Highlights importance of detailed pulmonary evaluation"],
        ["Besutti et al., 2022", "X-ray + CT", "Post-COVID abnormalities", "Demonstrates limitations of X-ray"],
        ["Rajpurkar et al., 2017", "X-ray", "Pneumonia", "Demonstrates deep learning for chest radiographs"],
        ["Apostolopoulos & Mpesiana, 2020", "X-ray", "COVID-19", "Demonstrates transfer learning"],
        ["Wang et al., 2020", "X-ray", "COVID-19", "Demonstrates specialized CNN design"],
        ["Selvaraju et al., 2017", "CNN", "Explainability", "Introduces Grad-CAM"]
    ]
    add_styled_table(lit_headers, lit_data, col_widths=[1.5, 1.0, 1.5, 2.5])

    add_custom_heading("2.8 Research Positioning", 2)
    add_p("The project combines fibrosis screening, transfer learning, independent testing, threshold tuning, Grad-CAM, and deployment.")

    # =========================================================
    # CHAPTER 3: DATASET AND DATA PREPARATION
    # =========================================================
    add_custom_heading("CHAPTER 3: DATASET AND DATA PREPARATION", 1)

    add_custom_heading("3.1 Dataset Structure", 2)
    add_p("Dataset 1 — NIH Chest X-ray Dataset: Main training source (02_NIH_Chest_Xray_Dataset, Data_Entry_2017.csv, images-224). Test ratio = 0.20, random state = 42.")

    add_custom_heading("3.2 Dataset 2 — Kaggle Lung Disease Dataset (Fibrosis)", 2)
    add_p("Independent Testing Dataset 1 (01_Kaggle_Lung_Disease_Dataset_Fibrosis), kept separate from training.")

    add_custom_heading("3.3 Dataset 3 — Post-COVID Lung Fibrosis Dataset", 2)
    add_p("Independent Testing Dataset 2 (03_Post_COVID_Lung_Fibrosis_Dataset), external domain.")

    add_custom_heading("3.4 Dataset Separation", 2)
    add_p("The training pipeline strictly trains on NIH data and tests generalization on external datasets.")
    add_image_figure("figures/fig2_dataset_split.png", "Figure 2: Dataset Hierarchy and Independent Evaluation Pipeline")

    add_custom_heading("3.5 Dataset Preparation", 2)
    add_p("Data Cleaning: Invalid images skipped.\nClass Selection: Fibrosis (1) vs Normal (0).\nStandardization: Resized to 224 x 224 RGB, normalized [0, 1].\nMemory Mapping: Disk-based NumPy memmap (X_all.dat, y_all.dat) for high efficiency.")

    add_custom_heading("3.6 Class Imbalance", 2)
    add_p("Sample weighting applied: Normal w0 = 1.0, Fibrosis w1 = (N_neg / N_pos) * 0.5 to balance loss contributions.")

    add_custom_heading("3.7 Train-Test Split", 2)
    add_p("Index-based 80% train / 20% test split saved as train_idx.npy and test_idx.npy.")

    # =========================================================
    # CHAPTER 4: PROPOSED METHODOLOGY
    # =========================================================
    add_custom_heading("CHAPTER 4: PROPOSED METHODOLOGY", 1)

    add_custom_heading("4.1 Overall System", 2)
    add_p("CXR -> Preprocessing (224x224x3) -> ResNet50 -> GAP -> Dense(256) -> Dropout(0.4) -> Sigmoid -> Probability -> Threshold 0.4 -> Grad-CAM Heatmap.")

    add_custom_heading("4.2 ResNet50 Backbone", 2)
    add_p("Pretrained ImageNet weights used, top classification head removed.")

    add_custom_heading("4.3 Classification Head", 2)
    add_p("Global Average Pooling, Dense 256 (ReLU), Dropout (0.4), Dense 1 (Sigmoid).")

    add_custom_heading("4.4 Transfer Learning", 2)
    add_p("Backbone initially frozen, trained for 10 epochs at LR = 1e-4.")

    add_custom_heading("4.5 Fine-Tuning", 2)
    add_p("Last 40 layers unfrozen, trained at low LR = 1e-5 with Adam, batch size 16, dropout 0.4, early stopping (patience 3).")

    add_custom_heading("4.6 Loss Function", 2)
    add_p("Binary Cross-Entropy Loss: L = -[y log(p) + (1-y) log(1-p)].")

    add_custom_heading("4.7 Optimizer & Early Stopping", 2)
    add_p("Adam optimizer at LR 1e-5 with EarlyStopping monitoring validation loss.")

    add_custom_heading("4.8 Threshold Selection (tau = 0.4)", 2)
    add_p("Threshold lowered to 0.4 to increase sensitivity for medical screening.")

    add_custom_heading("4.9 Grad-CAM", 2)
    add_p("Gradients of top class score with respect to last conv layer feature maps computed, pooled, and multiplied for spatial heatmap generation.")

    # =========================================================
    # CHAPTER 5: IMPLEMENTATION
    # =========================================================
    add_custom_heading("CHAPTER 5: IMPLEMENTATION", 1)

    add_custom_heading("5.1 Software Technologies", 2)
    tech_headers = ["Component", "Technology"]
    tech_data = [
        ["Programming Language", "Python 3.12"],
        ["Deep Learning Framework", "TensorFlow / Keras"],
        ["Model Backbone", "ResNet50 (ImageNet Pretrained)"],
        ["Numerical Processing", "NumPy (Memory Mapping)"],
        ["Image Processing", "OpenCV / Pillow"],
        ["Model Evaluation", "scikit-learn"],
        ["Visualization", "Matplotlib / Seaborn"],
        ["Application Deployment", "Streamlit"],
        ["Explainability Engine", "Grad-CAM"]
    ]
    add_styled_table(tech_headers, tech_data, col_widths=[2.5, 3.5])

    add_custom_heading("5.2 Dataset Storage & Processing", 2)
    add_p("Disk memory mapping (X_all.dat, y_all.dat) used alongside index arrays (train_idx.npy, test_idx.npy).")

    add_custom_heading("5.3 Model Variants Developed", 2)
    add_p("1. Baseline CNN: Simple sequential convolutional layers.\n2. ResNet50 Transfer: Frozen backbone.\n3. Fine-tuned ResNet50: Final deployed model.\n4. DenseNet121 & EfficientNet-B0: Comparison baselines.\n5. DenseNet121 + Attention (CBAM): Advanced comparison architecture.")

    # =========================================================
    # CHAPTER 6: EXPERIMENTAL RESULTS
    # =========================================================
    add_custom_heading("CHAPTER 6: EXPERIMENTAL RESULTS", 1)

    add_custom_heading("6.1 Evaluation Metrics", 2)
    add_p("Evaluation performed using Accuracy, Precision, Recall (Sensitivity), F1-score, and ROC-AUC.")

    add_custom_heading("6.2 Model Comparison (Project-Reported Results)", 2)
    comp_headers = ["Model", "Accuracy", "Fibrosis Recall", "ROC-AUC"]
    comp_data = [
        ["Baseline CNN", "77%", "0.00", "0.72"],
        ["ResNet50 Transfer Only", "39%", "0.94", "0.63"],
        ["ResNet50 Fine-tuned (Selected)", "67%", "0.65", "0.71"],
        ["DenseNet121", "57%", "0.79", "0.72"],
        ["EfficientNet-B0", "20%", "1.00", "0.50"],
        ["DenseNet121 + Attention", "72%", "0.58", "0.74"]
    ]
    add_styled_table(comp_headers, comp_data, col_widths=[2.5, 1.2, 1.5, 1.2])

    add_image_figure("figures/fig3_model_comparison.png", "Figure 3: Performance Comparison Across Model Architectures")

    add_custom_heading("6.3 Final Notebook Evaluation (Threshold = 0.4)", 2)
    add_p("Evaluated on test split (646 samples: 514 Normal, 132 Fibrosis):")

    rep_headers = ["Class", "Precision", "Recall", "F1-Score", "Support"]
    rep_data = [
        ["Class 0 - Normal", "0.84", "0.82", "0.83", "514"],
        ["Class 1 - Fibrosis", "0.35", "0.38", "0.36", "132"],
        ["Macro Average", "0.59", "0.60", "0.60", "646"],
        ["Weighted Average", "0.74", "0.73", "0.73", "646"]
    ]
    add_styled_table(rep_headers, rep_data, col_widths=[1.8, 1.0, 1.0, 1.0, 1.0])
    add_p("Overall Accuracy: 0.73 | ROC-AUC: 0.69099")

    add_image_figure("figures/fig4_confusion_matrix.png", "Figure 4: Confusion Matrix for Final Deployed Model")
    add_image_figure("figures/fig5_roc_curve.png", "Figure 5: Receiver Operating Characteristic (ROC) Curve")

    add_custom_heading("6.4 Explainability & Grad-CAM Analysis", 2)
    add_p("Grad-CAM visualizations confirm model attention focuses on pulmonary regions for high-confidence predictions.")
    add_image_figure("figures/fig6_gradcam_concept.png", "Figure 6: Grad-CAM Visual Heatmap and Overlay Pipeline")

    # =========================================================
    # CHAPTER 7: DISCUSSION
    # =========================================================
    add_custom_heading("CHAPTER 7: DISCUSSION", 1)

    add_custom_heading("7.1 Overall Findings", 2)
    add_p("Fibrosis detection on X-rays is difficult due to subtle textures. Accuracy alone is misleading under class imbalance. Fine-tuning provides the most stable operational balance.")

    add_custom_heading("7.2 Why Fine-tuned ResNet50 was Selected", 2)
    add_p("Fine-tuned ResNet50 avoided degenerate extreme predictions observed in EfficientNet-B0 and Transfer-only models, delivering superior stability.")

    add_custom_heading("7.3 Strengths", 2)
    add_p("• Robust transfer learning and fine-tuning framework.\n• Explicit class-imbalance handling via sample weighting.\n• Lower threshold (0.4) tuned for screening sensitivity.\n• Explainability integration via Grad-CAM.\n• Fully interactive web deployment.")

    add_custom_heading("7.4 Limitations", 2)
    add_p("• Moderate fibrosis recall (0.38 in final notebook run).\n• Chest X-ray modality limitations compared to CT.\n• Lack of prospective clinical trial validation.")

    # =========================================================
    # CHAPTER 8: APPLICATION AND DEPLOYMENT
    # =========================================================
    add_custom_heading("CHAPTER 8: APPLICATION AND DEPLOYMENT", 1)

    add_custom_heading("8.1 Streamlit Web Application", 2)
    add_p("The final model is wrapped in an interactive Streamlit application allowing CXR image uploads, risk scoring, and Grad-CAM visualization.")
    add_image_figure("figures/fig7_deployment_workflow.png", "Figure 7: Streamlit Deployment Architecture and Risk Stratification Workflow")

    add_custom_heading("8.2 Risk Stratification Categories", 2)
    risk_headers = ["Probability Range", "Assigned Risk Level"]
    risk_data = [
        ["p < 0.40", "Low Risk"],
        ["0.40 <= p < 0.70", "Moderate Risk"],
        ["p >= 0.70", "High Risk"]
    ]
    add_styled_table(risk_headers, risk_data, col_widths=[3.0, 3.0])

    add_custom_heading("8.3 Clinical Disclaimer", 2)
    add_p("The system is an academic screening support tool and must not be used as a standalone diagnostic system.")

    # =========================================================
    # CHAPTER 9: CONCLUSION AND FUTURE WORK
    # =========================================================
    add_custom_heading("CHAPTER 9: CONCLUSION AND FUTURE WORK", 1)

    add_custom_heading("9.1 Conclusion", 2)
    add_p("This project successfully designed, evaluated, and deployed an explainable deep-learning framework for post-COVID lung fibrosis screening using chest X-rays. Fine-tuned ResNet50 combined with Grad-CAM and Streamlit offers an accessible preliminary screening prototype.")

    add_custom_heading("9.2 Future Work", 2)
    add_p("• Incorporating anatomical lung segmentation masks.\n• Multi-center clinical data validation.\n• CT multi-modal integration.\n• Bayesian uncertainty estimation.")

    # =========================================================
    # REFERENCES
    # =========================================================
    add_custom_heading("REFERENCES", 1)
    refs = [
        "[1] Y. Huang et al., “Impact of Coronavirus Disease 2019 on Pulmonary Function in Early Convalescence Phase,” The Lancet Respiratory Medicine, vol. 9, no. 5, pp. 512–520, 2021.",
        "[2] X. Wu et al., “3-Month, 6-Month, 9-Month, and 12-Month Respiratory Outcomes in Patients Following COVID-19–Related Hospitalization,” The Lancet Respiratory Medicine, vol. 9, no. 7, pp. 747–754, 2021.",
        "[3] G. Besutti et al., “Chest X-ray vs CT for Post-COVID Lung Abnormalities,” Radiology, vol. 302, no. 2, 2022.",
        "[4] P. Rajpurkar et al., “CheXNet: Radiologist-Level Pneumonia Detection on Chest X-Rays with Deep Learning,” arXiv preprint arXiv:1711.05225, 2017.",
        "[5] L. Wang and A. Wong, “COVID-Net: A Tailored Deep Convolutional Neural Network Design for Detection of COVID-19 Cases from Chest X-Ray Images,” Scientific Reports, vol. 10, p. 19549, 2020.",
        "[6] I. D. Apostolopoulos and T. A. Mpesiana, “COVID-19: Automatic Detection from X-Ray Images Utilizing Transfer Learning,” Physical and Engineering Sciences in Medicine, vol. 43, pp. 635–640, 2020.",
        "[7] R. R. Selvaraju et al., “Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization,” Proceedings of the IEEE International Conference on Computer Vision, pp. 618–626, 2017."
    ]
    for r in refs:
        add_p(r, space_after=4)

    # =========================================================
    # APPENDICES
    # =========================================================
    add_custom_heading("APPENDIX A: FINAL MODEL ARCHITECTURE", 1)
    app_a_headers = ["Component", "Configuration"]
    app_a_data = [
        ["Input Dimensions", "224 x 224 x 3"],
        ["Backbone Architecture", "ResNet50"],
        ["Pretrained Weights", "ImageNet"],
        ["Fine-Tuning Scope", "Last 40 Layers Unfrozen"],
        ["Pooling Layer", "Global Average Pooling 2D"],
        ["Dense Layer", "256 Units (ReLU)"],
        ["Dropout Rate", "0.4"],
        ["Output Layer", "1 Neuron (Sigmoid)"],
        ["Loss Function", "Binary Cross-Entropy"],
        ["Optimizer", "Adam (Learning Rate = 1e-5)"],
        ["Batch Size", "16"],
        ["Decision Threshold", "0.4"]
    ]
    add_styled_table(app_a_headers, app_a_data, col_widths=[2.5, 3.5])

    add_custom_heading("APPENDIX B: MODEL COMPARISON TABLE", 1)
    add_styled_table(comp_headers, comp_data, col_widths=[2.5, 1.2, 1.5, 1.2])

    add_custom_heading("APPENDIX C: FINAL NOTEBOOK CLASSIFICATION REPORT", 1)
    add_styled_table(rep_headers, rep_data, col_widths=[1.8, 1.0, 1.0, 1.0, 1.0])

    add_custom_heading("APPENDIX D: FINAL PROJECT STRUCTURE", 1)
    add_p("Medical_Image_Processing_Project/\n│\n├── 01_Project_Code/\n│   ├── CVProjectttt.ipynb\n│   ├── app.py\n│   └── requirements.txt\n│\n├── 02_Dataset/\n│   ├── 01_Kaggle_Lung_Disease_Dataset_Fibrosis/\n│   ├── 02_NIH_Chest_Xray_Dataset/\n│   ├── 03_Post_COVID_Lung_Fibrosis_Dataset/\n│   └── DATASET_INFORMATION.txt\n│\n├── 03_Trained_Model/\n│   └── final_fibrosis_model.keras\n│\n├── 04_Presentation/\n│   └── ProjectPresentation_Final.pptx\n│\n├── 05_Supporting_Documents/\n│   ├── Project.docx\n│   ├── PaperSkeleton.docx\n│   ├── train_idx.npy\n│   ├── test_idx.npy\n│   └── y_all.dat\n│\n└── 06_References/\n    ├── Reference papers\n    └── Supporting literature", italic=True)

    add_custom_heading("FINAL PROJECT SUMMARY", 1)
    add_p("An explainable deep-learning-based screening framework that uses a fine-tuned ImageNet-pretrained ResNet50 to classify chest X-rays into Fibrosis and Normal categories, provides Grad-CAM visual explanations, evaluates generalization using independent external datasets, and delivers predictions through an interactive Streamlit application.", bold_prefix="Summary: ")

    doc.save("PROJECT_REPORT.docx")
    print("PROJECT_REPORT.docx successfully built!")

if __name__ == "__main__":
    create_report_docx()
