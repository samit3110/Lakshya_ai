import base64
import io
import asyncio
import re
from flask import Flask, request, jsonify, render_template
from groq import Groq
import edge_tts

app = Flask(__name__)

# Initialize Groq Client
client = Groq(
    api_key="your api key"
)

# KNOWLEDGE BASE WITH FULL SPECIFICATIONS
EXPANDED_KNOWLEDGE_BASE = """
LAKSHYA 2047 BUILDING OVERVIEW:
Lakshya 2047 is Parul University's premium, state-of-the-art multidisciplinary research and skill development hub. It is designed to bridge academia with industry 4.0 standards, housing specialized advanced laboratories powered by global tech giants. The building features cutting-edge infrastructure, high-speed campus networking, and industry-modeled environments to ensure students gain hands-on, job-ready engineering and technology experience.

GROUND FLOOR LABS (ADVANCED ENGINEERING & CORPORATE COLLABORATIONS):
- GF-01: NVIDIA Artificial Intelligence & Deep Learning Lab:
  * Hardware Specs: Equipped with 30+ high-end workstations powered by NVIDIA RTX Tensor Core GPUs and enterprise-grade processing units.
  * Specialization: Focused on Deep Learning, Neural Networks, Computer Vision, and Generative AI.
  * Student Benefits: Students train on industry-standard datasets, developing autonomous systems, predictive models, and AI algorithms directly applicable to global tech roles.
  
- GF-02: Cisco Networking & Advanced Communication Lab:
  * Hardware Specs: Features enterprise-grade Cisco routers, multi-layer switches, hardware firewalls, and network simulation racks.
  * Specialization: Advanced Network Architecture, Cyber Security frameworks, and Cloud Infrastructure management.
  * Student Benefits: Prepares students directly for CCNA/CCNP global certifications, teaching them how to design, secure, and maintain enterprise internet routing infrastructures.

- GF-03 & GF-06: ABB Industrial Automation Labs (Lab 1 & Lab 2):
  * Hardware Specs: Real-world ABB industrial robotic arms, programmable logic controllers (PLCs), and human-machine interface (HMI) panels.
  * Specialization: Robotic programming, assembly line automation, and smart manufacturing systems.
  * Student Benefits: Provides mechanical, electrical, and mechatronics students with rare, hands-on experience programming heavy machinery used in modern automated factories worldwide.

- GF-04: Industrial Drives & Control Lab:
  * Specs: Equipped with heavy-duty variable frequency drives (VFDs), AC/DC motor control centers, and power electronics diagnostic kits.
  * Focus: Efficient energy management and motor control systems for large manufacturing sectors.

- GF-04-A: Home Automation & Smart Systems Lab:
  * Specs: Features IoT-enabled smart appliances, microcontrollers, automated lighting, and sensor grids.
  * Focus: Designing smart city architectures, internet-of-things (IoT) ecosystems, and modern ambient intelligence.

- GF-05: PLC & SCADA Simulation Lab:
  * Specs: Outfitted with industrial monitoring software, logic control arrays, and supervisory data acquisition hubs.
  * Focus: Designing safety systems and master control interfaces for electrical grids and chemical processing plants.

- GF-08: AR/VR (Augmented & Virtual Reality) Immersive Lab:
  * Hardware Specs: Meta Quest and HTC Vive VR headsets, high-fidelity tracking sensors, and dedicated graphics development rigs.
  * Specialization: 3D spatial computing, immersive simulation building, and virtual asset creation.
  * Focus: Preparing students for game development, virtual medical simulations, and meta-universe software engineering.

NON-SPECIALIZED MULTI-DISCIPLINARY COMPUTING LABS (GROUND FLOOR):
- GF-07: Microsoft Cloud Computing & Software Lab (Advanced software development platforms).
- GF-11: ANSYS Engineering Simulation Lab (Structural, thermal, and fluid dynamics stress testing software).
- GF-12: Adobe Digital Design & Content Creation Lab (UI/UX design, visual computing, and digital media suites).
- GF-13: Autodesk CAD/CAM Design Lab (3D engineering modeling, architectural blueprinting, and industrial prototyping).
- GF-14: VLSI Electronic Design Lab (Micro-chip architecture design and semiconductor testing equipment).
- GF-15: AWS (Amazon Web Services) Devops Lab (Cloud architecture design and serverless system deployments).
- GF-16: Apple iOS App Development Lab (Equipped with Apple Mac workstations for native Swift app programming).

FIRST FLOOR LABS (DRONES, PROTOTYPING & FUTURE TECH):
- 101: RPTO (Remote Pilot Training Organization) Operation Setup Lab: Certified facility mapping out legal drone pilot procedures and flight line communications.
- 102: Drone Technician & Unmanned Aerial Vehicle (UAV) Lab: Direct structural maintenance, motor assembly, and electronic speed controller calibration setups for industrial drones.
- 103: Drone Battery System Repair & Power Management Lab: Specializes in Lithium-Polymer (LiPo) power safe diagnostics, high-capacity battery balancing, and cell testing.
- 104: Prototyping Zone: Open-access maker space featuring multi-material 3D printers, laser cutters, and rapid layout equipment.
- 105: Material Synthesis Zone: Physical-chemical workspace for compound structural analysis and innovative engineering material creation.
- 106 & 107: Major & Minor Machine Zones: Heavy and light-duty computer-numerical-control (CNC) lathes, drilling centers, and milling equipment for custom manufacturing.
- 110: Mind Lab: Advanced collaborative space dedicated to design-thinking, concept brainstorming, and tech startup planning.

MANAGEMENT & OPERATIONS PARTNERS:
-  Lakshya 2047 Building Manager: Located on the Third Floor. Controls day-to-day facilities and handles premium Global Certification Framework (GCF) Training coordination.
- Ethnotech Academy Representative: Stationed in the CFS Office (Campus Manager Office) inside the Ground Floor Board Room (GF-10). They actively manage corporate training curriculum and direct placement support programs.
- Parul University: A massive 250-acre private university boasting a prestigious NAAC A++ accreditation level, located in Vadodara, Gujarat.
- NSDC (National Skill Development Corporation): Working under the Ministry of Skill Development and Entrepreneurship to align lab training directly with national employment demands.

LEADERSHIP & INAUGURATION:
- Dr. Jitendra Singh (Union Minister of State for Science and Technology, Earth Sciences, and PMO) formally inaugurated this advanced building on May 8, 2026.
- University Leadership: Dr. Devanshu Patel (President), Dr. Parul Patel (Vice President), Dr. Geetika Madan Patel (Vice President & Medical Director), and Dr. Komal Patel (Vice President & Managing Trustee).
"what is lakshya 2047": "Lakshya 2047 is a state-of-the-art skill development and innovation center established to provide industry-oriented education, hands-on training, advanced laboratories, and research facilities for students.",
    "when was lakshya 2047 inaugurated": "Lakshya 2047 was inaugurated on 8 May 2026.",
    "who inaugurated lakshya 2047": "Lakshya 2047 was inaugurated by Dr. Jitendra Singh.",
    "who is dr jitendra singh": "Dr. Jitendra Singh is an Indian physician and politician serving as the 18th Minister of Science and Technology and Minister of Earth Sciences since 2024.",
    "who are the partners of lakshya 2047": "Lakshya 2047 has been established in partnership with Parul University, NSDC, and Ethnotech Academy.",

    "tell me about parul university": "Parul University is a premier private university located in Vadodara, Gujarat. It was established in 2015 and is known for its 250-acre campus, NAAC A++ accreditation, innovation, research, and industry-oriented education.",
    "what is nsdc": "The National Skill Development Corporation is a Public Private Partnership under the Ministry of Skill Development and Entrepreneurship, Government of India.",
    "what is ethnotech academy": "Ethnotech Academy is a Bengaluru-based skill development company established in 2013 that partners with educational institutions across India.",

    "how many floors are there in lakshya 2047": "Lakshya 2047 is a five-floor building.",
    "how many labs are on the ground floor": "The Ground Floor contains 14 laboratories, the Board Room, and the CFS Office.",
    "where is the board room": "The Board Room is located on the Ground Floor as GF-10.",
    "what is the board room used for": "The Board Room is used for meetings, presentations, conferences, planning sessions, and administrative discussions.",
    "where is the cfs office": "The CFS Office is located on the Ground Floor.",
    "who works in the cfs office": "The Campus Manager works in the CFS Office and manages GCF Training activities.",

    "which labs are on the right side of the ground floor": "The right side contains NVIDIA Lab, Cisco Lab, ABB Lab-1, Industrial Drives and Control Lab, Home Automation Lab, PLC and SCADA Lab, ABB Lab-2, Microsoft Lab, and AR VR Lab.",
    "which labs are on the left side of the ground floor": "The left side contains ANSYS Lab, Adobe Lab, Autodesk Lab, VLSI Lab, AWS Lab, and Apple Lab.",

    "what is nvidia lab": "The NVIDIA Lab focuses on Artificial Intelligence, Deep Learning, GPU Computing, Robotics, Computer Vision, and High Performance Computing.",
    "what is cisco lab": "The Cisco Lab provides training in networking, routing, switching, cybersecurity, IoT networking, and enterprise network configuration.",
    "what is abb lab 1": "ABB Lab 1 focuses on industrial robotics, automation systems, smart manufacturing, and robot programming.",
    "what is industrial drives and control lab": "The Industrial Drives and Control Lab provides training in PLCs, motor control, industrial control panels, IoT modules, heavy-duty motors, and automation systems.",
    "what is home automation lab": "The Home Automation Lab focuses on IoT and Smart Home Automation using ESP32, STM32, Zigbee, Z-Wave, Wi-Fi, Home Assistant, and Docker.",
    "what is plc and scada lab": "The PLC and SCADA Lab provides practical training in PLC programming, SCADA software, process automation, industrial logic development, and plant monitoring.",
    "what is abb lab 2": "ABB Lab 2 focuses on robotics, industrial automation, simulation technologies, laboratory automation, and data management systems.",
    "what is microsoft lab": "The Microsoft Lab supports Artificial Intelligence, Azure Cloud Computing, Azure Lab Services, Virtual Machines, software development, and hackathon projects.",
    "what is ar vr lab": "The AR VR Lab is equipped with Meta Quest headsets, motion sensors, Unity, and Blender for immersive learning and application development.",
    "what is ansys lab": "The ANSYS Lab specializes in Finite Element Analysis, Computational Fluid Dynamics, Thermal Analysis, and Electromagnetic Simulation.",
    "what is adobe lab": "The Adobe Lab supports technology previews, developer labs, creative software, multimedia design, and corporate research.",
    "what is autodesk lab": "The Autodesk Lab focuses on CAD design, product design, digital manufacturing, workforce readiness, and AI applications.",
    "what is vlsi lab": "The VLSI Lab is dedicated to designing, simulating, testing, and prototyping integrated circuits and microchips.",
    "what is aws lab": "The AWS Lab provides hands-on cloud computing experience with AWS services, cloud architecture, certification preparation, and AWS console management.",
    "what is apple lab": "The Apple Lab provides training in Swift Programming, Xcode, iOS Development, and macOS Development using iMacs and MacBooks.",

    "what is room 101": "Room 101 is the RPTO Operation Setup Lab used for commercial drone pilot training.",
    "what is room 102": "Room 102 is the Drone Technician Lab.",
    "what is room 103": "Room 103 is the Drone Battery System Repair Lab.",
    "what is room 104": "Room 104 is the Prototyping Zone.",
    "what is room 105": "Room 105 is the Material Synthesis Zone.",
    "what is room 106": "Room 106 is the Major Machine Zone.",
    "what is room 107": "Room 107 is the Minor Machine Zone.",
    "what is room 108": "Room 108 is the Activity Room.",
    "what is room 109": "Room 109 is the Staff Room.",
    "what is room 110": "Room 110 is the Mind Lab.",
   

    "where is the seminar hall on first floor": "The First Floor Seminar Hall is Room 118.",
    "where is the seminar hall on second floor": "The Second Floor Seminar Hall is Room 216.",
    "where is the seminar hall on third floor": "The Third Floor Seminar Hall is Room 316.",
    "where is the seminar hall on fourth floor": "The Fourth Floor Seminar Hall is Room 416.",
    "where is the seminar hall on fifth floor": "The Fifth Floor Seminar Hall is Room 516.",
    "ground floor": "The Ground Floor contains 14 advanced laboratories, the Board Room GF-10, and the CFS Office. The labs include NVIDIA, Cisco, ABB Lab-1, Industrial Drives and Control Lab, Home Automation Lab, PLC and SCADA Lab, ABB Lab-2, Microsoft Lab, AR VR Lab, ANSYS Lab, Adobe Lab, Autodesk Lab, VLSI Lab, AWS Lab, and Apple Lab.",

  "first floor": "The First Floor contains specialized drone laboratories, innovation zones, an activity room, a staff room, classrooms 111 to 117, and Seminar Hall 118. Important rooms include RPTO Operation Setup Lab, Drone Technician Lab, Drone Battery System Repair Lab, Prototyping Zone, Material Synthesis Zone, Major Machine Zone, Minor Machine Zone, Activity Room, Staff Room, and Mind Lab.",

  "room 101": "Room 101 is the RPTO Operation Setup Lab. It trains students to become certified commercial drone pilots through flight simulation, drone assembly, practical flying, and commercial drone operations.",

  "room 102": "Room 102 is the Drone Technician Lab. Students learn UAV assembly, calibration, avionics integration, drone maintenance, PX4 flight controller tuning, and UAV programming.",

  "room 103": "Room 103 is the Drone Battery System Repair Lab. It focuses on Lithium Polymer and Lithium Ion batteries, diagnostics, maintenance, repair, and battery safety.",

  "room 104": "Room 104 is the Prototyping Zone used for innovation, rapid prototyping, electronic testing, product design, and AICTE IDEA Lab activities.",

  "room 105": "Room 105 is the Material Synthesis Zone where advanced materials, compounds, and nanomaterials are developed using specialized equipment.",

  "room 106": "Room 106 is the Major Machine Zone containing industrial machinery for fiber laser cutting, heavy fabrication, metal engraving, and manufacturing.",

  "room 107": "Room 107 is the Minor Machine Zone used for 3D printing, prototype development, custom enclosures, and light fabrication work.",

  "room 108": "Room 108 is the Activity Room used for workshops, collaborative activities, extracurricular events, and student engagement programs.",

  "room 109": "Room 109 is the First Floor Staff Room for faculty and staff members.",

  "room 110": "Room 110 is the Mind Lab dedicated to creativity, innovation, brainstorming, problem-solving, and advanced learning.",

  "room 118": "Room 118 is the First Floor Seminar Hall used for seminars, workshops, guest lectures, conferences, and student presentations.",

  "second floor": "The Second Floor is dedicated to classrooms 201 to 215, Staff Room 208, and Seminar Hall 216. It is used for academic lectures, technical training, workshops, faculty lectures, and skill development programs.",

  "room 208": "Room 208 is the Second Floor Staff Room used for meetings, lesson preparation, administration, and staff discussions.",

  "room 216": "Room 216 is the Second Floor Seminar Hall used for seminars, guest lectures, workshops, conferences, and training programs.",

  "third floor": "The Third Floor contains classrooms 301 to 315, Staff Room 308, Seminar Hall 316, and the Lakshya 2047 Manager Office. It supports academic teaching, certification programs, workshops, and skill development training.",

  "room 308": "Room 308 is the Third Floor Staff Room used for faculty coordination, meetings, academic planning, and administration.",

  "room 316": "Room 316 is the Third Floor Seminar Hall used for seminars, technical presentations, industry expert sessions, workshops, and conferences.",

  "lakshya manager office": "The Lakshya 2047 Manager Office is located on the Third Floor. The manager supervises building operations, laboratories, GCF training activities, and administrative functions.",

  "fourth floor": "The Fourth Floor contains classrooms 401 to 415, Staff Room 408, and Seminar Hall 416. It supports academic classes, technical training, workshops, certification courses, and skill development programs.",

  "room 408": "Room 408 is the Fourth Floor Staff Room used for faculty meetings, lesson planning, administration, and staff coordination.",

  "room 416": "Room 416 is the Fourth Floor Seminar Hall used for seminars, workshops, conferences, guest lectures, technical events, and student presentations.",

  "fifth floor": "The Fifth Floor contains classrooms 501 to 515, Staff Room 508, and Seminar Hall 516. It is used for academic learning, technical courses, certification programs, workshops, and practical sessions.",

  "room 508": "Room 508 is the Fifth Floor Staff Room used for faculty coordination, administration, lesson preparation, and meetings.",

  "room 516": "Room 516 is the Fifth Floor Seminar Hall used for seminars, conferences, technical workshops, industry expert sessions, guest lectures, student presentations, and academic events.",

  "building summary": "Lakshya 2047 is a five-floor innovation and skill development center. The Ground Floor contains advanced laboratories and administrative facilities. The First Floor contains drone labs and innovation zones. The Second, Third, Fourth, and Fifth Floors contain classrooms, staff rooms, and seminar halls. The building supports industry-oriented education, research, innovation, workshops, and skill development programs.",
  "who is the lakshya manager": "Divyesh Hariyani is a Manager - Center for Future Skills (cfs) & Assistant Professor at Parul Institute of Engineering and Technology",
  "who is the manager of cfs": "Divyesh Hariyani is a Manager - Center for Future Skills (cfs) & Assistant Professor at Parul Institute of Engineering and Technology",
  "who is the manger of cfs": "Divyesh Hariyani is a Manager - Center for Future Skills (cfs) & Assistant Professor at Parul Institute of Engineering and Technology",
  "manager of cfs": "Divyesh Hariyani is a Manager - Center for Future Skills (cfs) & Assistant Professor at Parul Institute of Engineering and Technology",
  "manger of cfs": "Divyesh Hariyani is a Manager - Center for Future Skills (cfs) & Assistant Professor at Parul Institute of Engineering and Technology",
  "cfs manager": "Divyesh Hariyani is a Manager - Center for Future Skills (cfs) & Assistant Professor at Parul Institute of Engineering and Technology",
  "cfs manger": "Divyesh Hariyani is a Manager - Center for Future Skills (cfs) & Assistant Professor at Parul Institute of Engineering and Technology",
  PARUL UNIVERSITY PRESIDENT DR.DEVANSHU PATEL
The President of Parul University is Dr. Devanshu Patel. He is a medical doctor by training and a dynamic edupreneur who has rapidly expanded the university. Under his leadership, the institution in Vadodara, Gujarat, has grown from housing 4,000 students to a massive global campus with over 70,000 learners.

PARUL UNIVERSITY VICE PRESIDENT Parul University has three Vice Presidents, each overseeing a specific domain:
1.Dr. Parul Patel: Vice President of Student Affairs and General Administration.
Dr. Parul Patel is the Vice President of Student Affairs and General Administration, as well as Chair of the Admissions Committee at Parul University in Vadodara, Gujarat. She is the founding figure for whom the university and PASM Trust are named.
2.Dr. Geetika Madan Patel: Vice President of Quality, Research, and Health Sciences.
Dr. Geetika Madan Patel is the Vice President of Quality, Research, and Health Sciences at Parul University in Vadodara, Gujarat. She also serves as the Medical Director for Parul Sevashram Hospital and the Managing Trustee of New Era Senior Secondary School.
3.Dr. Komal Patel: Vice President of Medical and Paramedical Health Sciences.Dr. Komal Patel is a vice president of medical and paramedical health sciences and medical director at 
Parul University
 in Vadodara, Gujarat. She also serves as a managing trustee of the Parul Arogya Seva Mandal (PSAM) Trust, Parul Sevashram Hospital and director of Parul Pharmaceuticals Pvt
 
"In firsts floor there are also 8 lab 101,102,103,104,105,106,107,110.
101= RPTO OPERATION SETUP LAB An RPTO (Remote Pilot Training Organization) setup lab is a specialized facility designed to meet India's Directorate General of Civil Aviation (DGCA) norms. It trains students to become certified commercial drone pilots, offering a blend of flight simulation, drone assembly, and practical piloting

102= DRONE TECHNICIAN LAB A Drone Technician Lab is a specialized training and prototyping workspace dedicated to the assembly, calibration, maintenance, and programming of Unmanned Aerial Vehicles (UAVs). These facilities provide hands-on experience in electronics soldering, avionics integration, BLDC motor diagnostics, flight controller (e.g., PX4) tuning, and real-world safety procedures

103= DRONE BATTERY SYSTEM REPAIR LAB A Drone Battery System Repair Lab is a specialized facility focused on the diagnosis, maintenance, cell replacement, and safe management of lithium-polymer (LiPo) and lithium-ion (Li-ion) UAV batteries. These labs prevent unexpected flight hazards and extend the life of expensive drone fleets.

104= PROTOTYPING ZONE A Prototyping Zone is a dedicated physical or digital workspace—such as an AICTE IDEA Lab or an interactive design workspace—equipped with tools for rapid product fabrication, electronic testing, and iteration. It acts as an adjustable infrastructure allowing designers to physically build, test, and refine early product concepts before scaling to mass manufacturing

105= MATERIAL SYNTHESIS ZONE A Material Synthesis Zone refers to a dedicated laboratory or reactor area where raw elements are combined and processed into new compounds, nanomaterials, or crystals. These zones are strictly compartmentalized into specialized areas—such as high-temperature heating chambers and processing reactors—to manage thermal loads and safety

106= MAJOR MACHINE ZONE The "Major Machine Zone" generally refers to fiber laser cutting zones or localized heavy-duty machining centers. These specialized equipment areas use industrial laser beam technology to execute heavy fabrication, high-precision subtractive cutting, and metal engraving

107= MINOR MACHINE ZONE The term "Miner Machine Zone" likely refers to 3D-printed brackets, mounts, or custom enclosures designed for cryptocurrency mining hardware (like Bitcoin or GPU rigs). It can also represent digital models of mining sites or "print farms".

110= MIND LAB

IN FIRST FLOOR 108 WE ALSO HAVE ONE ACTIVITY ROOM
AND 109 STAFF ROOM

1 FLOOR
111,112,113,114,115,116,117 ARE CLASSROOM 118 IS SEMINAR

2 FLOOR
201,202,203,204,205,206,207,209,210,211,212,213,214,215 ARE CLASSROOM
208 STAFF ROOM
216 SEMINAR HALL

3 FLOOR
301,302,303,304,305,306,307,309,310,311,312,313,314,315 ARE CLASSROOM
308 STAFF ROOM
316 SEMINAR HALL

4 FLOOR
401,402,403,404,405,406,407,409,410,411,412,413,414,415 ARE CLASSROOM
408 STAFF ROOM
416 SEMINAR HALL

5 FLOOR
501,502,503,504,505,506,507,509,510,511,512,513,514,515 ARE CLASSROOM
508 STAFF ROOM
516 SEMINAR HALL

WE HAVE 7 SPECIALIZATION LAB AND 7 UNSPECIALIZATION  LAB 
SPECIALIZATION LAB ARE
GF-01 NVIDIA LAB 
GF-02 CISCO LAB 
GF-03 ABB LAB-1 
GF-04 INDUSTRIAL DRIVES & CONTROL LAB / INSIDE THAT LAB WE HAVE ONE MORE LAB GF-04-A HOME AUTOMATION LAB 
GF-05 PLC & SCADA LAB 
GF-06 ABB LAB-2 
GF-08 AR/VR LAB
UNSPECIALIZATION LAB ARE
GF-07 MICROSOFT LAB 
GF-11 ANSYS LAB
GF-12 ADOBE LAB
GF-13 AUTODESK LAB
GF-14 VLSI LAB
GF-15 AWS LAB
GF-16 APPLE LAB

IN THIS BUILDING WE HAVE LAB
we have 14 lab in ground floor

LAB 1 TO 8 ARE IN THE RIGHT SIDE AND 11 TO 16 IN LEFT SIDE
right side lab
GF-01 NVIDIA LAB 
Gf-02 CISCO LAB 
GF-03 ABB LAB-1 
GF-04 INDUSTRIAL DRIVES & CONTROL LAB / INSIDE THAT LAB WE HAVE ONE MORE LAB GF-04-A HOME AUTOMATION LAB 
GF-05 PLC & SCADA LAB 
GF-06 ABB LAB-2 
GF-08 AR/VR LAB
GF-07 MICROSOFT LAB 

left side lab
GF-11 ANSYS LAB
GF-12 ADOBE LAB
GF-13 AUTODESK LAB
GF-14 VLSI LAB
GF-15 AWS LAB
GF-16 APPLE LAB

Mr. Prashaka Shukla is a Manager of Ethnotech Academy at Lakshya 2047.
He is responsible for the overall management and coordination of all laboratories located on the Ground Floor of the Lakshya 2047 building.

UI/UX Designer & Developer - Vedant Sakpal , Frontend Developer - Aniket Phapal, Backend Developer - Daksh Bhinde,Backend Developer- Sumit Kumar, AI Model Training & Development - Samit Patel
}
"""

