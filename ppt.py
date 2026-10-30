from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Set slide dimensions to widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definitions
    BG_COLOR = RGBColor(15, 23, 42)      # Deep Dark Blue/Slate
    CYAN_COLOR = RGBColor(6, 182, 212)   # High-tech Cyan
    WHITE_COLOR = RGBColor(255, 255, 255)
    MUTED_GRAY = RGBColor(156, 163, 175)
    SLATE_BOX_BG = RGBColor(30, 41, 59)  # Semi-dark slate for tiles

    def apply_dark_background(slide):
        """Fills the slide background with the deep slate color."""
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_slide_header(slide, title_text):
        """Adds a consistent styled title to content slides."""
        tx_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(11.83), Inches(1.0))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = WHITE_COLOR

    # ----------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # ----------------------------------------------------
    slide_1 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide_1)

    # Title & Subtitle text frame
    title_box = slide_1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.33), Inches(4.5))
    tf = title_box.text_frame
    tf.word_wrap = True

    p_title = tf.paragraphs[0]
    p_title.text = "AI-Based Gesture Controlled\nDrone Simulation"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(48)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE_COLOR
    p_title.alignment = PP_ALIGN.CENTER
    p_title.space_after = Pt(20)

    p_sub = tf.add_paragraph()
    p_sub.text = "CDAC Drone Department Internship"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(22)
    p_sub.font.color.rgb = CYAN_COLOR
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_after = Pt(10)

    p_presenter = tf.add_paragraph()
    p_presenter.text = "Presented By: Ishant Garg"
    p_presenter.font.name = "Arial"
    p_presenter.font.size = Pt(18)
    p_presenter.font.color.rgb = MUTED_GRAY
    p_presenter.alignment = PP_ALIGN.CENTER
    p_presenter.space_after = Pt(30)

    # Tech Stack Box
    p_tech = tf.add_paragraph()
    p_tech.text = "Tech Stack: PX4 Autopilot | Gazebo Harmonic | Ubuntu (WSL2) | MAVLink & MAVSDK | OpenCV | AI/ML"
    p_tech.font.name = "Arial"
    p_tech.font.size = Pt(14)
    p_tech.font.bold = True
    p_tech.font.color.rgb = CYAN_COLOR
    p_tech.alignment = PP_ALIGN.CENTER


    # ----------------------------------------------------
    # SLIDE 2: PROJECT OBJECTIVE
    # ----------------------------------------------------
    slide_2 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide_2)
    add_slide_header(slide_2, "Project Objective")

    # Column 1: Goal (Card style)
    shape_goal = slide_2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(1.8), Inches(5.6), Inches(4.5))
    shape_goal.fill.solid()
    shape_goal.fill.fore_color.rgb = SLATE_BOX_BG
    shape_goal.line.color.rgb = CYAN_COLOR
    shape_goal.line.width = Pt(1.5)
    
    tf_goal = shape_goal.text_frame
    tf_goal.word_wrap = True
    tf_goal.margin_left = tf_goal.margin_top = tf_goal.margin_right = tf_goal.margin_bottom = Inches(0.4)
    p_goal_title = tf_goal.paragraphs[0]
    p_goal_title.text = "The Main Goal"
    p_goal_title.font.name = "Arial"
    p_goal_title.font.size = Pt(24)
    p_goal_title.font.bold = True
    p_goal_title.font.color.rgb = CYAN_COLOR
    p_goal_title.space_after = Pt(20)

    p_goal_desc = tf_goal.add_paragraph()
    p_goal_desc.text = "Develop an AI-powered autonomous drone capable of understanding hand gestures and executing drone commands in a simulated environment before physical deployment."
    p_goal_desc.font.name = "Arial"
    p_goal_desc.font.size = Pt(18)
    p_goal_desc.font.color.rgb = WHITE_COLOR

    # Column 2: Objectives List
    shape_obj = slide_2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.98), Inches(1.8), Inches(5.6), Inches(4.5))
    shape_obj.fill.solid()
    shape_obj.fill.fore_color.rgb = SLATE_BOX_BG
    shape_obj.line.color.rgb = SLATE_BOX_BG # No border

    tf_obj = shape_obj.text_frame
    tf_obj.word_wrap = True
    tf_obj.margin_left = tf_obj.margin_top = tf_obj.margin_right = tf_obj.margin_bottom = Inches(0.4)
    
    p_obj_title = tf_obj.paragraphs[0]
    p_obj_title.text = "Key Objectives"
    p_obj_title.font.name = "Arial"
    p_obj_title.font.size = Pt(24)
    p_obj_title.font.bold = True
    p_obj_title.font.color.rgb = WHITE_COLOR
    p_obj_title.space_after = Pt(20)

    objectives = [
        "Create high-fidelity simulation environment",
        "Build stable PX4 flight control stack",
        "Integrate AI computer vision model (MediaPipe)",
        "Generate & validate robust flight commands",
        "Safely deploy on physical drone hardware"
    ]

    for obj in objectives:
        p_item = tf_obj.add_paragraph()
        p_item.text = f"•  {obj}"
        p_item.font.name = "Arial"
        p_item.font.size = Pt(16)
        p_item.font.color.rgb = MUTED_GRAY
        p_item.space_after = Pt(12)


    # ----------------------------------------------------
    # SLIDE 3: SYSTEM ARCHITECTURE
    # ----------------------------------------------------
    slide_3 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide_3)
    add_slide_header(slide_3, "System Architecture Flow")

    # We will build a visual pipeline using connected text boxes or arrows
    steps = [
        "Webcam Input",
        "OpenCV & MediaPipe Processing",
        "Gesture Recognition System",
        "Command Mapping Logic",
        "MAVSDK / MAVLink API",
        "PX4 Flight Controller",
        "Gazebo Physics Simulation"
    ]

    for i, step in enumerate(steps):
        top_pos = Inches(1.6 + (i * 0.72))
        
        # Draw Box
        box = slide_3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), top_pos, Inches(8.33), Inches(0.55))
        box.fill.solid()
        box.fill.fore_color.rgb = SLATE_BOX_BG
        box.line.color.rgb = CYAN_COLOR if i % 2 == 0 else MUTED_GRAY
        box.line.width = Pt(1.5)
        
        tf_box = box.text_frame
        tf_box.word_wrap = True
        p_step = tf_box.paragraphs[0]
        p_step.text = f"{i+1}. {step}"
        p_step.font.name = "Arial"
        p_step.font.size = Pt(16)
        p_step.font.bold = True
        p_step.font.color.rgb = WHITE_COLOR
        p_step.alignment = PP_ALIGN.CENTER


    # ----------------------------------------------------
    # SLIDE 4: COMPLETE WORKFLOW (PHASES)
    # ----------------------------------------------------
    slide_4 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide_4)
    add_slide_header(slide_4, "Project Development Phases")

    phases = [
        {"title": "Phase 1: Setup", "desc": "Configure Ubuntu in WSL2. Install PX4 Toolchain & Gazebo simulation suites."},
        {"title": "Phase 2: Simulation", "desc": "Spawn the custom quadcopter. Set up environment sensors & camera topics."},
        {"title": "Phase 3: AI Engine", "desc": "Implement hand gesture landmark tracking and mapping algorithms."},
        {"title": "Phase 4: Control", "desc": "Construct reliable MAVSDK Python bindings to convert gestures to controls."},
        {"title": "Phase 5: Deployment", "desc": "Export control loops to real companion computer on hardware flight controller."}
    ]

    for i, phase in enumerate(phases):
        left_pos = Inches(0.75 + (i * 2.4))
        
        # Visual Card for Phase
        card = slide_4.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(1.8), Inches(2.2), Inches(4.5))
        card.fill.solid()
        card.fill.fore_color.rgb = SLATE_BOX_BG
        card.line.color.rgb = CYAN_COLOR if i == 0 else MUTED_GRAY
        card.line.width = Pt(1.5)
        
        tf_card = card.text_frame
        tf_card.word_wrap = True
        tf_card.margin_left = tf_card.margin_top = tf_card.margin_right = tf_card.margin_bottom = Inches(0.2)
        
        p_title = tf_card.paragraphs[0]
        p_title.text = phase["title"]
        p_title.font.name = "Arial"
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = CYAN_COLOR
        p_title.space_after = Pt(15)
        
        p_desc = tf_card.add_paragraph()
        p_desc.text = phase["desc"]
        p_desc.font.name = "Arial"
        p_desc.font.size = Pt(13)
        p_desc.font.color.rgb = WHITE_COLOR


    # ----------------------------------------------------
    # SLIDE 5: CURRENT PROGRESS
    # ----------------------------------------------------
    slide_5 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide_5)
    add_slide_header(slide_5, "Development Progress & Obstacles")

    # Progress Column
    prog_card = slide_5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(1.8), Inches(5.6), Inches(4.5))
    prog_card.fill.solid()
    prog_card.fill.fore_color.rgb = SLATE_BOX_BG
    prog_card.line.color.rgb = RGBColor(16, 185, 129) # Emerald Green Border
    prog_card.line.width = Pt(1.5)

    tf_prog = prog_card.text_frame
    tf_prog.word_wrap = True
    tf_prog.margin_left = tf_prog.margin_top = tf_prog.margin_right = tf_prog.margin_bottom = Inches(0.3)
    
    p_prog_title = tf_prog.paragraphs[0]
    p_prog_title.text = "Completed Milestones"
    p_prog_title.font.name = "Arial"
    p_prog_title.font.size = Pt(22)
    p_prog_title.font.bold = True
    p_prog_title.font.color.rgb = RGBColor(16, 185, 129)
    p_prog_title.space_after = Pt(15)

    milestones = [
        "Ubuntu & WSL2 operational environment",
        "PX4 flight controller build success",
        "Successful PX4 SITL simulation",
        "Active local MAVLink telemetry stream",
        "Drone models spawning correctly inside simulation"
    ]
    for ms in milestones:
        p_ms = tf_prog.add_paragraph()
        p_ms.text = f"[✓]  {ms}"
        p_ms.font.name = "Arial"
        p_ms.font.size = Pt(14)
        p_ms.font.color.rgb = WHITE_COLOR
        p_ms.space_after = Pt(10)

    # Challenge Column
    chal_card = slide_5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.98), Inches(1.8), Inches(5.6), Inches(4.5))
    chal_card.fill.solid()
    chal_card.fill.fore_color.rgb = SLATE_BOX_BG
    chal_card.line.color.rgb = RGBColor(239, 68, 68) # Red Alert Border
    chal_card.line.width = Pt(1.5)

    tf_chal = chal_card.text_frame
    tf_chal.word_wrap = True
    tf_chal.margin_left = tf_chal.margin_top = tf_chal.margin_right = tf_chal.margin_bottom = Inches(0.3)
    
    p_chal_title = tf_chal.paragraphs[0]
    p_chal_title.text = "Current Challenge"
    p_chal_title.font.name = "Arial"
    p_chal_title.font.size = Pt(22)
    p_chal_title.font.bold = True
    p_chal_title.font.color.rgb = RGBColor(239, 68, 68)
    p_chal_title.space_after = Pt(15)

    p_chal_desc = tf_chal.add_paragraph()
    p_chal_desc.text = "Gazebo GUI Rendering Issue:\n\nRunning Windows 10 with WSL2 restricts default GUI pipeline access. The backend telemetry, simulation engines, and PX4 SITL function perfectly, but X-Server GUI configuration requires active debugging."
    p_chal_desc.font.name = "Arial"
    p_chal_desc.font.size = Pt(16)
    p_chal_desc.font.color.rgb = WHITE_COLOR


    # ----------------------------------------------------
    # SLIDE 6: FUTURE AI MODULES (Grid Layout)
    # ----------------------------------------------------
    slide_6 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide_6)
    add_slide_header(slide_6, "Future AI Control Modules")

    modules = [
        "Gesture Controlled Flight", "YOLO Object Detection",
        "Target/Human Tracking", "Vehicle Detection Engine",
        "Obstacle Avoidance System", "Autonomous Path Planning",
        "Smart Emergency Landing", "Adaptive Mission Logic"
    ]

    for idx, mod in enumerate(modules):
        row = idx // 4
        col = idx % 4
        
        left_pos = Inches(0.75 + (col * 3.0))
        top_pos = Inches(2.0 + (row * 2.2))
        
        card = slide_6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, Inches(2.8), Inches(1.8))
        card.fill.solid()
        card.fill.fore_color.rgb = SLATE_BOX_BG
        card.line.color.rgb = CYAN_COLOR
        card.line.width = Pt(1)
        
        tf_card = card.text_frame
        tf_card.word_wrap = True
        tf_card.margin_left = tf_card.margin_top = tf_card.margin_right = tf_card.margin_bottom = Inches(0.15)
        
        # Center align titles vertically and horizontally
        p = tf_card.paragraphs[0]
        p.text = mod
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = WHITE_COLOR
        p.alignment = PP_ALIGN.CENTER


    # ----------------------------------------------------
    # SLIDE 7: FUTURE ROADMAP
    # ----------------------------------------------------
    slide_7 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide_7)
    add_slide_header(slide_7, "Development Roadmap")

    steps = [
        "Environment Ready",
        "PX4 Core Config",
        "Simulate Vehicle",
        "Train AI CV System",
        "Gesture Decoder",
        "MAVSDK Binding",
        "Simulation Testing",
        "Real Deployment"
    ]

    # Map linear steps with arrows or connectors
    for i, step in enumerate(steps):
        # We will stagger them or put them in 2 elegant rows
        row = i // 4
        col = i % 4
        
        left_pos = Inches(0.75 + (col * 3.0))
        top_pos = Inches(2.0 + (row * 2.2))
        
        box = slide_7.shapes.add_shape(MSO_SHAPE.CHEVRON, left_pos, top_pos, Inches(2.8), Inches(1.5))
        box.fill.solid()
        box.fill.fore_color.rgb = SLATE_BOX_BG
        box.line.color.rgb = CYAN_COLOR if idx < 3 else MUTED_GRAY
        box.line.width = Pt(1)
        
        tf_box = box.text_frame
        tf_box.word_wrap = True
        
        p = tf_box.paragraphs[0]
        p.text = f"Step {i+1}\n\n{step}"
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = WHITE_COLOR
        p.alignment = PP_ALIGN.CENTER


    # ----------------------------------------------------
    # SLIDE 8: THANK YOU & CONCLUSION
    # ----------------------------------------------------
    slide_8 = prs.slides.add_slide(blank_layout)
    apply_dark_background(slide_8)

    # Main text box for Thank You
    ty_box = slide_8.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.33), Inches(4.5))
    tf_ty = ty_box.text_frame
    tf_ty.word_wrap = True

    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "Thank You!"
    p_ty.font.name = "Arial"
    p_ty.font.size = Pt(54)
    p_ty.font.bold = True
    p_ty.font.color.rgb = WHITE_COLOR
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.space_after = Pt(25)

    p_goal_re = tf_ty.add_paragraph()
    p_goal_re.text = "Questions & Feedback"
    p_goal_re.font.name = "Arial"
    p_goal_re.font.size = Pt(24)
    p_goal_re.font.bold = True
    p_goal_re.font.color.rgb = CYAN_COLOR
    p_goal_re.alignment = PP_ALIGN.CENTER
    p_goal_re.space_after = Pt(20)

    p_next = tf_ty.add_paragraph()
    p_next.text = "Next Target: Integrate full loop tracking with simulated drone feedback telemetry."
    p_next.font.name = "Arial"
    p_next.font.size = Pt(16)
    p_next.font.color.rgb = MUTED_GRAY
    p_next.alignment = PP_ALIGN.CENTER

    prs.save("Drone_Simulation_Presentation.pptx")
    print("Presentation successfully saved as 'Drone_Simulation_Presentation.pptx'")

if __name__ == "__main__":
    create_presentation()
    