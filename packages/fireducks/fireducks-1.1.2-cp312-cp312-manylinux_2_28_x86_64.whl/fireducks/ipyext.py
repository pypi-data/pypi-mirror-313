import sys
import IPython.display

import fireducks.tracing as tracing


def trace_to_profile(js: str):
    import json

    exclude_events = [
        "fireducks.core.evaluate",
        "fireducks_ext.execute",
        "fire::ExecuteBEF",
    ]

    obj = json.loads(js)
    events = [e for e in obj["traceEvents"] if "pid" in e]

    tmp = []
    elapsed = 0
    for e in events:
        if e["name"] in exclude_events:
            continue
        if e["name"].startswith("fallback:"):
            elapsed += e["dur"]
            e["type"] = "fallback"
            e["name"] = e["name"][len("fallback:") :]
        elif e["name"].startswith("fireducks."):
            elapsed += e["dur"]
            k_name = e["name"][len("fireducks.") :]
            if k_name.startswith("make_"):
                continue
            e["type"] = "kernel"
            e["name"] = k_name
        else:
            # e["type"] = "other"
            # ignore other events
            continue

        tmp += [[e[k] for k in ["name", "type", "dur"]]]

    import pandas

    df = pandas.DataFrame(tmp, columns=["name", "type", "dur"])
    g = df.groupby("name", as_index=False).agg(
        type=("type", "first"),
        n_calls=("dur", "count"),
        dur=("dur", "sum"),
    )
    ret = g.sort_values("dur", ascending=False, ignore_index=True)
    ret["dur"] /= 1e3

    if "ipykernel" in sys.modules:
        total_duration = round(elapsed / 1e3, 4)
        fb_duration = round(ret.loc[ret["type"] == "fallback", "dur"].sum(), 4)
        caption = (
            "profiling-summary:: "
            f"total: {total_duration} msec (fallback: {fb_duration} msec)"
        )
        styles = [
            dict(
                selector="caption",
                props=[("text-align", "center"), ("color", "salmon")],
            )
        ]
        if pandas.options.styler.render.max_rows is None:
            pandas.options.styler.render.max_rows = pandas.get_option(
                "display.min_rows"
            )
        return (
            ret.rename(columns={"dur": "duration (msec)"})
            .style.set_caption(caption)
            .set_table_styles(styles)
        )
    else:
        # pandas.io.formats.style.Styler object doesn't implement __repr__(),
        # hence cannot be displayed on a non-interactive terminal using
        # IPython.display.display(). Therefore, returning dataframe object
        # as it is without adding the caption.
        return ret.rename(columns={"dur": "duration (msec)"})


def profile(line, cell):
    def pretty_print(s):
        df = trace_to_profile(s)
        IPython.display.display(df)

    with tracing.trace(pretty_print):
        get_ipython().run_cell(cell).raise_error()


def load_ipython_extension(ipython):
    ipython.register_magic_function(profile, "cell", "fireducks.profile")
