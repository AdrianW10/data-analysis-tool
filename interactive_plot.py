import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Method to plot the data in a customized and interactive way
def interactive_plot(df, filter=False):

    if filter:
        with st.expander("View Filtered Data"):
            st.write(df)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Scatter Plot", "Line Chart", "Bar Chart", "Pie Chart", "Boxplot", 
                                                                "Histogram"])
    

    with tab1:
        st.subheader("Interactive Scatter Plots")
        col1, col2 = st.columns(2)

        x1 = col1.selectbox('X - Axis', options=df.columns)
        y1 = col2.selectbox('Y - Axis', options=df.columns)

        point_color = st.color_picker('Choose a color for data points', 
                                                                    "#1f77b4")
        if st.checkbox("Show regression line"):
            line_color = st.color_picker('Choose a color for the trendline', 
                                                                    "#1f77b4")
            plot = px.scatter(df, x=x1, y=y1, trendline="ols", 
                                        trendline_color_override=line_color)
        else:
            plot = px.scatter(df, x=x1, y=y1)

        plot.update_traces(marker=dict(color=point_color))
        st.plotly_chart(plot, use_container_width=True)

    with tab2:
        st.subheader("Interactive Line Charts")
        col1, col2 = st.columns(2)

        x2 = col1.selectbox('  X - Axis', options=df.columns, index=None)
        y2 = col2.multiselect('Y - Axes', options=df.columns)

        if x2 and y2:
            colors = []
            for y in y2:
                color = st.color_picker(f'Choose a color for {y}', "#1f77b4", 
                                                                        key=y)
                colors.append(color)

            data = []
            for y, color in zip(y2, colors):
                data.append(go.Scatter(
                    x=df[x2],
                    y=df[y],
                    mode='lines',
                    name=y,
                    line=dict(color=color)
                ))

            layout = go.Layout(
                xaxis_title=x2,
                yaxis_title='Values',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Interactive Bar Charts")
        col1, col2 = st.columns(2)

        x3 = col1.multiselect(' X - Axis', options=df.columns)
        y3 = col2.selectbox(' Y - Axis', options=df.columns, index=None)

        if x3 and y3:
            colors = []
            for category in x3:
                color = st.color_picker(f'Choose a color for {category}', 
                                                    "#1f77b4", key=category)
                colors.append(color)

            show_barmode = st.selectbox("Choose bar mode", options=["group", 
                                                            "stack"], index=0)
            data = []
            for category, color in zip(x3, colors):
                data.append(go.Bar(
                    x=df[category],
                    y=df[y3],
                    name=category,
                    marker_color=color,
                ))

            n = len(x3)
            layout = go.Layout(
                barmode=show_barmode,
                xaxis_title='Categories' if n > 1 else x3[0],
                yaxis_title=y3,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Interactive Pie Charts")
        col1, col2 = st.columns(2)

        categories = col1.selectbox('Choose a category', options=df.columns, 
                                                                    index=None)
        values = col2.selectbox('Choose a value', options=df.columns, 
                                                                    index=None)
        if categories:
            unique_categories = df[categories].unique()
            colors = {}
            n = len(unique_categories)
            i = 0
            for _ in range((n // 4) + 1):
                for col in st.columns(4):
                    if i < n:
                        category = unique_categories[i]
                        color = col.color_picker(
                            f'Choose a color for {category}', 
                            "#1f77b4", key=category
                            )
                        colors[category] = color
                        i += 1
                    else:
                        col.empty()

            fig = px.pie(df, names=categories, values=values, color=categories, 
                        color_discrete_map=colors)

            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.subheader("Interactive Boxplots")
        col1, col2 = st.columns(2)

        x4 = col1.multiselect('X - Axes', options=df.columns)
        y4 = col2.selectbox('  Y - Axis', options=df.columns, index=None)

        if x4 and y4:
            colors = []
            for x in x4:
                color = st.color_picker(f'Pick a color for {x}', "#1f77b4", 
                                                                        key=x)
                colors.append(color)

            data = []
            for x, color in zip(x4, colors):
                data.append(go.Box(
                    x=df[x],
                    y=df[y4],
                    name=x,
                    marker_color=color
                ))

            n = len(x4)
            layout = go.Layout(
                xaxis_title="Categories" if n > 1 else x4[0],
                yaxis_title=y4,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, use_container_width=True)

    with tab6:
        st.subheader("Interactive Histograms")
        category = st.selectbox(' Choose a category', options=df.columns, 
                                                                    index=None)
        if category:
            hist_color = st.color_picker('Choose a color for the histogram', 
                                                                    "#1f77b4")
            fig = px.histogram(df, x=category)
            fig.update_traces(marker=dict(color=hist_color))
            st.plotly_chart(fig, use_container_width=True)
