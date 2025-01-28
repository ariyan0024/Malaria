import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('PROJECT MALARIA')
initial_A = st.slider('Initial frequency of allele A', 0.0, 1.0, 0.6)
initial_S = st.slider("Initial frequency of allele S", 0.0, 1.0, 0.4)

if initial_A + initial_S != 1.0:
    st.error("Initial frequencies of A and S must sum to 1.0")
else:
    malaria_prevalence = st.slider("Malaria Prevalence rate(%)", 0, 100, 70)
    number_of_generations = st.number_input("Number of generations to simulate", min_value = 1, max_value = 1000, value = 100)
    st.write("""Maximum Value of number of generations = 1000""")

    def genetics_simulation(initial_A, initial_S, malaria_prevalence, number_of_generations):
        malaria_prevalence /= 100.0
        AA_fitness = 1 - malaria_prevalence
        AS_fitness = 1.0
        SS_fitness = 0.2
        frequency_A = initial_A
        frequency_S = initial_S
        frequency_A_till_end = [frequency_A]
        frequency_S_till_end = [frequency_S]

        for number in range(number_of_generations):
            AA = frequency_A ** 2
            AS = 2 * frequency_A * frequency_S  #Hardy–Weinberg principle
            SS = frequency_S ** 2

            # Mean fitness
            mean_fitness = (AA * AA_fitness) + (AS * AS_fitness) + (SS * SS_fitness)
                
            # Update allele frequencies
            frequency_A = ((AA * AA_fitness) + (0.5 * AS * AS_fitness)) / mean_fitness
            frequency_S = ((SS * SS_fitness) + (0.5 * AS * AS_fitness)) / mean_fitness

            # Store frequencies
            frequency_A_till_end.append(frequency_A)
            frequency_S_till_end.append(frequency_S)

        return frequency_A_till_end, frequency_S_till_end

    if st.button("Run Simulation"):
        frequency_A_till_end, frequency_S_till_end = genetics_simulation(
            initial_A, initial_S, malaria_prevalence, number_of_generations
        )

        # Visualization using Line Chart
        st.write("### Allele Frequency Trends Over Generations")
        data = {
            'Generations': range(int(number_of_generations) + 1),
            'Allele A': frequency_A_till_end,
            'Allele S': frequency_S_till_end
        }
        df = pd.DataFrame(data)
        df = df.set_index('Generations')
        st.line_chart(df)

        # Results
        st.subheader("Final Allele Frequencies")
        st.write(f"Allele A: {frequency_A_till_end[-1]:.3f}")
        st.write(f"Allele S: {frequency_S_till_end[-1]:.3f}")
