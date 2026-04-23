import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import matplotlib.pyplot as plt

from simulation.astronaut_model import Astronaut
from simulation.event_engine import simulate_day
from biogears.biogears_interface import generate_physiological_state
from analytics.monte_carlo import run_monte_carlo_simulation
from analytics.risk_analysis import compute_risk_metrics


st.title("Astronaut Fatigue & Sleep Deprivation Digital Twin")


# ---------------- Mission Settings ----------------

days = st.slider("Mission Duration (days)", 10, 60, 30)

mission_type = st.selectbox(
    "Mission Profile",
    ["nominal", "high_stress"]
)


astronaut = Astronaut()


for day in range(days):

    if mission_type == "high_stress":
        astronaut.stress += 1

    simulate_day(astronaut, day)


# ---------------- Mission Timeline ----------------

st.subheader("Mission Timeline")

fig, ax = plt.subplots()

ax.plot(astronaut.history["fatigue"], label="Fatigue")
ax.plot(astronaut.history["stress"], label="Stress")
ax.plot(astronaut.history["cognition"], label="Cognitive Performance")

# Mission phase markers
ax.axvline(x=5, linestyle="--", color="gray", label="Adaptation Phase Start")
ax.axvline(x=15, linestyle="--", color="gray", label="Normal Operations Start")
ax.axvline(x=25, linestyle="--", color="gray", label="High Workload Phase Start")

ax.set_xlabel("Mission Day")
ax.set_ylabel("Value")
ax.set_title("Astronaut Health State Over Mission")

ax.legend()

st.pyplot(fig)


# ---------------- Digital Twin State ----------------

st.subheader("Final Digital Twin State")

st.write("Final Fatigue:", round(astronaut.fatigue, 2))
st.write("Final Stress:", round(astronaut.stress, 2))
st.write("Final Cognitive Performance:", round(astronaut.cognitive_performance, 2))


# ---------------- Physiological State ----------------

phys = generate_physiological_state(astronaut.fatigue, astronaut.stress)

st.write("Heart Rate:", round(phys["heart_rate"], 2), "bpm")
st.write("Oxygen Saturation:", round(phys["oxygen_saturation"], 2), "%")
st.write("Respiration Rate:", round(phys["respiration_rate"], 2), "breaths/min")


# ---------------- Astronaut Visualization ----------------

st.subheader("Astronaut Digital Twin Visualization")

if astronaut.fatigue < 80:

    st.markdown(
        "<h1 style='text-align:center;color:green;'>🧑‍🚀</h1>",
        unsafe_allow_html=True
    )
    st.success("Astronaut Status: NORMAL")

elif astronaut.fatigue < 150:

    st.markdown(
        "<h1 style='text-align:center;color:orange;'>🧑‍🚀</h1>",
        unsafe_allow_html=True
    )
    st.warning("Astronaut Status: MODERATE FATIGUE")

else:

    st.markdown(
        "<h1 style='text-align:center;color:red;'>🧑‍🚀</h1>",
        unsafe_allow_html=True
    )
    st.error("Astronaut Status: CRITICAL FATIGUE")


# ---------------- Health Status Panel ----------------

st.subheader("Astronaut Health Status Panel")


# Fatigue Status
if astronaut.fatigue < 80:
    st.success("Fatigue Status: 🟢 NORMAL")
elif astronaut.fatigue < 150:
    st.warning("Fatigue Status: 🟠 MODERATE")
else:
    st.error("Fatigue Status: 🔴 CRITICAL")


# Stress Status
if astronaut.stress < 40:
    st.success("Stress Status: 🟢 NORMAL")
elif astronaut.stress < 80:
    st.warning("Stress Status: 🟠 MODERATE")
else:
    st.error("Stress Status: 🔴 CRITICAL")


# Cognition Status
if astronaut.cognitive_performance > 70:
    st.success("Cognitive Performance: 🟢 NORMAL")
elif astronaut.cognitive_performance > 40:
    st.warning("Cognitive Performance: 🟠 DEGRADED")
else:
    st.error("Cognitive Performance: 🔴 CRITICAL")


# Heart Rate Status
if phys["heart_rate"] < 90:
    st.success("Heart Rate Status: 🟢 NORMAL")
elif phys["heart_rate"] < 120:
    st.warning("Heart Rate Status: 🟠 ELEVATED")
else:
    st.error("Heart Rate Status: 🔴 CRITICAL")


# ---------------- Monte Carlo Risk Prediction ----------------

st.subheader("Mission Risk Prediction (Monte Carlo Simulation)")

runs = st.slider("Monte Carlo Runs", 100, 2000, 500)

fatigue_results = run_monte_carlo_simulation(
    runs,
    mission_type=mission_type
)

metrics = compute_risk_metrics(fatigue_results)

st.write("Average Mission Fatigue:", round(metrics["average_fatigue"], 2))
st.write("Probability of Critical Fatigue:", round(metrics["probability_critical_fatigue"], 2))


# ---------------- Risk Distribution ----------------

fig2, ax2 = plt.subplots()

ax2.hist(fatigue_results, bins=30)

ax2.set_title("Fatigue Distribution Across Missions")
ax2.set_xlabel("Final Mission Fatigue")
ax2.set_ylabel("Number of Missions")

st.pyplot(fig2)