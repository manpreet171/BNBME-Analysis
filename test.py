import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Hardcoded data
data = {
    'Month': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07', '2024-08'],
    'BNBME_Occ': [47, 63, 74, 87, 55, 45, 15, 32],
    'Luxe_Occ': [36, 88, 74, 88, 58, 54, 23, 43],
    'Anantara_Occ': [47, 70, 58, 68, 48, 38, 36, 38],
    'BNBME_RevPAR': [467, 584, 812, 803, 395, 305, 79, 130],
    'Luxe_RevPAR': [444, 887, 716, 772, 334, 304, 119, 221],
    'Anantara_RevPAR': [445, 649, 566, 593, 308, 205, 153, 162],
    'BNBME_ADR': [992, 927, 1096, 922, 722, 677, 522, 410],
    'Luxe_ADR': [1240, 1007, 966, 882, 572, 565, 514, 512],
    'Anantara_ADR': [954, 924, 972, 867, 635, 540, 425, 429]
}

# Creating DataFrame
df = pd.DataFrame(data)
df['BNBME_RevPAR_per_Occ'] = df['BNBME_RevPAR'] / df['BNBME_Occ']
df['Luxe_RevPAR_per_Occ'] = df['Luxe_RevPAR'] / df['Luxe_Occ']
df['Anantara_RevPAR_per_Occ'] = df['Anantara_RevPAR'] / df['Anantara_Occ']

# Performance Indices
df['Occupancy_Index'] = df['BNBME_Occ'] / df['Anantara_Occ']
df['ADR_Index'] = df['BNBME_ADR'] / df['Anantara_ADR']
df['RevPAR_Index'] = df['BNBME_RevPAR'] / df['Anantara_RevPAR']

# Market Share and RevPAR Gap
df['Total_Market_RevPAR'] = df['BNBME_RevPAR'] + df['Luxe_RevPAR'] + df['Anantara_RevPAR']
df['BNBME_Market_Share'] = df['BNBME_RevPAR'] / df['Total_Market_RevPAR']
df['RevPAR_Gap_with_Luxe'] = df['BNBME_RevPAR'] - df['Luxe_RevPAR']

# Streamlit App

