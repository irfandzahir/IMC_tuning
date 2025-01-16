import streamlit as st
import pandas as pd

def calculate_pi(K, tau, theta, tau_c):
    """Calculate Kc and tau_I for a PI controller."""
    Kc = tau / (K * (tau_c + theta))
    tau_I = tau
    return Kc, tau_I

def calculate_pid(K, tau, theta, tau_c):
    """Calculate Kc, tau_I, and tau_D for a PID controller."""
    Kc = (tau + theta / 2) / (K * (tau_c + theta / 2))  # Corrected equation for Kc as per Case H
    tau_I = tau + theta / 2  # Integral time remains the same
    tau_D = (tau * theta) / (2 * tau + theta)  # Corrected equation for tau_D as per Case H
    return Kc, tau_I, tau_D

def main():
    st.title("FOPTD Controller Parameter Calculator")

    # Input panel on the left
    with st.sidebar:
        st.header("Input Parameters")
        K = st.number_input("Process Gain (K):", min_value=0.0, value=1.0)
        tau = st.number_input("Time Constant (τ):", min_value=0.0, value=1.0)
        theta = st.number_input("Time Delay (θ):", min_value=0.0, value=0.100, format="%.3f")
        tau_c = st.number_input("Controller Time Constant (τ_c):", min_value=0.0, value=1.000, format="%.3f")

        controller_type = st.selectbox("Controller Type:", ["PI", "PID"], index=0)

    # Perform calculation based on controller type
    if controller_type == "PI":
        Kc, tau_I = calculate_pi(K, tau, theta, tau_c)
        tau_D = None  # Not applicable for PI controller
    elif controller_type == "PID":
        Kc, tau_I, tau_D = calculate_pid(K, tau, theta, tau_c)

    # Prepare results in a table
    data = {
        "Parameter": ["Controller Type", "Controller Gain (Kc)", "Integral Time (τ_I)", "Derivative Time (τ_D)"],
        "Value": [
            controller_type,
            f"{Kc:.4f}",
            f"{tau_I:.4f}",
            f"{tau_D:.4f}" if tau_D is not None else "Not applicable",
        ],
    }
    df = pd.DataFrame(data)

    # Display results
    st.header("Calculated Parameters")
    st.table(df)

if __name__ == "__main__":
    main()
