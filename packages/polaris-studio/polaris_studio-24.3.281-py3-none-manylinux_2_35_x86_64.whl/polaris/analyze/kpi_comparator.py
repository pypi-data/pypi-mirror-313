# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
# matplotlib 3.8 should have type hints, until then we just ignore
from itertools import cycle
import logging
import math
import traceback
from pathlib import Path
from re import Pattern
from typing import Optional
from uuid import uuid1

import numpy as np
import pandas as pd
import seaborn as sns  # type: ignore

from polaris.analyze.result_kpis import ResultKPIs
from polaris.utils.pandas_utils import filter_df


# We have to delay importing of matplotlib as it causes CI problems for QPolaris
# import matplotlib.pyplot as plt  # type: ignore


class KpiComparator:
    """This class provides an easy way to group together multiple runs of POLARIS and compare their outputs. Runs KPIs are
    added along with a string based name which is used as the label for that run in any subsequent plots which are
    generated.

    ::

        from polaris.analyze.kpi_comparator import KpiComparator

        results = KpiComparator()
        results.add_run(ResultKPIs.from_iteration(ref_project_dir / f"{city}_iteration_2"), 'REF_iteration_2')
        results.add_run(ResultKPIs.from_iteration(eval_project_dir / f"{city}_iteration_2"), 'EVAL_iteration_2')

    Metric comparison plots can then be generated in a notebook using:

    ::

        results.plot_mode_share()
        results.plot_vmt()
        results.plot_vmt_by_link_type()

    Any number of runs can be added using `add_run` up to the limit of readability on the generated plots.

    The object can also be used to generate a set of csv files for input into Excel (if you really have to use Excel):

    ::

        results.dump_to_csvs(output_dir = "my_csv_dump_dir")
    """

    def __init__(self):
        import matplotlib.pyplot as plt

        plt.rc("axes", axisbelow=True)  # We want our grid lines to sit behind our chart elements

        self.runs = {}
        self.results = None

    def add_run(self, kpi: ResultKPIs, run_id: str):
        if kpi is None:
            return
        if run_id in self.runs:
            run_id = f"{run_id}-{str(uuid1())[0:6]}"
        self.runs[run_id] = kpi

    def has_run(self, run_id):
        return run_id in self.runs

    def dump_to_csvs(self, output_dir, metrics_to_dump=None, **kwargs):
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        metrics = metrics_to_dump or ResultKPIs.available_metrics()
        metrics = set(metrics) - {"num_adults", "num_employed", "num_hh", "tts"}  # remove legacy scalar metrics
        for m in metrics:
            df = self._get_results(m, **kwargs)
            if df is not None and isinstance(df, pd.DataFrame):
                df.to_csv(Path(output_dir) / f"{m}.csv")

        return metrics

    def plot_everything(self, **kwargs):
        exclusions = ["plot_multiple_gaps", "plot_everything"]
        plot_methods = [e for e in dir(self) if e.startswith("plot_") and e not in exclusions]
        for p in plot_methods:
            if callable(self.__getattribute__(p)):
                fn = self.__getattribute__(p)
                fn(**kwargs)

    @classmethod
    def available_plots(self):
        exclusions = ["plot_multiple_gaps", "plot_everything"]
        return [e.replace("plot_", "") for e in dir(self) if e.startswith("plot_") and e not in exclusions]

    def plot_mode_share(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("mode_shares", **kwargs)
        df = df[~(df["mode"].str.contains("FAIL") | df["mode"].str.contains("NO_MOVE"))]
        if df is None or df.empty:
            logging.warning("There were no results for 'mode_shares'")
            return

        fig, axes = plt.subplots(2, 2, figsize=(20, 10))

        def f(y, ax, title):
            sns.barplot(df, x="mode", y=y, hue="run_id", ax=ax)
            ax.set(title=title)
            ax.set_ylim([0, 0.90])
            KpiComparator._style_axes([ax], rotate_x_labels=False)

        f("total_pr", axes[0, 0], title="Total")
        f("HBW_pr", axes[1, 0], title="HBW")
        f("HBO_pr", axes[0, 1], title="HBO")
        f("NHB_pr", axes[1, 1], title="NHB")
        KpiComparator._style_axes(np.ravel(axes), rotate_x_labels=60)
        return fig

    def plot_population(self, **kwargs):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(5, 5))
        _ = sns.barplot(ax=ax, data=self._get_results("population", **kwargs), x="run_id", y="num_persons")
        KpiComparator._style_axes([ax], rotate_x_labels=False)
        return fig

    def plot_congestion_pricing(self, **kwargs):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(5, 5))
        df = self._get_results("road_pricing", **kwargs).reset_index(drop=True)
        p = sns.barplot(ax=ax, data=df, x="run_id", y="total_revenue")
        p.set_title("Congestion Pricing Revenue")
        KpiComparator._style_axes([ax], rotate_x_labels=False)
        return fig

    def plot_transit(self, **kwargs):
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        df = self._get_results("transit_boardings", **kwargs)
        df["mode-agency"] = df["mode"] + "-" + df["agency"]
        sns.barplot(data=df, x="mode-agency", y="boardings", hue="run_id", errorbar=None, ax=axes[0]).set_title(
            "Boardings"
        )
        sns.barplot(data=df, x="mode-agency", y="alightings", hue="run_id", errorbar=None, ax=axes[1]).set_title(
            "Alightings"
        )
        KpiComparator._style_axes(axes, rotate_x_labels=False)
        return fig

    def add_iter(x):
        if isinstance(x, pd.DataFrame):
            x["iter"] = x.run_id.str.replace(".*_iteration_", "", regex=True)
        else:
            raise RuntimeError(f"Unknown argument type for add_iter: {type(x)}")
        return x

    def across_iterations(self, cols, **kwargs):
        import matplotlib.pyplot as plt

        df = kwargs["df"]
        x_col = kwargs.get("x", "iter")
        if x_col == "iter" and x_col not in df.columns:
            df = KpiComparator.add_iter(df)
        group_col = kwargs["group_by"]
        groups = df[group_col].unique()
        colors = cycle(sns.color_palette("colorblind") + sns.color_palette("pastel") + sns.color_palette("bright"))

        num_rows = math.ceil((len(cols) + 1) / 2)
        fig, axes = plt.subplots(num_rows, 2, figsize=(12 * num_rows + 4, 15))
        axes = axes.flatten()

        legend = []

        # Add a dummy line using ALL the available x values (in case there are missing values in a group)
        x = sorted(df[x_col].unique())
        dummy_lines = [
            axes[i + 1].plot(x, df[col].mean() * np.ones_like(x, dtype=np.float32)) for i, col in enumerate(cols.keys())
        ]

        agg = kwargs["agg"] if "agg" in kwargs else {k: "mean" for k in cols.keys()}

        # For each identified group...
        for g, color in zip(groups, colors):
            # Filter to just the given group, then average across each unique x-value
            df_ = df[df[group_col] == g].groupby(x_col).agg(agg).reset_index().sort_values(x_col)

            # Add a line to each subplot for the current grouping
            for i, col in enumerate(cols.keys()):
                (line,) = axes[i + 1].plot(df_[x_col], df_[col], color=color, marker="o")
            legend += [(line, g)]

        # Remove the dummy lines
        [line[0].remove() for line in dummy_lines]

        # Set titles for each subplot
        for i, title in enumerate(cols.values()):
            axes[i + 1].set_title(title)

        # Use top left sub-plot for legend and style the axes
        fontsize = np.interp(len(legend), [4, 12], [24, 10], left=24, right=10)
        axes[0].legend([e[0] for e in legend], [e[1] for e in legend], loc="center", fontsize=fontsize)
        KpiComparator._style_axes(axes[1:], rotate_x_labels=60)

        return fig

    def plot_act_dist(self, act_type: Optional[str] = None, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("activity_distances", **kwargs)

        if act_type is not None:
            df = df[df["acttype"].str.upper() == act_type.upper()]
        if df is None or df.empty:
            logging.warning("There were no results for 'activity_distances'")
            return

        if "group_by" in kwargs:
            kwargs["df"] = df
            return self.across_iterations(
                {"ttime_avg": "Travel Time (min)", "dist_avg": "Distance (miles)", "count": "Count"},
                agg={"ttime_avg": "mean", "dist_avg": "mean", "count": "sum"},
                **kwargs,
            )
        else:
            fig, axes = plt.subplots(1, 3, figsize=(28, 5))
            sns.barplot(ax=axes[0], data=df, x="acttype", y="ttime_avg", hue="run_id")
            axes[0].legend([], [], frameon=False)
            sns.barplot(ax=axes[1], data=df, x="acttype", y="dist_avg", hue="run_id")
            axes[1].legend([], [], frameon=False)
            sns.barplot(ax=axes[2], data=df, x="acttype", y="count", hue="run_id")
            KpiComparator._style_axes(axes, rotate_x_labels=60)
            return fig

    def plot_vmt(self, **kwargs):
        if "df" not in kwargs:
            df = self._get_results("vmt_vht", **kwargs).reset_index()

            if "mode" in kwargs:
                df = filter_df(df, {"mode": kwargs["mode"]})

            if df is None or df.empty:
                logging.warning("There were no results for 'vmt'")
                return

            df = df[~(df["mode"].str.contains("FAIL") | df["mode"].str.contains("NO_MOVE"))]
            kwargs["df"] = df.groupby(["mode", "run_id"]).sum().reset_index()

        kwargs["group_by"] = kwargs.get("group_by", "mode")
        cols = {"million_VMT": "VMT (millions)", "speed_mph": "Speed (mi/h)", "count": "Number of trips"}
        kwargs["agg"] = {"million_VMT": "sum", "speed_mph": "mean", "count": "sum"}
        return self.across_iterations(cols, **kwargs)

    def plot_vehicle_connectivity(self, **kwargs):
        import matplotlib.pyplot as plt

        df_veh_tech = self._get_results("vehicle_technology", **kwargs)

        # Add a passenger/truck designation column
        df_veh_tech["fleet_type"] = "passenger"
        df_veh_tech.loc[df_veh_tech.class_type.str.startswith("TRUCK"), "fleet_type"] = "truck"

        # Figure out the percentage (relative to the total pass/truck vehicles for that run) for each row
        group_by_key = kwargs.get("group_by", "run_id")

        # Calculate the proportion of the total (passenger or truck) fleet that each row representes
        key = ["fleet_type", "run_id"]
        df_veh_tech["proportion"] = (
            100.0 * df_veh_tech["veh_count"] / df_veh_tech.groupby(key)["veh_count"].transform("sum")
        )

        _, axes = plt.subplots(1, 1, figsize=(10, 5))
        df_veh_tech["connectivity"] = "Not Connected"
        df_veh_tech.loc[df_veh_tech.connected == "Yes", "connectivity"] = "Connected"

        x_col = kwargs.get("x", "run_id")
        df_ = df_veh_tech.groupby(list({x_col, "connectivity", group_by_key, "fleet_type"})).agg({"proportion": "sum"})
        df_ = df_.reset_index()

        df_["proportion"] = 100.0 - df_["proportion"]
        fig = sns.lineplot(df_, x=x_col, y="proportion", hue=group_by_key, ax=axes, style="fleet_type")
        fig.legend(loc="center left", bbox_to_anchor=(1.05, 0.5), ncol=1)

        axes.set_title("Proportion of Connected Vehicles within Fleet")
        axes.set_ylabel("Proportion (%)")

    @staticmethod
    def _style_axes(axes, grid=True, rotate_x_labels=False, fontsize=14, titles=None, suptitle=None):
        for ax in axes:
            if grid:
                ax.grid(True, which="both", axis="y", color="#000000", alpha=0.15, zorder=0)
            if rotate_x_labels:
                ax.tick_params(axis="x", rotation=rotate_x_labels)
            if fontsize is not None:
                ax.tick_params(axis="x", labelsize=fontsize)
                ax.set_title(ax.get_title(), fontsize=fontsize + 4)

        if titles is not None:
            [ax.set_title(title) for (ax, title) in zip(axes, titles)]
        if suptitle is not None:
            import matplotlib.pyplot as plt

            plt.suptitle(suptitle)

    @staticmethod
    def _style_target_bars(patches):
        import matplotlib.pyplot as plt

        plt.setp(patches, linewidth=2, edgecolor="#000000aa", zorder=2, facecolor="#ffffff11", linestyle="--")

    def plot_vmt_by_link_type(self, **kwargs):
        import matplotlib.pyplot as plt

        if (df := self._get_results("vmt_vht_by_link", **kwargs)) is None:
            logging.info("No data for vmt_vht_by_link")
            return

        df = df.groupby(["type", "run_id"]).sum().reset_index()

        def add_speed(label, hours):
            vmt = df[[f"vmt_{i}" for i in hours]]
            vht = df[[f"vht_{i}" for i in hours]]
            df[f"speed_{label}"] = vmt.sum(axis=1) / vht.sum(axis=1)

        add_speed("daily", ["daily"])
        add_speed("am_peak", [6, 7, 8])
        add_speed("pm_peak", [15, 16, 17])
        add_speed("off_peak", set(range(0, 24)) - {6, 7, 8} - {15, 16, 17})

        fig, axes = plt.subplots(2, 2, figsize=(15, 11))
        axes = np.ravel(axes)
        _ = sns.barplot(df, x="type", y="vmt_daily", hue="run_id", ax=axes[0], errorbar=None)
        _ = sns.barplot(df, x="type", y="speed_off_peak", hue="run_id", ax=axes[1], errorbar=None)
        _ = sns.barplot(df, x="type", y="speed_am_peak", hue="run_id", ax=axes[2], errorbar=None)
        _ = sns.barplot(df, x="type", y="speed_pm_peak", hue="run_id", ax=axes[3], errorbar=None)
        KpiComparator._style_axes(axes, rotate_x_labels=30)

        return fig

    def plot_gaps(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("gaps", **kwargs)
        if df is None or df.empty:
            logging.warning("No gap data for this run")
            return
        fig = plt.figure(figsize=(16, 6))
        colors = sns.color_palette(n_colors=3)
        fig.gca().plot(df["run_id"], df["relative_gap"], color=colors[0], marker="o")
        fig.gca().plot(df["run_id"], df["relative_gap_abs"], color=colors[1], marker="o")
        fig.gca().plot(df["run_id"], df["relative_gap_min0"], color=colors[2], marker="o")
        fig.gca().legend(["relative_gap", "relative_gap_abs", "relative_gap_min0"])
        KpiComparator._style_axes([fig.gca()], rotate_x_labels=30)
        return fig

    @staticmethod
    def plot_multiple_gaps(kpi_results):
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(16, 6))
        colors = sns.color_palette(n_colors=len(kpi_results))
        i = 0
        for id, k in ((id, k) for id, k in kpi_results.items() if k is not None):
            df = k._get_results("gaps", False, False)
            if df is None:
                logging.error("df is None?")
                continue
            df = df.sort_values("run_id")
            fig.gca().plot(df["run_id"], df["relative_gap"], color=colors[i], marker="o", label=id)
            i = i + 1
        fig.gca().grid(True, which="both", color="#000000", alpha=0.2)
        return fig

    def plot_pax_in_network(self, **kwargs):
        import matplotlib.pyplot as plt

        # this has a problem if there are missing values in the summary file, filter to X to select only the bits that exist for all summary files
        df = self._get_results("summary", **kwargs)
        df = df[df.simulated_time < 86340]
        df.sort_values(["run_id", "simulated_time"], inplace=True)

        fig = plt.figure(figsize=(16, 6))
        run_ids = sorted(df.run_id.unique())
        colors = sns.color_palette("blend:#7AB,#EDA", n_colors=len(run_ids))

        colors = sns.color_palette("flare", n_colors=len(run_ids))
        colors = sns.color_palette("light:#5A9", n_colors=len(run_ids))

        for run_id, color in zip(run_ids, colors):
            df_ = df[df.run_id == run_id]
            fig.gca().plot(df_["simulated_time"] / 3600, df_["pax_in_network"], color=color)

        KpiComparator._style_axes([fig.gca()], rotate_x_labels=False)
        fig.gca().legend(run_ids)
        return fig

    def plot_cpu_mem(self, **kwargs):
        import matplotlib.pyplot as plt

        if (df := self._get_results("summary", **kwargs)) is None:
            logging.info("No summary file data available")
            return

        df = df[["simulated_time", "wallclock_time(ms)", "physical_memory_usage", "run_id"]]
        df["hour"] = df["simulated_time"] / 3600
        df["runtime"] = df["wallclock_time(ms)"] / 1000

        fig, ax = plt.subplots(1, 2, figsize=(20, 7))

        sns.lineplot(data=df, x="hour", y="physical_memory_usage", hue="run_id", ax=ax[0])
        sns.lineplot(data=df, x="hour", y="runtime", hue="run_id", ax=ax[1])

        ax[0].set_ylim(0, ax[0].get_ylim()[1])
        ax[0].set_ylabel("Peak memory (MB)")
        ax[1].set_ylabel("Runtime (s)")
        fig.suptitle("Runtime and Memory usage")

        return fig

    def plot_network_gaps(self, **kwargs):
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(15, 15))

        df = self._get_results("network_gaps_by_link_type", **kwargs)
        sns.barplot(df, x="link_type", y="abs_gap", hue="run_id", ax=axes[0, 0], errorbar=None).set_title("Gap (abs)")
        sns.barplot(df, x="link_type", y="gap", hue="run_id", ax=axes[0, 1], errorbar=None).set_title("Gap")
        KpiComparator._style_axes(axes[0, :], rotate_x_labels=60)

        df = self._get_results("network_gaps_by_hour", **kwargs)
        df.fillna(0.0, inplace=True)  # early morning hours have some weird values
        sns.lineplot(df, x="hour", y="abs_gap", hue="run_id", ax=axes[1, 0], errorbar=None).set_title("Gap (abs)")
        sns.lineplot(df, x="hour", y="gap", hue="run_id", ax=axes[1, 1], errorbar=None).set_title("Gap")
        KpiComparator._style_axes(axes[1, :], rotate_x_labels=False)
        return fig

    def plot_skim_stats(self, show_min_max=False, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("skim_stats", **kwargs)
        df.sort_values("interval", inplace=True)
        if df is None or df.empty:
            logging.warning("No skim stats to plot")
            return

        def f(metric, mode, ax, ylabel):
            df_ = df[(df.metric == metric) & (df["mode"] == mode)]
            run_ids = df.run_id.unique()
            colors = sns.color_palette(n_colors=len(run_ids))
            line_width = 3
            for run_id, color in zip(run_ids, colors):
                df__ = df_[df_.run_id == run_id]
                x = (df__["interval"] / 60).astype(int)

                ax.plot(x, df__["avg"], linestyle="-", color=color, label=run_id, linewidth=line_width)
                line_width -= 0.5
                if show_min_max:
                    ax.plot(x, df__["min"], linestyle="--", color=color)
                    ax.plot(x, df__["max"], linestyle="--", color=color)
            ax.legend()
            ax.set_xticks(x)
            ax.set_ylabel(ylabel)

        fig, axes = plt.subplots(4, 1, figsize=(20, 5 * 4))
        fig.suptitle("Skim change over time (min/max dashed, avg solid)")
        f("time", "Auto", ax=axes[0], ylabel="Time (min)")
        f("distance", "Auto", ax=axes[1], ylabel="Distance (m)")
        f("time", "Bus", ax=axes[2], ylabel="Bus Time (min)")
        f("time", "Rail", ax=axes[3], ylabel="Rail Time (min)")
        KpiComparator._style_axes(axes)
        return fig

    def plot_trip_length_distributions(self, max_dist=None, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("trip_length_distribution", **kwargs)
        if df is None or df.empty:
            logging.warning("No TLfD stats to plot")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        for run_id in df.run_id.unique():
            df_ = df[df.run_id == run_id]
            df_ = df_.sort_values(by="distance")

            # For large models, using 200 to 400 bins yields much better curves
            ax.plot(df_.distance, df_.trips, label=run_id)

        if max_dist is not None:
            ax.set_xlim(0, max_dist)

        ax.legend(loc="upper right")
        ax.set(title="Trip length distribution")
        ax.set_ylabel("km")
        ax.set_ylabel("Trips")
        return fig

    def plot_activity_start_time_distributions(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("activity_start_time_distributions", **kwargs)
        if df is None or df.empty:
            logging.warning("No trip departure time data to plot")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        for run_id in df.run_id.unique():
            df_ = df[df.run_id == run_id]
            df_ = df_.sort_values(by="trip_start")

            # For large models, using 200 to 400 bins yields much better curves
            ax.plot(df_.trip_start, df_.trips, label=run_id)

        ax.legend(loc="upper right")
        ax.set(title="Activity Start distribution")
        ax.set_ylabel("km")
        ax.set_ylabel("Trips")
        return fig

    def plot_tnc(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("tnc_request_stats", **kwargs)
        df["operator_mode"] = df["tnc_operator"] + "-mode_" + df["service_mode"].astype(str)

        if df is None or df.empty:
            logging.warning("There were no results for 'tnc_request_stats'")
            return

        fig, axes = plt.subplots(1, 3, figsize=(20, 8))

        def f(y, ax, title, ylabel):
            sns.barplot(df, x="operator_mode", y=y, hue="run_id", ax=ax)
            ax.set(title=title)
            ax.set_xlabel(None)
            ax.set_ylabel(ylabel)

        f("demand", axes[0], title="Demand", ylabel="trips")
        f("wait", axes[1], title="Wait time", ylabel="hours")
        f("ivtt", axes[2], title="IVTT", ylabel="hours")
        KpiComparator._style_axes(np.ravel(axes), rotate_x_labels=30)
        return fig

    def plot_rmse_vs_observed(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("rmse_vs_observed", **kwargs)

        if df is None or df.empty:
            logging.warning("There were no results for RMSEs")
            return

        fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(20, 8))

        def f(y, ax, title):
            sns.barplot(df, hue="run_id", y=y, ax=ax)
            ax.set(title=title, xlabel=None, ylabel=None)

        f("RMSE_activity", axes[0], title="Activity Generation")
        f("RMSE_mode", axes[1], title="Mode Share")
        f("RMSE_mode_boardings", axes[2], title="Mode Boardings")
        f("RMSE_destination", axes[3], title="TTime by Activity")
        f("RMSE_timing", axes[4], title="Departure Time")
        KpiComparator._style_axes(np.ravel(axes), rotate_x_labels=30)
        return fig

    def _overlay_barplots(self, df, x_col, ax, title):
        sns.barplot(data=df, x=x_col, y="target", errorbar=None, color="white", width=0.85, ax=ax)
        KpiComparator._style_target_bars(ax.patches)
        sns.barplot(data=df, x=x_col, y="simulated", hue="run_id", errorbar=None, ax=ax, width=0.75)
        ax.set(title=title, xlabel=None, ylabel=None)

    def plot_calibration_for_activity_generation(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("calibration_act_gen", **kwargs)

        if df is None or df.empty:
            logging.warning("There were no results for calibrating activity generation")
            return

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))
        self._overlay_barplots(df, "acttype", axes[0], "By Activity Type")
        self._overlay_barplots(df, "pertype", axes[1], "By Person Type")

        fig.suptitle("Activity Generation Calibration", fontsize=16)
        fig.subplots_adjust(hspace=0.3)
        KpiComparator._style_axes(axes, rotate_x_labels=50, fontsize=12)

        return fig

    def plot_calibration_for_mode_share(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("calibration_mode_share", **kwargs)

        if df is None or df.empty:
            logging.warning("There were no results for calibrating mode share")
            return

        fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(20, 8), sharey="col")

        self._overlay_barplots(df[df["type"] == "HBW"], "mode", axes[0], "Home-Based Work")
        self._overlay_barplots(df[df["type"] == "HBO"], "mode", axes[1], "Home-Based Other")
        self._overlay_barplots(df[df["type"] == "NHB"], "mode", axes[2], "Non Home-Based")
        self._overlay_barplots(df[df["type"] == "TOTAL"], "mode", axes[3], "Total")

        fig.suptitle("Mode Share Calibration", fontsize=16)
        KpiComparator._style_axes(axes, rotate_x_labels=50, fontsize=12)

        return fig

    def plot_calibration_timing(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("calibration_timing", **kwargs)

        if df is None or df.empty:
            logging.warning("There were no results for calibrating timing choice")
            return

        def f(act_type, ax, title):
            self._overlay_barplots(df[df["act_type"] == act_type], "period", ax, title)

        activities = df["act_type"].unique()
        activities = activities[activities != "TOTAL"]
        activities = np.append(activities, "TOTAL")

        df.period = df.period.map(
            {
                "NIGHT": "00:00 to 06:00",
                "AMPEAK": "06:00 to 09:00",
                "AMOFFPEAK": "09:00 to 12:00",
                "PMOFFPEAK": "12:00 to 16:00",
                "PMPEAK": "16:00 to 19:00",
                "EVENING": "19:00 to 24:00",
            }
        )
        df = df.sort_values("period")

        ncols = 6
        nrows = len(activities) // ncols + 1
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20, 8), sharey="all", sharex="all")
        axes = axes.reshape(-1)
        for i, act_type in enumerate(activities):
            f(act_type, axes[i], act_type)
            axes[i].set_ylim(0, 1)
            for side in ["top", "left", "right"]:
                axes[i].spines[side].set_visible(False)
                axes[i].tick_params(axis="y", which="major", length=0)

        KpiComparator._style_axes(axes, rotate_x_labels=90, fontsize=12)
        for j in range(i + 1, nrows * ncols):
            axes[j].set_frame_on(False)
            axes[j].grid(False)
            axes[j].tick_params(axis="y", which="major", length=0)

        fig.suptitle("Timing Choice Calibration", fontsize=16)
        fig.subplots_adjust(hspace=0.3)
        return fig

    def plot_calibration_destination(self, **kwargs):
        import matplotlib.pyplot as plt

        df = self._get_results("calibration_destination", **kwargs)

        if df is None or df.empty:
            logging.warning("There were no results for calibrating destination choice")
            return

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 8), sharey="all", sharex="all")
        self._overlay_barplots(df, "acttype", ax, "Trip Distance Calibration")
        KpiComparator._style_axes([ax], rotate_x_labels=50, fontsize=14)

        return fig

    def _get_results(self, result_name, **kwargs):
        """Collates together dataframes from each run and annotates them appropriately."""
        if "df" in kwargs:
            # Allow a user to pass in a pre-existing data frame
            df = kwargs["df"]
        else:
            run_ids = self._limit_run_ids(**kwargs)
            skip_cache = kwargs.get("skip_cache", False)
            force_cache = kwargs.get("force_cache", False)
            dfs = [
                self._maybe_metric(result_name, kpi, run_id, skip_cache=skip_cache, force_cache=force_cache)
                for run_id, kpi in self.runs.items()
                if run_id in run_ids
            ]
            dfs = [df for df in dfs if df is not None and not df.empty]
            if not dfs:
                return None
            df = pd.concat(dfs)

        if kwargs.get("df_transform", None) is not None:
            df = kwargs["df_transform"](df)
        if kwargs.get("df_filter", None) is not None:
            df = filter_df(df, kwargs["df_filter"])
        if (sort_key := kwargs.get("sort_key", None)) is not None:
            if callable(sort_key):
                df.sort_values(by="run_id", key=sort_key, inplace=True)
            else:
                df.sort_values(by=sort_key, inplace=True)
        else:
            df.sort_values(by="run_id", inplace=True)
        return df

    def _limit_run_ids(self, **kwargs):
        limit_runs = kwargs.get("limit_runs", None)
        if limit_runs is None:
            return set(self.runs.keys())

        # limit runs
        if isinstance(limit_runs, int):
            # limit_runs is a number of runs to show (either first N if N>0, or last N otherwise)
            run_ids = list(self.runs.keys())
            return set(run_ids[-limit_runs:]) if limit_runs > 0 else set(run_ids[:-limit_runs])
        elif isinstance(limit_runs, Pattern):
            return {r for r in self.runs.keys() if limit_runs.match(r)}
        else:
            return {r for r in self.runs.keys() if limit_runs(r)}
        return set(limit_runs)

    def _maybe_metric(self, metric, kpi, run_id, skip_cache, force_cache):
        try:
            return self._add_run_attributes(
                kpi.get_cached_kpi_value(metric, skip_cache=skip_cache, force_cache=force_cache), run_id
            )
        except Exception:
            tb = traceback.format_exc()
            logging.info(f"Exception while getting {metric} for {run_id}")
            logging.info(tb)
            return None
        finally:
            kpi.close()

    def _add_run_attributes(self, df, run_id):
        return df if df is None or not isinstance(df, pd.DataFrame) else df.assign(run_id=run_id)
