import streamlit as st
import streamlit.components.v1 as components
import json
import hashlib
from typing import Optional, Tuple, Union, Dict, Any

from lets_plot._type_utils import standardize_dict
from lets_plot._global_settings import get_js_cdn_url
from lets_plot.plot.core import PlotSpec

from .plot_html_helper import (
    _wrap_in_html_doc,
    _static_display_html_with_fixed_sizing,
    _static_display_html_with_relative_sizing,
    _static_configure_html
)


def _get_spec_hash(plot_spec: Dict[str, Any]) -> str:
    """Create a hash of plot specifications"""
    plot_spec_str = json.dumps(plot_spec, sort_keys=True)
    return hashlib.md5(plot_spec_str.encode()).hexdigest()


def _get_state_hash(plot_spec: Dict[str, Any], use_container_width: bool, height: int) -> str:
    """Create a hash of plot specifications and parameters"""
    plot_spec_str = json.dumps(plot_spec, sort_keys=True)
    hash_str = f"{plot_spec_str}_{use_container_width}_{height}"
    return hashlib.md5(hash_str.encode()).hexdigest()


def _get_plot_size(plot_spec: Dict[str, Any]) -> Optional[Tuple[int, int]]:
    """
    Extract width and height from plot specification if present.
    """
    if isinstance(plot_spec, dict) and "ggsize" in plot_spec:
        ggsize = plot_spec["ggsize"]
        if isinstance(ggsize, dict):
            width = ggsize.get("width")
            height = ggsize.get("height")
            try:
                if width is not None and height is not None:
                    # Convert to int and validate they are positive
                    width_int = int(width)
                    height_int = int(height)
                    if width_int > 0 and height_int > 0:
                        return width_int, height_int
            except (ValueError, TypeError):
                pass
    return None


def _contains_toolbar(plot_spec: Dict[str, Any]) -> bool:
    """Check if plot specification contains toolbar"""
    return isinstance(plot_spec, dict) and "ggtoolbar" in plot_spec


def lets_plot_chart(
        plot: Union[Dict[str, Any], PlotSpec],
        use_container_width: bool = False,
        height: int = 400,
        key: Optional[Union[str, int]] = None
) -> None:
    """
    Display a lets-plot chart in Streamlit.

    Parameters
    ----------
    plot : Union[Dict[str, Any], PlotSpec]
        The lets-plot chart to display. Can be either a dictionary containing
        plot specifications or a PlotSpec object.
    use_container_width : bool, default=False
        If True, sets the chart width to match the container width.
    height : int, default=400
        Height of the chart in pixels.
    key : Optional[Union[str, int]], default=None
        Optional key that uniquely identifies the chart.

        Specify a key when your app needs to frequently redraw the same chart
        with different specifications. Without a key, each redraw with a new
        specification creates a new entry in Streamlit's session state,
        which can lead to memory leaks over time.

    Returns
    -------
    None
        This function displays the plot in the Streamlit app but does not
        return any value.

    Raises
    ------
    Exception
        If there is an error displaying the plot. The specific error message
        will be shown in the Streamlit app.
    """
    try:
        if isinstance(plot, dict):
            # could be Vega Lite specs.
            plot_spec = plot
        else:
            plot_spec = plot.as_dict()

        # 'standardize_dict' before trying to get the hash.
        plot_spec = standardize_dict(plot_spec)
        if key is None:
            key = _get_spec_hash(plot_spec)
        else:
            key = str(key)  # Convert int to str if needed

        # Calculate hash of current state
        current_hash = _get_state_hash(plot_spec, use_container_width, height)

        # Keys to access previous hash and html from the session state
        state_key = f"lets_plot_{key}_state_key"

        if state_key not in st.session_state:
            st.session_state[state_key] = dict(
                state_hash=None,
                content=None,
                height=None
            )

        render_plot_spec = True
        if st.session_state[state_key]["state_hash"] == current_hash:
            render_plot_spec = False

        if render_plot_spec:
            show_toolbar = _contains_toolbar(plot_spec)

            # Try to get size from plot specification
            plot_size = _get_plot_size(plot_spec)
            if plot_size:
                width, height = plot_size
            else:
                width = 600  # default width
                if show_toolbar and height >= 100:
                    height -= 33  # Adjust for toolbar height (see DefaultToolbarJs.kt)

            plot_spec_js = json.dumps(plot_spec)

            if use_container_width:
                display_html = _static_display_html_with_relative_sizing(
                    plot_spec_js,
                    height=height,
                    reactive=True,
                    show_toolbar=show_toolbar
                )
            else:
                display_html = _static_display_html_with_fixed_sizing(
                    plot_spec_js,
                    size=(width, height),
                    show_toolbar=show_toolbar
                )

            height += 33  # Adjust for toolbar height (see DefaultToolbarJs.kt)

            # Get the JavaScript library URL
            script_url = get_js_cdn_url()
            config_html = _static_configure_html(script_url)

            plot_html = _wrap_in_html_doc(config_html, display_html)

            st.session_state[state_key] = dict(
                state_hash=current_hash,
                content=plot_html,
                height=height
            )

        else:
            # Use cached HTML to prevent plot flickering.
            plot_html = str(st.session_state[state_key]["content"])
            height = int(st.session_state[state_key]["height"])

        components.html(plot_html, height=height)

    except Exception as e:
        st.error(f"Error displaying plot: {str(e)}")
        raise