CLEAN_SYSTEM_PROMPT = (
    "You are Jarvis, a strict informational terminal for the Lakshya 2047 building at Parul University.\n"
    "You must reply strictly in English.\n\n"
    "CRITICAL GROUNDING RULES:\n"
    "1. You have NO general knowledge. You do not know anything about the world outside the KNOWLEDGE BASE block provided below.\n"
    "2. You are completely forbidden from inventing, estimating, or hallucinating details. If a specification, feature, lab, size, or number is not explicitly written in the text below, it does not exist.\n"
    "3. Do NOT say there are 'lecture halls', '25 classrooms', 'dormitories', or 'security features' because those are NOT listed in the text.\n"
    "4. For greetings/small talk (e.g., 'hi', 'hello', 'who are you'), reply with exactly this sentence: 'Hello, I am Jarvis, your technical guide for the Lakshya 2047 facility.'\n"
    "5. For any query that cannot be answered with 100% certainty using only the text below, you must reply with exactly: 'I am not authorized to provide that information, sir.' Do not add any extra words or pleasantries.\n\n"
    "DATA SOURCE:\n"
    f"{EXPANDED_KNOWLEDGE_BASE}"
    # "You are Jarvis, the elite guide for the Lakshya 2047 building at Parul University.\n"
    # "You must reply strictly in English.\n\n"
    # "RESPONSE RULES:\n"
    # "1. Provide a direct, natural, and comprehensive response based on the Knowledge Base. Use proper spacing and clean structural layout.\n"
    # "2. If a parent or visitor asks about a lab or specification, provide full complete details. Do not summarize or omit crucial data.\n"
    # "3. Do not use conversational fillers or code block tags.\n\n"
    "CRITICAL BOUNDARY RULES:\n"
    "1. Base your knowledge ONLY on the provided KNOWLEDGE BASE text.\n"
    "2. If out of scope, politely mention that you are configured specifically to assist with the technical infrastructure of the Lakshya 2047 facility."
    "3. If the question is normal, give a response around 20-30 words and if asked for details, give response around 150 words."
    "4. Don't add any extra details. Use the information which is provided in EXPANDED_KNOWLEDGE_BASE."
    "5. Use ONLY information from the Knowledge Base."
)

