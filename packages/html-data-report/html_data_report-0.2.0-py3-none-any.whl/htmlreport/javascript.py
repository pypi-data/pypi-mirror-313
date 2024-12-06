def _get_plotly_resize_script() -> str:
    return r"""
        <script>
            $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
                var new_tab = e.target // newly activated tab
                var xx = Plotly.d3.selectAll( `[id='${new_tab.attributes["aria-controls"].value}']  .plotly-graph-div`);
                if(  xx.length && xx[0].length ) {
                    xx[0].forEach(element => {
                        setTimeout( () => x(element), 30);
                    });
                }
            })
        </script>
        <script>
            function x(gd_i) {
                Plotly.Plots.resize(gd_i);
            }
        </script>
        """
