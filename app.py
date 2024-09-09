from flask import Flask, render_template, request
import plotly.graph_objects as go
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # CREATE X, A, B LISTS (for x, a+bi)
        res = {'high': [0.002, 5001], 'med': [0.01, 1001], 'low': [0.05, 201]}
        try:
            n = float(request.form['n'])
        except ValueError:
            return "Error: Invalid input value for n. Please enter a numeric value.", 400

        resolution = request.form['resolution']
        selected_res = res[resolution]

        x_list = [round(n * selected_res[0], 2) for n in range(selected_res[1])]
        complex_values = [complex((n)**x) for x in x_list]
        a_list = [cv.real for cv in complex_values]
        b_list = [cv.imag for cv in complex_values]

        # CREATE 3D PLOT USING PLOTLY
        fig = go.Figure(data=[go.Scatter3d(
            x=x_list,
            y=a_list,
            z=b_list,
            mode='markers',
            marker=dict(
                size=1,
                color='blue'
            )
        )])

        # AXIS LABELS
        fig.update_layout(
            scene=dict(
                xaxis_title='X-axis',
                yaxis_title='Real Part (a)',
                zaxis_title='Imaginary Part (b)'
            )
        )

        # TITLE
        fig.update_layout(title=f'[Interactive] {n}^x')

        # CONVERT FIGURE TO HTML
        graph_html = fig.to_html(full_html=False)

        return render_template('index.html', plot_generated=True, graph_html=graph_html)

    return render_template('index.html', plot_generated=False)

if __name__ == '__main__':
    app.run()
