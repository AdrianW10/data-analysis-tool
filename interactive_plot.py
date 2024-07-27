import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

#from data_processor import filter_data, get_user_selection
# Methode, um die Daten benutzerdefiniert und interaktiv zu plotten
def interactive_plot(df, filter=False):

    if filter:
        with st.expander("Gefilterte Daten ansehen"):
            st.write(df)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Scatter Plot", "Line Chart", "Bar Chart","Pie Chart", "Boxplot", "Histogram"])
    

    with tab1:
        st.subheader("Interaktive Scatter Plots")
        col1, col2 = st.columns(2)

        # Auswahl der Achsen
        x1 = col1.selectbox('X - Achse', options=df.columns)
        y1 = col2.selectbox('Y - Achse', options=df.columns)

        # Farben für Datenpunkte und Regressionslinie auswählen
        point_color = st.color_picker('Wähle eine Farbe für die Datenpunkte',"#1f77b4")

        # Scatter-Plot erstellen
        if st.checkbox("Regressionslinie anzeigen"):
            line_color = st.color_picker('Wähle eine Farbe für die Trendlinie',"#1f77b4")
            plot = px.scatter(df, x=x1, y=y1, trendline="ols", trendline_color_override=line_color)
        else:
            plot = px.scatter(df, x=x1, y=y1)

        # Datenpunktfarbe anpassen
        plot.update_traces(marker=dict(color=point_color))

        st.plotly_chart(plot, use_container_width=True)

    with tab2:
        st.subheader("Interaktive Liniendiagramme")
        col1, col2 = st.columns(2)

        # Mehrfachauswahl für die X-Achse
        x2 = col1.selectbox('  X - Achse', options=df.columns, index=None)
        y2 = col2.multiselect('Y - Achsen', options=df.columns)

        if x2 and y2:
            # Farben für jede Linie auswählen
            colors = []
            for y in y2:
                color = st.color_picker(f'Wähle eine farbe für {y}', "#1f77b4", key=y)
                colors.append(color)

            # Erstellen der Linien für das Diagramm
            data = []
            for y, color in zip(y2, colors):
                data.append(go.Scatter(
                    x=df[x2],
                    y=df[y],
                    mode='lines',
                    name=y,
                    line=dict(color=color)
                ))

            # Erstellen des Layouts für das Diagramm
            layout = go.Layout(
                xaxis_title=x2,
                yaxis_title='Values',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            # Erstellen der Figur
            fig = go.Figure(data=data, layout=layout)

            # Anzeigen des Diagramms
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Interaktive Balkendiagramme")
        col1, col2 = st.columns(2)

        x3 = col1.multiselect(' X - Achse', options=df.columns)
        y3 = col2.selectbox(' Y - Achse', options=df.columns, index=None)

        if x3 and y3:
            colors = []
            for category in x3:
                color = st.color_picker(f'Wähle eine farbe für {category}', "#1f77b4", key=category)
                colors.append(color)

            show_barmode = st.selectbox("Wähle den Balkenmodus", options=["group", "stack"], index=0)

            # Erstellen der Balken für das Diagramm
            data = []
            for category, color in zip(x3, colors):
                data.append(go.Bar(
                    x=df[category],
                    y=df[y3],
                    name=category,
                    marker_color=color,
                ))
            n = len(x3)
            # Erstellen des Layouts für das Diagramm
            layout = go.Layout(
                barmode=show_barmode,
                xaxis_title='Kategories' if n >1 else x3[0],
                yaxis_title=y3,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            # Erstellen der Figur
            fig = go.Figure(data=data, layout=layout)

            # Anzeigen des Diagramms
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Interaktive Kuchendiagramme")
        col1, col2 = st.columns(2)

        # Auswahl der Kategorien und Werte
        categories = col1.selectbox('Wähle eine Kategorie', options=df.columns, index=None)
        values = col2.selectbox('Wähle einen Wert', options=df.columns, index=None)

        # Farben für jedes Segment auswählen
        if categories:
            unique_categories = df[categories].unique()
            colors = {}
            n = len(unique_categories) 
            i = 0
            for _ in range((n // 4) + 1):
                for col in st.columns(4):
                    if i < n:
                        category = unique_categories[i]
                        color = col.color_picker(f'Wähle eine farbe für {category}', "#1f77b4", key=category)
                        colors[category] = color
                        i += 1
                    else: 
                        col.empty()
        

            # Erstellen des Kuchendiagramms
            fig = px.pie(df, names=categories, values=values, color=categories, 
                        color_discrete_map=colors)

            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.subheader("Interaktive Boxplots")
        col1, col2 = st.columns(2)

        # Auswahl der Achsen
        x4= col1.multiselect('X - Achsen', options=df.columns)
        y4 = col2.selectbox('  Y - Achse', options=df.columns, index=None)

        # Farben für jede Y-Achsen Kategorie auswählen
        if x4 and y4:
            colors = []
            for x in x4:
                color = st.color_picker(f'Pick a color for {x}', "#1f77b4", key=x)
                colors.append(color)

            # Erstellen der Boxplots für das Diagramm
            data = []
            for x, color in zip(x4, colors):
                data.append(go.Box(
                    x=df[x],
                    y=df[y4],
                    name=x,
                    marker_color=color
                ))
            n = len(x4)
            # Erstellen des Layouts für das Diagramm
            layout = go.Layout(
                xaxis_title="Kategories" if n > 1 else x4[0],
                yaxis_title=y4,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            # Erstellen der Figur
            fig = go.Figure(data=data, layout=layout)

            # Anzeigen des Diagramms
            st.plotly_chart(fig, use_container_width=True)

    with tab6:
        st.subheader("Interaktive Histogramme")

        # Auswahl der Kategorie
        category = st.selectbox(' Wähle eine Kategorie', options=df.columns, index=None)
        if category:
            # Farbe für das Histogramm auswählen
            hist_color = st.color_picker('Wähle eine Farbe für das Histogramm',"#1f77b4")

            # Erstellen des Histogramms
            fig = px.histogram(df, x=category)

            # Farbe des Histogramms anpassen
            fig.update_traces(marker=dict(color=hist_color))

            st.plotly_chart(fig, use_container_width=True)