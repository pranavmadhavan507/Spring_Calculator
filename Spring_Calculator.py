import customtkinter
import math
pi = math.pi

#Setup
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x800")
root.title("Spring Calculator")
 
frame = customtkinter.CTkFrame(master = root)
frame.pack(pady = 20, padx = 60, fill = "both", expand = "True")

#User Input
end_type_label = customtkinter.CTkLabel(master = frame, text = "End Type")
end_type_label.pack(pady = 5)
end_type_entry= customtkinter.CTkOptionMenu(master = frame, values = ["Seclect an End Type","Plain",
                                                                       "Plain and ground",
                                                                       "Squared or closed",
                                                                       "Squared and ground",],)
end_type_entry.pack()

material_label = customtkinter.CTkLabel(master = frame, text = "Material")
material_label.pack(pady = 5)
material_entry = customtkinter.CTkOptionMenu(master = frame,values = ["Seclect a material","Music wire (ASTM No. A228)",
                                                                       "Hard-drawn wire (ASTM No. A227)",
                                                                       "Chrome-vanadium wire (ASTM No. A232)",
                                                                       "Chrome-silicon wire (ASTM No. A401)",
                                                                       "302 stainless wire (ASTM No. A313)",
                                                                       "Phosphor-bronze wire (ASTM No. B159)"],)
material_entry.pack()

loading_label = customtkinter.CTkLabel(master = frame, text = "Loading Type")
loading_label.pack(pady = 5)
loading_entry = customtkinter.CTkOptionMenu(master = frame, values = ["Select a loading type", "Static", "Cyclic"])
loading_entry.pack()

load_max_label = customtkinter.CTkLabel(master = frame, text = "Max Load (lbf)")
load_max_label.pack(pady=5)
load_max_entry = customtkinter.CTkEntry(master = frame, width = 250, placeholder_text = "enter 0 for static load")
load_max_entry.pack()

load_min_label = customtkinter.CTkLabel(master = frame, text = "Min Load (lbf)")
load_min_label.pack(pady = 5)
load_min_entry = customtkinter.CTkEntry(master = frame, width = 250, placeholder_text="Enter 0 for static load")
load_min_entry.pack()

static_load_label = customtkinter.CTkLabel(master = frame, text = "Static Load (lbf)")
#static_load_label.pack(pady=5)
static_load_entry = customtkinter.CTkEntry(master = frame, width = 250, placeholder_text="Enter 0 for cyclic load")
#static_load_entry.pack(pady=5)

wire_d_label = customtkinter.CTkLabel(master = frame, text = "Wire Diameter (inches)")
wire_d_label.pack(pady = 5)
wire_d_entry = customtkinter.CTkEntry(master = frame, width = 250, placeholder_text="")
wire_d_entry.pack()

outer_d_label = customtkinter.CTkLabel(master = frame, text = "Outer Diameter (inches)")
outer_d_label.pack(pady = 5)
outer_d_entry = customtkinter.CTkEntry(master = frame, width = 250, placeholder_text="")
outer_d_entry.pack()

free_length_label = customtkinter.CTkLabel(master = frame, text = "Free Length (inches)")
free_length_label.pack(pady = 5)
free_length_entry = customtkinter.CTkEntry(master = frame, width = 250, placeholder_text="")
free_length_entry.pack()

solid_length_label = customtkinter.CTkLabel(master = frame, text = "Solid Length (inches)")
solid_length_label.pack(pady = 5)
solid_length_entry = customtkinter.CTkEntry(master = frame, width = 250, placeholder_text="")
solid_length_entry.pack()

#Function to convert user entry into usable values
def inputs():
    global end_type, material, wire_diameter, outer_diameter, free, solid, loading_type, maxload, minload, staticload
    end_type = end_values(end_type_entry.get()) #returns a number between 1 and 4 depending on the end type
    material = materials(material_entry.get()) #returns a number between 1 and 6 depending on the material 
    loading_type = load(loading_entry.get())
    maxload = float(load_max_entry.get())
    minload = float(load_min_entry.get())
    #staticload = float(static_load_entry.get())
    wire_diameter = float(wire_d_entry.get())
    outer_diameter = float(outer_d_entry.get())
    free = float(free_length_entry.get())
    solid = float(solid_length_entry.get())

    [pitch, Nt, Na, k, tau, Fcomp, nf] = calculations(material, end_type, loading_type, wire_diameter, outer_diameter, free, solid, maxload, minload)
    pitch_label = customtkinter.CTkLabel(master = frame, text = f"Pitch is {pitch:.2f} inches\n")
    pitch_label.pack()
    Nt_label = customtkinter.CTkLabel(master = frame, text = f"Total number of coils is {Nt:.2f}\n")
    Nt_label.pack()
    Na_label = customtkinter.CTkLabel(master = frame, text = f"Total number of active coils {Na:.2f}\n")
    Na_label.pack()
    k_label = customtkinter.CTkLabel(master = frame, text = f"The spring rate is {k:.2f} lb/in\n")
    k_label.pack()
    Fcomp_label = customtkinter.CTkLabel(master = frame, text = f"The force needed to compress is {Fcomp:.2f} lbf\n")
    Fcomp_label.pack()
    nf_label = customtkinter.CTkLabel(master = frame, text = f"Factor of safety for static yielding is {nf:.1f}") 
    nf_label.pack()

    #label = customtkinter.CTkLabel(master = frame, text = f"Outer diameter is {outer_diameter}")
    #label.pack()