# Adding the image at the top of the app
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://www.yello.ae/img/ae/f/1539409694-97-bnbme-holiday-homes-by-hoteliers.png" alt="BNBME Logo">
    </div>
    """, 
    unsafe_allow_html=True
)

st.title('Detailed BNBME Performance Dashboard (2024)')
st.write("Explore BNBME's performance metrics in detail, including advanced indices and comparisons.")

# Select Comparison Mode
comparison_mode = st.radio('Select Comparison Mode', ['Solo', 'Comparison'])

# Solo Mode
if comparison_mode == 'Solo':
    # Metric selection restricted to three options
    metric = st.selectbox('Select a Metric to Visualize', ['Occupancy', 'ADR', 'RevPAR'])

    if metric == 'Occupancy':
        st.subheader('Occupancy Trends (Solo)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['BNBME_Occ'], marker='o', label='BNBME')
        ax.set_title('BNBME Monthly Occupancy Trends (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('Occupancy Rate (%)')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Performance**: BNBME had an average occupancy rate of 52.25%.
        - **Highs and Lows**: The highest occupancy was in April (87%), while the lowest was in July (15%).
        - **Patterns**: BNBME struggled during the summer months, indicating a need for targeted strategies to maintain occupancy.
        """)

    elif metric == 'ADR':
        st.subheader('ADR Trends (Solo)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['BNBME_ADR'], marker='o', label='BNBME')
        ax.set_title('BNBME Monthly ADR Trends (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('ADR ($)')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Performance**: BNBME maintained a strong ADR of $783.50.
        - **Highs and Lows**: The highest ADR was in March ($1096), while the lowest was in August ($410).
        - **Patterns**: BNBME's pricing strategy was effective during peak periods but faced challenges in maintaining high ADR during off-peak months.
        """)

    elif metric == 'RevPAR':
        st.subheader('RevPAR Trends (Solo)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['BNBME_RevPAR'], marker='o', label='BNBME')
        ax.set_title('BNBME Monthly RevPAR Trends (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('RevPAR ($)')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Performance**: BNBME's average RevPAR was $446.88.
        - **Highs and Lows**: The peak RevPAR was in March ($812), while the lowest was in July ($79).
        - **Patterns**: BNBME outperformed during peak periods but struggled significantly in off-peak months.
        """)

# Comparison Mode
elif comparison_mode == 'Comparison':
    comparison_options = st.multiselect(
        'Select Competitor(s) to Compare Against',
        ['Luxe (Competitor)', 'Anantara (Market)'],
        default=['Luxe (Competitor)', 'Anantara (Market)']
    )

    # Select Metric to Visualize (All metrics are available)
    metric = st.selectbox('Select a Metric to Visualize', [
        'Occupancy', 'RevPAR', 'ADR', 
        'RevPAR per Occupancy Point', 'Performance Indices', 
        'RevPAR Market Share', 'RevPAR Gap with Luxe'
    ])

    if metric == 'Occupancy':
        st.subheader('Occupancy Trends (Comparison)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['BNBME_Occ'], marker='o', label='BNBME')
        if 'Luxe (Competitor)' in comparison_options:
            ax.plot(df['Month'], df['Luxe_Occ'], marker='o', label='Luxe (Competitor)')
        if 'Anantara (Market)' in comparison_options:
            ax.plot(df['Month'], df['Anantara_Occ'], marker='o', label='Anantara (Market)')
        ax.set_title('Monthly Occupancy Trends (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('Occupancy Rate (%)')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Performance**: BNBME had an average occupancy rate of 52.25%, slightly above the market (Anantara) average but below Luxe’s 58.00%.
        - **Highs and Lows**: The highest occupancy was in April (87%), while the lowest was in July (15%).
        - **Patterns**: BNBME struggled during the summer months, indicating a need for targeted strategies to maintain occupancy.
        """)

    elif metric == 'RevPAR':
        st.subheader('RevPAR Trends (Comparison)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['BNBME_RevPAR'], marker='o', label='BNBME')
        if 'Luxe (Competitor)' in comparison_options:
            ax.plot(df['Month'], df['Luxe_RevPAR'], marker='o', label='Luxe (Competitor)')
        if 'Anantara (Market)' in comparison_options:
            ax.plot(df['Month'], df['Anantara_RevPAR'], marker='o', label='Anantara (Market)')
        ax.set_title('Monthly RevPAR Trends (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('RevPAR ($)')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Performance**: BNBME's average RevPAR was $446.88, higher than the market average but slightly lower than Luxe's.
        - **Highs and Lows**: The peak RevPAR was in March ($812), while the lowest was in July ($79).
        - **Patterns**: BNBME outperformed the market during peak periods but struggled significantly in off-peak months.
        """)

    elif metric == 'ADR':
        st.subheader('ADR Trends (Comparison)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['BNBME_ADR'], marker='o', label='BNBME')
        if 'Luxe (Competitor)' in comparison_options:
            ax.plot(df['Month'], df['Luxe_ADR'], marker='o', label='Luxe (Competitor)')
        if 'Anantara (Market)' in comparison_options:
            ax.plot(df['Month'], df['Anantara_ADR'], marker='o', label='Anantara (Market)')
        ax.set_title('Monthly ADR Trends (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('ADR ($)')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Performance**: BNBME maintained a strong ADR of $783.50, nearly identical to Luxe's and higher than the market average.
        - **Highs and Lows**: The highest ADR was in March ($1096), while the lowest was in August ($410).
        - **Patterns**: BNBME's pricing strategy was effective during peak periods but faced challenges in maintaining high ADR during off-peak months.
        """)

    elif metric == 'RevPAR per Occupancy Point':
        st.subheader('RevPAR per Occupancy Point (Comparison)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['BNBME_RevPAR_per_Occ'], marker='o', label='BNBME')
        if 'Luxe (Competitor)' in comparison_options:
            ax.plot(df['Month'], df['Luxe_RevPAR_per_Occ'], marker='o', label='Luxe (Competitor)')
        if 'Anantara (Market)' in comparison_options:
            ax.plot(df['Month'], df['Anantara_RevPAR_per_Occ'], marker='o', label='Anantara (Market)')
        ax.set_title('RevPAR per Occupancy Point (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('RevPAR per Occupancy Point ($)')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Efficiency**: BNBME's RevPAR per Occupancy Point was $7.84, showing high revenue efficiency comparable to Luxe.
        - **Highs and Lows**: The highest efficiency was in March ($10.97), and the lowest was in July ($4.06).
        - **Patterns**: The drop in efficiency during the summer suggests a need for strategies to maintain performance in off-peak periods.
        """)

    elif metric == 'Performance Indices':
        st.subheader('Performance Indices (Comparison)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['Occupancy_Index'], marker='o', label='Occupancy Index')
        ax.plot(df['Month'], df['ADR_Index'], marker='o', label='ADR Index')
        ax.plot(df['Month'], df['RevPAR_Index'], marker='o', label='RevPAR Index')
        ax.axhline(y=1, color='gray', linestyle='--', label='Market Average')
        ax.set_title('BNBME Performance Indices Relative to Market (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('Index Value')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Performance**: BNBME generally outperformed the market, with strong indices in March and April.
        - **Highs and Lows**: The highest RevPAR Index was in March (1.49), showing a 49% higher RevPAR compared to the market. The lowest was in July (0.52), indicating underperformance during the summer.
        - **Patterns**: BNBME showed strong performance in peak months but struggled to maintain this advantage during the off-peak season, particularly in July.
        """)

    elif metric == 'RevPAR Market Share':
        st.subheader('BNBME RevPAR Market Share (Comparison)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['BNBME_Market_Share'] * 100, marker='o', label='Market Share (%)')
        ax.set_title('BNBME RevPAR Market Share (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('Market Share (%)')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Market Share**: BNBME captured an average of 32.65% of the total market RevPAR, with the highest share in March (38.78%) and the lowest in July (22.51%).
        - **Highs and Lows**: The market share was strongest in peak months like March and April, but significantly weakened in the summer months.
        - **Patterns**: The decline in market share during off-peak months suggests that BNBME needs to strengthen its strategies to maintain or grow its share during these periods.
        """)

    elif metric == 'RevPAR Gap with Luxe':
        st.subheader('RevPAR Gap: BNBME vs Luxe (Comparison)')
        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['RevPAR_Gap_with_Luxe'], marker='o', label='RevPAR Gap ($)')
        ax.set_title('RevPAR Gap: BNBME vs Luxe (2024)')
        ax.set_xlabel('Month')
        ax.set_ylabel('RevPAR Gap ($)')
        ax.axhline(y=0, color='gray', linestyle='--', label='No Gap')
        ax.legend()
        st.pyplot(fig)

        st.write("""
        **Analysis**:
        - **Overall Gap**: On average, BNBME's RevPAR trailed Luxe by $27.75, with the largest gap in February (-$303) and the smallest gap in March (+$96).
        - **Highs and Lows**: BNBME outperformed Luxe in March and April, but lagged significantly in February and during the summer months.
        - **Patterns**: The data suggests that while BNBME can compete effectively during peak periods, it struggles to maintain this competitiveness during off-peak periods, especially in comparison to Luxe.
        """)
