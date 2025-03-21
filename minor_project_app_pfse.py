import streamlit as st
import hand_calculations as hcalc
import sections_db as sect_db
import beams as bm
import forallpeople as si
import plotly.graph_objects as go


#MAKE WIDE MODE DEFAULT
st.set_page_config(layout='wide')

# SECTION DB AND SECTION GEOMETRY PROPERTIES
st.sidebar.subheader("Results Parameters")
steel_section_list = sect_db.aisc_w_sections('si').iloc[::-1]
steel_sections = st.sidebar.multiselect("Pick sections", steel_section_list['Section'], default=steel_section_list['Section'][0])
steel_section = st.sidebar.selectbox("Section for example calculations", steel_sections)
try:
    steel_section_data = steel_section_list.loc[steel_section]        
except KeyError:
    st.error("No section selected. Select a steel section to begin")
    raise KeyError(None)


# GLOBAL BEAM BRACING AND LOADING PROPERTIES
L_unbr = st.sidebar.number_input("Unbraced length, L$_{unbr}$ (mm)", value=2000, min_value=1)
min_length = st.sidebar.number_input("Minimum beam length (mm)", value=200, min_value=1)
interval = st.sidebar.number_input("Length step interval (mm)", value=200, min_value=1)
max_length = st.sidebar.number_input("Maximum beam length (mm)", value=30000, min_value = min_length + interval)
omega_2 = st.sidebar.number_input("Equivalent moment factor, $\omega_{2}$", value=1.0, max_value=2.5, min_value=1.0)


# MATERIAL PROPERTIES and CODE VALUES (Should remain consistant)
fy = st.sidebar.number_input("Steel yield strength, f$_{y}$ (MPa)", value=345, min_value=1)
E = st.sidebar.number_input("Elastic modulus, E$_{s}$ (GPa)", value=200, min_value=1)
G = st.sidebar.number_input("Shear modulus, G (GPa)", value=77, min_value=1)
phi = st.sidebar.number_input("Resistance factor, $\phi$", value=0.9, min_value=0.1)


## For sample calculations below
steel_beam_sample_calc = bm.steel_beam_from_section_name_si(
    steel_section, L_unbr, fy, omega_2, E, G, phi)


## For sample calculations below
section_class = steel_beam_sample_calc.section_class()
section_class_maj = section_class[0]
Mrxu = steel_beam_sample_calc.moment_capacity()


## Accumulate all selected beams (and their properties) in a list
steel_beams = []
for beam in steel_sections:
    steel_beams.append(bm.steel_beam_from_section_name_si(
        beam, L_unbr, fy, omega_2, E, G, phi))


#COORDINATES FOR UNBRACED MOMENT DIAGRAM
x_coords = list(range(min_length, max_length, interval))

y_coords = []
for beam in steel_beams:
    y_coords_i =[]
    for x_coord in x_coords:
        beam.length = x_coord
        Mu_length = beam.moment_capacity()
        y_coords_i.append(Mu_length)
    y_coords.append(y_coords_i)


# Plot lines
fig = go.Figure()

fig.layout.title.text = "Factored moment resistance vs unbraced length"
fig.layout.xaxis.title = "Unbraced length (mm)"
fig.layout.yaxis.title = "Mr (Nm)"


fig.add_vline(x=L_unbr, line_width=1, line_dash="dash", line_color="green", name="Unbraced length")

for idx, beam in enumerate(steel_beams):
    fig.add_trace(
        go.Scatter(
        x=x_coords, 
        y=y_coords[idx],
        name=beam.beam_tag
        )
    )

fig.add_trace(
    go.Scatter(
        y=[Mrxu],
        x=[L_unbr],
        name="Unbraced capcity for sample calculation"
    )
)

st.header('Factored Moment Resistance of Unbraced WF Steel Section')
st.plotly_chart(fig)


## Handcalc rendering of sample calculations
si.environment("structural")


# Defining units for the sample calculations
bf_unit = steel_beam_sample_calc.bf * si.mm
tf_unit = steel_beam_sample_calc.tf * si.mm
d_unit = steel_beam_sample_calc.d * si.mm
tw_unit = steel_beam_sample_calc.tw * si.mm

Sx_unit = steel_beam_sample_calc.Sx * si.mm**3
Zx_unit = steel_beam_sample_calc.Zx * si.mm**3
fy_unit = fy * si.MPa
L_unbr_unit = L_unbr * si.mm
E_unit = E * si.GPa
Iy_unit = steel_beam_sample_calc.Iy * si.mm**4
G_unit = G * si.GPa
J_unit = steel_beam_sample_calc.J * si.mm**4
Cw_unit = steel_beam_sample_calc.Cw * si.mm**6

section_class_latex, section_class_value = hcalc.calc_section_class(bf_unit, tf_unit, d_unit, tw_unit, fy)
m_latex, m_value = hcalc.calc_M(Sx_unit, Zx_unit, fy_unit, L_unbr_unit, E_unit, Iy_unit, G_unit, J_unit, Cw_unit, omega_2, section_class_maj, phi)

# Headers for Streamlit app
st.header(f'Example Calculations for {steel_section_data['Section']}')

with st.expander("Section class checks"):
    st.latex(section_class_latex)

with st.expander("Unbraced moment capacity of WF beam"):
    st.latex(m_latex)

with st.expander("Assumptions and Exclusions"):
    st.write("The above sample calculations are based on CSA S16:24 and AISC Shapes Database v15.0 and assume the following:\n"
    "1) Beam is a doubly symmetric wide-flange section \n"
    "2) Beam has no axial load (i.e. is not a beam-column) \n"
    "3) Class 4 sections are not limited by local buckling (Future improvement here [CL 13.5c)ii) and iii)]) \n"
    "4) Beam is loaded at or below shear centre of the section or point of loading are brace points and considered to provide lateral or torsional restraint \n"
    "5) Metric units are utilized throughout."
    )
