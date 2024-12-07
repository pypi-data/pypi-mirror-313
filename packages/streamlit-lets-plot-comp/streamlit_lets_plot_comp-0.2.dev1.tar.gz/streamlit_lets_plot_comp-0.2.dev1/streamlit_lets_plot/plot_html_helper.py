import random
import string


def random_string(length=6):
    """Generate a random string of fixed length"""
    return ''.join(random.choices(string.ascii_letters, k=length))


def _wrap_in_html_doc(config_html, display_html):
    """Wrap the HTML content in a basic HTML document"""
    return f"""
<html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
            }}
        </style>
        {config_html}
    </head>
    <body>
        {display_html}
    </body>
</html>
"""


def _static_configure_html(script_url):
    """Generate the HTML for loading the lets-plot library"""
    return f'<script type="text/javascript" data-lets-plot-script="library" src="{script_url}"></script>'


def plot_container_html_snippet(show_toolbar: bool, fit_width: bool):
    """Generate the HTML snippet for the plot container"""
    if fit_width:
        output_div_style = "'display: inline-block; width: 100%;'"
    else:
        output_div_style = "'display: inline-block;'"

    if show_toolbar:
        return f"""
               // Wrapper for toolbar and chart
               var outputDiv = document.createElement('div');
               outputDiv.setAttribute('style', {output_div_style});
               containerDiv.appendChild(outputDiv);

               // Toolbar
               var toolbar = new LetsPlot.tools.DefaultToolbar();
               outputDiv.appendChild(toolbar.getElement());

               // Plot
               var plotContainer = document.createElement('div');
               outputDiv.appendChild(plotContainer);
        """
    else:
        return """
               var toolbar = null;
               var plotContainer = containerDiv;
        """


def _static_display_html_with_fixed_sizing(plot_spec_js, size, show_toolbar=False):
    """Generate HTML for fixed-size plot display"""
    output_id = random_string()
    width, height = size

    return f"""
    <div id="{output_id}"></div>
    <script type="text/javascript" data-lets-plot-script="plot">
    (function() {{
        var plotSpec={plot_spec_js};
        var containerDiv = document.getElementById("{output_id}");

{plot_container_html_snippet(show_toolbar, fit_width=False)}               

        var options = {{
            sizing: {{
                width_mode: "fixed",
                height_mode: "fixed",
                width: {width},
                height: {height}
            }}
        }};
        var fig = LetsPlot.buildPlotFromRawSpecs(plotSpec, -1, -1, plotContainer, options);
        if (toolbar) {{
            toolbar.bind(fig);
        }}
    }})();
    </script>
    """


def _static_display_html_with_relative_sizing(plot_spec_js, height, reactive: bool, show_toolbar=False):
    """Generate HTML for responsive plot display"""
    output_id = random_string()

    return f"""
    <div id="{output_id}"></div>
    <script type="text/javascript" data-lets-plot-script="plot">
    (function() {{
        var containerDiv = document.getElementById("{output_id}");
        var lastAppliedWidth = 0;
        var fig = null;
        var observer = new ResizeObserver(function(entries) {{
            for (let entry of entries) {{
                var width = containerDiv.clientWidth
                if (entry.contentBoxSize && width > 0 && Math.abs(lastAppliedWidth - width) > 1) {{
                    lastAppliedWidth = width;
                    if (observer && !{str(reactive).lower()}) {{
                        observer.disconnect();
                        observer = null;
                    }}

                    var plotSpec={plot_spec_js};

{plot_container_html_snippet(show_toolbar, fit_width=True)}               

                    var options = {{
                        sizing: {{
                            width_mode: "fit",
                            height_mode: "fixed",
                            width: width,
                            height: {height}
                        }}
                    }};
                        
                    //console.log(`width = ${{width}}`);
                    if (fig == null) {{
                        fig = LetsPlot.buildPlotFromRawSpecs(plotSpec, -1, -1, plotContainer, options);
                        if (toolbar) {{
                            toolbar.bind(fig);
                        }}
                    }} else {{
                        //console.log(`update view, options: ${{JSON.stringify(options, null, 2)}}`);
                        fig.updateView({{}}, options);
                    }}
            
                    break;
                }}
            }}
        }});
        observer.observe(containerDiv);
    }})();
    </script>
    """