def load(loading):
    if loading == "Static":
        loading_val = 1
    else:
        loading_val = 2
    return loading_val

def end_values(end_type_par):
    if end_type_par == "Plain":
        end_val = 1
    elif end_type_par == "Plain and ground":
        end_val = 2
    elif end_type_par == "Squared or closed":
        end_val = 3
    elif end_type_par == "Squared and ground":
        end_val = 4
    return end_val

def materials(material_par):
    if material_par == "Music wire (ASTM No. A228)":
        material_val = 1
    elif material_par == "Hard-drawn wire (ASTM No. A227)":
        material_val = 2
    elif material_par == "Chrome-vanadium wire (ASTM No. A232)":
        material_val = 3
    elif material_par == "Chrome-silicon wire (ASTM No. A401)":
        material_val = 4
    elif material_par == "302 stainless wire (ASTM No. A313)":
        material_val = 5
    elif material_par == "Phosphor-bronze wire (ASTM No. B159)":
        material_val = 6
    return material_val


def calculations(material_value, end_value, loading_value, d, O_D, L_0, L_s, F_max, F_min):
    #Diameter
    D = O_D - d

    if material_value == 1: #Music Wire
        m = .145
        A = 201
        U = 0.45
        if d < 0.032: 
            G = 12
            E = 29.5
        elif d > 0.033 and d < 0.063: 
            G = 11.8
            E = 29
        elif d > 0.064 and d < 0.125: 
            G = 11.75
            E = 28.5
        elif d > .125: 
            G = 11.6
            E = 28
    elif material_value == 2: #Hard Drawn Wire 
        m = .190
        A = 147
        U = 0.45
        if d < 0.032: 
            G = 11.7
            E = 28.8
        elif d > 0.033 and d < 0.063: 
            G = 11.6
            E = 28.7
        elif d > 0.064 and d < 0.125: 
            G = 11.5
            E = 28.6
        elif d > .125: 
            G = 11.4
            E = 28.5
    elif material_value == 3: #Chrome vanadium wire 
        m = .168
        A = 169
        E = 29.5
        G = 11.2
        U = 0.65 
    elif material_value == 4: #Chrome Silicon Wire
        U = 0.65
        m = .108
        A = 202
        E = 29.5
        G = 11.2
    elif material_value == 5: #302 stainless wire
        U = 0.45
        G = 10
        E = 28
        m = .146
        A = 169 
    elif material_value == 6: #Phoshpor broze wire
        U = 0.45
        E = 15
        G = 6
        if d > 0.004 and d < 0.022: 
            m = 0
            A = 145
        elif d >= .022 and d < 0.075: 
            m = .028
            A = 121
        elif d >= 0.075 and d < 0.3: 
            m = .064
            A = 110

    #Calculations 
    S_ut = (A/(d**m))*(10**3)

    #Number of Coils Calculation
    N_t = L_s/d

    #End Type Calculation 
    if end_value == 1: 
        #Plain
        N = 0
    elif end_value == 2:
        #Plain and Ground
        N = 1
    elif end_value == 3: 
        #Squared or Closed
        N = 2
    elif end_value == 4: 
        #Squared and Ground
        N = 2

    #Active Coils Calculation
    N_a = N_t - N

    #Pitch Calculation
    Pitch = (L_0-(2*d))/N_a

    #Spring Rate Calculation 
    k = ((d**4)*(G*(10**6)))/(8*(D**3)*N_a)

    #Compression Force
    F_comp = k*(L_0-L_s)

    #Calculate C
    C = D/d

    #Calculate K_b
    K_b = ((4*C)+2)/((4*C)-3)

    #Calculate tau
    tau = K_b*(8*F_comp*D)/(pi*(d**3))

    #Calculate S_sy
    S_sy = (U * S_ut)

    if loading_value == 1:
        #Static Safety Factor
        FS = S_sy/tau
        n = FS
    elif loading_value == 2: 
        #Infinite Life Safety Factor
        
        #Force Calculations
        F_m = (F_max + F_min)/2
        F_a = (F_max - F_min)/2
        
        #Tau Calculations
        tau_a = K_b*(8*F_a*D)/(pi*(d**3))
        tau_m = K_b*(8*F_m*D)/(pi*(d**3))
        
        #Strength Calculations
        S_su = 0.67*S_ut
        S_se = (35000)/(1-(55000/S_su))
        
        #FS
        n_f = ((tau_a/S_se)+(tau_m/S_su))**(-1)
        n = n_f

    return Pitch, N_t, N_a, k, tau, F_comp, n

#Button to trigger program to calculate answers
button  = customtkinter.CTkButton(master = frame, text = "Calculate", command = inputs)
button.pack(pady = 30)

root.mainloop()
