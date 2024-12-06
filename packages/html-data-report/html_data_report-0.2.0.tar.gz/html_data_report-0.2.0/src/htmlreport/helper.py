import base64
from io import BytesIO

import matplotlib.pyplot as plt


def get_mpl_plot_as_base64(fig: plt.Figure) -> str:

    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    encoded = base64.b64encode(image_png).decode("utf-8")
    return encoded