async def generate_edge_tts_bytes(text):
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

def prepare_full_voice_text(text):
    clean_text = re.sub(r'[\*\-\#\_\`\•]', ' ', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/text-chat', methods=['POST'])
def text_chat():
    data = request.get_json() or {}
    user_text = data.get("text", "").strip()
    
    if not user_text:
        return jsonify({"error": "No text message provided"}), 400
        
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": CLEAN_SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )
        ai_text_reply = chat_completion.choices[0].message.content.strip()

        audio_text = prepare_full_voice_text(ai_text_reply)

        audio_base64 = ""
        if audio_text:
            try:
                out_audio_bytes = asyncio.run(generate_edge_tts_bytes(audio_text))
                audio_base64 = base64.b64encode(out_audio_bytes).decode('utf-8')
            except Exception as tts_err:
                print(f"TTS Failure: {tts_err}")

        return jsonify({
            "user_text": user_text,
            "ai_text": ai_text_reply,
            "audio_base64": audio_base64
        })
    except Exception as e:
        print(f"=== TEXT ROUTE ERROR ===\n{str(e)}")
        return jsonify({"user_text": user_text, "ai_text": f"Error processing request: {str(e)}", "audio_base64": ""}), 200

@app.route('/api/voice-chat', methods=['POST'])
def voice_chat():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file received"}), 400
        
    audio_file = request.files['audio']
    audio_bytes = audio_file.read()

    try:
        transcription = client.audio.transcriptions.create(
            file=("user_voice.webm", io.BytesIO(audio_bytes)),
            model="whisper-large-v3",
            response_format="json"
        )
        user_text = transcription.text

        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": CLEAN_SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )
        ai_text_reply = chat_completion.choices[0].message.content.strip()

        audio_text = prepare_full_voice_text(ai_text_reply)

        audio_base64 = ""
        if audio_text:
            try:
                out_audio_bytes = asyncio.run(generate_edge_tts_bytes(audio_text))
                audio_base64 = base64.b64encode(out_audio_bytes).decode('utf-8')
            except Exception as tts_err:
                print(f"TTS Failure: {tts_err}")
        
        return jsonify({
            "user_text": user_text,
            "ai_text": ai_text_reply,
            "audio_base64": audio_base64
        })
    except Exception as e:
        print(f"=== VOICE ROUTE ERROR ===\n{str(e)}")
        return jsonify({"user_text": "Voice Request Received", "ai_text": f"Error parsing response stream: {str(e)}", "audio_base64": ""}), 200

if __name__ == '__main__':
    print("Mission Control Auto-Voice starting... Open http://127.0.0.1:5000 in your browser!")
    app.run(debug=True, port=5000)
