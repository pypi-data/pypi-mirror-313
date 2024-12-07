import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import warnings
import logging
from typing import Union
from .ips import (
    isa,
    fsave,
    fload,
    mkdir,
    listdir,
    figsave,
    strcmp,
    unique,
    get_os,
    ssplit,
    flatten,
    plt_font,
    run_once_within,
    df_format,
    df_corr,
    df_scaler
)
import scipy.stats as scipy_stats
from .stats import *
import os

# Suppress INFO messages from fontTools
logging.getLogger("fontTools").setLevel(logging.ERROR)
logging.getLogger("matplotlib").setLevel(logging.ERROR)

warnings.simplefilter("ignore", category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)


def add_text(ax=None, height_offset=0.5, fmt=".1f", **kwargs):
    """Adds text annotations for various types of Seaborn and Matplotlib plots.
    Args:
        ax: Axes object.
        height_offset: 0.5 (default) The vertical distance (offset) to place the text.
        fmt: Default is ".1f" for one decimal place.
        **kwargs: Additional keyword arguments for the text function
    Usage:
        ax = sns.barplot(x='Category', y='Values', data=data)
        add_text(ax=ax, height_offset=1.0, color='black', fontsize=12)

    The function will automatically detect the type of plot and add annotations accordingly.
    It supports annotations for:
    - **Bar Plots**: Displays the height of each bar.
    - **Box Plots**: Shows the height of the boxes.
    - **Scatter and Line Plots**: Displays the y-value for each point.
    - **Histograms and KDE Plots**: Shows the maximum height of the bars.
    - **Other Plots**: If the Axes contains containers, it handles those as well.
    """
    from matplotlib.collections import LineCollection

    ha = kwargs.pop("ha", "center")
    va = kwargs.pop("va", "bottom")
    if ax is None:
        ax = plt.gca()
    # Check if the Axes has patches (for bar, count, boxen, violin, and other plots with bars)
    # Check for artists (for box plots)
    if hasattr(ax, "artists") and ax.artists:
        print("artists")
        for box in ax.artists:
            if hasattr(box, "get_height") and hasattr(box, "get_y"):
                height = box.get_y() + box.get_height()  # For box plots

                ax.text(
                    box.get_x() + box.get_width() / 2.0,
                    height + height_offset,
                    format(height, fmt),
                    ha=ha,
                    va=va,
                    **kwargs,
                )

    # Scatter plot or line plot
    if hasattr(ax, "lines"):
        print("lines")
        for line in ax.lines:
            if hasattr(line, "get_xydata"):
                xdata, ydata = line.get_xydata().T  # Get x and y data points
                for x, y in zip(xdata, ydata):
                    ax.text(x, y + height_offset, format(y, fmt), **kwargs)

    if hasattr(ax, "patches") and ax.patches:
        print("patches")
        for p in ax.patches:
            if hasattr(p, "get_height"):
                height = p.get_height()  # For bar plots

                ax.text(
                    p.get_x() + p.get_width() / 2.0,
                    height + height_offset,
                    format(height, fmt),
                    ha=ha,
                    va=va,
                    **kwargs,
                )
    # For histplot, kdeplot, rugplot
    if hasattr(ax, "collections"):
        print("collections")
        for collection in ax.collections:
            # If it is a histogram or KDE plot
            if isinstance(collection, LineCollection):
                for path in collection.get_paths():
                    if hasattr(path, "vertices"):
                        vertices = path.vertices
                        # Get the heights (y values) for histogram or KDE plots
                        ax.text(
                            vertices[:, 0].mean(),
                            vertices[:, 1].max() + height_offset,
                            format(vertices[:, 1].max(), fmt),
                            **kwargs,
                        )
            # Handle point, strip, and swarm plots
            elif isinstance(collection, LineCollection):
                for path in collection.get_paths():
                    vertices = path.vertices
                    ax.text(
                        vertices[:, 0].mean(),
                        vertices[:, 1].max() + height_offset,
                        format(vertices[:, 1].max(), fmt),
                        **kwargs,
                    )
        # Handle bar charts (not from seaborn)
    if hasattr(ax, "containers"):
        print("containers")
        for container in ax.containers:
            for bar in container:
                if hasattr(bar, "get_height"):
                    height = bar.get_height()

                    ax.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        height + height_offset,
                        format(height, fmt),
                        ha=ha,
                        va=va,
                        **kwargs,
                    )

def pval2str(p):
    if p > 0.05:
        txt = ""
    elif 0.01 <= p <= 0.05:
        txt = "*"
    elif 0.001 <= p < 0.01:
        txt = "**"
    elif p < 0.001:
        txt = "***"
    return txt

def heatmap(
    data,
    ax=None,
    kind="corr",  #'corr','direct','pivot'
    method="pearson",# for correlation: ‘pearson’(default), ‘kendall’, ‘spearman’
    columns="all",  # pivot, default: coll numeric columns
    style=0,# for correlation
    index=None,  # pivot
    values=None,  # pivot
    fontsize=10, 
    tri="u",
    mask=True,
    k=1,
    vmin=None,
    vmax=None,
    size_scale=500,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    show_indicator = True,# only for style==1
    cluster=False,
    inplace=False,
    figsize=(10, 8),
    row_cluster=True,  # Perform clustering on rows
    col_cluster=True,  # Perform clustering on columns
    dendrogram_ratio=(0.2, 0.1),  # Adjust size of dendrograms
    cbar_pos=(0.02, 1, 0.02, 0.1),  # Adjust colorbar position
    xticklabels=True,  # Show column labels
    yticklabels=True,  # Show row labels
    **kwargs,
):
    """
    plot heatmap or clustermap for a given dataset (DataFrame).

    Parameters:
    - data (pd.DataFrame): The input data to visualize.
    - ax (matplotlib.Axes, optional): Axis object to plot on. If None and cluster=False, a new axis is created.
    - kind (str, default="corr"): Type of heatmap to plot. Options:
        - "corr": Correlation heatmap based on numeric columns.
        - "direct": Direct visualization of the numeric data.
        - "pivot": Creates a heatmap using the `pivot_table` method.
    - columns (str or list, default="all"): Columns to include in the heatmap. For pivoting, this specifies the 'columns' argument.
    - index (str, optional): For pivot heatmap, sets the 'index' argument.
    - values (str, optional): For pivot heatmap, sets the 'values' argument.
    - tri (str, default="u"): Specifies whether to show the 'upper' or 'lower' triangle in the heatmap.
    - mask (bool, default=True): Whether to mask half of the correlation matrix.
    - k (int, default=1): Controls how much of the triangle is masked in correlation heatmaps.
    - annot (bool, default=True): If True, writes the data values in each cell.
    - cmap (str, default="coolwarm"): The colormap for the heatmap.
    - fmt (str, default=".2f"): String formatting code for annotating cells.
    - cluster (bool, default=False): If True, a clustermap with hierarchical clustering is plotted.
    - inplace (bool, default=False): If True, modifies the original data. Not currently used.
    - figsize (tuple, default=(10, 8)): Size of the figure for the heatmap.
    - row_cluster (bool, default=True): Perform clustering on rows.
    - col_cluster (bool, default=True): Perform clustering on columns.
    - dendrogram_ratio (tuple, default=(0.2, 0.1)): Adjust the size of the dendrograms.
    - cbar_pos (tuple, default=(0.02, 1, 0.02, 0.1)): Adjust the position of the colorbar.
    - xticklabels (bool, default=True): Show or hide the column labels.
    - yticklabels (bool, default=True): Show or hide the row labels.
    - **kwargs: Additional arguments passed to `sns.heatmap` or `sns.clustermap`.
    """
    if ax is None and not cluster:
        ax = plt.gca()
    # Select numeric columns or specific subset of columns
    if columns == "all":
        df_numeric = data.select_dtypes(include=[np.number])
    else:
        df_numeric = data[columns]

    kinds = ["corr", "direct", "pivot"]
    kind = strcmp(kind, kinds)[0]
    print(kind)
    if "corr" in kind:  # correlation
        methods = ["pearson", "spearman", "kendall"]
        method = strcmp(method, methods)[0]
        # Compute the correlation matrix
        data4heatmap = df_numeric.corr(method=method)
        # Generate mask for the upper triangle if mask is True
        if mask:
            if "u" in tri.lower():  # upper => np.tril
                mask_array = np.tril(np.ones_like(data4heatmap, dtype=bool), k=k)
            else:  # lower => np.triu
                mask_array = np.triu(np.ones_like(data4heatmap, dtype=bool), k=k)
        else:
            mask_array = None

        # Remove conflicting kwargs
        kwargs.pop("mask", None)
        kwargs.pop("annot", None)
        kwargs.pop("cmap", None)
        kwargs.pop("fmt", None)

        kwargs.pop("clustermap", None)
        kwargs.pop("row_cluster", None)
        kwargs.pop("col_cluster", None)
        kwargs.pop("dendrogram_ratio", None)
        kwargs.pop("cbar_pos", None)
        kwargs.pop("xticklabels", None)
        kwargs.pop("col_cluster", None)

        # Plot the heatmap or clustermap
        if cluster:
            # Create a clustermap
            cluster_obj = sns.clustermap(
                data4heatmap,
                # ax=ax,
                mask=mask_array,
                annot=annot,
                cmap=cmap,
                fmt=fmt,
                figsize=figsize,  # Figure size, adjusted for professional display
                row_cluster=row_cluster,  # Perform clustering on rows
                col_cluster=col_cluster,  # Perform clustering on columns
                dendrogram_ratio=dendrogram_ratio,  # Adjust size of dendrograms
                cbar_pos=cbar_pos,  # Adjust colorbar position
                xticklabels=xticklabels,  # Show column labels
                yticklabels=yticklabels,  # Show row labels
                **kwargs,  # Pass any additional arguments to sns.clustermap
            )
            df_row_cluster = pd.DataFrame()
            df_col_cluster = pd.DataFrame()
            if row_cluster:
                from scipy.cluster.hierarchy import linkage, fcluster
                from scipy.spatial.distance import pdist

                # Compute pairwise distances
                distances = pdist(data, metric="euclidean")
                # Perform hierarchical clustering
                linkage_matrix = linkage(distances, method="average")
                # Get cluster assignments based on the distance threshold
                row_clusters_value = fcluster(
                    linkage_matrix, t=1.5, criterion="distance"
                )
                df_row_cluster["row_cluster"] = row_clusters_value
            if col_cluster:
                col_distances = pdist(
                    data4heatmap.T, metric="euclidean"
                )  # Transpose for column clustering
                col_linkage_matrix = linkage(col_distances, method="average")
                col_clusters_value = fcluster(
                    col_linkage_matrix, t=1.5, criterion="distance"
                )
                df_col_cluster = pd.DataFrame(
                    {"Cluster": col_clusters_value}, index=data4heatmap.columns
                )

            return (
                cluster_obj.ax_row_dendrogram,
                cluster_obj.ax_col_dendrogram,
                cluster_obj.ax_heatmap,
                df_row_cluster,
                df_col_cluster,
            )
        else:
            if style==0:
                # Create a standard heatmap
                ax = sns.heatmap(
                    data4heatmap,
                    ax=ax,
                    mask=mask_array,
                    annot=annot,
                    cmap=cmap,
                    fmt=fmt,
                    **kwargs,  # Pass any additional arguments to sns.heatmap
                )
                return ax
            elif style==1:
                if isinstance(cmap, str):
                    cmap = plt.get_cmap(cmap)
                norm = plt.Normalize(vmin=-1, vmax=1)
                r_, p_ = df_corr(data4heatmap, method=method)
                # size_r_norm=df_scaler(data=r_, method="minmax", vmin=-1,vmax=1)
                # 初始化一个空的可绘制对象用于颜色条
                scatter_handles = []
                # 循环绘制气泡图和数值
                for i in range(len(r_.columns)):
                    for j in range(len(r_.columns)):
                        if (i < j) if "u" in tri.lower() else (j<i):  # 对角线左上部只显示气泡
                            color = cmap(norm(r_.iloc[i, j]))  # 根据相关系数获取颜色
                            scatter = ax.scatter(
                                i, j, s=np.abs(r_.iloc[i, j])*size_scale, color=color, 
                                # alpha=1,edgecolor=edgecolor,linewidth=linewidth,
                                **kwargs
                            )
                            scatter_handles.append(scatter)  # 保存scatter对象用于颜色条
                            # add *** indicators
                            if show_indicator:
                                ax.text(
                                    i,
                                    j,
                                    pval2str(p_.iloc[i, j]),
                                    ha="center",
                                    va="center",
                                    color="k",
                                    fontsize=fontsize * 1.3,
                                )
                        elif (i > j) if "u" in tri.lower() else (j>i):  # 对角只显示数值
                            color = cmap(norm(r_.iloc[i, j]))  # 数值的颜色同样基于相关系数
                            ax.text(
                                i,
                                j,
                                f"{r_.iloc[i, j]:{fmt}}",
                                ha="center",
                                va="center",
                                color=color,
                                fontsize=fontsize,
                            )
                        else:  # 对角线部分，显示空白
                            ax.scatter(i, j, s=1, color="white")
                # 设置坐标轴标签
                figsets(xticks=range(len(r_.columns)),
                        xticklabels=r_.columns, 
                        xangle=90,
                        fontsize=fontsize,
                        yticks=range(len(r_.columns)),
                        yticklabels=r_.columns,
                        xlim=[-0.5,len(r_.columns)-0.5],
                        ylim=[-0.5,len(r_.columns)-0.5]
                        ) 
                # 添加颜色条
                sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
                sm.set_array([])  # 仅用于显示颜色条
                plt.colorbar(sm, ax=ax, label="Correlation Coefficient")
                return ax
    elif "dir" in kind:  # direct
        data4heatmap = df_numeric
    elif "pi" in kind:  # pivot
        try:
            print(
                f'pivot: \n\tneed at least 3 param: e.g., index="Task", columns="Model", values="Score"'
            )
            data4heatmap = data.pivot(index=index, columns=columns, values=values)
        except:
            print(
                f'pivot_table: \n\tneed at least 4 param: e.g., index="Task", columns="Model", values="Score",aggfunc="mean"'
            )
            aggfunc = "mean"
            for k_, v_ in kwargs.items():
                if "agg" in k_.lower():
                    aggfunc = v_
            kwargs.pop(k_, None)
            data4heatmap = data.pivot_table(
                index=index, columns=columns, values=values, aggfunc=aggfunc
            )
    else:
        print(f'"{kind}" is not supported')
    # Remove conflicting kwargs
    kwargs.pop("mask", None)
    kwargs.pop("annot", None)
    kwargs.pop("cmap", None)
    kwargs.pop("fmt", None)

    kwargs.pop("clustermap", None)
    kwargs.pop("row_cluster", None)
    kwargs.pop("col_cluster", None)
    kwargs.pop("dendrogram_ratio", None)
    kwargs.pop("cbar_pos", None)
    kwargs.pop("xticklabels", None)
    kwargs.pop("col_cluster", None)

    # Plot the heatmap or clustermap
    if cluster:
        # Create a clustermap
        cluster_obj = sns.clustermap(
            data4heatmap,
            # ax=ax,
            # mask=mask_array,
            annot=annot,
            cmap=cmap,
            fmt=fmt,
            figsize=figsize,  # Figure size, adjusted for professional display
            row_cluster=row_cluster,  # Perform clustering on rows
            col_cluster=col_cluster,  # Perform clustering on columns
            dendrogram_ratio=dendrogram_ratio,  # Adjust size of dendrograms
            cbar_pos=cbar_pos,  # Adjust colorbar position
            xticklabels=xticklabels,  # Show column labels
            yticklabels=yticklabels,  # Show row labels
            **kwargs,  # Pass any additional arguments to sns.clustermap
        )
        df_row_cluster = pd.DataFrame()
        df_col_cluster = pd.DataFrame()
        if row_cluster:
            from scipy.cluster.hierarchy import linkage, fcluster
            from scipy.spatial.distance import pdist

            # Compute pairwise distances
            distances = pdist(data, metric="euclidean")
            # Perform hierarchical clustering
            linkage_matrix = linkage(distances, method="average")
            # Get cluster assignments based on the distance threshold
            row_clusters_value = fcluster(linkage_matrix, t=1.5, criterion="distance")
            df_row_cluster["row_cluster"] = row_clusters_value
        if col_cluster:
            col_distances = pdist(
                data4heatmap.T, metric="euclidean"
            )  # Transpose for column clustering
            col_linkage_matrix = linkage(col_distances, method="average")
            col_clusters_value = fcluster(
                col_linkage_matrix, t=1.5, criterion="distance"
            )
            df_col_cluster = pd.DataFrame(
                {"Cluster": col_clusters_value}, index=data4heatmap.columns
            )

        return (
            cluster_obj.ax_row_dendrogram,
            cluster_obj.ax_col_dendrogram,
            cluster_obj.ax_heatmap,
            df_row_cluster,
            df_col_cluster,
        )
    else:
        # Create a standard heatmap
        if style==0:
            ax = sns.heatmap(
                data4heatmap,
                ax=ax,
                annot=annot,
                cmap=cmap,
                fmt=fmt,
                **kwargs,  # Pass any additional arguments to sns.heatmap
            )
            # Return the Axes object for further customization if needed
            return ax            
        elif style==1:
            if isinstance(cmap, str):
                cmap = plt.get_cmap(cmap)
            if vmin is None:
                vmin=np.min(data4heatmap)
            if vmax is None:
                vmax=np.max(data4heatmap)
            norm = plt.Normalize(vmin=vmin, vmax=vmax)

            # 初始化一个空的可绘制对象用于颜色条
            scatter_handles = []
            # 循环绘制气泡图和数值 
            print(len(data4heatmap.index),len(data4heatmap.columns))
            for i in range(len(data4heatmap.index)):
                for j in range(len(data4heatmap.columns)):
                    color = cmap(norm(data4heatmap.iloc[i, j]))  # 根据相关系数获取颜色
                    scatter = ax.scatter(j,i, s=np.abs(data4heatmap.iloc[i, j])*size_scale, color=color, **kwargs)
                    scatter_handles.append(scatter)  # 保存scatter对象用于颜色条

            # 设置坐标轴标签
            figsets(xticks=range(len(data4heatmap.columns)),
                    xticklabels=data4heatmap.columns, 
                    xangle=90,
                    fontsize=fontsize,
                    yticks=range(len(data4heatmap.index)),
                    yticklabels=data4heatmap.index,
                    xlim=[-0.5,len(data4heatmap.columns)-0.5],
                    ylim=[-0.5,len(data4heatmap.index)-0.5]
                    ) 
            # 添加颜色条
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])  # 仅用于显示颜色条
            plt.colorbar(sm, ax=ax, 
                        #  label="Correlation Coefficient"
                         )
            return ax


# !usage: py2ls.plot.heatmap()
# penguins_clean = penguins.replace([np.inf, -np.inf], np.nan).dropna()
# from py2ls import plot

# _, axs = plt.subplots(2, 2, figsize=(10, 10))
# # kind='pivot'
# plot.heatmap(
#     ax=axs[0][0],
#     data=sns.load_dataset("glue"),
#     kind="pi",
#     index="Model",
#     columns="Task",
#     values="Score",
#     fmt=".1f",
#     cbar_kws=dict(shrink=1),
#     annot_kws=dict(size=7),
# )
# # kind='direct'
# plot.heatmap(
#     ax=axs[0][1],
#     data=sns.load_dataset("penguins").iloc[:10, 2:6],
#     kind="direct",
#     tri="lower",
#     fmt=".1f",
#     k=1,
#     cbar_kws=dict(shrink=1),
#     annot_kws=dict(size=7),
# )

# # kind='corr'
# plot.heatmap(
#     ax=axs[1][0],
#     data=sns.load_dataset("penguins"),
#     kind="corr",
#     fmt=".1f",
#     k=-1,
#     cbar_kws=dict(shrink=1),
#     annot_kws=dict(size=7),
# )
# # kind='corr'
# plot.heatmap(
#     ax=axs[1][1],
#     data=penguins_clean.iloc[:15, :10],
#     kind="direct",
#     tri="lower",
#     fmt=".1f",
#     k=1,
#     annot=False,
#     cluster=True,
#     cbar_kws=dict(shrink=1),
#     annot_kws=dict(size=7),
# )


def catplot(data, *args, **kwargs):
    """
    catplot(data, opt=None, ax=None)
    The catplot function is designed to provide a flexible way to create various types of
    categorical plots. It supports multiple plot layers such as bars, error bars, scatter
    plots, box plots, violin plots, and lines. Each plot type is handled by its own internal
    function, allowing for separation of concerns and modularity in the design.
    Args:
        data (array): data matrix
    """
    from matplotlib.colors import to_rgba
    import os

    def plot_bars(data, data_m, opt_b, xloc, ax, label=None):
        if "l" in opt_b["loc"]:
            xloc_s = xloc - opt_b["x_dist"]
        elif "r" in opt_b["loc"]:
            xloc_s = xloc + opt_b["x_dist"]
        elif "i" in opt_b["loc"]:
            xloc_s = xloc
            xloc_s[:, 0] += opt_b["x_dist"]
            xloc_s[:, -1] -= opt_b["x_dist"]
        elif "o" in opt_b["loc"]:
            xloc_s = xloc
            xloc_s[:, 0] -= opt_b["x_dist"]
            xloc_s[:, -1] += opt_b["x_dist"]
        elif "c" in opt_b["loc"] or "m" in opt_b["loc"]:
            xloc_s = xloc
        else:
            xloc_s = xloc

        bar_positions = get_positions(
            xloc_s, opt_b["loc"], opt_b["x_width"], data.shape[0]
        )
        bar_positions = np.nanmean(bar_positions, axis=0)
        for i, (x, y) in enumerate(zip(bar_positions, data_m)):
            color = to_rgba(opt_b["FaceColor"][i % len(opt_b["FaceColor"])])
            if label is not None and i < len(label):
                ax.bar(
                    x,
                    y,
                    width=opt_b["x_width"],
                    color=color,
                    edgecolor=opt_b["EdgeColor"],
                    alpha=opt_b["FaceAlpha"],
                    linewidth=opt_b["LineWidth"],
                    hatch=opt_b["hatch"],
                    label=label[i],
                )
            else:
                ax.bar(
                    x,
                    y,
                    width=opt_b["x_width"],
                    color=color,
                    edgecolor=opt_b["EdgeColor"],
                    alpha=opt_b["FaceAlpha"],
                    linewidth=opt_b["LineWidth"],
                    hatch=opt_b["hatch"],
                )

    def plot_errors(data, data_m, opt_e, xloc, ax, label=None):
        error_positions = get_positions(
            xloc, opt_e["loc"], opt_e["x_dist"], data.shape[0]
        )
        error_positions = np.nanmean(error_positions, axis=0)
        errors = np.nanstd(data, axis=0, ddof=1)
        if opt_e["error"] == "sem":
            errors /= np.sqrt(np.sum(~np.isnan(data), axis=0))
        if opt_e["LineStyle"] != "none":
            # draw lines
            ax.plot(
                error_positions,
                data_m,
                color=opt_e["LineColor"],
                linestyle=opt_e["LineStyle"],
                linewidth=opt_e["LineWidth"],
                alpha=opt_e["LineAlpha"],
            )

        if not isinstance(opt_e["FaceColor"], list):
            opt_e["FaceColor"] = [opt_e["FaceColor"]]
        if not isinstance(opt_e["MarkerEdgeColor"], list):
            opt_e["MarkerEdgeColor"] = [opt_e["MarkerEdgeColor"]]
        for i, (x, y, err) in enumerate(zip(error_positions, data_m, errors)):
            if label is not None and i < len(label):
                if opt_e["MarkerSize"] == "auto":
                    ax.errorbar(
                        x,
                        y,
                        yerr=err,
                        fmt=opt_e["Marker"],
                        ecolor=opt_e["LineColor"],
                        elinewidth=opt_e["LineWidth"],
                        lw=opt_e["LineWidth"],
                        ls=opt_e["LineStyle"],
                        capsize=opt_e["CapSize"],
                        capthick=opt_e["CapLineWidth"],
                        mec=opt_e["MarkerEdgeColor"][i % len(opt_e["MarkerEdgeColor"])],
                        mfc=opt_e["FaceColor"][i % len(opt_e["FaceColor"])],
                        visible=opt_e["Visible"],
                        label=label[i],
                    )
                else:
                    ax.errorbar(
                        x,
                        y,
                        yerr=err,
                        fmt=opt_e["Marker"],
                        ecolor=opt_e["LineColor"],
                        elinewidth=opt_e["LineWidth"],
                        lw=opt_e["LineWidth"],
                        ls=opt_e["LineStyle"],
                        capsize=opt_e["CapSize"],
                        capthick=opt_e["CapLineWidth"],
                        markersize=opt_e["MarkerSize"],
                        mec=opt_e["MarkerEdgeColor"][i % len(opt_e["MarkerEdgeColor"])],
                        mfc=opt_e["FaceColor"][i % len(opt_e["FaceColor"])],
                        visible=opt_e["Visible"],
                        label=label[i],
                    )
            else:
                if opt_e["MarkerSize"] == "auto":
                    ax.errorbar(
                        x,
                        y,
                        yerr=err,
                        fmt=opt_e["Marker"],
                        ecolor=opt_e["LineColor"],
                        elinewidth=opt_e["LineWidth"],
                        lw=opt_e["LineWidth"],
                        ls=opt_e["LineStyle"],
                        capsize=opt_e["CapSize"],
                        capthick=opt_e["CapLineWidth"],
                        mec=opt_e["MarkerEdgeColor"][i % len(opt_e["MarkerEdgeColor"])],
                        mfc=opt_e["FaceColor"][i % len(opt_e["FaceColor"])],
                        visible=opt_e["Visible"],
                    )
                else:
                    ax.errorbar(
                        x,
                        y,
                        yerr=err,
                        fmt=opt_e["Marker"],
                        ecolor=opt_e["LineColor"],
                        elinewidth=opt_e["LineWidth"],
                        lw=opt_e["LineWidth"],
                        ls=opt_e["LineStyle"],
                        capsize=opt_e["CapSize"],
                        capthick=opt_e["CapLineWidth"],
                        markersize=opt_e["MarkerSize"],
                        mec=opt_e["MarkerEdgeColor"][i % len(opt_e["MarkerEdgeColor"])],
                        mfc=opt_e["FaceColor"][i % len(opt_e["FaceColor"])],
                        visible=opt_e["Visible"],
                    )

    def plot_scatter(data, opt_s, xloc, ax, label=None):
        if "l" in opt_s["loc"]:
            xloc_s = xloc - opt_s["x_dist"]
        elif "r" in opt_s["loc"]:
            xloc_s = xloc + opt_s["x_dist"]
        elif "i" in opt_s["loc"]:
            xloc_s = xloc
            xloc_s[:, 0] += opt_s["x_dist"]
            xloc_s[:, -1] -= opt_s["x_dist"]
        elif "o" in opt_s["loc"]:
            xloc_s = xloc
            xloc_s[:, 0] -= opt_s["x_dist"]
            xloc_s[:, -1] += opt_s["x_dist"]
        elif "c" in opt_s["loc"] or "m" in opt_s["loc"]:
            xloc_s = xloc
        else:
            xloc_s = xloc

        scatter_positions = get_positions(
            xloc_s, opt_s["loc"], opt_s["x_width"], data.shape[0]
        )
        for i, (x, y) in enumerate(zip(scatter_positions.T, data.T)):
            color = to_rgba(opt_s["FaceColor"][i % len(opt_s["FaceColor"])])
            if label is not None and i < len(label):
                ax.scatter(
                    x,
                    y,
                    color=color,
                    alpha=opt_s["FaceAlpha"],
                    edgecolor=opt_s["MarkerEdgeColor"],
                    s=opt_s["MarkerSize"],
                    marker=opt_s["Marker"],
                    linewidths=opt_s["LineWidth"],
                    cmap=opt_s["cmap"],
                    label=label[i],
                )
            else:
                ax.scatter(
                    x,
                    y,
                    color=color,
                    alpha=opt_s["FaceAlpha"],
                    edgecolor=opt_s["MarkerEdgeColor"],
                    s=opt_s["MarkerSize"],
                    marker=opt_s["Marker"],
                    linewidths=opt_s["LineWidth"],
                    cmap=opt_s["cmap"],
                )

    def plot_boxplot(data, bx_opt, xloc, ax, label=None):
        if "l" in bx_opt["loc"]:
            X_bx = xloc - bx_opt["x_dist"]
        elif "r" in bx_opt["loc"]:
            X_bx = xloc + bx_opt["x_dist"]
        elif "i" in bx_opt["loc"]:
            X_bx = xloc
            X_bx[:, 0] += bx_opt["x_dist"]
            X_bx[:, -1] -= bx_opt["x_dist"]
        elif "o" in bx_opt["loc"]:
            X_bx = xloc
            X_bx[:, 0] -= bx_opt["x_dist"]
            X_bx[:, -1] += bx_opt["x_dist"]
        elif "c" in bx_opt["loc"] or "m" in bx_opt["loc"]:
            X_bx = xloc
        else:
            X_bx = xloc

        boxprops = dict(color=bx_opt["EdgeColor"], linewidth=bx_opt["BoxLineWidth"])
        flierprops = dict(
            marker=bx_opt["OutlierMarker"],
            markerfacecolor=bx_opt["OutlierFaceColor"],
            markeredgecolor=bx_opt["OutlierEdgeColor"],
            markersize=bx_opt["OutlierSize"],
        )
        whiskerprops = dict(
            linestyle=bx_opt["WhiskerLineStyle"],
            color=bx_opt["WhiskerLineColor"],
            linewidth=bx_opt["WhiskerLineWidth"],
        )
        capprops = dict(
            color=bx_opt["CapLineColor"],
            linewidth=bx_opt["CapLineWidth"],
        )
        medianprops = dict(
            linestyle=bx_opt["MedianLineStyle"],
            color=bx_opt["MedianLineColor"],
            linewidth=bx_opt["MedianLineWidth"],
        )
        meanprops = dict(
            linestyle=bx_opt["MeanLineStyle"],
            color=bx_opt["MeanLineColor"],
            linewidth=bx_opt["MeanLineWidth"],
        )
        # MeanLine or MedianLine only keep only one
        if bx_opt["MeanLine"]:  # MeanLine has priority
            bx_opt["MedianLine"] = False
        # rm NaNs
        cleaned_data = [data[~np.isnan(data[:, i]), i] for i in range(data.shape[1])]

        bxp = ax.boxplot(
            cleaned_data,
            positions=X_bx,
            notch=bx_opt["Notch"],
            patch_artist=True,
            boxprops=boxprops,
            flierprops=flierprops,
            whiskerprops=whiskerprops,
            capwidths=bx_opt["CapSize"],
            showfliers=bx_opt["Outliers"],
            showcaps=bx_opt["Caps"],
            capprops=capprops,
            medianprops=medianprops,
            meanline=bx_opt["MeanLine"],
            showmeans=bx_opt["MeanLine"],
            meanprops=meanprops,
            widths=bx_opt["x_width"],
            label=label,
        )
        if not bx_opt["MedianLine"]:
            for median in bxp["medians"]:
                median.set_visible(False)

        if bx_opt["BoxLineWidth"] < 0.1:
            bx_opt["EdgeColor"] = "none"
        else:
            bx_opt["EdgeColor"] = bx_opt["EdgeColor"]
        if not isinstance(bx_opt["FaceColor"], list):
            bx_opt["FaceColor"]=[bx_opt["FaceColor"]]
        if len(bxp["boxes"])!= len(bx_opt["FaceColor"]) and (len(bx_opt["FaceColor"])==1):
            bx_opt["FaceColor"]=bx_opt["FaceColor"] *len(bxp["boxes"]) 
        for patch, color in zip(bxp["boxes"], bx_opt["FaceColor"]):
            patch.set_facecolor(to_rgba(color, bx_opt["FaceAlpha"]))

        if bx_opt["MedianLineTop"]:
            ax.set_children(ax.get_children()[::-1])  # move median line forward

    def plot_violin(data, opt_v, xloc, ax, label=None, vertical=True):
        violin_positions = get_positions(
            xloc, opt_v["loc"], opt_v["x_dist"], data.shape[0]
        )
        violin_positions = np.nanmean(violin_positions, axis=0)
        for i, (x, ys) in enumerate(zip(violin_positions, data.T)):
            ys = ys[~np.isnan(ys)]
            if np.all(ys == ys[0]):  # Check if data is constant
                print(
                    "Data is constant; KDE cannot be applied. Plotting a flat line instead."
                )
                if vertical:
                    ax.plot(
                        [x - opt_v["x_width"] / 2, x + opt_v["x_width"] / 2],
                        [ys[0], ys[0]],
                        color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                        lw=2,
                        label=label[i] if label else None,
                    )
                else:
                    ax.plot(
                        [ys[0], ys[0]],
                        [x - opt_v["x_width"] / 2, x + opt_v["x_width"] / 2],
                        color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                        lw=2,
                        label=label[i] if label else None,
                    )
            else:
                from scipy.stats import gaussian_kde

                kde = gaussian_kde(ys, bw_method=opt_v["BandWidth"])
                min_val, max_val = ys.min(), ys.max()
                y_vals = np.linspace(min_val, max_val, opt_v["NumPoints"])
                kde_vals = kde(y_vals)
                kde_vals = kde_vals / kde_vals.max() * opt_v["x_width"]
                if label is not None and i < len(label):
                    if len(ys) > 1:
                        if "r" in opt_v["loc"].lower():
                            ax.fill_betweenx(
                                y_vals,
                                x,
                                x + kde_vals,
                                color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                                alpha=opt_v["FaceAlpha"],
                                edgecolor=opt_v["EdgeColor"],
                                label=label[i],
                                lw=opt_v["LineWidth"],
                                hatch=(
                                    opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                    if opt_v["hatch"] is not None
                                    else None
                                ),
                            )
                        elif (
                            "l" in opt_v["loc"].lower()
                            and not "f" in opt_v["loc"].lower()
                        ):
                            ax.fill_betweenx(
                                y_vals,
                                x - kde_vals,
                                x,
                                color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                                alpha=opt_v["FaceAlpha"],
                                edgecolor=opt_v["EdgeColor"],
                                label=label[i],
                                lw=opt_v["LineWidth"],
                                hatch=(
                                    opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                    if opt_v["hatch"] is not None
                                    else None
                                ),
                            )
                        elif (
                            "o" in opt_v["loc"].lower()
                            or "both" in opt_v["loc"].lower()
                        ):
                            ax.fill_betweenx(
                                y_vals,
                                x - kde_vals,
                                x + kde_vals,
                                color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                                alpha=opt_v["FaceAlpha"],
                                edgecolor=opt_v["EdgeColor"],
                                label=label[i],
                                lw=opt_v["LineWidth"],
                                hatch=(
                                    opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                    if opt_v["hatch"] is not None
                                    else None
                                ),
                            )
                        elif "i" in opt_v["loc"].lower():
                            if i % 2 == 1:  # odd number
                                ax.fill_betweenx(
                                    y_vals,
                                    x - kde_vals,
                                    x,
                                    color=opt_v["FaceColor"][
                                        i % len(opt_v["FaceColor"])
                                    ],
                                    alpha=opt_v["FaceAlpha"],
                                    edgecolor=opt_v["EdgeColor"],
                                    label=label[i],
                                    lw=opt_v["LineWidth"],
                                    hatch=(
                                        opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                        if opt_v["hatch"] is not None
                                        else None
                                    ),
                                )
                            else:
                                ax.fill_betweenx(
                                    y_vals,
                                    x,
                                    x + kde_vals,
                                    color=opt_v["FaceColor"][
                                        i % len(opt_v["FaceColor"])
                                    ],
                                    alpha=opt_v["FaceAlpha"],
                                    edgecolor=opt_v["EdgeColor"],
                                    label=label[i],
                                    lw=opt_v["LineWidth"],
                                    hatch=(
                                        opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                        if opt_v["hatch"] is not None
                                        else None
                                    ),
                                )
                        elif "f" in opt_v["loc"].lower():
                            ax.fill_betweenx(
                                y_vals,
                                x - kde_vals,
                                x + kde_vals,
                                color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                                alpha=opt_v["FaceAlpha"],
                                edgecolor=opt_v["EdgeColor"],
                                label=label[i],
                                lw=opt_v["LineWidth"],
                                hatch=(
                                    opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                    if opt_v["hatch"] is not None
                                    else None
                                ),
                            )
                else:
                    if "r" in opt_v["loc"].lower():
                        ax.fill_betweenx(
                            y_vals,
                            x,
                            x + kde_vals,
                            color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                            alpha=opt_v["FaceAlpha"],
                            edgecolor=opt_v["EdgeColor"],
                            lw=opt_v["LineWidth"],
                            hatch=(
                                opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                if opt_v["hatch"] is not None
                                else None
                            ),
                        )
                    elif (
                        "l" in opt_v["loc"].lower() and not "f" in opt_v["loc"].lower()
                    ):
                        ax.fill_betweenx(
                            y_vals,
                            x - kde_vals,
                            x,
                            color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                            alpha=opt_v["FaceAlpha"],
                            edgecolor=opt_v["EdgeColor"],
                            lw=opt_v["LineWidth"],
                            hatch=(
                                opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                if opt_v["hatch"] is not None
                                else None
                            ),
                        )
                    elif "o" in opt_v["loc"].lower() or "both" in opt_v["loc"].lower():
                        ax.fill_betweenx(
                            y_vals,
                            x - kde_vals,
                            x + kde_vals,
                            color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                            alpha=opt_v["FaceAlpha"],
                            edgecolor=opt_v["EdgeColor"],
                            lw=opt_v["LineWidth"],
                            hatch=(
                                opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                if opt_v["hatch"] is not None
                                else None
                            ),
                        )
                    elif "i" in opt_v["loc"].lower():
                        if i % 2 == 1:  # odd number
                            ax.fill_betweenx(
                                y_vals,
                                x - kde_vals,
                                x,
                                color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                                alpha=opt_v["FaceAlpha"],
                                edgecolor=opt_v["EdgeColor"],
                                lw=opt_v["LineWidth"],
                                hatch=(
                                    opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                    if opt_v["hatch"] is not None
                                    else None
                                ),
                            )
                        else:
                            ax.fill_betweenx(
                                y_vals,
                                x,
                                x + kde_vals,
                                color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                                alpha=opt_v["FaceAlpha"],
                                edgecolor=opt_v["EdgeColor"],
                                lw=opt_v["LineWidth"],
                                hatch=(
                                    opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                    if opt_v["hatch"] is not None
                                    else None
                                ),
                            )
                    elif "f" in opt_v["loc"].lower():
                        ax.fill_betweenx(
                            y_vals,
                            x - kde_vals,
                            x + kde_vals,
                            color=opt_v["FaceColor"][i % len(opt_v["FaceColor"])],
                            alpha=opt_v["FaceAlpha"],
                            edgecolor=opt_v["EdgeColor"],
                            lw=opt_v["LineWidth"],
                            hatch=(
                                opt_v["hatch"][i % len(opt_v["FaceColor"])]
                                if opt_v["hatch"] is not None
                                else None
                            ),
                        )

    def plot_ridgeplot(data, x, y, opt_r, **kwargs_figsets):
        # in the sns.FacetGrid class, the 'hue' argument is the one that is the one that will be represented by colors with 'palette'
        if opt_r["column4color"] is None:
            column4color = x
        else:
            column4color = opt_r["column4color"]

        if opt_r["row_labels"] is None:
            opt_r["row_labels"] = data[x].unique().tolist()

        if isinstance(opt_r["FaceColor"], str):
            opt_r["FaceColor"] = [opt_r["FaceColor"]]
        if len(opt_r["FaceColor"]) == 1:
            opt_r["FaceColor"] = np.tile(
                opt_r["FaceColor"], [1, len(opt_r["row_labels"])]
            )[0]
        if len(opt_r["FaceColor"]) > len(opt_r["row_labels"]):
            opt_r["FaceColor"] = opt_r["FaceColor"][: len(opt_r["row_labels"])]

        g = sns.FacetGrid(
            data=data,
            row=x,
            hue=column4color,
            aspect=opt_r["aspect"],
            height=opt_r["subplot_height"],
            palette=opt_r["FaceColor"],
        )

        # kdeplot
        g.map(
            sns.kdeplot,
            y,
            bw_adjust=opt_r["bw_adjust"],
            clip_on=opt_r["clip"],
            fill=opt_r["fill"],
            alpha=opt_r["FaceAlpha"],
            linewidth=opt_r["EdgeLineWidth"],
        )

        # edge / line of kdeplot
        if opt_r["EdgeColor"] is not None:
            g.map(
                sns.kdeplot,
                y,
                bw_adjust=opt_r["bw_adjust"],
                clip_on=opt_r["clip"],
                color=opt_r["EdgeColor"],
                lw=opt_r["EdgeLineWidth"],
            )
        else:
            g.map(
                sns.kdeplot,
                y,
                bw_adjust=opt_r["bw_adjust"],
                clip_on=opt_r["clip"],
                color=opt_r["EdgeColor"],
                lw=opt_r["EdgeLineWidth"],
            )

        # add a horizontal line
        if opt_r["xLineColor"] is not None:
            g.map(
                plt.axhline,
                y=0,
                lw=opt_r["xLineWidth"],
                clip_on=opt_r["clip"],
                color=opt_r["xLineColor"],
            )
        else:
            g.map(
                plt.axhline,
                y=0,
                lw=opt_r["xLineWidth"],
                clip_on=opt_r["clip"],
            )

        if isinstance(opt_r["color_row_label"], str):
            opt_r["color_row_label"] = [opt_r["color_row_label"]]
        if len(opt_r["color_row_label"]) == 1:
            opt_r["color_row_label"] = np.tile(
                opt_r["color_row_label"], [1, len(opt_r["row_labels"])]
            )[0]

        # loop over the FacetGrid figure axes (g.axes.flat)
        for i, ax in enumerate(g.axes.flat):
            if kwargs_figsets.get("xlim", False):
                ax.set_xlim(kwargs_figsets.get("xlim", False))
            if kwargs_figsets.get("xlim", False):
                ax.set_ylim(kwargs_figsets.get("ylim", False))
            if i == 0:
                row_x = opt_r["row_label_loc_xscale"] * np.abs(
                    np.diff(ax.get_xlim())
                ) + np.min(ax.get_xlim())
                row_y = opt_r["row_label_loc_yscale"] * np.abs(
                    np.diff(ax.get_ylim())
                ) + np.min(ax.get_ylim())
                ax.set_title(kwargs_figsets.get("title", ""))
            ax.text(
                row_x,
                row_y,
                opt_r["row_labels"][i],
                fontweight=opt_r["fontweight"],
                fontsize=opt_r["fontsize"],
                color=opt_r["color_row_label"][i],
            )
            figsets(**kwargs_figsets)

        # we use matplotlib.Figure.subplots_adjust() function to get the subplots to overlap
        g.fig.subplots_adjust(hspace=opt_r["subplot_hspace"])

        # eventually we remove axes titles, yticks and spines
        g.set_titles("")
        g.set(yticks=[])
        g.set(ylabel=opt_r["subplot_ylabel"])
        # if kwargs_figsets:
        #     g.set(**kwargs_figsets)
        if kwargs_figsets.get("xlim", False):
            g.set(xlim=kwargs_figsets.get("xlim", False))
        g.despine(bottom=True, left=True)

        plt.setp(
            ax.get_xticklabels(),
            fontsize=opt_r["fontsize"],
            fontweight=opt_r["fontweight"],
        )
        # if opt_r["ylabel"] is None:
        #     opt_r["ylabel"] = y
        # plt.xlabel(
        #     opt_r["ylabel"], fontweight=opt_r["fontweight"], fontsize=opt_r["fontsize"]
        # )
        return g, opt_r

    def plot_lines(data, opt_l, opt_s, ax):
        if "l" in opt_s["loc"]:
            xloc_s = xloc - opt_s["x_dist"]
        elif "r" in opt_s["loc"]:
            xloc_s = xloc + opt_s["x_dist"]
        elif "i" in opt_s["loc"]:
            xloc_s = xloc
            xloc_s[:, 0] += opt_s["x_dist"]
            xloc_s[:, -1] -= opt_s["x_dist"]
        elif "o" in opt_s["loc"]:
            xloc_s = xloc
            xloc_s[:, 0] -= opt_s["x_dist"]
            xloc_s[:, -1] += opt_s["x_dist"]
        elif "c" in opt_s["loc"] or "m" in opt_s["loc"]:
            xloc_s = xloc
        else:
            xloc_s = xloc

        scatter_positions = get_positions(
            xloc_s, opt_s["loc"], opt_s["x_width"], data.shape[0]
        )
        for incol in range(data.shape[1] - 1):
            for irow in range(data.shape[0]):
                if not np.isnan(data[irow, incol]):
                    if (
                        opt_l["LineStyle"] is not None
                        and not opt_l["LineStyle"] == "none"
                    ):
                        x_data = [
                            scatter_positions[irow, incol],
                            scatter_positions[irow, incol + 1],
                        ]
                        y_data = [data[irow, incol], data[irow, incol + 1]]

                        ax.plot(
                            x_data,
                            y_data,
                            color=opt_l["LineColor"],
                            linestyle=opt_l["LineStyle"],
                            linewidth=opt_l["LineWidth"],
                            alpha=opt_l["LineAlpha"],
                        )

    def get_positions(xloc, loc_type, x_width, n_row=None):
        if "rand" in loc_type:
            scatter_positions = np.zeros((n_row, len(xloc)))
            np.random.seed(111)
            for i, x in enumerate(xloc):
                scatter_positions[:, i] = np.random.uniform(
                    x - x_width, x + x_width, n_row
                )
            return scatter_positions
        elif "l" in loc_type:
            return np.tile(xloc - x_width, (n_row, 1))
        elif "r" in loc_type and not "d" in loc_type:
            return np.tile(xloc + x_width, (n_row, 1))
        elif "i" in loc_type:
            return np.tile(
                np.concatenate([xloc[:1] + x_width, xloc[1:-1], xloc[-1:] - x_width]),
                (n_row, 1),
            )
        elif "o" in loc_type:
            return np.tile(
                np.concatenate([xloc[:1] - x_width, xloc[1:-1], xloc[-1:] + x_width]),
                (n_row, 1),
            )
        else:
            return np.tile(xloc, (n_row, 1))

    def sort_catplot_layers(custom_order, full_order=["b", "bx", "e", "v", "s", "l"]):
        """
        sort layers
        """
        if "r" in full_order:
            return ["r"]
        # Ensure custom_order is a list of strings
        custom_order = [str(layer) for layer in custom_order]
        j = 1
        layers = list(range(len(full_order)))
        for i in range(len(full_order)):
            if full_order[i] not in custom_order:
                layers[i] = i
            else:
                layers[i] = None
        j = 0
        for i in range(len(layers)):
            if layers[i] is None:
                full_order[i] = custom_order[j]
                j += 1
        return full_order
        # # Example usage:
        # custom_order = ['s', 'bx', 'e']
        # full_order = sort_catplot_layers(custom_order)

    ax = kwargs.get("ax", None)
    col = kwargs.get("col", None)
    report = kwargs.get("report", True)
    vertical = kwargs.get("vertical", True)
    stats_subgroup = kwargs.get("stats_subgroup", True)
    if not col:
        kw_figsets = kwargs.get("figsets", None)
        # check the data type
        if isinstance(data, pd.DataFrame):
            df = data.copy()
            x = kwargs.get("x", None)
            y = kwargs.get("y", None)
            hue = kwargs.get("hue", None)
            data = df2array(data=data, x=x, y=y, hue=hue)
            y_max_loc = np.max(data, axis=0)
            xticklabels = []
            if hue is not None:
                # for i in df[x].unique().tolist():
                #     for j in df[hue].unique().tolist():
                #         xticklabels.append(i + "-" + j)
                for i in df[x].unique().tolist():
                    xticklabels.append(i)
                x_len = len(df[x].unique().tolist())
                hue_len = len(df[hue].unique().tolist())
                xticks = generate_xticks_with_gap(x_len, hue_len)
                xticks_x_loc = generate_xticks_x_labels(x_len, hue_len)
                default_x_width = 0.85
                legend_hue = df[hue].unique().tolist()
                default_colors = get_color(hue_len)

                # ! stats info
                stats_param = kwargs.get("stats", False)
                res = pd.DataFrame()  # Initialize an empty DataFrame to store results
                ihue = 1
                for i in df[x].unique().tolist():
                    print(i)  # to indicate which 'x'
                    if hue and stats_param:
                        if stats_subgroup:
                            data_temp = df[df[x] == i]
                            hue_labels = data_temp[hue].unique().tolist()
                            if isinstance(stats_param, dict):
                                if len(hue_labels) > 2:
                                    if "factor" in stats_param.keys():
                                        res_tmp = FuncMultiCmpt(
                                            data=data_temp, dv=y, **stats_param
                                        )
                                    else:
                                        res_tmp = FuncMultiCmpt(
                                            data=data_temp,
                                            dv=y,
                                            factor=hue,
                                            **stats_param,
                                        )
                                elif bool(stats_param):
                                    res_tmp = FuncMultiCmpt(
                                        data=data_temp, dv=y, factor=hue
                                    )
                                else:
                                    res_tmp = "did not work properly"
                                display_output(res_tmp)
                                res = pd.concat(
                                    [res, pd.DataFrame([res_tmp])],
                                    ignore_index=True,
                                    axis=0,
                                )
                            else:
                                if isinstance(stats_param, dict):
                                    pmc = stats_param.get("pmc", "pmc")
                                    pair = stats_param.get("pair", "unpaired")
                                else:
                                    pmc = "pmc"
                                    pair = "unpair"

                                res_tmp = FuncCmpt(
                                    x1=data_temp.loc[
                                        data_temp[hue] == hue_labels[0], y
                                    ].tolist(),
                                    x2=data_temp.loc[
                                        data_temp[hue] == hue_labels[1], y
                                    ].tolist(),
                                    pmc=pmc,
                                    pair=pair,
                                )
                                display_output(res_tmp)
                        else:
                            if isinstance(stats_param, dict):
                                if len(xticklabels) > 2:
                                    if "factor" in stats_param.keys():
                                        res_tmp = FuncMultiCmpt(
                                            data=df, dv=y, **stats_param
                                        )
                                    else:
                                        res_tmp = FuncMultiCmpt(
                                            data=df[df[x] == i],
                                            dv=y,
                                            factor=hue,
                                            **stats_param,
                                        )
                                elif bool(stats_param):
                                    res_tmp = FuncMultiCmpt(
                                        data=df[df[x] == i], dv=y, factor=hue
                                    )
                                else:
                                    res_tmp = "did not work properly"
                                display_output(res_tmp)
                                res = pd.concat(
                                    [res, pd.DataFrame([res_tmp])],
                                    ignore_index=True,
                                    axis=0,
                                )
                            else:
                                if isinstance(stats_param, dict):
                                    pmc = stats_param.get("pmc", "pmc")
                                    pair = stats_param.get("pair", "unpaired")
                                else:
                                    pmc = "pmc"
                                    pair = "unpair"

                                data_temp = df[df[x] == i]
                                hue_labels = data_temp[hue].unique().tolist()
                                res_tmp = FuncCmpt(
                                    x1=data_temp.loc[
                                        data_temp[hue] == hue_labels[0], y
                                    ].tolist(),
                                    x2=data_temp.loc[
                                        data_temp[hue] == hue_labels[1], y
                                    ].tolist(),
                                    pmc=pmc,
                                    pair=pair,
                                )
                                display_output(res_tmp)
                    ihue += 1

            else:
                # ! stats info
                stats_param = kwargs.get("stats", False)
                for i in df[x].unique().tolist():
                    xticklabels.append(i)
                xticks = np.arange(1, len(xticklabels) + 1).tolist()
                xticks_x_loc = np.arange(1, len(xticklabels) + 1).tolist()
                legend_hue = xticklabels
                default_colors = get_color(len(xticklabels))
                default_x_width = 0.5
                res = None
                if x and stats_param:
                    if isinstance(stats_param, dict):
                        if len(xticklabels) > 2:
                            res = FuncMultiCmpt(data=df, dv=y, factor=x, **stats_param)
                        else:
                            res = FuncCmpt(
                                x1=df.loc[df[x] == xticklabels[0], y].tolist(),
                                x2=df.loc[df[x] == xticklabels[1], y].tolist(),
                                **stats_param,
                            )
                    elif bool(stats_param):
                        if len(xticklabels) > 2:
                            res = FuncMultiCmpt(data=df, dv=y, factor=x)
                        else:
                            res = FuncCmpt(
                                x1=df.loc[df[x] == xticklabels[0], y].tolist(),
                                x2=df.loc[df[x] == xticklabels[1], y].tolist(),
                            )
                    else:
                        res = "did not work properly"
                display_output(res)

            # when the xticklabels are too long, rotate the labels a bit
            xangle = 30 if max([len(i) for i in xticklabels]) > 50 else 0
            if kw_figsets is not None:
                kw_figsets = {
                    "ylabel": y,
                    # "xlabel": x,
                    "xticks": xticks_x_loc,  # xticks,
                    "xticklabels": xticklabels,
                    "xangle": xangle,
                    **kw_figsets,
                }
            else:
                kw_figsets = {
                    "ylabel": y,
                    # "xlabel": x,
                    "xticks": xticks_x_loc,  # xticks,
                    "xticklabels": xticklabels,
                    "xangle": xangle,
                }
        else:
            if isinstance(data, np.ndarray):
                df = array2df(data)
                x = "group"
                y = "value"
            xticklabels = []
            stats_param = kwargs.get("stats", False)
            for i in df[x].unique().tolist():
                xticklabels.append(i)
            xticks = np.arange(1, len(xticklabels) + 1).tolist()
            xticks_x_loc = np.arange(1, len(xticklabels) + 1).tolist()
            legend_hue = xticklabels
            default_colors = get_color(len(xticklabels))
            default_x_width = 0.5
            res = None
            if x and stats_param:
                if isinstance(stats_param, dict):
                    res = FuncMultiCmpt(data=df, dv=y, factor=x, **stats_param)
                elif bool(stats_param):
                    res = FuncMultiCmpt(data=df, dv=y, factor=x)
                else:
                    res = "did not work properly"
            display_output(res)

        # full_order
        opt = kwargs.get("opt", {})

        # load style:
        style_use = None
        for k, v in kwargs.items():
            if "style" in k and "exp" not in k:
                style_use = v
                break
        if style_use is not None:
            try:
                dir_curr_script = os.path.dirname(os.path.abspath(__file__))
                dir_style = dir_curr_script + "/data/styles/"
                if isinstance(style_use, str):
                    style_load = fload(dir_style + style_use + ".json")
                else:
                    style_load = fload(
                        listdir(dir_style, "json", verbose=False).path.tolist()[
                            style_use
                        ]
                    )
                style_load = remove_colors_in_dict(style_load)
                opt.update(style_load)
            except:
                print(f"cannot find the style'{style_use}'")

        color_custom = kwargs.get("c", default_colors)
        if not isinstance(color_custom, list):
            color_custom = list(color_custom)
        # if len(color_custom) < data.shape[1]:
        #     color_custom.extend(get_color(data.shape[1]-len(color_custom),cmap='tab20'))
        opt.setdefault("c", color_custom)

        opt.setdefault("loc", {})
        opt["loc"].setdefault("go", 0)
        opt["loc"].setdefault("xloc", xticks)

        # export setting
        opt.setdefault("style", {})
        opt.setdefault("layer", ["b", "bx", "e", "v", "s", "l"])

        opt.setdefault("b", {})
        opt["b"].setdefault("go", 1)
        opt["b"].setdefault("loc", "c")
        opt["b"].setdefault("FaceColor", color_custom)
        opt["b"].setdefault("FaceAlpha", 1)
        opt["b"].setdefault("EdgeColor", "k")
        opt["b"].setdefault("EdgeAlpha", 1)
        opt["b"].setdefault("LineStyle", "-")
        opt["b"].setdefault("LineWidth", 0.8)
        opt["b"].setdefault("x_width", default_x_width)
        opt["b"].setdefault("x_dist", opt["b"]["x_width"])
        opt["b"].setdefault("ShowBaseLine", "off")
        opt["b"].setdefault("hatch", None)

        opt.setdefault("e", {})
        opt["e"].setdefault("go", 1)
        opt["e"].setdefault("loc", "l")
        opt["e"].setdefault("LineWidth", 2)
        opt["e"].setdefault("CapLineWidth", 1)
        opt["e"].setdefault("CapSize", 2)
        opt["e"].setdefault("Marker", "none")
        opt["e"].setdefault("LineStyle", "none")
        opt["e"].setdefault("LineColor", "k")
        opt["e"].setdefault("LineAlpha", 0.5)
        opt["e"].setdefault("LineJoin", "round")
        opt["e"].setdefault("MarkerSize", "auto")
        opt["e"].setdefault("FaceColor", color_custom)
        opt["e"].setdefault("MarkerEdgeColor", "none")
        opt["e"].setdefault("Visible", True)
        opt["e"].setdefault("Orientation", "vertical")
        opt["e"].setdefault("error", "sem")
        opt["e"].setdefault("x_width", default_x_width / 5)
        opt["e"].setdefault("x_dist", opt["e"]["x_width"])
        opt["e"].setdefault("cap_dir", "b")

        opt.setdefault("s", {})
        opt["s"].setdefault("go", 1)
        opt["s"].setdefault("loc", "r")
        opt["s"].setdefault("FaceColor", color_custom)
        opt["s"].setdefault("cmap", None)
        opt["s"].setdefault("FaceAlpha", 1)
        opt["s"].setdefault("x_width", default_x_width / 5 * 0.5)
        opt["s"].setdefault("x_dist", opt["s"]["x_width"])
        opt["s"].setdefault("Marker", "o")
        opt["s"].setdefault("MarkerSize", 15)
        opt["s"].setdefault("LineWidth", 0.8)
        opt["s"].setdefault("MarkerEdgeColor", "k")

        opt.setdefault("l", {})
        opt["l"].setdefault("go", 0)
        opt["l"].setdefault("LineStyle", "-")
        opt["l"].setdefault("LineColor", "k")
        opt["l"].setdefault("LineWidth", 0.5)
        opt["l"].setdefault("LineAlpha", 0.5)

        opt.setdefault("bx", {})
        opt["bx"].setdefault("go", 0)
        opt["bx"].setdefault("loc", "r")
        opt["bx"].setdefault("FaceColor", color_custom)
        opt["bx"].setdefault("EdgeColor", "k")
        opt["bx"].setdefault("FaceAlpha", 0.85)
        opt["bx"].setdefault("EdgeAlpha", 1)
        opt["bx"].setdefault("LineStyle", "-")
        opt["bx"].setdefault("x_width", default_x_width / 5)
        opt["bx"].setdefault("x_dist", opt["bx"]["x_width"])
        opt["bx"].setdefault("ShowBaseLine", "off")
        opt["bx"].setdefault("Notch", False)
        opt["bx"].setdefault("Outliers", "on")
        opt["bx"].setdefault("OutlierMarker", "+")
        opt["bx"].setdefault("OutlierFaceColor", "r")
        opt["bx"].setdefault("OutlierEdgeColor", "k")
        opt["bx"].setdefault("OutlierSize", 6)
        # opt['bx'].setdefault('PlotStyle', 'traditional')
        # opt['bx'].setdefault('FactorDirection', 'auto')
        opt["bx"].setdefault("LineWidth", 0.5)
        opt["bx"].setdefault("Whisker", opt["bx"]["LineWidth"])
        opt["bx"].setdefault("Orientation", "vertical")
        opt["bx"].setdefault("BoxLineWidth", opt["bx"]["LineWidth"])
        opt["bx"].setdefault("FaceColor", "k")
        opt["bx"].setdefault("WhiskerLineStyle", "-")
        opt["bx"].setdefault("WhiskerLineColor", "k")
        opt["bx"].setdefault("WhiskerLineWidth", opt["bx"]["LineWidth"])
        opt["bx"].setdefault("Caps", True)
        opt["bx"].setdefault("CapLineColor", "k")
        opt["bx"].setdefault("CapLineWidth", opt["bx"]["LineWidth"])
        opt["bx"].setdefault("CapSize", 0.2)
        opt["bx"].setdefault("MedianLine", True)
        opt["bx"].setdefault("MedianLineStyle", "-")
        opt["bx"].setdefault("MedianStyle", "line")
        opt["bx"].setdefault("MedianLineColor", "k")
        opt["bx"].setdefault("MedianLineWidth", opt["bx"]["LineWidth"] * 4)
        opt["bx"].setdefault("MedianLineTop", False)
        opt["bx"].setdefault("MeanLine", False)
        opt["bx"].setdefault("showmeans", opt["bx"]["MeanLine"])
        opt["bx"].setdefault("MeanLineStyle", "-")
        opt["bx"].setdefault("MeanLineColor", "w")
        opt["bx"].setdefault("MeanLineWidth", opt["bx"]["LineWidth"] * 4)

        # Violin plot options
        opt.setdefault("v", {})
        opt["v"].setdefault("go", 0)
        opt["v"].setdefault("x_width", 0.3)
        opt["v"].setdefault("x_dist", opt["v"]["x_width"])
        opt["v"].setdefault("loc", "r")
        opt["v"].setdefault("EdgeColor", "none")
        opt["v"].setdefault("LineWidth", 0.5)
        opt["v"].setdefault("FaceColor", color_custom)
        opt["v"].setdefault("FaceAlpha", 1)
        opt["v"].setdefault("BandWidth", "scott")
        opt["v"].setdefault("Function", "pdf")
        opt["v"].setdefault("Kernel", "gau")
        opt["v"].setdefault("hatch", None)
        opt["v"].setdefault("NumPoints", 500)
        opt["v"].setdefault("BoundaryCorrection", "reflection")

        # ridgeplot
        opt.setdefault("r", {})
        opt["r"].setdefault("go", 0)
        opt["r"].setdefault("bw_adjust", 1)
        opt["r"].setdefault("clip", False)
        opt["r"].setdefault("FaceColor", get_color(20))
        opt["r"].setdefault("FaceAlpha", 1)
        opt["r"].setdefault("EdgeLineWidth", 1.5)
        opt["r"].setdefault("fill", True)
        opt["r"].setdefault("EdgeColor", "none")
        opt["r"].setdefault("xLineWidth", opt["r"]["EdgeLineWidth"] + 0.5)
        opt["r"].setdefault("xLineColor", "none")
        opt["r"].setdefault("aspect", 8)
        opt["r"].setdefault("subplot_hspace", -0.3)  # overlap subplots
        opt["r"].setdefault("subplot_height", 0.75)
        opt["r"].setdefault("subplot_ylabel", "")
        opt["r"].setdefault("column4color", None)
        opt["r"].setdefault("row_labels", None)
        opt["r"].setdefault("row_label_loc_xscale", 0.01)
        opt["r"].setdefault("row_label_loc_yscale", 0.05)
        opt["r"].setdefault("fontweight", plt.rcParams["font.weight"])
        opt["r"].setdefault("fontsize", plt.rcParams["font.size"])
        opt["r"].setdefault("color_row_label", "k")
        opt["r"].setdefault("ylabel", None)

        data_m = np.nanmean(data, axis=0)
        nr, nc = data.shape

        for key in kwargs.keys():
            if key in opt:
                if isinstance(kwargs[key], dict):
                    opt[key].update(kwargs[key])
                else:
                    opt[key] = kwargs[key]
        if isinstance(opt["loc"]["xloc"], list):
            xloc = np.array(opt["loc"]["xloc"])
        else:
            xloc = opt["loc"]["xloc"]
        if opt["r"]["go"]:
            layers = sort_catplot_layers(opt["layer"], "r")
        else:
            layers = sort_catplot_layers(opt["layer"])

        if ("ax" not in locals() or ax is None) and not opt["r"]["go"]:
            ax = plt.gca()
        label = kwargs.get("label", "bar")
        if label:
            if "b" in label:
                legend_which = "b"
            elif "s" in label:
                legend_which = "s"
            elif "bx" in label:
                legend_which = "bx"
            elif "e" in label:
                legend_which = "e"
            elif "v" in label:
                legend_which = "v"
        else:
            legend_which = None
        for layer in layers:
            if layer == "b" and opt["b"]["go"]:
                if legend_which == "b":
                    plot_bars(data, data_m, opt["b"], xloc, ax, label=legend_hue)
                else:
                    plot_bars(data, data_m, opt["b"], xloc, ax, label=None)
            elif layer == "e" and opt["e"]["go"]:
                if legend_which == "e":
                    plot_errors(data, data_m, opt["e"], xloc, ax, label=legend_hue)
                else:
                    plot_errors(data, data_m, opt["e"], xloc, ax, label=None)
            elif layer == "s" and opt["s"]["go"]:
                if legend_which == "s":
                    plot_scatter(data, opt["s"], xloc, ax, label=legend_hue)
                else:
                    plot_scatter(data, opt["s"], xloc, ax, label=None)
            elif layer == "bx" and opt["bx"]["go"]:
                if legend_which == "bx":
                    plot_boxplot(data, opt["bx"], xloc, ax, label=legend_hue)
                else:
                    plot_boxplot(data, opt["bx"], xloc, ax, label=None)
            elif layer == "v" and opt["v"]["go"]:
                if legend_which == "v":
                    plot_violin(
                        data, opt["v"], xloc, ax, label=legend_hue, vertical=vertical
                    )
                else:
                    plot_violin(data, opt["v"], xloc, ax, vertical=vertical, label=None)
            elif layer == "r" and opt["r"]["go"]:
                kwargs_figsets = kwargs.get("figsets", None)
                if x and y:
                    if kwargs_figsets:
                        plot_ridgeplot(df, x, y, opt["r"], **kwargs_figsets)
                    else:
                        plot_ridgeplot(df, x, y, opt["r"])
            elif all([layer == "l", opt["l"]["go"], opt["s"]["go"]]):
                plot_lines(data, opt["l"], opt["s"], ax)

        if kw_figsets is not None and not opt["r"]["go"]:
            figsets(ax=ax, **kw_figsets)
        show_legend = kwargs.get("show_legend", True)
        if show_legend and not opt["r"]["go"]:
            ax.legend()
        # ! add asterisks in the plot
        if stats_param:
            if len(xticklabels) >= 1:
                if hue is None:
                    add_asterisks(
                        ax,
                        res,
                        xticks_x_loc,
                        xticklabels,
                        y_loc=np.nanmax(data),
                        report_go=report,
                    )
                else:  # hue is not None
                    ihue = 1
                    for i in df[x].unique().tolist():
                        data_temp = df[df[x] == i]
                        hue_labels = data_temp[hue].unique().tolist()
                        if stats_param:
                            if len(hue_labels) > 2:
                                if isinstance(stats_param, dict):
                                    if "factor" in stats_param.keys():
                                        res_tmp = FuncMultiCmpt(
                                            data=df, dv=y, **stats_param
                                        )
                                    else:
                                        res_tmp = FuncMultiCmpt(
                                            data=df[df[x] == i],
                                            dv=y,
                                            factor=hue,
                                            **stats_param,
                                        )
                                elif bool(stats_param):
                                    res_tmp = FuncMultiCmpt(
                                        data=df[df[x] == i], dv=y, factor=hue
                                    )
                                else:
                                    res_tmp = "did not work properly"
                                xloc_curr = hue_len * (ihue - 1)

                                add_asterisks(
                                    ax,
                                    res_tmp,
                                    xticks[xloc_curr : xloc_curr + hue_len],
                                    legend_hue,
                                    y_loc=np.nanmax(data),
                                    report_go=report,
                                )
                            else:
                                if isinstance(stats_param, dict):
                                    pmc = stats_param.get("pmc", "pmc")
                                    pair = stats_param.get("pair", "unpaired")
                                else:
                                    pmc = "pmc"
                                    pair = "unpair"
                                res_tmp = FuncCmpt(
                                    x1=data_temp.loc[
                                        data_temp[hue] == hue_labels[0], y
                                    ].tolist(),
                                    x2=data_temp.loc[
                                        data_temp[hue] == hue_labels[1], y
                                    ].tolist(),
                                    pmc=pmc,
                                    pair=pair,
                                )
                                xloc_curr = hue_len * (ihue - 1)
                                add_asterisks(
                                    ax,
                                    res_tmp,
                                    xticks[xloc_curr : xloc_curr + hue_len],
                                    legend_hue,
                                    y_loc=np.nanmax(data),
                                    report_go=report,
                                )
                        ihue += 1
            else:  # 240814: still has some bugs
                if isinstance(res, dict):
                    tab_res = pd.DataFrame(res[1], index=[0])
                    x1 = df.loc[df[x] == xticklabels[0], y].tolist()
                    x2 = df.loc[df[x] == xticklabels[1], y].tolist()
                    tab_res[f"{xticklabels[0]}(mean±sem)"] = [str_mean_sem(x1)]
                    tab_res[f"{xticklabels[1]}(mean±sem)"] = [str_mean_sem(x2)]
                    add_asterisks(
                        ax,
                        res[1],
                        xticks_x_loc,
                        xticklabels,
                        y_loc=np.max([x1, x2]),
                        report_go=report,
                    )
                elif isinstance(res, pd.DataFrame):
                    display(res)
                    print("still has some bugs")
                    x1 = df.loc[df[x] == xticklabels[0], y].tolist()
                    x2 = df.loc[df[x] == xticklabels[1], y].tolist()
                    add_asterisks(
                        ax,
                        res,
                        xticks_x_loc,
                        xticklabels,
                        y_loc=np.max([x1, x2]),
                        report_go=report,
                    )

        style_export = kwargs.get("style_export", None)
        if style_export and (style_export != style_use):
            dir_curr_script = os.path.dirname(os.path.abspath(__file__))
            dir_style = dir_curr_script + "/data/styles/"
            fsave(dir_style + style_export + ".json", opt)

        return ax, opt
    else:
        col_names = data[col].unique().tolist()
        nrow, ncol = kwargs.get("subplots", [len(col_names), 1])
        figsize = kwargs.get("figsize", [3 * ncol, 3 * nrow])
        fig, axs = plt.subplots(nrow, ncol, figsize=figsize, squeeze=False)
        axs = axs.flatten()
        key2rm = ["data", "ax", "col", "subplots"]
        for k2rm in key2rm:
            if k2rm in kwargs:
                del kwargs[k2rm]
        for i, ax in enumerate(axs):
            # ax = axs[i][0] if len(col_names) > 1 else axs[0]
            if i < len(col_names):
                df_sub = data.loc[data[col] == col_names[i]]
                _, opt = catplot(ax=ax, data=df_sub, **kwargs)
                ax.set_title(f"{col}={col_names[i]}")
                x_label = kwargs.get("x", None)
                if x_label:
                    ax.set_xlabel(x_label)
        print(f"Axis layout shape: {axs.shape}")
        return axs, opt


def get_cmap():
    return plt.colormaps()


def read_mplstyle(style_file):
    """
    example usage:
    style_file = "/ std-colors.mplstyle"
    style_dict = read_mplstyle(style_file)
    """
    # Load the style file
    plt.style.use(style_file)

    # Get the current style properties
    style_dict = plt.rcParams

    # Convert to dictionary
    style_dict = dict(style_dict)
    # Print the style dictionary
    for i, j in style_dict.items():
        print(f"\n{i}::::{j}")
    return style_dict


def figsets(*args, **kwargs):
    import matplotlib
    from cycler import cycler

    matplotlib.rc("text", usetex=False)

    fig = plt.gcf()
    fontsize = kwargs.get("fontsize", 11)
    plt.rcParams["font.size"] = fontsize
    fontname = kwargs.pop("fontname", "Arial")
    fontname = plt_font(fontname)  # 显示中文

    sns_themes = ["white", "whitegrid", "dark", "darkgrid", "ticks"]
    sns_contexts = ["notebook", "talk", "poster"]  # now available "paper"
    scienceplots_styles = [
        "science",
        "nature",
        "scatter",
        "ieee",
        "no-latex",
        "std-colors",
        "high-vis",
        "bright",
        "dark_background",
        "science",
        "high-vis",
        "vibrant",
        "muted",
        "retro",
        "grid",
        "high-contrast",
        "light",
        "cjk-tc-font",
        "cjk-kr-font",
    ]

    def set_step_1(ax, key, value):
        nonlocal fontsize, fontname
        if ("fo" in key) and (("size" in key) or ("sz" in key)):
            fontsize = value
            plt.rcParams.update(
                {
                    "font.size": fontsize,
                    "figure.titlesize": fontsize,
                    "axes.titlesize": fontsize,
                    "axes.labelsize": fontsize,
                    "xtick.labelsize": fontsize,
                    "ytick.labelsize": fontsize,
                    "legend.fontsize": fontsize,
                    "legend.title_fontsize": fontsize,
                }
            )

            # Customize tick labels
            ax.tick_params(axis="both", which="major", labelsize=fontsize)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontname(fontname)

            # Optionally adjust legend font properties if a legend is included
            if ax.get_legend():
                for text in ax.get_legend().get_texts():
                    text.set_fontsize(fontsize)
                    text.set_fontname(fontname)
        # style
        if "st" in key.lower() or "th" in key.lower():
            if isinstance(value, str):
                if (value in plt.style.available) or (value in scienceplots_styles):
                    plt.style.use(value)
                elif value in sns_themes:
                    sns.set_style(value)
                elif value in sns_contexts:
                    sns.set_context(value)
                else:
                    print(
                        f"\nWarning\n'{value}' is not a plt.style,select on below:\n{plt.style.available+sns_themes+sns_contexts+scienceplots_styles}"
                    )
            if isinstance(value, list):
                for i in value:
                    if (i in plt.style.available) or (i in scienceplots_styles):
                        plt.style.use(i)
                    elif i in sns_themes:
                        sns.set_style(i)
                    elif i in sns_contexts:
                        sns.set_context(i)
                    else:
                        print(
                            f"\nWarning\n'{i}' is not a plt.style,select on below:\n{plt.style.available+sns_themes+sns_contexts+scienceplots_styles}"
                        )
        if "la" in key.lower():
            if "loc" in key.lower() or "po" in key.lower():
                for i in value:
                    if "l" in i.lower() and not "g" in i.lower():
                        ax.yaxis.set_label_position("left")
                    if "r" in i.lower() and not "o" in i.lower():
                        ax.yaxis.set_label_position("right")
                    if "t" in i.lower() and not "l" in i.lower():
                        ax.xaxis.set_label_position("top")
                    if "b" in i.lower() and not "o" in i.lower():
                        ax.xaxis.set_label_position("bottom")
            if ("x" in key.lower()) and (
                "tic" not in key.lower() and "tk" not in key.lower()
            ):
                ax.set_xlabel(value, fontname=fontname, fontsize=fontsize)
            if ("y" in key.lower()) and (
                "tic" not in key.lower() and "tk" not in key.lower()
            ):
                ax.set_ylabel(value, fontname=fontname, fontsize=fontsize)
            if ("z" in key.lower()) and (
                "tic" not in key.lower() and "tk" not in key.lower()
            ):
                ax.set_zlabel(value, fontname=fontname, fontsize=fontsize)
        if key == "xlabel" and isinstance(value, dict):
            ax.set_xlabel(**value)
        if key == "ylabel" and isinstance(value, dict):
            ax.set_ylabel(**value)
        # tick location
        if "tic" in key.lower() or "tk" in key.lower():
            if ("loc" in key.lower()) or ("po" in key.lower()):
                if isinstance(value, str):
                    value = [value]
                if isinstance(value, list):
                    loc = []
                    for i in value:
                        ax.tick_params(
                            axis="both",
                            which="both",
                            bottom=False,
                            top=False,
                            left=False,
                            right=False,
                            labelbottom=False,
                            labelleft=False,
                        )
                        if ("l" in i.lower()) and ("a" not in i.lower()):
                            ax.yaxis.set_ticks_position("left")
                        if "r" in i.lower():
                            ax.yaxis.set_ticks_position("right")
                        if "t" in i.lower():
                            ax.xaxis.set_ticks_position("top")
                        if "b" in i.lower():
                            ax.xaxis.set_ticks_position("bottom")
                        if i.lower() in ["a", "both", "all", "al", ":"]:
                            ax.tick_params(
                                axis="both",  # Apply to both axes
                                which="both",  # Apply to both major and minor ticks
                                bottom=True,  # Show ticks at the bottom
                                top=True,  # Show ticks at the top
                                left=True,  # Show ticks on the left
                                right=True,  # Show ticks on the right
                                labelbottom=True,  # Show labels at the bottom
                                labelleft=True,  # Show labels on the left
                            )
                        if i.lower() in ["xnone", "xoff", "none"]:
                            ax.tick_params(
                                axis="x",
                                which="both",
                                bottom=False,
                                top=False,
                                left=False,
                                right=False,
                                labelbottom=False,
                                labelleft=False,
                            )
                        if i.lower() in ["ynone", "yoff", "none"]:
                            ax.tick_params(
                                axis="y",
                                which="both",
                                bottom=False,
                                top=False,
                                left=False,
                                right=False,
                                labelbottom=False,
                                labelleft=False,
                            )
            # ticks / labels
            elif "x" in key.lower():
                if value is None:
                    value = []
                if "la" not in key.lower():
                    ax.set_xticks(value)
                if "la" in key.lower():
                    ax.set_xticklabels(value)
            elif "y" in key.lower():
                if value is None:
                    value = []
                if "la" not in key.lower():
                    ax.set_yticks(value)
                if "la" in key.lower():
                    ax.set_yticklabels(value)
            elif "z" in key.lower():
                if value is None:
                    value = []
                if "la" not in key.lower():
                    ax.set_zticks(value)
                if "la" in key.lower():
                    ax.set_zticklabels(value)
        # rotation
        if "angle" in key.lower() or ("rot" in key.lower()):
            if "x" in key.lower():
                if value in [0, 90, 180, 270]:
                    ax.tick_params(axis="x", rotation=value)
                    for tick in ax.get_xticklabels():
                        tick.set_horizontalalignment("center")
                elif value > 0:
                    ax.tick_params(axis="x", rotation=value)
                    for tick in ax.get_xticklabels():
                        tick.set_horizontalalignment("right")
                elif value < 0:
                    ax.tick_params(axis="x", rotation=value)
                    for tick in ax.get_xticklabels():
                        tick.set_horizontalalignment("left")
            if "y" in key.lower():
                ax.tick_params(axis="y", rotation=value)
                for tick in ax.get_yticklabels():
                    tick.set_horizontalalignment("right")

        if "bo" in key in key:  # box setting, and ("p" in key or "l" in key):
            if isinstance(value, (str, list)):
                # locations = ["left", "right", "top", "bottom"]
                # for loc, spi in ax.spines.items():
                #     if loc in locations:
                #         spi.set_color("none")  # no spine
                locations = []
                for i in value:
                    if "l" in i.lower() and not "t" in i.lower():
                        locations.append("left")
                    if "r" in i.lower() and not "o" in i.lower():  # right
                        locations.append("right")
                    if "t" in i.lower() and not "r" in i.lower():  # top
                        locations.append("top")
                    if "b" in i.lower() and not "t" in i.lower():
                        locations.append("bottom")
                    if i.lower() in ["a", "both", "all", "al", ":"]:
                        [
                            locations.append(x)
                            for x in ["left", "right", "top", "bottom"]
                        ]
                if "none" in value:
                    locations = []  # hide all
                # check spines
                for loc, spi in ax.spines.items():
                    if loc in locations:
                        # spi.set_color("k")
                        spi.set_position(("outward", 0))
                    else:
                        spi.set_color("none")  # no spine
        if "tick" in key.lower():  # tick ticks tick_para ={}
            if isinstance(value, dict):
                for k, val in value.items():
                    if "wh" in k.lower():
                        ax.tick_params(
                            which=val
                        )  # {'major', 'minor', 'both'}, default: 'major'
                    elif "dir" in k.lower():
                        ax.tick_params(direction=val)  # {'in', 'out', 'inout'}
                    elif "len" in k.lower():  # length
                        ax.tick_params(length=val)
                    elif ("wid" in k.lower()) or ("wd" in k.lower()):  # width
                        ax.tick_params(width=val)
                    elif "ax" in k.lower():  # ax
                        ax.tick_params(axis=val)  # {'x', 'y', 'both'}, default: 'both'
                    elif ("c" in k.lower()) and ("ect" not in k.lower()):
                        ax.tick_params(colors=val)  # Tick color.
                    elif "pad" in k.lower() or "space" in k.lower():
                        ax.tick_params(
                            pad=val
                        )  # float, distance in points between tick and label
                    elif (
                        ("lab" in k.lower() or "text" in k.lower())
                        and ("s" in k.lower())
                        and ("z" in k.lower())
                    ):  # label_size
                        ax.tick_params(
                            labelsize=val
                        )  # float, distance in points between tick and label
        if "text" in key.lower():
            if isinstance(value, dict):
                ax.text(**value)
            elif isinstance(value, list):
                if all([isinstance(i, dict) for i in value]):
                    [ax.text(**value_) for value_ in value]
            # e.g.,
            # figsets(ax=ax,
            # text=[
            #     dict(
            #         x=1,
            #         y=1.3,
            #         s="Wake",
            #         c="k",
            #         bbox=dict(facecolor="0.8", edgecolor="none", boxstyle="round,pad=0.1"),
            #     ),
            #     dict(
            #         x=1,
            #         y=0.4,
            #         s="Sleep",
            #         c="k",
            #         bbox=dict(facecolor="0.8", edgecolor="none", boxstyle="round,pad=0.05"),
            #     ),
            # ])

        if "mi" in key.lower() and "tic" in key.lower():  # minor_ticks
            import matplotlib.ticker as tck

            if "x" in value.lower() or "x" in key.lower():
                ax.xaxis.set_minor_locator(tck.AutoMinorLocator())  # ax.minorticks_on()
            if "y" in value.lower() or "y" in key.lower():
                ax.yaxis.set_minor_locator(
                    tck.AutoMinorLocator()
                )  # ax.minorticks_off()
            if value.lower() in ["both", ":", "all", "a", "b", "on"]:
                ax.minorticks_on()
        if key == "colormap" or key == "cmap":
            plt.set_cmap(value)

    def set_step_2(ax, key, value):
        nonlocal fontsize, fontname
        if key == "figsize":
            pass
        if "xlim" in key.lower():
            ax.set_xlim(value)
        if "ylim" in key.lower():
            ax.set_ylim(value)
        if "zlim" in key.lower():
            ax.set_zlim(value)
        if "sc" in key.lower():  # scale
            if "x" in key.lower():
                ax.set_xscale(value)
            if "y" in key.lower():
                ax.set_yscale(value)
            if "z" in key.lower():
                ax.set_zscale(value)
        if key == "grid":
            if isinstance(value, dict):
                for k, val in value.items():
                    if "wh" in k.lower():  # which
                        ax.grid(
                            which=val
                        )  # {'major', 'minor', 'both'}, default: 'major'
                    elif "ax" in k.lower():  # ax
                        ax.grid(axis=val)  # {'x', 'y', 'both'}, default: 'both'
                    elif ("c" in k.lower()) and ("ect" not in k.lower()):  # c: color
                        ax.grid(color=val)  # Tick color.
                    elif "l" in k.lower() and ("s" in k.lower()):  # ls:line stype
                        ax.grid(linestyle=val)
                    elif "l" in k.lower() and ("w" in k.lower()):  # lw: line width
                        ax.grid(linewidth=val)
                    elif "al" in k.lower():  # alpha:
                        ax.grid(alpha=val)
            else:
                if value == "on" or value is True:
                    ax.grid(visible=True)
                elif value == "off" or value is False:
                    ax.grid(visible=False)
        if "tit" in key.lower():
            if "sup" in key.lower():
                plt.suptitle(value, fontname=fontname, fontsize=fontsize)
            else:
                ax.set_title(value, fontname=fontname, fontsize=fontsize)
        if key.lower() in ["spine", "adjust", "ad", "sp", "spi", "adj", "spines"]:
            if isinstance(value, bool) or (value in ["go", "do", "ja", "yes"]):
                if value:
                    adjust_spines(ax)  # dafault distance=2
            if isinstance(value, (float, int)):
                adjust_spines(ax=ax, distance=value)
        if "c" in key.lower() and (
            "sp" in key.lower() or "ax" in key.lower()
        ):  # spine color
            for loc, spi in ax.spines.items():
                spi.set_color(value)
        if "leg" in key.lower():  # legend
            legend_kws = kwargs.get("legend", None)
            if legend_kws:
                # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
                ax.legend(**legend_kws)
            else:
                legend = ax.get_legend()
                if legend is not None:
                    legend.remove()
        if (
            any(["colorbar" in key.lower(), "cbar" in key.lower()])
            and "loc" in key.lower()
        ):
            cbar = ax.collections[0].colorbar  # Access the colorbar from the plot
            cbar.ax.set_position(
                value
            )  # [left, bottom, width, height] [0.475, 0.15, 0.04, 0.25]

    for arg in args:
        if isinstance(arg, matplotlib.axes._axes.Axes):
            ax = arg
            args = args[1:]
    ax = kwargs.get("ax", plt.gca())
    if "ax" not in locals() or ax is None:
        ax = plt.gca()
    for key, value in kwargs.items():
        set_step_1(ax, key, value)
        set_step_2(ax, key, value)
    for arg in args:
        if isinstance(arg, dict):
            for k, val in arg.items():
                set_step_1(ax, k, val)
            for k, val in arg.items():
                set_step_2(ax, k, val)
        else:
            Nargin = len(args) // 2
            ax.labelFontSizeMultiplier = 1
            ax.titleFontSizeMultiplier = 1
            ax.set_facecolor("w")

            for ip in range(Nargin):
                key = args[ip * 2].lower()
                value = args[ip * 2 + 1]
                set_step_1(ax, key, value)
            for ip in range(Nargin):
                key = args[ip * 2].lower()
                value = args[ip * 2 + 1]
                set_step_2(ax, key, value)

    colors = get_color(8)
    matplotlib.rcParams["axes.prop_cycle"] = cycler(color=colors)
    if len(fig.get_axes()) > 1:
        try:
            plt.tight_layout()
        except Exception as e:
            print(e)


def split_legend(ax, n=2, loc=None, title=None, bbox=None, ncol=1, **kwargs):
    """
    split_legend(
        ax,
        n=2,
        loc=["upper left", "lower right"],
        labelcolor="k",
        fontsize=6,
    )
    """
    # Retrieve all lines and labels from the axis
    handles, labels = ax.get_legend_handles_labels()
    num_labels = len(labels)

    # Calculate the number of labels per legend part
    labels_per_part = (num_labels + n - 1) // n  # Round up
    # Create a list to hold each legend object
    legends = []

    # Default locations and titles if not specified
    if loc is None:
        loc = ["best"] * n
    if title is None:
        title = [None] * n
    if bbox is None:
        bbox = [None] * n

    # Loop to create each split legend
    for i in range(n):
        # Calculate the range of labels for this part
        start_idx = i * labels_per_part
        end_idx = min(start_idx + labels_per_part, num_labels)

        # Skip if no labels in this range
        if start_idx >= end_idx:
            break

        # Subset handles and labels
        part_handles = handles[start_idx:end_idx]
        part_labels = labels[start_idx:end_idx]

        # Create the legend for this part
        legend = ax.legend(
            handles=part_handles,
            labels=part_labels,
            loc=loc[i],
            title=title[i],
            ncol=ncol,
            bbox_to_anchor=bbox[i],
            **kwargs,
        )

        # Add the legend to the axis and save it to the list
        (
            ax.add_artist(legend) if i != (n - 1) else None
        )  # the lastone will be added automaticaly
        legends.append(legend)
    return legends


def get_colors(n: int = 1,cmap: str = "auto",by: str = "start",alpha: float = 1.0,output: str = "hue",*args,**kwargs):
    return get_color(n=n, cmap=cmap, alpha=alpha, output=output, *args, **kwargs)


def get_color(
    n: int = 1,
    cmap: str = "auto",
    by: str = "start",
    alpha: float = 1.0,
    output: str = "hue",
    *args,
    **kwargs,
):
    from cycler import cycler

    def cmap2hex(cmap_name):
        cmap_ = matplotlib.pyplot.get_cmap(cmap_name)
        colors = [cmap_(i) for i in range(cmap_.N)]
        return [matplotlib.colors.rgb2hex(color) for color in colors]
        # usage: clist = cmap2hex("viridis")

    # Cycle times, total number is n (default n=10)
    def cycle2list(colorlist, n=10):
        cycler_ = cycler(tmp=colorlist)
        clist = []
        for i, c_ in zip(range(n), cycler_()):
            clist.append(c_["tmp"])
            if i > n:
                break
        return clist

    # Converts hexadecimal color codes to RGBA values
    def hue2rgb(hex_colors, alpha=1.0):
        def hex_to_rgba(hex_color, alpha=1.0):
            """Converts a hexadecimal color code to RGBA values."""
            if hex_color.startswith("#"):
                hex_color = hex_color.lstrip("#")
            rgb = tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
            return rgb + (alpha,)

        if isinstance(hex_colors, str):
            return hex_to_rgba(hex_colors, alpha)
        elif isinstance(hex_colors, list):
            """Converts a list of hexadecimal color codes to a list of RGBA values."""
            rgba_values = [hex_to_rgba(hex_color, alpha) for hex_color in hex_colors]
            return rgba_values

    def rgba2hue(rgba_color):
        if len(rgba_color) == 3:
            r, g, b = rgba_color
            a = 1
        else:
            r, g, b, a = rgba_color
        # Convert each component to a scale of 0-255
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        a = int(a * 255)
        if a < 255:
            return "#{:02X}{:02X}{:02X}{:02X}".format(r, g, b, a)
        else:
            return "#{:02X}{:02X}{:02X}".format(r, g, b)

    # sc.pl.palettes.default_20
    cmap_20 = [
        "#1f77b4",
        "#ff7f0e",
        "#279e68",
        "#d62728",
        "#aa40fc",
        "#8c564b",
        "#e377c2",
        "#b5bd61",
        "#17becf",
        "#aec7e8",
        "#ffbb78",
        "#98df8a",
        "#ff9896",
        "#c5b0d5",
        "#c49c94",
        "#f7b6d2",
        "#dbdb8d",
        "#9edae5",
        "#ad494a",
        "#8c6d31",
    ]
    # sc.pl.palettes.zeileis_28
    cmap_28 = [
        "#023fa5",
        "#7d87b9",
        "#bec1d4",
        "#d6bcc0",
        "#bb7784",
        "#8e063b",
        "#4a6fe3",
        "#8595e1",
        "#b5bbe3",
        "#e6afb9",
        "#e07b91",
        "#d33f6a",
        "#11c638",
        "#8dd593",
        "#c6dec7",
        "#ead3c6",
        "#f0b98d",
        "#ef9708",
        "#0fcfc0",
        "#9cded6",
        "#d5eae7",
        "#f3e1eb",
        "#f6c4e1",
        "#f79cd4",
        "#7f7f7f",
        "#c7c7c7",
        "#1CE6FF",
        "#336600",
    ]
    if cmap == "gray":
        cmap = "grey"
    elif cmap == "20":
        cmap = cmap_20
    elif cmap == "28":
        cmap = cmap_28
    # Determine color list based on cmap parameter
    if isinstance(cmap, str):
        if "aut" in cmap:
            if n == 1:
                colorlist = ["#3A4453"]
            elif n == 2:
                colorlist = ["#3A4453", "#FF2C00"]
            elif n == 3:
                colorlist = ["#66c2a5", "#fc8d62", "#8da0cb"]
            elif n == 4:
                colorlist = ["#FF2C00", "#087cf7", "#FBAF63", "#3C898A"]
            elif n == 5:
                colorlist = ["#FF2C00", "#459AA9", "#B25E9D", "#4B8C3B", "#EF8632"]
            elif n == 6:
                colorlist = [
                    "#FF2C00",
                    "#91bfdb",
                    "#B25E9D",
                    "#4B8C3B",
                    "#EF8632",
                    "#24578E",
                ]
            elif n == 7:
                colorlist = [
                    "#7F7F7F",
                    "#459AA9",
                    "#B25E9D",
                    "#4B8C3B",
                    "#EF8632",
                    "#24578E",
                    "#FF2C00",
                ]
            elif n == 8:
                # colorlist = ['#1f77b4','#ff7f0e','#367B7F','#51B34F','#d62728','#aa40fc','#e377c2','#17becf']
                # colorlist = ["#367C7E","#51B34F","#881A11","#E9374C","#EF893C","#010072","#385DCB","#EA43E3"]
                colorlist = [
                    "#78BFDA",
                    "#D52E6F",
                    "#F7D648",
                    "#A52D28",
                    "#6B9F41",
                    "#E18330",
                    "#E18B9D",
                    "#3C88CC",
                ]
            elif n == 9:
                colorlist = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#367B7F",
                    "#ff9896",
                    "#d62728",
                    "#aa40fc",
                    "#e377c2",
                    "#51B34F",
                    "#17becf",
                ]
            elif n == 10:
                colorlist = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#367B7F",
                    "#ff9896",
                    "#51B34F",
                    "#d62728" "#aa40fc",
                    "#e377c2",
                    "#375FD2",
                    "#17becf",
                ]
            elif 10 < n <= 20:
                colorlist = cmap_20
            else:
                colorlist = cmap_28
            by = "start"
        elif any(["cub" in cmap.lower(), "sns" in cmap.lower()]):
            if kwargs:
                colorlist = sns.cubehelix_palette(n, **kwargs)
            else:
                colorlist = sns.cubehelix_palette(
                    n, start=0.5, rot=-0.75, light=0.85, dark=0.15, as_cmap=False
                )
            colorlist = [matplotlib.colors.rgb2hex(color) for color in colorlist]
        elif any(["hls" in cmap.lower(), "hsl" in cmap.lower()]):
            if kwargs:
                colorlist = sns.hls_palette(n, **kwargs)
            else:
                colorlist = sns.hls_palette(n)
            colorlist = [matplotlib.colors.rgb2hex(color) for color in colorlist]
        elif any(["col" in cmap.lower(), "pal" in cmap.lower()]):
            palette, desat, as_cmap = None, None, False
            if kwargs:
                for k, v in kwargs.items():
                    if "p" in k:
                        palette = v
                    elif "d" in k:
                        desat = v
                    elif "a" in k:
                        as_cmap = v
            colorlist = sns.color_palette(
                palette=palette, n_colors=n, desat=desat, as_cmap=as_cmap
            )
            colorlist = [matplotlib.colors.rgb2hex(color) for color in colorlist]
        else:
            if by == "start":
                by = "linspace"
            colorlist = cmap2hex(cmap)
    elif isinstance(cmap, list):
        colorlist = cmap

    # Determine method for generating color list
    if "st" in by.lower() or "be" in by.lower():
        clist = cycle2list(colorlist, n=n)
    if "l" in by.lower() or "p" in by.lower():
        clist = []
        [
            clist.append(colorlist[i])
            for i in [int(i) for i in np.linspace(0, len(colorlist) - 1, n)]
        ]

    if "rgb" in output.lower():
        return hue2rgb(clist, alpha)
    elif "h" in output.lower():
        hue_list = []
        [hue_list.append(rgba2hue(i)) for i in hue2rgb(clist, alpha)]
        return hue_list
    else:
        raise ValueError("Invalid output type. Choose 'rgb' or 'hue'.")


def stdshade(ax=None, *args, **kwargs):
    """
    usage:
    plot.stdshade(data_array, c=clist[1], lw=2, ls="-.", alpha=0.2)
    """
    from scipy.signal import savgol_filter

    # Separate kws_line and kws_fill if necessary
    kws_line = kwargs.pop("kws_line", {})
    kws_fill = kwargs.pop("kws_fill", {})

    # Merge kws_line and kws_fill into kwargs
    kwargs.update(kws_line)
    kwargs.update(kws_fill)

    def str2list(str_):
        l = []
        [l.append(x) for x in str_]
        return l

    def hue2rgb(hex_colors):
        def hex_to_rgb(hex_color):
            """Converts a hexadecimal color code to RGB values."""
            if hex_colors.startswith("#"):
                hex_color = hex_color.lstrip("#")
            return tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

        if isinstance(hex_colors, str):
            return hex_to_rgb(hex_colors)
        elif isinstance(hex_colors, (list)):
            """Converts a list of hexadecimal color codes to a list of RGB values."""
            rgb_values = [hex_to_rgb(hex_color) for hex_color in hex_colors]
            return rgb_values

    if (
        isinstance(ax, np.ndarray)
        and ax.ndim == 2
        and min(ax.shape) > 1
        and max(ax.shape) > 1
    ):
        y = ax
        ax = plt.gca()
    if ax is None:
        ax = plt.gca()
    alpha = kwargs.get("alpha", 0.2)
    acolor = kwargs.get("color", "k")
    acolor = kwargs.get("c", "k")
    paraStdSem = "sem"
    plotStyle = "-"
    plotMarker = "none"
    smth = 1
    l_c_one = ["r", "g", "b", "m", "c", "y", "k", "w"]
    l_style2 = ["--", "-."]
    l_style1 = ["-", ":"]
    l_mark = ["o", "+", "*", ".", "x", "_", "|", "s", "d", "^", "v", ">", "<", "p", "h"]
    # Check each argument
    for iarg in range(len(args)):
        if (
            isinstance(args[iarg], np.ndarray)
            and args[iarg].ndim == 2
            and min(args[iarg].shape) > 1
            and max(args[iarg].shape) > 1
        ):
            y = args[iarg]
        # Except y, continuous data is 'F'
        if (isinstance(args[iarg], np.ndarray) and args[iarg].ndim == 1) or isinstance(
            args[iarg], range
        ):
            x = args[iarg]
            if isinstance(x, range):
                x = np.arange(start=x.start, stop=x.stop, step=x.step)
        # Only one number( 0~1), 'alpha' / color
        if isinstance(args[iarg], (int, float)):
            if np.size(args[iarg]) == 1 and 0 <= args[iarg] <= 1:
                alpha = args[iarg]
        if isinstance(args[iarg], (list, tuple)) and np.size(args[iarg]) == 3:
            acolor = args[iarg]
            acolor = tuple(acolor) if isinstance(acolor, list) else acolor
        # Color / plotStyle /
        if (
            isinstance(args[iarg], str)
            and len(args[iarg]) == 1
            and args[iarg] in l_c_one
        ):
            acolor = args[iarg]
        else:
            if isinstance(args[iarg], str):
                if args[iarg] in ["sem", "std"]:
                    paraStdSem = args[iarg]
                if args[iarg].startswith("#"):
                    acolor = hue2rgb(args[iarg])
                if str2list(args[iarg])[0] in l_c_one:
                    if len(args[iarg]) == 3:
                        k = [i for i in str2list(args[iarg]) if i in l_c_one]
                        if k != []:
                            acolor = k[0]
                        st = [i for i in l_style2 if i in args[iarg]]
                        if st != []:
                            plotStyle = st[0]
                    elif len(args[iarg]) == 2:
                        k = [i for i in str2list(args[iarg]) if i in l_c_one]
                        if k != []:
                            acolor = k[0]
                        mk = [i for i in str2list(args[iarg]) if i in l_mark]
                        if mk != []:
                            plotMarker = mk[0]
                        st = [i for i in l_style1 if i in args[iarg]]
                        if st != []:
                            plotStyle = st[0]
                if len(args[iarg]) == 1:
                    k = [i for i in str2list(args[iarg]) if i in l_c_one]
                    if k != []:
                        acolor = k[0]
                    mk = [i for i in str2list(args[iarg]) if i in l_mark]
                    if mk != []:
                        plotMarker = mk[0]
                    st = [i for i in l_style1 if i in args[iarg]]
                    if st != []:
                        plotStyle = st[0]
                if len(args[iarg]) == 2:
                    st = [i for i in l_style2 if i in args[iarg]]
                    if st != []:
                        plotStyle = st[0]
        # smth
        if (
            isinstance(args[iarg], (int, float))
            and np.size(args[iarg]) == 1
            and args[iarg] >= 1
        ):
            smth = args[iarg]
    smth = kwargs.get("smth", smth)
    if "x" not in locals() or x is None:
        x = np.arange(1, y.shape[1] + 1)
    elif len(x) < y.shape[1]:
        y = y[:, x]
        nRow = y.shape[0]
        nCol = y.shape[1]
        print(f"y was corrected, please confirm that {nRow} row, {nCol} col")
    else:
        x = np.arange(1, y.shape[1] + 1)

    if x.shape[0] != 1:
        x = x.T
    yMean = np.nanmean(y, axis=0)
    if smth > 1:
        yMean = savgol_filter(np.nanmean(y, axis=0), smth, 1)
    else:
        yMean = np.nanmean(y, axis=0)
    if paraStdSem == "sem":
        if smth > 1:
            wings = savgol_filter(
                np.nanstd(y, axis=0, ddof=1) / np.sqrt(y.shape[0]), smth, 1
            )
        else:
            wings = np.nanstd(y, axis=0, ddof=1) / np.sqrt(y.shape[0])
    elif paraStdSem == "std":
        if smth > 1:
            wings = savgol_filter(np.nanstd(y, axis=0, ddof=1), smth, 1)
        else:
            wings = np.nanstd(y, axis=0, ddof=1)

    # fill_kws = kwargs.get('fill_kws', {})
    # line_kws = kwargs.get('line_kws', {})

    # setting form kwargs
    lw = kwargs.get("lw", 0.5)
    ls = kwargs.get("ls", plotStyle)
    marker = kwargs.get("marker", plotMarker)
    label = kwargs.get("label", None)
    label_line = kwargs.get("label_line", None)
    label_fill = kwargs.get("label_fill", None)
    alpha = kwargs.get("alpha", alpha)
    color = kwargs.get("color", acolor)
    if not label_line and label:
        label_line = label
    kwargs["lw"] = lw
    kwargs["ls"] = ls
    kwargs["label_line"] = label_line
    kwargs["label_fill"] = label_fill

    # set kws_line
    if "color" not in kws_line:
        kws_line["color"] = color
    if "lw" not in kws_line:
        kws_line["lw"] = lw
    if "ls" not in kws_line:
        kws_line["ls"] = ls
    if "marker" not in kws_line:
        kws_line["marker"] = marker
    if "label" not in kws_line:
        kws_line["label"] = label_line

    # set kws_line
    if "color" not in kws_fill:
        kws_fill["color"] = color
    if "alpha" not in kws_fill:
        kws_fill["alpha"] = alpha
    if "lw" not in kws_fill:
        kws_fill["lw"] = 0
    if "label" not in kws_fill:
        kws_fill["label"] = label_fill

    fill = ax.fill_between(x, yMean + wings, yMean - wings, **kws_fill)
    line = ax.plot(x, yMean, **kws_line)

    # figsets
    kw_figsets = kwargs.get("figsets", None)
    if kw_figsets is not None:
        figsets(ax=ax, **kw_figsets)

    return line[0], fill


"""
########## Usage 1 ##########
plot.stdshade(data,
              'b',
              ':',
              'd',
              0.1,
              4,
              label='ddd',
              label_line='label_line',
              label_fill="label-fill")
plt.legend()

########## Usage 2 ##########
plot.stdshade(data,
              'm-',
              alpha=0.1,
              lw=2,
              ls=':',
              marker='d',
              color='b',
              smth=4,
              label='ddd',
              label_line='label_line',
              label_fill="label-fill")
plt.legend()

"""


def adjust_spines(ax=None, spines=["left", "bottom"], distance=2):
    if ax is None:
        ax = plt.gca()
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(("outward", distance))  # outward by 2 points
            # spine.set_smart_bounds(True)
        else:
            spine.set_color("none")  # don't draw spine
    # turn off ticks where there is no spine
    if "left" in spines:
        ax.yaxis.set_ticks_position("left")
    else:
        ax.yaxis.set_ticks([])
    if "bottom" in spines:
        ax.xaxis.set_ticks_position("bottom")
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])


# And then plot the data:


# def add_colorbar(im, width=None, pad=None, **kwargs):
#     # usage: add_colorbar(im, width=0.01, pad=0.005, label="PSD (dB)", shrink=0.8)
#     l, b, w, h = im.axes.get_position().bounds  # get boundaries
#     width = width or 0.1 * w  # get width of the colorbar
#     pad = pad or width  # get pad between im and cbar
#     fig = im.axes.figure  # get figure of image
#     cax = fig.add_axes([l + w + pad, b, width, h])  # define cbar Axes
#     return fig.colorbar(im, cax=cax, **kwargs)  # draw cbar


def add_colorbar(
    im,
    cmap="viridis",
    vmin=-1,
    vmax=1,
    orientation="vertical",
    width_ratio=0.05,
    pad_ratio=0.02,
    shrink=1.0,
    **kwargs,
):
    import matplotlib as mpl

    if all([cmap, vmin, vmax]):
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    else:
        norm = False
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    l, b, w, h = im.axes.get_position().bounds  # position: left, bottom, width, height
    if orientation == "vertical":
        width = width_ratio * w
        pad = pad_ratio * w
        cax = im.figure.add_axes(
            [l + w + pad, b, width, h * shrink]
        )  # Right of the image
    else:
        height = width_ratio * h
        pad = pad_ratio * h
        cax = im.figure.add_axes(
            [l, b - height - pad, w * shrink, height]
        )  # Below the image
    cbar = im.figure.colorbar(sm, cax=cax, orientation=orientation, **kwargs)
    return cbar


# Usage:
# add_colorbar(im, width_ratio=0.03, pad_ratio=0.01, orientation='horizontal', label="PSD (dB)")


def generate_xticks_with_gap(x_len, hue_len):
    """
    Generate a concatenated array based on x_len and hue_len,
    and return only the positive numbers.

    Parameters:
    - x_len: int, number of segments to generate
    - hue_len: int, length of each hue

    Returns:
    - numpy array: Concatenated array containing only positive numbers
    """

    arrays = [
        np.arange(1, hue_len + 1) + hue_len * (x_len - i) + (x_len - i)
        for i in range(max(x_len, hue_len), 0, -1)  # i iterates from 3 to 1
    ]
    concatenated_array = np.concatenate(arrays)
    positive_array = concatenated_array[concatenated_array > 0].tolist()

    return positive_array


def generate_xticks_x_labels(x_len, hue_len):
    arrays = [
        np.arange(1, hue_len + 1) + hue_len * (x_len - i) + (x_len - i)
        for i in range(max(x_len, hue_len), 0, -1)  # i iterates from 3 to 1
    ]
    return [np.mean(i) for i in arrays if np.mean(i) > 0]


def remove_colors_in_dict(
    data: dict, sections_to_remove_facecolor=["b", "e", "s", "bx", "v"]
):
    # Remove "FaceColor" from specified sections
    for section in sections_to_remove_facecolor:
        if section in data and ("FaceColor" in data[section]):
            del data[section]["FaceColor"]

    if "c" in data:
        del data["c"]
    if "loc" in data:
        del data["loc"]
    return data


def add_asterisks(ax, res, xticks_x_loc, xticklabels, **kwargs_funcstars):
    if len(xticklabels) > 2:
        if isinstance(res, dict):
            pval_groups = res["res_tab"]["p-unc"].tolist()[0]
        else:
            pval_groups = res["res_tab"]["PR(>F)"].tolist()[0]
        report_go = kwargs_funcstars.get("report_go", False)
        if pval_groups <= 0.05:
            A_list = res["res_posthoc"]["A"].tolist()
            B_list = res["res_posthoc"]["B"].tolist()
            xticklabels_array = np.array(xticklabels)
            yscal_ = 0.99
            for A, B, P in zip(
                res["res_posthoc"]["A"].tolist(),
                res["res_posthoc"]["B"].tolist(),
                res["res_posthoc"]["p-unc"].tolist(),
            ):
                index_A = np.where(xticklabels_array == A)[0][0]
                index_B = np.where(xticklabels_array == B)[0][0]
                FuncStars(
                    ax=ax,
                    x1=xticks_x_loc[index_A],
                    x2=xticks_x_loc[index_B],
                    pval=P,
                    yscale=yscal_,
                    **kwargs_funcstars,
                )
                if P <= 0.05:
                    yscal_ -= 0.075
        if report_go:
            try:
                if isinstance(res["APA"], list):
                    APA_str = res["APA"][0]
                else:
                    APA_str = res["APA"]
            except:
                pass

            FuncStars(
                ax=ax,
                x1=(
                    xticks_x_loc[0] - (xticks_x_loc[-1] - xticks_x_loc[0]) / 3
                    if xticks_x_loc[0] > 1
                    else xticks_x_loc[0]
                ),
                x2=(
                    xticks_x_loc[0] - (xticks_x_loc[-1] - xticks_x_loc[0]) / 3
                    if xticks_x_loc[0] > 1
                    else xticks_x_loc[0]
                ),
                pval=None,
                report_scale=np.random.uniform(0.7, 0.99),
                report=APA_str,
                fontsize_note=8,
            )
    else:
        if isinstance(res, tuple):
            res = res[1]
            pval_groups = res["pval"]
            FuncStars(
                ax=ax,
                x1=xticks_x_loc[0],
                x2=xticks_x_loc[1],
                pval=pval_groups,
                **kwargs_funcstars,
            )
        # else:
        #     pval_groups = res["pval"]
        #     FuncStars(
        #         ax=ax,
        #         x1=1,
        #         x2=2,
        #         pval=pval_groups,
        #         **kwargs_funcstars,
        #     )


def style_examples(
    dir_save="/Users/macjianfeng/Dropbox/github/python/py2ls/.venv/lib/python3.12/site-packages/py2ls/data/styles/example",
):
    f = listdir(
        "/Users/macjianfeng/Dropbox/github/python/py2ls/.venv/lib/python3.12/site-packages/py2ls/data/styles/",
        kind=".json",
        verbose=False,
    )
    display(f.sample(2))
    # def style_example(dir_save,)
    # Sample data creation
    np.random.seed(42)
    categories = ["A", "B", "C", "D", "E"]
    data = pd.DataFrame(
        {
            "value": np.concatenate(
                [np.random.normal(loc, 0.4, 100) for loc in range(5)]
            ),
            "category": np.repeat(categories, 100),
        }
    )
    for i in range(f.num[0]):
        plt.figure()
        _, _ = catplot(
            data=data,
            x="category",
            y="value",
            style=i,
            figsets=dict(title=f"style{i+1} or style idx={i}"),
        )
        figsave(
            dir_save,
            f"{f.name[i]}.pdf",
        )


import matplotlib.pyplot as plt
from PIL import Image


def thumbnail(dir_img_list: list, figsize=(10, 10), dpi=100, show=False, verbose=False):
    """
    Display a thumbnail figure of all images in the specified directory.

    Args:
        dir_img_list (list): List of image file paths to display.
        figsize (tuple): Size of the figure (width, height) in inches.
        dpi (int): Dots per inch for the figure.
    """
    if verbose:
        print(
            'thumbnail(listdir("./img-innere-medizin-ii", ["jpeg", "jpg", "png"]).fpath.tolist(),figsize=[5,5],dpi=200)'
        )
    num_images = len(dir_img_list)
    if num_images == 0:
        print("No images found to display.")
        return None

    # Calculate the number of rows and columns for the grid
    cols = int(num_images**0.5)
    rows = (num_images // cols) + (num_images % cols > 0)

    fig, axs = plt.subplots(rows, cols, figsize=figsize, dpi=dpi)
    axs = axs.flatten()  # Flatten the grid for easy iteration

    for ax, image_file in zip(axs, dir_img_list):
        try:
            img = Image.open(image_file)
            ax.imshow(img)
            ax.axis("off")  # Hide axes
        except (IOError, FileNotFoundError) as e:
            ax.axis("off")  # Still hide axes if image can't be loaded

    # Hide any remaining unused axes
    for ax in axs[len(dir_img_list) :]:
        ax.axis("off")

    plt.tight_layout()
    if show:
        plt.show()


def get_params_from_func_usage(function_signature):
    import re

    # Regular expression to match parameter names, ignoring '*' and '**kwargs'
    keys_pattern = r"(?<!\*\*)\b(\w+)="
    # Find all matches
    matches = re.findall(keys_pattern, function_signature)
    return matches


def plot_xy(
    data: pd.DataFrame = None,
    x=None,
    y=None,
    ax=None,
    kind: Union[str, list] = None,  # Specify the kind of plot
    verbose=False,
    **kwargs,
):
    # You can call the original plotxy function if needed
    # or simply replicate the functionality here
    return plotxy(data, x, y, ax, kind, verbose, **kwargs)


def plotxy(
    data: pd.DataFrame = None,
    x=None,
    y=None,
    ax=None,
    kind_: Union[str, list] = "scatter",  # Specify the kind of plot
    verbose=False,
    **kwargs,
):
    """
    e.g., plotxy(data=data_log, x="Component_1", y="Component_2", hue="Cluster",kind='scater)
    Create a variety of plots based on the kind parameter.

    Parameters:
        data (pd.DataFrame): DataFrame containing the data.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        hue (str): Column name for the hue (color) grouping.
        ax: Matplotlib axes object for the plot.
        kind (str): Type of plot ('scatter', 'line', 'displot', 'kdeplot', etc.).
        verbose (bool): If True, print default settings instead of plotting.
        **kwargs: Additional keyword arguments for the plot functions.

    Returns:
        ax or FacetGrid: Matplotlib axes object or FacetGrid for displot.
    """
    # Check for valid plot kind
    # Default arguments for various plot types
    from pathlib import Path

    # Get the current script's directory as a Path object
    current_directory = Path(__file__).resolve().parent

    if not "default_settings" in locals():
        default_settings = fload(current_directory / "data" / "usages_sns.json")
    if not "sns_info" in locals():
        sns_info = pd.DataFrame(fload(current_directory / "data" / "sns_info.json"))

    valid_kinds = list(default_settings.keys())
    # print(valid_kinds)
    if kind_ is not None:
        if isinstance(kind_, str):
            kind_ = [kind_]
        kind_ = [strcmp(i, valid_kinds)[0] for i in kind_]
    else:
        verbose = True

    if verbose:
        if kind_ is not None:
            for k in kind_:
                if k in valid_kinds:
                    print(f"{k}:\n\t{default_settings[k]}")
        usage_str = """plotxy(data=ranked_genes,
        x="log2(fold_change)",
        y="-log10(p-value)",
        palette=get_color(3, cmap="coolwarm"),
        kind_=["scatter","rug"],
        kws_rug=dict(height=0.2),
        kws_scatter=dict(s=20, color=get_color(3)[2]),
        verbose=0)
        """
        print(f"currently support to plot:\n{valid_kinds}\n\nusage:\n{usage_str}")
        return  # Do not plot, just print the usage

    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break
    kws_add_text = {}
    for k_arg, v_arg in kwargs.items():
        if "add" in k_arg and "text" in k_arg:  # add_text
            kws_add_text = v_arg
            kwargs.pop(k_arg, None)
            break
    zorder = 0
    for k in kind_:
        # preprocess data
        try:
            data=df_preprocessing_(data, kind=k)
            if 'variable' in data.columns and 'value' in data.columns:
                x,y='variable','value' 
        except Exception as e:
            print(e)
        zorder += 1
        # indicate 'col' features
        col = kwargs.get("col", None)
        sns_with_col = [
            "catplot",
            "histplot",
            "relplot",
            "lmplot",
            "pairplot",
            "displot",
            "kdeplot",
        ]
        if col is not None:
            if not k in sns_with_col:
                print(
                    f"tips:\n'{k}' has no 'col' param, you could try with {sns_with_col}"
                )
        # (1) return FcetGrid
        if k == "jointplot":
            kws_joint = kwargs.pop("kws_joint", kwargs)
            kws_joint = {
                k: v for k, v in kws_joint.items() if not k.startswith("kws_")
            }
            hue = kwargs.get("hue", None)
            if isinstance(kws_joint, dict) or hue is None:  # Check if kws_ellipse is a dictionary
                kws_joint.pop("hue", None)  # Safely remove 'hue' if it exists

            palette = kwargs.get("palette", None)
            if palette is None:
                palette = kws_joint.pop(
                    "palette", get_color(data[hue].nunique()) if hue is not None else None
                )
            else:
                kws_joint.pop("palette", palette)
            stats=kwargs.pop("stats",None)
            if stats:
                stats=kws_joint.pop("stats",True)
            if stats:
                r, p_value = scipy_stats.pearsonr(data[x], data[y])
            for key in ["palette", "alpha", "hue","stats"]:
                kws_joint.pop(key, None) 
            g = sns.jointplot(data=data, x=x, y=y,hue=hue,palette=palette, **kws_joint)
            if stats:
                g.ax_joint.annotate(
                    f"pearsonr = {r:.2f} p = {p_value:.3f}",
                    xy=(0.6, 0.98),
                    xycoords="axes fraction",
                    fontsize=12,
                    color="black",
                    ha="center",
                )
        elif k == "lmplot":
            kws_lm = kwargs.pop("kws_lm", kwargs)
            stats = kwargs.pop("stats", True)  # Flag to calculate stats
            hue = kwargs.pop("hue", None)  # Get the hue argument (if any)
            col = kwargs.pop("col", None)  # Get the col argument (if any)
            row = kwargs.pop("row", None)  # Get the row argument (if any)

            # Create the linear model plot (lmplot)
            g = sns.lmplot(data=data, x=x, y=y, hue=hue, col=col, row=row, **kws_lm)

            # Compute Pearson correlation and p-value statistics
            if stats:
                stats_per_facet = {}
                stats_per_hue = {}

                # If no hue, col, or row, calculate stats for the entire dataset
                if all([hue is None, col is None, row is None]):
                    r, p_value = scipy_stats.pearsonr(data[x], data[y])
                    stats_per_facet[(None, None)] = (r, p_value)  # Store stats for the entire dataset

                else: 
                    if hue is None and (col is not None or row is not None):
                        for ax in g.axes.flat:
                            facet_name = ax.get_title()
                            if '=' in facet_name:
                                # Assume facet_name is like 'Column = Value'
                                facet_column_name = facet_name.split('=')[0].strip()  # Column name before '='
                                facet_value_str = facet_name.split('=')[1].strip()  # Facet value after '='
                                
                                # Try converting facet_value to match the data type of the DataFrame column
                                facet_column_dtype = data[facet_column_name].dtype
                                if facet_column_dtype == 'int' or facet_column_dtype == 'float':
                                    facet_value = pd.to_numeric(facet_value_str, errors='coerce')  # Convert to numeric
                                else:
                                    facet_value = facet_value_str  # Treat as a string if not numeric
                            else:
                                facet_column_name = facet_name.split('=')[0].strip()  # Column name before '='
                                facet_value=facet_name.split('=')[1].strip() 
                            facet_data = data[data[facet_column_name] == facet_value]
                            if not facet_data.empty:
                                r, p_value = scipy_stats.pearsonr(facet_data[x], facet_data[y])
                                stats_per_facet[facet_name] = (r, p_value)
                            else:
                                stats_per_facet[facet_name] = (None, None)  # Handle empty facets

            # Annotate the stats on the plot
            for ax in g.axes.flat:
                if stats:
                    # Adjust the position for each facet to avoid overlap
                    idx=1
                    shift_factor = 0.02 * idx  # Adjust this factor as needed to prevent overlap
                    y_position = 0.98 - shift_factor  # Dynamic vertical shift for each facet
                    
                    if all([hue is None, col is None, row is None]):
                        # Use stats for the entire dataset if no hue, col, or row
                        r, p_value = stats_per_facet.get((None, None), (None, None))
                        if r is not None and p_value is not None:
                            ax.annotate(
                                f"pearsonr = {r:.2f} p = {p_value:.3f}",
                                xy=(0.6, y_position),
                                xycoords="axes fraction",
                                fontsize=12,
                                color="black",
                                ha="center",
                            )
                        else:
                            ax.annotate(
                                "No stats available",
                                xy=(0.6, y_position),
                                xycoords="axes fraction",
                                fontsize=12,
                                color="black",
                                ha="center",
                            )
                    elif hue is not None:
                        if (col is None and row is None): 
                            hue_categories = sorted(flatten(data[hue],verbose=0))
                            idx=1
                            for category in hue_categories:
                                subset_data = data[data[hue] == category]
                                r, p_value = scipy_stats.pearsonr(subset_data[x], subset_data[y])
                                stats_per_hue[category] = (r, p_value)
                                shift_factor = 0.05 * idx  # Adjust this factor as needed to prevent overlap
                                y_position = 0.98 - shift_factor  # Dynamic vertical shift for each facet
                                ax.annotate(
                                    f"{category}: pearsonr = {r:.2f} p = {p_value:.3f}",
                                    xy=(0.6, y_position),
                                    xycoords="axes fraction",
                                    fontsize=12,
                                    color="black",
                                    ha="center",
                                )
                                idx+=1
                        else:
                            for ax in g.axes.flat:
                                facet_name = ax.get_title()
                                if '=' in facet_name:
                                    # Assume facet_name is like 'Column = Value'
                                    facet_column_name = facet_name.split('=')[0].strip()  # Column name before '='
                                    facet_value_str = facet_name.split('=')[1].strip()  # Facet value after '='
                                    
                                    # Try converting facet_value to match the data type of the DataFrame column
                                    facet_column_dtype = data[facet_column_name].dtype
                                    if facet_column_dtype == 'int' or facet_column_dtype == 'float':
                                        facet_value = pd.to_numeric(facet_value_str, errors='coerce')  # Convert to numeric
                                    else:
                                        facet_value = facet_value_str  # Treat as a string if not numeric
                                else:
                                    facet_column_name = facet_name.split('=')[0].strip()  # Column name before '='
                                    facet_value=facet_name.split('=')[1].strip() 
                                facet_data = data[data[facet_column_name] == facet_value]
                                if not facet_data.empty:
                                    r, p_value = scipy_stats.pearsonr(facet_data[x], facet_data[y])
                                    stats_per_facet[facet_name] = (r, p_value)
                                else:
                                    stats_per_facet[facet_name] = (None, None)  # Handle empty facets
 
                                ax.annotate(
                                    f"pearsonr = {r:.2f} p = {p_value:.3f}",
                                    xy=(0.6, y_position),
                                    xycoords="axes fraction",
                                    fontsize=12,
                                    color="black",
                                    ha="center",
                                ) 
                    elif hue is None and (col is not None or row is not None):
                        # Annotate stats for each facet
                        facet_name = ax.get_title()
                        r, p_value = stats_per_facet.get(facet_name, (None, None))
                        if r is not None and p_value is not None:
                            ax.annotate(
                                f"pearsonr = {r:.2f} p = {p_value:.3f}",
                                xy=(0.6, y_position),
                                xycoords="axes fraction",
                                fontsize=12,
                                color="black",
                                ha="center",
                            )
                        else:
                            ax.annotate(
                                "No stats available",
                                xy=(0.6, y_position),
                                xycoords="axes fraction",
                                fontsize=12,
                                color="black",
                                ha="center")

        elif k == "catplot_sns":
            kws_cat = kwargs.pop("kws_cat", kwargs)
            g = sns.catplot(data=data, x=x, y=y, **kws_cat)
        elif k == "displot":
            kws_dis = kwargs.pop("kws_dis", kwargs)
            # displot creates a new figure and returns a FacetGrid
            g = sns.displot(data=data, x=x,y=y,  **kws_dis)

        # (2) return axis
        if ax is None:
            ax = plt.gca()
        if k == "catplot":
            kws_cat = kwargs.pop("kws_cat", kwargs)
            g = catplot(data=data, x=x, y=y, ax=ax, **kws_cat)
        elif k == "stdshade":
            kws_stdshade = kwargs.pop("kws_stdshade", kwargs)
            ax = stdshade(ax=ax, **kwargs)
        elif k=="ellipse":
            kws_ellipse = kwargs.pop("kws_ellipse", kwargs)
            kws_ellipse = {
                k: v for k, v in kws_ellipse.items() if not k.startswith("kws_")
            }
            hue = kwargs.get("hue", None)
            if isinstance(kws_ellipse, dict) or hue is None:  # Check if kws_ellipse is a dictionary
                kws_ellipse.pop("hue", None)  # Safely remove 'hue' if it exists

            palette = kwargs.get("palette", None)
            if palette is None:
                palette = kws_ellipse.pop(
                    "palette", get_color(data[hue].nunique()) if hue is not None else None
                )
            alpha = kws_ellipse.pop("alpha", 0.1)
            hue_order = kwargs.get("hue_order",None)
            if hue_order is None:
                hue_order = kws_ellipse.get("hue_order",None)
            if hue_order: 
                data["hue"] = pd.Categorical(data[hue], categories=hue_order, ordered=True)
                data = data.sort_values(by="hue")
            for key in ["palette", "alpha", "hue","hue_order"]:
                kws_ellipse.pop(key, None) 
            ax=ellipse(
                ax=ax,
                data=data,
                x=x,
                y=y,
                hue=hue,
                palette=palette,
                alpha=alpha,
                zorder=zorder,
                **kws_ellipse,
            )
        elif k == "scatterplot":
            kws_scatter = kwargs.pop("kws_scatter", kwargs)
            kws_scatter = {
                k: v for k, v in kws_scatter.items() if not k.startswith("kws_")
            }
            hue = kwargs.get("hue", None)
            if isinstance(kws_scatter, dict):  # Check if kws_scatter is a dictionary
                kws_scatter.pop("hue", None)  # Safely remove 'hue' if it exists
            palette=kws_scatter.get("palette",None)
            if palette is None:
                palette = kws_scatter.pop(
                    "palette", get_color(data[hue].nunique()) if hue is not None else None
                )
            s = kws_scatter.pop("s", 10)
            alpha = kws_scatter.pop("alpha", 0.7)                       
            for key in ["s", "palette", "alpha", "hue"]:
                kws_scatter.pop(key, None)

            ax = sns.scatterplot(
                ax=ax,
                data=data,
                x=x,
                y=y,
                hue=hue,
                palette=palette,
                s=s,
                alpha=alpha,
                zorder=zorder,
                **kws_scatter,
            )
        elif k == "histplot":
            kws_hist = kwargs.pop("kws_hist", kwargs)
            kws_hist = {k: v for k, v in kws_hist.items() if not k.startswith("kws_")}
            ax = sns.histplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_hist)
        elif k == "kdeplot": 
            kws_kde = kwargs.pop("kws_kde", kwargs)
            kws_kde = {
                k: v for k, v in kws_kde.items() if not k.startswith("kws_")
            }
            hue = kwargs.get("hue", None)
            if isinstance(kws_kde, dict) or hue is None:  # Check if kws_kde is a dictionary
                kws_kde.pop("hue", None)  # Safely remove 'hue' if it exists

            palette = kwargs.get("palette", None)
            if palette is None:
                palette = kws_kde.pop(
                    "palette", get_color(data[hue].nunique()) if hue is not None else None
                )
            alpha = kws_kde.pop("alpha", 0.05)
            for key in ["palette", "alpha", "hue"]:
                kws_kde.pop(key, None) 
            ax = sns.kdeplot(data=data, x=x, y=y, palette=palette,hue=hue, ax=ax,alpha=alpha, zorder=zorder, **kws_kde)
        elif k == "ecdfplot":
            kws_ecdf = kwargs.pop("kws_ecdf", kwargs)
            kws_ecdf = {k: v for k, v in kws_ecdf.items() if not k.startswith("kws_")}
            ax = sns.ecdfplot(data=data, x=x,y=y,  ax=ax, zorder=zorder, **kws_ecdf)
        elif k == "rugplot":
            kws_rug = kwargs.pop("kws_rug", kwargs)
            kws_rug = {k: v for k, v in kws_rug.items() if not k.startswith("kws_")}
            ax = sns.rugplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_rug)
        elif k == "stripplot":
            kws_strip = kwargs.pop("kws_strip", kwargs)
            kws_strip = {k: v for k, v in kws_strip.items() if not k.startswith("kws_")}
            dodge = kws_strip.pop("dodge", True)
            ax = sns.stripplot(
                data=data, x=x, y=y, ax=ax, zorder=zorder, dodge=dodge, **kws_strip
            )
        elif k == "swarmplot":
            kws_swarm = kwargs.pop("kws_swarm", kwargs)
            kws_swarm = {k: v for k, v in kws_swarm.items() if not k.startswith("kws_")}
            ax = sns.swarmplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_swarm)
        elif k == "boxplot":
            kws_box = kwargs.pop("kws_box", kwargs)
            kws_box = {k: v for k, v in kws_box.items() if not k.startswith("kws_")}
            ax = sns.boxplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_box)
        elif k == "violinplot":
            kws_violin = kwargs.pop("kws_violin", kwargs)
            kws_violin = {
                k: v for k, v in kws_violin.items() if not k.startswith("kws_")
            }
            ax = sns.violinplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_violin)
        elif k == "boxenplot":
            kws_boxen = kwargs.pop("kws_boxen", kwargs)
            kws_boxen = {k: v for k, v in kws_boxen.items() if not k.startswith("kws_")}
            ax = sns.boxenplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_boxen)
        elif k == "pointplot":
            kws_point = kwargs.pop("kws_point", kwargs)
            kws_point = {k: v for k, v in kws_point.items() if not k.startswith("kws_")}
            ax = sns.pointplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_point)
        elif k == "barplot":
            kws_bar = kwargs.pop("kws_bar", kwargs)
            kws_bar = {k: v for k, v in kws_bar.items() if not k.startswith("kws_")}
            ax = sns.barplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_bar)
        elif k == "countplot":
            kws_count = kwargs.pop("kws_count", kwargs)
            kws_count = {k: v for k, v in kws_count.items() if not k.startswith("kws_")}
            if not kws_count.get("hue", None):
                kws_count.pop("palette", None)
            ax = sns.countplot(data=data, x=x, y=y, ax=ax, zorder=zorder, **kws_count)
        elif k == "regplot":
            kws_reg = kwargs.pop("kws_reg", kwargs)
            kws_reg = {k: v for k, v in kws_reg.items() if not k.startswith("kws_")}
            stats = kwargs.pop("stats", True)  # Flag to calculate stats
    
            # Compute Pearson correlation if stats is True
            if stats:
                r, p_value = scipy_stats.pearsonr(data[x], data[y])
            ax = sns.regplot(data=data, x=x, y=y, ax=ax,   **kws_reg)
            
            # Annotate the Pearson correlation and p-value
            ax.annotate(
                    f"pearsonr = {r:.2f} p = {p_value:.3f}",
                    xy=(0.6, 0.98),
                    xycoords="axes fraction",
                    fontsize=12,
                    color="black",
                    ha="center",
                )
        elif k == "residplot":
            kws_resid = kwargs.pop("kws_resid", kwargs)
            kws_resid = {k: v for k, v in kws_resid.items() if not k.startswith("kws_")}
            ax = sns.residplot(
                data=data, x=x, y=y, lowess=True, zorder=zorder, ax=ax, **kws_resid
            )
        elif k == "lineplot":
            kws_line = kwargs.pop("kws_line", kwargs)
            kws_line = {k: v for k, v in kws_line.items() if not k.startswith("kws_")}
            ax = sns.lineplot(ax=ax, data=data, x=x, y=y, zorder=zorder, **kws_line)

        figsets(ax=ax, **kws_figsets)
        if kws_add_text:
            add_text(ax=ax, **kws_add_text) if kws_add_text else None
    if run_once_within(10):
        for k in kind_:
            print(f"\n{k}⤵ ")
            print(default_settings[k])
            # print("=>\t",sns_info[sns_info["Functions"].str.contains(k)].iloc[:, -1].tolist()[0],"\n")
    if "g" in locals():
        if ax is not None:
            return g, ax
    return ax

import pandas as pd


def df_preprocessing_(data, kind, verbose=False):
    """
    Automatically formats data for various seaborn plot types.

    Parameters:
    - data (pd.DataFrame): Original DataFrame.
    - kind (str): Type of seaborn plot, e.g., "heatmap", "boxplot", "violinplot", "lineplot", "scatterplot", "histplot", "kdeplot", "catplot", "barplot".
    - verbose (bool): If True, print detailed information about the data format conversion.

    Returns:
    - pd.DataFrame: Formatted DataFrame ready for the specified seaborn plot type.
    """
    # Determine data format: 'long', 'wide', or 'uncertain'
    df_format_ = df_format(data)

    # Correct plot type name
    kind = strcmp(
        kind,
        [
            "heatmap",
            "pairplot",
            "jointplot",  # Typically requires wide format for axis variables
            "facetgrid",   # Used for creating small multiples (can work with wide format)
            "barplot",     # Can be used with wide format
            "pointplot",   # Works well with wide format
            "pivot_table", # Works with wide format (aggregated data)
            "boxplot",
            "violinplot",
            "stripplot",
            "swarmplot",
            "catplot",
            "lineplot",
            "scatterplot",
            "relplot",
            "barplot",     # Can also work with long format (aggregated data in long form)
            "boxenplot",   # Similar to boxplot, works with long format
            "countplot",   # Works best with long format (categorical data)
            "heatmap",     # Can work with long format after reshaping
            "lineplot",    # Can work with long format (time series, continuous)
            "histplot",    # Can be used with both wide and long formats
            "kdeplot",     # Works with both wide and long formats
            "ecdfplot",    # Works with both formats
            "scatterplot", # Can work with both formats depending on data structure
            "lineplot",    # Can work with both wide and long formats
            "area plot",   # Can work with both formats, useful for stacked areas
            "violinplot",  # Can work with both formats depending on categorical vs continuous data
            "ellipse",# ellipse plot, default confidence=0.95
        ],
    )[0]

    wide_kinds = [ 
        "pairplot",
    ]

    # Define plot types that require 'long' format
    long_kinds = [
        "catplot",
    ]

    # Flexible kinds: distribution plots can use either format
    flexible_kinds = [
        "jointplot",  # Typically requires wide format for axis variables
        "lineplot",    # Can work with long format (time series, continuous)
        "lineplot",
        "scatterplot",
        "barplot",     # Can also work with long format (aggregated data in long form)
        "boxenplot",   # Similar to boxplot, works with long format
        "countplot",   # Works best with long format (categorical data)
        "regplot",
        "violinplot",
        "stripplot",
        "swarmplot",
        "boxplot",
        "histplot",    # Can be used with both wide and long formats
        "kdeplot",     # Works with both wide and long formats
        "ecdfplot",    # Works with both formats
        "scatterplot", # Can work with both formats depending on data structure
        "lineplot",    # Can work with both wide and long formats
        "area plot",   # Can work with both formats, useful for stacked areas
        "violinplot",  # Can work with both formats depending on categorical vs continuous data
        "relplot",
        "pointplot",   # Works well with wide format
        "ellipse",
    ]

    # Wide format (e.g., for heatmap and pairplot)
    if kind in wide_kinds:
        if df_format_ != "wide":
            if verbose:
                print("Converting to wide format for", kind)
            return data.corr() if kind == "heatmap" else data
        return data

    # Long format for categorical plots or time series
    elif kind in long_kinds:
        if df_format_ == "wide":
            if verbose:
                print("Converting wide data to long format for", kind)
            return pd.melt(data, var_name="variable", value_name="value")
        elif df_format_ == "uncertain":
            if verbose:
                print("Data format is uncertain, attempting to melt for", kind)
            return pd.melt(data, var_name="variable", value_name="value")
        return data

    # Flexible format: distribution plots can use either long or wide
    elif kind in flexible_kinds:
        if df_format_ == "wide" or df_format_ == "long":
            return data
        if verbose:
            print("Converting uncertain format to long format for distribution plots")
        return pd.melt(data, var_name="variable", value_name="value")

    else:
        if verbose:
            print("Unrecognized plot type; returning original data without conversion.")
        return data


def norm_cmap(data, cmap="coolwarm", min_max=[0, 1]):
    norm_ = plt.Normalize(min_max[0], min_max[1])
    colormap = plt.get_cmap(cmap)
    return colormap(norm_(data))


def volcano(
    data: pd.DataFrame,
    x: str,
    y: str,
    gene_col: str = None,
    top_genes=[5, 5],  # [down-regulated, up-regulated]
    thr_x=np.log2(1.5),  # default: 0.585
    thr_y=-np.log10(0.05),
    sort_xy="x",  #'y', 'xy'
    colors=("#00BFFF", "#9d9a9a", "#FF3030"),
    s=20,
    fill=True,  # plot filled scatter
    facecolor="none",
    edgecolor="none",
    edgelinewidth=0.5,
    alpha=0.8,
    legend=False,
    ax=None,
    verbose=False,
    kws_text=dict(fontsize=10, color="k"),
    kws_bbox=dict(
        facecolor="none", alpha=0.5, edgecolor="black", boxstyle="round,pad=0.3"
    ),  # '{}' to hide
    kws_arrow=dict(color="k", lw=0.5),  # '{}' to hide
    **kwargs,
):
    """
    Generates a customizable scatter plot (e.g., volcano plot).

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame containing the data to plot.
    x : str
        Column name for x-axis values (e.g., log2FoldChange).
    y : str
        Column name for y-axis values (e.g., -log10(FDR)).
    gene_col : str, optional
        Column name for gene names. If provided, gene names will be displayed. Default is None.
    top_genes : int, list, optional
        Number of top genes to label based on y-axis values. Default is 5.
    thr_x : float, optional
        Threshold for x-axis values. Default is 0.585.
    thr_y : float, optional
        Threshold for y-axis values (e.g., significance threshold). Default is -np.log10(0.05).
    colors : tuple, optional
        Colors for points above/below thresholds and neutral points. Default is ("red", "blue", "gray").
    figsize : tuple, optional
        Figure size. Default is (6, 4).
    s : int, optional
        Size of points in the plot. Default is 20.
    fontsize : int, optional
        Font size for gene labels. Default is 10.
    alpha : float, optional
        Transparency of the points. Default is 0.8.
    legend : bool, optional
        Whether to show a legend. Default is False.
    """
    usage_str = """
    _, axs = plt.subplots(1, 1, figsize=(4, 5))
    volcano(
        ax=axs,
        data=ranked_genes,
        x="log2(fold_change)",
        y="-log10(p-value)",
        gene_col="ID_REF",
        top_genes=6,
        thr_x=np.log2(1.2),
        # thr_y=-np.log10(0.05),
        colors=("#00BFFF", "#9d9a9a", "#FF3030"),
        fill=0,
        alpha=1,
        facecolor="none",
        s=20,
        edgelinewidth=0.5,
        edgecolor="0.5",
        kws_text=dict(fontsize=10, color="k"),
        kws_arrow=dict(style="-", color="k", lw=0.5),
        # verbose=True,
        figsets=dict(ylim=[0, 10], title="df"),
    )
    """
    if verbose:
        print(usage_str)
        return
    from adjustText import adjust_text

    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break

    data = data.copy()
    # filter nan
    data = data.dropna(subset=[x, y])  # Drop rows with NaN in x or y
    data.loc[:, "color"] = np.where(
        (data[x] > thr_x) & (data[y] > thr_y),
        colors[2],
        np.where((data[x] < -thr_x) & (data[y] > thr_y), colors[0], colors[1]),
    )
    top_genes = [top_genes, top_genes] if isinstance(top_genes, int) else top_genes

    # could custom how to select the top genes, x: x has priority
    sort_by_x_y = [x, y] if sort_xy == "x" else [y, x]
    ascending_up = [True, True] if sort_xy == "x" else [False, True]
    ascending_down = [False, True] if sort_xy == "x" else [False, False]

    down_reg_genes = (
        data[(data["color"] == colors[0]) & (data[x].abs() > thr_x) & (data[y] > thr_y)]
        .sort_values(by=sort_by_x_y, ascending=ascending_up)
        .head(top_genes[0])
    )
    up_reg_genes = (
        data[(data["color"] == colors[2]) & (data[x].abs() > thr_x) & (data[y] > thr_y)]
        .sort_values(by=sort_by_x_y, ascending=ascending_down)
        .head(top_genes[1])
    )
    sele_gene = pd.concat([down_reg_genes, up_reg_genes])

    palette = {colors[0]: colors[0], colors[1]: colors[1], colors[2]: colors[2]}
    # Plot setup
    if ax is None:
        ax = plt.gca()

    # Handle fill parameter
    if fill:
        facecolors = data["color"]  # Fill with colors
        edgecolors = edgecolor  # Set edgecolor
    else:
        facecolors = facecolor  # No fill, use edge color as the face color
        edgecolors = data["color"]

    ax = sns.scatterplot(
        ax=ax,
        data=data,
        x=x,
        y=y,
        hue="color",
        palette=palette,
        s=s,
        linewidths=edgelinewidth,
        color=facecolors,
        edgecolor=edgecolors,
        alpha=alpha,
        legend=legend,
        **kwargs,
    )

    # Add threshold lines for x and y axes
    ax.axhline(y=thr_y, color="black", linestyle="--", lw=1)
    ax.axvline(x=-thr_x, color="black", linestyle="--", lw=1)
    ax.axvline(x=thr_x, color="black", linestyle="--", lw=1)

    # Add gene labels for selected significant points
    if gene_col:
        texts = []
        # if kws_text:
        fontname = kws_text.pop("fontname", "Arial")
        textcolor = kws_text.pop("color", "k")
        fontsize = kws_text.pop("fontsize", 10)
        arrowstyles = [
            "->",
            "<-",
            "<->",
            "<|-",
            "-|>",
            "<|-|>",
            "-",
            "-[",
            "-[",
            "fancy",
            "simple",
            "wedge",
        ]
        arrowstyle = kws_arrow.pop("style", "<|-")
        arrowstyle = strcmp(arrowstyle, arrowstyles, scorer="strict")[0]
        expand = kws_arrow.pop("expand", (1.05, 1.1))
        arrowcolor = kws_arrow.pop("color", "0.4")
        arrowlinewidth = kws_arrow.pop("lw", 0.75)
        shrinkA = kws_arrow.pop("shrinkA", 0)
        shrinkB = kws_arrow.pop("shrinkB", 0)
        mutation_scale = kws_arrow.pop("head", 10)
        arrow_fill = kws_arrow.pop("fill", False)
        for i in range(sele_gene.shape[0]):
            if isinstance(textcolor, list):  # be consistant with dots's color
                textcolor = colors[0] if sele_gene[x].iloc[i] > 0 else colors[1]
            texts.append(
                ax.text(
                    x=sele_gene[x].iloc[i],
                    y=sele_gene[y].iloc[i],
                    s=sele_gene[gene_col].iloc[i],
                    bbox=kws_bbox if kws_bbox else None,
                    fontdict={
                        "fontsize": fontsize,
                        "color": textcolor,
                        "fontname": fontname,
                    },
                )
            )
        print(arrowstyle)
        adjust_text(
            texts,
            expand=expand,
            min_arrow_len=5,
            ax=ax,
            arrowprops=dict(
                arrowstyle=arrowstyle,
                fill=arrow_fill,
                color=arrowcolor,
                lw=arrowlinewidth,
                shrinkA=shrinkA,
                shrinkB=shrinkB,
                mutation_scale=mutation_scale,
                **kws_arrow,
            ),
        )

    figsets(**kws_figsets)


def sns_func_info(dir_save=None):
    sns_info = {
        "Functions": [
            "relplot",
            "scatterplot",
            "lineplot",
            "lmplot",
            "catplot",
            "stripplot",
            "boxplot",
            "violinplot",
            "boxenplot",
            "pointplot",
            "barplot",
            "countplot",
            "displot",
            "histplot",
            "kdeplot",
            "ecdfplot",
            "rugplot",
            "regplot",
            "residplot",
            "pairplot",
            "jointplot",
            "plotting_context",
        ],
        "Category": [
            "relational",
            "relational",
            "relational",
            "relational",
            "categorical",
            "categorical",
            "categorical",
            "categorical",
            "categorical",
            "categorical",
            "categorical",
            "categorical",
            "distribution",
            "distribution",
            "distribution",
            "distribution",
            "distribution",
            "regression",
            "regression",
            "grid-based(fig)",
            "grid-based(fig)",
            "context",
        ],
        "Detail": [
            "A figure-level function for creating scatter plots and line plots. It combines the functionality of scatterplot and lineplot.",
            "A function for creating scatter plots, useful for visualizing the relationship between two continuous variables.",
            "A function for drawing line plots, often used to visualize trends over time or ordered categories.",
            "A figure-level function for creating linear model plots, combining regression lines with scatter plots.",
            "A figure-level function for creating categorical plots, which can display various types of plots like box plots, violin plots, and bar plots in one function.",
            "A function for creating a scatter plot where one of the variables is categorical, helping visualize distribution along a categorical axis.",
            "A function for creating box plots, which summarize the distribution of a continuous variable based on a categorical variable.",
            "A function for creating violin plots, which combine box plots and KDEs to visualize the distribution of data.",
            "A function for creating boxen plots, an enhanced version of box plots that better represent data distributions with more quantiles.",
            "A function for creating point plots, which show the mean (or another estimator) of a variable for each level of a categorical variable.",
            "A function for creating bar plots, which represent the mean (or other estimators) of a variable with bars, typically used with categorical data.",
            "A function for creating count plots, which show the counts of observations in each categorical bin.",
            "A figure-level function that creates distribution plots. It can visualize histograms, KDEs, and ECDFs, making it versatile for analyzing the distribution of data.",
            "A function for creating histograms, useful for showing the frequency distribution of a continuous variable.",
            "A function for creating kernel density estimate (KDE) plots, which visualize the probability density function of a continuous variable.",
            "A function for creating empirical cumulative distribution function (ECDF) plots, which show the proportion of observations below a certain value.",
            "A function that adds a rug plot to the axes, representing individual data points along an axis.",
            "A function for creating regression plots, which fit and visualize a regression model on scatter data.",
            "A function for creating residual plots, useful for diagnosing the fit of a regression model.",
            "A figure-level function that creates a grid of scatter plots for each pair of variables in a dataset, often used for exploratory data analysis.",
            "A figure-level function that combines scatter plots and histograms (or KDEs) to visualize the relationship between two variables and their distributions.",
            "Not a plot itself, but a function that allows you to change the context (style and scaling) of your plots to fit different publication requirements or visual preferences.",
        ],
    }
    if dir_save is None:
        if "mac" in get_os():
            dir_save = "/Users/macjianfeng/Dropbox/github/python/py2ls/py2ls/data/"
        else:
            dir_save = "Z:\\Jianfeng\\temp\\"
    dir_save += "/" if not dir_save.endswith("/") else ""
    fsave(
        dir_save + "sns_info.json",
        sns_info,
    )


def get_color_overlap(*colors):
    import matplotlib.colors as mcolors

    """Blend multiple colors by averaging their RGB values."""
    rgbs = [mcolors.to_rgb(color) for color in colors]
    blended_rgb = [sum(channel) / len(channel) for channel in zip(*rgbs)]
    return mcolors.to_hex(blended_rgb)


def desaturate_color(color, saturation_factor=0.5):
    """Reduce the saturation of a color by a given factor (between 0 and 1)."""
    import matplotlib.colors as mcolors
    import colorsys

    # Convert the color to RGB
    rgb = mcolors.to_rgb(color)
    # Convert RGB to HLS (Hue, Lightness, Saturation)
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # Reduce the saturation
    s *= saturation_factor
    # Convert back to RGB
    return colorsys.hls_to_rgb(h, l, s)


def textsets(
    text,
    fontname="Arial",
    fontsize=11,
    fontweight="normal",
    fontstyle="normal",
    fontcolor="k",
    backgroundcolor=None,
    shadow=False,
    ha="center",
    va="center",
):
    if text:  # Ensure text exists
        if fontname:
            text.set_fontname(plt_font(fontname))
        if fontsize:
            text.set_fontsize(fontsize)
        if fontweight:
            text.set_fontweight(fontweight)
        if fontstyle:
            text.set_fontstyle(fontstyle)
        if fontcolor:
            text.set_color(fontcolor)
        if backgroundcolor:
            text.set_backgroundcolor(backgroundcolor)
        text.set_horizontalalignment(ha)
        text.set_verticalalignment(va)
        if shadow:
            text.set_path_effects(
                [matplotlib.patheffects.withStroke(linewidth=3, foreground="gray")]
            )


def venn(
    lists: list,
    labels: list = None,
    ax=None,
    colors=None,
    edgecolor=None,
    alpha=0.5,
    saturation=0.75,
    linewidth=0,  # default no edge
    linestyle="-",
    fontname="Arial",
    fontsize=10,
    fontcolor="k",
    fontweight="normal",
    fontstyle="normal",
    ha="center",
    va="center",
    shadow=False,
    subset_fontsize=10,
    subset_fontweight="normal",
    subset_fontstyle="normal",
    subset_fontcolor="k",
    backgroundcolor=None,
    custom_texts=None,
    show_percentages=True,  # display percentage
    fmt="{:.1%}",
    ellipse_shape=False,  # 椭圆形
    ellipse_scale=[1.5, 1],  # not perfect, 椭圆形的形状
    **kwargs,
):
    """
    Advanced Venn diagram plotting function with extensive customization options.
    Usage:
        # Define the two sets
        set1 = [1, 2, 3, 4, 5]
        set2 = [4, 5, 6, 7, 8]
        set3 = [1, 2, 4, 7, 9, 10, 11, 6, 103]
        _, axs = plt.subplots(1, 2)
        venn(
            [set1, set2],
            ["Set A", "Set B"],
            colors=["r", "b"],
            edgecolor="r",
            linewidth=0,
            ax=axs[0],
        )
        venn(
            [set1, set2, set3],
            ["Set A", "Set B", "Set 3"],
            colors=["r", "g", "b"],
            saturation=0.8,
            linewidth=[3, 5, 7],
            linestyle=[":", "-", "--"],
            # edgecolor="r",
            # alpha=1,
            ax=axs[1],
        )

    Parameters:
        lists: list of sets, 2 or 3 sets
        labels: list of strings, labels for the sets
        ax: matplotlib axis, optional
        colors: list of colors, colors for the Venn diagram patches
        edgecolor: string, color of the circle edges
        alpha: float, transparency level for the patches
        linewidth: float, width of the circle edges
        linestyle: string, line style for the circles
        fontname: string, font for set labels
        fontsize: int, font size for set labels
        fontweight: string, weight of the set label font (e.g., 'bold', 'light')
        fontstyle: string, style of the set label font (e.g., 'italic')
        label_align: string, horizontal alignment of set labels ('left', 'center', 'right')
        label_baseline: string, vertical alignment of set labels ('top', 'center', 'bottom')
        subset_fontsize: int, font size for subset labels (the numbers)
        subset_fontweight: string, weight of subset label font
        subset_fontstyle: string, style of subset label font
        subset_label_format: string, format for subset labels (e.g., "{:.2f}" for floats)
        shadow: bool, add shadow effect to the patches
        custom_texts: list of custom texts to replace the subset labels
        **kwargs: additional keyword arguments passed to venn2 or venn3
    """
    if ax is None:
        ax = plt.gca()
    if isinstance(lists, dict):
        labels = list(lists.keys())
        lists = list(lists.values())
    if isinstance(lists[0], set):
        lists = [list(i) for i in lists]
    lists = [set(flatten(i, verbose=False)) for i in lists]
    # Function to apply text styles to labels
    if colors is None:
        colors = ["r", "b"] if len(lists) == 2 else ["r", "g", "b"]
    if labels is None:
        if len(lists) == 2:
            labels = ["set1", "set2"] 
        elif len(lists) == 3: 
            labels = ["set1", "set2", "set3"]
        elif len(lists) == 4: 
            labels = ["set1", "set2", "set3","set4"]
        elif len(lists) == 5: 
            labels = ["set1", "set2", "set3","set4","set55"]
        elif len(lists) == 6: 
            labels = ["set1", "set2", "set3","set4","set5","set6"]
        elif len(lists) == 7: 
            labels = ["set1", "set2", "set3","set4","set5","set6","set7"]
    if edgecolor is None:
        edgecolor = colors
    colors = [desaturate_color(color, saturation) for color in colors]
    universe = len(set.union(*lists))

    # Check colors and auto-calculate overlaps
    def get_count_and_percentage(set_count, subset_count):
        percent = subset_count / set_count if set_count > 0 else 0
        return (
            f"{subset_count}\n({fmt.format(percent)})"
            if show_percentages
            else f"{subset_count}"
        )
    if fmt is not None:
        if not fmt.startswith("{"):
            fmt="{:" + fmt + "}"
    if len(lists) == 2: 

        from matplotlib_venn import venn2, venn2_circles

        # Auto-calculate overlap color for 2-set Venn diagram
        overlap_color = get_color_overlap(colors[0], colors[1]) if colors else None

        # Draw the venn diagram
        v = venn2(subsets=lists, set_labels=labels, ax=ax, **kwargs)
        venn_circles = venn2_circles(subsets=lists, ax=ax)
        set1, set2 = lists[0], lists[1]
        v.get_patch_by_id("10").set_color(colors[0])
        v.get_patch_by_id("01").set_color(colors[1])
        try:
            v.get_patch_by_id("11").set_color(
                get_color_overlap(colors[0], colors[1]) if colors else None
            )
        except Exception as e:
            print(e)
        # v.get_label_by_id('10').set_text(len(set1 - set2))
        # v.get_label_by_id('01').set_text(len(set2 - set1))
        # v.get_label_by_id('11').set_text(len(set1 & set2))
        
        v.get_label_by_id("10").set_text(
            get_count_and_percentage(universe, len(set1 - set2))
        )
        v.get_label_by_id("01").set_text(
            get_count_and_percentage(universe, len(set2 - set1))
        )
        try:
            v.get_label_by_id("11").set_text(
                get_count_and_percentage(universe, len(set1 & set2))
            )
        except Exception as e:
            print(e)

        if not isinstance(linewidth, list):
            linewidth = [linewidth]
        if isinstance(linestyle, str):
            linestyle = [linestyle]
        if not isinstance(edgecolor, list):
            edgecolor = [edgecolor]
        linewidth = linewidth * 2 if len(linewidth) == 1 else linewidth
        linestyle = linestyle * 2 if len(linestyle) == 1 else linestyle
        edgecolor = edgecolor * 2 if len(edgecolor) == 1 else edgecolor
        for i in range(2):
            venn_circles[i].set_lw(linewidth[i])
            venn_circles[i].set_ls(linestyle[i])
            venn_circles[i].set_edgecolor(edgecolor[i])
        # 椭圆
        if ellipse_shape:
            import matplotlib.patches as patches

            for patch in v.patches:
                patch.set_visible(False)  # Hide original patches if using ellipses
            center1 = v.get_circle_center(0)
            center2 = v.get_circle_center(1)
            ellipse1 = patches.Ellipse(
                (center1.x, center1.y),
                width=ellipse_scale[0],
                height=ellipse_scale[1],
                edgecolor=edgecolor[0] if edgecolor else colors[0],
                facecolor=colors[0],
                lw=(
                    linewidth if isinstance(linewidth, (int, float)) else 1.0
                ),  # Ensure lw is a number
                ls=linestyle[0],
                alpha=(
                    alpha if isinstance(alpha, (int, float)) else 0.5
                ),  # Ensure alpha is a number
            )
            ellipse2 = patches.Ellipse(
                (center2.x, center2.y),
                width=ellipse_scale[0],
                height=ellipse_scale[1],
                edgecolor=edgecolor[1] if edgecolor else colors[1],
                facecolor=colors[1],
                lw=(
                    linewidth if isinstance(linewidth, (int, float)) else 1.0
                ),  # Ensure lw is a number
                ls=linestyle[0],
                alpha=(
                    alpha if isinstance(alpha, (int, float)) else 0.5
                ),  # Ensure alpha is a number
            )
            ax.add_patch(ellipse1)
            ax.add_patch(ellipse2)
        # Apply styles to set labels
        for i, text in enumerate(v.set_labels):
            textsets(
                text,
                fontname=fontname,
                fontsize=fontsize,
                fontweight=fontweight,
                fontstyle=fontstyle,
                fontcolor=fontcolor,
                ha=ha,
                va=va,
                shadow=shadow,
            )

        # Apply styles to subset labels
        for i, text in enumerate(v.subset_labels):
            if text:  # Ensure text exists
                if custom_texts:  # Custom text handling
                    text.set_text(custom_texts[i])
                textsets(
                    text,
                    fontname=fontname,
                    fontsize=subset_fontsize,
                    fontweight=subset_fontweight,
                    fontstyle=subset_fontstyle,
                    fontcolor=subset_fontcolor,
                    ha=ha,
                    va=va,
                    shadow=shadow,
                )
        # Set transparency level
        for patch in v.patches:
            if patch:
                patch.set_alpha(alpha)
                if "none" in edgecolor or 0 in linewidth:
                    patch.set_edgecolor("none")
        return ax
    elif len(lists) == 3: 

        from matplotlib_venn import venn3, venn3_circles

        # Auto-calculate overlap colors for 3-set Venn diagram
        colorAB = get_color_overlap(colors[0], colors[1]) if colors else None
        colorAC = get_color_overlap(colors[0], colors[2]) if colors else None
        colorBC = get_color_overlap(colors[1], colors[2]) if colors else None
        colorABC = (
            get_color_overlap(colors[0], colors[1], colors[2]) if colors else None
        )
        set1, set2, set3 = lists[0], lists[1], lists[2]

        # Draw the venn diagram
        v = venn3(subsets=lists, set_labels=labels, ax=ax, **kwargs)
        v.get_patch_by_id("100").set_color(colors[0])
        v.get_label_by_id("100").set_text(get_count_and_percentage(universe, len(set1 - set2 - set3)))
        v.get_patch_by_id("010").set_color(colors[1])
        v.get_label_by_id("010").set_text(get_count_and_percentage(universe, len(set2 - set1 - set3)))
        try:
            v.get_patch_by_id("001").set_color(colors[2])
            v.get_label_by_id("001").set_text(get_count_and_percentage(universe, len(set3 - set1 - set2)))
        except Exception as e:
            print(e)
        try:
            v.get_patch_by_id("110").set_color(colorAB)
            v.get_label_by_id("110").set_text(get_count_and_percentage(universe, len(set1 & set2 - set3)))
        except Exception as e:
            print(e)
        try:
            v.get_patch_by_id("101").set_color(colorAC)
            v.get_label_by_id("101").set_text(get_count_and_percentage(universe, len(set1 & set3 - set2)))
        except Exception as e:
            print(e)
        try:
            v.get_patch_by_id("011").set_color(colorBC)
            v.get_label_by_id("011").set_text(get_count_and_percentage(universe, len(set2 & set3 - set1)))
        except Exception as e:
            print(e)
        try:
            v.get_patch_by_id("111").set_color(colorABC)
            v.get_label_by_id("111").set_text(get_count_and_percentage(universe, len(set1 & set2 & set3)))
        except Exception as e:
            print(e)

        # Apply styles to set labels
        for i, text in enumerate(v.set_labels):
            textsets(
                text,
                fontname=fontname,
                fontsize=fontsize,
                fontweight=fontweight,
                fontstyle=fontstyle,
                fontcolor=fontcolor,
                ha=ha,
                va=va,
                shadow=shadow,
            )

        # Apply styles to subset labels
        for i, text in enumerate(v.subset_labels):
            if text:  # Ensure text exists
                if custom_texts:  # Custom text handling
                    text.set_text(custom_texts[i])
                textsets(
                    text,
                    fontname=fontname,
                    fontsize=subset_fontsize,
                    fontweight=subset_fontweight,
                    fontstyle=subset_fontstyle,
                    fontcolor=subset_fontcolor,
                    ha=ha,
                    va=va,
                    shadow=shadow,
                )

        venn_circles = venn3_circles(subsets=lists, ax=ax)
        if not isinstance(linewidth, list):
            linewidth = [linewidth]
        if isinstance(linestyle, str):
            linestyle = [linestyle]
        if not isinstance(edgecolor, list):
            edgecolor = [edgecolor]
        linewidth = linewidth * 3 if len(linewidth) == 1 else linewidth
        linestyle = linestyle * 3 if len(linestyle) == 1 else linestyle
        edgecolor = edgecolor * 3 if len(edgecolor) == 1 else edgecolor

        # edgecolor=[to_rgba(i) for i in edgecolor]

        for i in range(3):
            venn_circles[i].set_lw(linewidth[i])
            venn_circles[i].set_ls(linestyle[i])
            venn_circles[i].set_edgecolor(edgecolor[i])

        # 椭圆形
        if ellipse_shape:
            import matplotlib.patches as patches

            for patch in v.patches:
                patch.set_visible(False)  # Hide original patches if using ellipses
            center1 = v.get_circle_center(0)
            center2 = v.get_circle_center(1)
            center3 = v.get_circle_center(2)
            ellipse1 = patches.Ellipse(
                (center1.x, center1.y),
                width=ellipse_scale[0],
                height=ellipse_scale[1],
                edgecolor=edgecolor[0] if edgecolor else colors[0],
                facecolor=colors[0],
                lw=(
                    linewidth if isinstance(linewidth, (int, float)) else 1.0
                ),  # Ensure lw is a number
                ls=linestyle[0],
                alpha=(
                    alpha if isinstance(alpha, (int, float)) else 0.5
                ),  # Ensure alpha is a number
            )
            ellipse2 = patches.Ellipse(
                (center2.x, center2.y),
                width=ellipse_scale[0],
                height=ellipse_scale[1],
                edgecolor=edgecolor[1] if edgecolor else colors[1],
                facecolor=colors[1],
                lw=(
                    linewidth if isinstance(linewidth, (int, float)) else 1.0
                ),  # Ensure lw is a number
                ls=linestyle[0],
                alpha=(
                    alpha if isinstance(alpha, (int, float)) else 0.5
                ),  # Ensure alpha is a number
            )
            ellipse3 = patches.Ellipse(
                (center3.x, center3.y),
                width=ellipse_scale[0],
                height=ellipse_scale[1],
                edgecolor=edgecolor[1] if edgecolor else colors[1],
                facecolor=colors[1],
                lw=(
                    linewidth if isinstance(linewidth, (int, float)) else 1.0
                ),  # Ensure lw is a number
                ls=linestyle[0],
                alpha=(
                    alpha if isinstance(alpha, (int, float)) else 0.5
                ),  # Ensure alpha is a number
            )
            ax.add_patch(ellipse1)
            ax.add_patch(ellipse2)
            ax.add_patch(ellipse3)
        # Set transparency level
        for patch in v.patches:
            if patch:
                patch.set_alpha(alpha)
                if "none" in edgecolor or 0 in linewidth:
                    patch.set_edgecolor("none")
        return ax

        
    dict_data = {}
    for i_list, list_ in enumerate(lists):
        dict_data[labels[i_list]]={*list_}

    if 3<len(lists)<6:        
        from venn import venn as vn

        legend_loc=kwargs.pop("legend_loc", "upper right") 
        ax=vn(dict_data,ax=ax,legend_loc=legend_loc,**kwargs) 

        return ax
    else:
        from venn import pseudovenn
        cmap=kwargs.pop("cmap","plasma")
        ax=pseudovenn(dict_data, cmap=cmap,ax=ax,**kwargs)

        return ax




#! subplots, support automatic extend new axis
def subplot(
    rows: int = 2,
    cols: int = 2,
    figsize: Union[tuple, list] = [8, 8],
    sharex=False,
    sharey=False,
    verbose=False,
    fig=None,
    **kwargs,
):
    """
    nexttile = subplot(
        8,
        2,
        figsize=(8, 9),
        sharey=True,
        sharex=True,
    )

    for i in range(8):
        ax = nexttile()
        x = np.linspace(0, 10, 100) + i
        ax.plot(x, np.sin(x + i) + i, label=f"Plot {i + 1}")
        ax.legend()
        ax.set_title(f"Tile {i + 1}")
        ax.set_ylabel(f"Tile {i + 1}")
        ax.set_xlabel(f"Tile {i + 1}")
    """
    from matplotlib.gridspec import GridSpec

    if verbose:
        print(
            f"usage:\n\tnexttile = subplot(2, 2, figsize=(5, 5), sharex=False, sharey=False)\n\tax = nexttile()"
        )

    figsize_recommend = f"subplot({rows}, {cols}, figsize={figsize})"
    if fig is None:
        fig = plt.figure(figsize=figsize, constrained_layout=True)
    grid_spec = GridSpec(rows, cols, figure=fig)
    occupied = set()
    row_first_axes = [None] * rows  # Track the first axis in each row (for sharey)
    col_first_axes = [None] * cols  # Track the first axis in each column (for sharex)

    def expand_ax():
        nonlocal rows, grid_spec,cols,row_first_axes,fig,figsize,figsize_recommend
        # fig_height = fig.get_figheight()
        # subplot_height = fig_height / rows
        rows += 1  # Expands by adding a row
        # figsize = (figsize[0], fig_height+subplot_height)
        fig.set_size_inches(figsize)
        grid_spec = GridSpec(rows, cols, figure=fig)
        row_first_axes.append(None)
        figsize_recommend=f"Warning: 建议设置 subplot({rows}, {cols})"
        print(figsize_recommend)
    def nexttile(rowspan=1, colspan=1, **kwargs):
        nonlocal rows, cols, occupied, grid_spec,fig,figsize_recommend
        for row in range(rows):
            for col in range(cols):
                if all(
                    (row + r, col + c) not in occupied
                    for r in range(rowspan)
                    for c in range(colspan)
                ):
                    break
            else:
                continue
            break
        
        else:
            expand_ax()
            return nexttile(rowspan=rowspan, colspan=colspan, **kwargs)

        sharex_ax, sharey_ax = None, None

        if sharex:
            sharex_ax = col_first_axes[col]
        if sharey:
            sharey_ax = row_first_axes[row]
        ax = fig.add_subplot(
            grid_spec[row : row + rowspan, col : col + colspan],
            sharex=sharex_ax,
            sharey=sharey_ax,
            **kwargs,
        )

        if row_first_axes[row] is None:
            row_first_axes[row] = ax
        if col_first_axes[col] is None:
            col_first_axes[col] = ax
            
        for r in range(row, row + rowspan):
            for c in range(col, col + colspan):
                occupied.add((r, c))
            
        return ax
    return nexttile


#! radar chart
def radar(
    data: pd.DataFrame,
    columns=None,
    ylim=(0, 100),
    facecolor=None,
    edgecolor="none",
    edge_linewidth=0.5,
    fontsize=10,
    fontcolor="k",
    size=6,
    linewidth=1,
    linestyle="-",
    alpha=0.3,
    fmt=".1f",
    marker="o",
    bg_color="0.8",
    bg_alpha=None,
    grid_interval_ratio=0.2,
    show_value=False,# show text for each value
    cmap=None,
    legend_loc="upper right",
    legend_fontsize=10,
    grid_color="gray",
    grid_alpha=0.5,
    grid_linestyle="--",
    grid_linewidth=0.5,
    circular: bool = False,
    tick_fontsize=None,
    tick_fontcolor="0.65",
    tick_loc=None,  # label position
    turning=None,
    ax=None,
    sp=2,
    verbose=True,
    axis=0,
    **kwargs,
):
    """
    Example DATA:
        df = pd.DataFrame(
                data=[
                    [80, 90, 60],
                    [80, 20, 90],
                    [80, 95, 20],
                    [80, 95, 20],
                    [80, 30, 100],
                    [80, 30, 90],
                    [80, 80, 50],
                ],
                index=["HP", "MP", "ATK", "DEF", "SP.ATK", "SP.DEF", "SPD"],
                columns=["Hero", "Warrior", "Wizard"],
            )
        usage 1: 
            radar(data=df)
        usage 2: 
            radar(data=df["Wizard"])
        usage 3:
            radar(data=df, columns="Wizard")
        usage 4:
            nexttile = subplot(1, 2)
            radar(data=df, columns="Wizard", ax=nexttile(projection="polar"))
            pie(data=df, columns="Wizard", ax=nexttile(), width=0.5, pctdistance=0.7)
    Parameters:
        - data (pd.DataFrame): The data to plot. Each column corresponds to a variable, and each row represents a data point.
        - ylim (tuple): The limits of the radial axis (y-axis). Default is (0, 100).
        - color: The color(s) for the plot. Can be a single color or a list of colors.
        - fontsize (int): Font size for the angular labels (x-axis).
        - fontcolor (str): Color for the angular labels.
        - size (int): The size of the markers for each data point.
        - linewidth (int): Line width for the plot lines.
        - linestyle (str): Line style for the plot lines.
        - alpha (float): The transparency level for the filled area.
        - marker (str): The marker style for the data points.
        - value_offset=0.93,# offset of the text of each value
        - edgecolor (str): The color for the marker edges.
        - edge_linewidth (int): Line width for the marker edges.
        - bg_color (str): Background color for the radar chart.
        - grid_interval_ratio (float): Determines the intervals for the grid lines as a fraction of the y-limit.
        - cmap (str): The colormap to use if `color` is a list.
        - legend_loc (str): The location of the legend.
        - legend_fontsize (int): Font size for the legend.
        - grid_color (str): Color for the grid lines.
        - grid_alpha (float): Transparency of the grid lines.
        - grid_linestyle (str): Style of the grid lines.
        - grid_linewidth (int): Line width of the grid lines.
        - circular (bool): If True, use circular grid lines. If False, use spider-style grid lines (straight lines).
        - tick_fontsize (int): Font size for the radial (y-axis) labels.
        - tick_fontcolor (str): Font color for the radial (y-axis) labels.
        - tick_loc (float or None): The location of the radial tick labels (between 0 and 1). If None, it is automatically calculated.
        - turning (float or None): Rotation of the radar chart. If None, it is not applied.
        - ax (matplotlib.axes.Axes or None): The axis on which to plot the radar chart. If None, a new axis will be created.
        - sp (int): Padding for the ticks from the plot area.
        - **kwargs: Additional arguments for customization.
    """
    if run_once_within(20,reverse=True) and verbose:
        usage_="""usage:
        radar(
            data: pd.DataFrame, #The data to plot. Each column corresponds to a variable, and each row represents a data point.
            ylim=(0, 100),# ylim (tuple): The limits of the radial axis (y-axis). Default is (0, 100).
            facecolor=get_color(5),#The color(s) for the plot. Can be a single color or a list of colors.
            edgecolor="none",#for the marker edges.
            edge_linewidth=0.5,#for the marker edges.
            fontsize=10,# Font size for the angular labels (x-axis).
            fontcolor="k",# Color for the angular labels.
            size=6,#The size of the markers for each data point.
            linewidth=1, 
            linestyle="-",
            alpha=0.5,#for the filled area.
            fmt=".1f",
            marker="o",# for the data points.
            bg_color="0.8",
            bg_alpha=None,
            grid_interval_ratio=0.2,#Determines the intervals for the grid lines as a fraction of the y-limit.
            show_value=False,# show text for each value
            cmap=None,
            legend_loc="upper right",
            legend_fontsize=10,
            grid_color="gray",
            grid_alpha=0.5,
            grid_linestyle="--",
            grid_linewidth=0.5,
            circular: bool = False,#If True, use circular grid lines. If False, use spider-style grid lines (straight lines)
            tick_fontsize=None,#for the radial (y-axis) labels.
            tick_fontcolor="0.65",#for the radial (y-axis) labels.
            tick_loc=None,  # label position
            turning=None,#Rotation of the radar chart
            ax=None,
            sp=2,#Padding for the ticks from the plot area.
            **kwargs,
        )"""
        print(usage_)
    if circular:
        from matplotlib.colors import to_rgba
    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break
    if axis==1:
        data=data.T
    if isinstance(data, dict):
        data = pd.DataFrame(pd.Series(data))
    if ~isinstance(data, pd.DataFrame):
        data=pd.DataFrame(data)
    if isinstance(data, pd.DataFrame):
        data=data.select_dtypes(include=np.number)
    if isinstance(columns,str):
        columns=[columns]
    if columns is None:
        columns = list(data.columns)
    data=data[columns]
    categories = list(data.index) 
    num_vars = len(categories)

    # Set y-axis limits and grid intervals
    vmin, vmax = ylim

    # Set up angle for each category on radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop to ensure straight-line connections

    # If no axis is provided, create a new one
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # bg_color
    if bg_alpha is None:
        bg_alpha = alpha
    (
        ax.set_facecolor(to_rgba(bg_color, alpha=bg_alpha))
        if circular
        else ax.set_facecolor("none")
    )
    # Set up the radar chart with straight-line connections
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axis per variable and add labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    if circular:
        # * cicular style
        ax.yaxis.set_ticks(np.arange(vmin, vmax + 1, vmax * grid_interval_ratio))
        ax.grid(
            axis="both",
            color=grid_color,
            linestyle=grid_linestyle,
            alpha=grid_alpha,
            linewidth=grid_linewidth,
            dash_capstyle="round",
            dash_joinstyle="round",
        )
        ax.spines["polar"].set_color(grid_color)
        ax.spines["polar"].set_linewidth(grid_linewidth)
        ax.spines["polar"].set_linestyle("-")
        ax.spines["polar"].set_alpha(grid_alpha)
        ax.spines["polar"].set_capstyle("round")
        ax.spines["polar"].set_joinstyle("round")

    else:
        # * spider style: spider-style grid (straight lines, not circles)
        # Create the spider-style grid (straight lines, not circles)
        for i in range(1, int((vmax-vmin)/ ((vmax-vmin)*grid_interval_ratio))+1):#int(vmax * grid_interval_ratio) + 1): 
            ax.plot(
                angles + [angles[0]],  # Closing the loop
                [i * vmax * grid_interval_ratio] * (num_vars + 1)
                + [i * vmax * grid_interval_ratio],
                color=grid_color,
                linestyle=grid_linestyle,
                alpha=grid_alpha,
                linewidth=grid_linewidth,
            )
        # set bg_color
        ax.fill(angles, [vmax] * (data.shape[0] + 1), color=bg_color, alpha=bg_alpha)
        ax.yaxis.grid(False)
    # Move radial labels away from plotted line
    if tick_loc is None:
        tick_loc = (
            np.mean([angles[0], angles[1]]) / (2 * np.pi) * 360 if circular else 0
        )

    ax.set_rlabel_position(tick_loc)
    ax.set_theta_offset(turning) if turning is not None else None
    ax.tick_params(
        axis="x", labelsize=fontsize, colors=fontcolor
    )  # Optional: for angular labels
    tick_fontsize = fontsize - 2 if fontsize is None else tick_fontsize
    ax.tick_params(
        axis="y", labelsize=tick_fontsize, colors=tick_fontcolor
    )  # For radial labels
    if not circular:
        ax.spines["polar"].set_visible(False)
    ax.tick_params(axis="x", pad=sp)  # move spines outward
    ax.tick_params(axis="y", pad=sp)  # move spines outward
    # colors
    if facecolor is not None:
        if not isinstance(facecolor,list):
            facecolor=[facecolor]
        colors = facecolor
    else:
        colors = (
            get_color(data.shape[1])
            if cmap is None
            else plt.get_cmap(cmap)(np.linspace(0, 1, data.shape[1]))
        )

    # Plot each row with straight lines
    for i, (col, val) in enumerate(data.items()):
        values = val.tolist()
        values += values[:1]  # Close the loop
        ax.plot(
            angles,
            values,
            color=colors[i],
            linewidth=linewidth,
            linestyle=linestyle,
            label=col,
            clip_on=False,
        )
        ax.fill(angles, values, color=colors[i], alpha=alpha)
        # Add text labels for each value at each angle
        labeled_points = set() #这样同一个点就不会标多次了
        if show_value:
            for angle, value in zip(angles, values):
                if (angle, value) not in labeled_points:
                    # offset_radius = value * value_offset
                    lim_ = np.max(values)
                    sep_in = lim_/5
                    sep_low=sep_in*2
                    sep_med=sep_in*3
                    sep_hig=sep_in*4
                    sep_out=lim_*5
                    if value<sep_in:
                        offset_radius = value * 0.7
                    elif value<sep_low:
                        offset_radius = value * 0.8
                    elif sep_low<=value<sep_med:
                        offset_radius = value * 0.85
                    elif sep_med<=value<sep_hig:
                        offset_radius = value * 0.9
                    elif sep_hig<=value<sep_out:
                        offset_radius = value * 0.93
                    else:
                        offset_radius = value * 0.98
                    ax.text(
                        angle, 
                        offset_radius,
                        f"{value:{fmt}}", 
                        ha="center", 
                        va="center", 
                        fontsize=fontsize, 
                        color=fontcolor,
                        zorder=11
                    )
                    labeled_points.add((angle, value))

    ax.set_ylim(ylim)
    # Add markers for each data point
    for i,  (col, val) in enumerate(data.items()):
        ax.plot(
            angles,
            list(val) + [val[0]],  # Close the loop for markers
            color=colors[i],
            marker=marker,
            markersize=size,
            markeredgecolor=edgecolor,
            markeredgewidth=edge_linewidth,
            zorder=10,
            clip_on=False,
        )
    # ax.tick_params(axis='y', labelleft=False, left=False)
    if "legend" in kws_figsets:
        figsets(ax=ax, **kws_figsets)
    else:

        figsets(
            ax=ax,
            legend=dict(
                loc=legend_loc,
                fontsize=legend_fontsize,
                bbox_to_anchor=[1.1, 1.4],
                ncols=2,
            ),
            **kws_figsets,
        )
    return ax


def pie(
    data:pd.Series,
    columns:list = None,
    facecolor=None,
    explode=[0.1],
    startangle=90,
    shadow=True,
    fontcolor="k",
    fmt=".2f", 
    width=None,# the center blank
    pctdistance=0.85,
    labeldistance=1.1,
    kws_wedge={},
    kws_text={},
    kws_arrow={},
    center=(0, 0),
    radius=1,
    frame=False,
    fontsize=10,
    edgecolor="white",
    edgewidth=1,
    cmap=None,
    show_value=False,
    show_label=True,# False: only show the outer layer, if it is None, not show
    expand_label=(1.2,1.2),
    kws_bbox={},#dict(facecolor="none", alpha=0.5, edgecolor="black", boxstyle="round,pad=0.3"),  # '{}' to hide
    show_legend=True,
    legend_loc="upper right",
    bbox_to_anchor=[1.4, 1.1],
    legend_fontsize=10,
    rotation_correction=0,
    verbose=True,
    ax=None,
    **kwargs
): 
    from adjustText import adjust_text
    if run_once_within(20,reverse=True) and verbose:
        usage_="""usage:
            pie(
            data:pd.Series,
            columns:list = None,
            facecolor=None,
            explode=[0.1],
            startangle=90,
            shadow=True,
            fontcolor="k",
            fmt=".2f", 
            width=None,# the center blank
            pctdistance=0.85,
            labeldistance=1.1,
            kws_wedge={},
            kws_text={}, 
            center=(0, 0),
            radius=1,
            frame=False,
            fontsize=10,
            edgecolor="white",
            edgewidth=1,
            cmap=None,
            show_value=False,
            show_label=True,# False: only show the outer layer, if it is None, not show
            show_legend=True,
            legend_loc="upper right",
            bbox_to_anchor=[1.4, 1.1],
            legend_fontsize=10,
            rotation_correction=0,
            verbose=True,
            ax=None,
            **kwargs
        )
        
    usage 1: 
    data = {"Segment A": 30, "Segment B": 50, "Segment C": 20}

    ax = pie(
        data=data,
        # columns="Segment A",
        explode=[0, 0.2, 0],
        # width=0.4,
        show_label=False,
        fontsize=10,
        # show_value=1,
        fmt=".3f",
    )

    # prepare dataset
    df = pd.DataFrame(
        data=[
                [80, 90, 60],
                [80, 20, 90],
                [80, 95, 20],
                [80, 95, 20],
                [80, 30, 100],
                [80, 30, 90],
                [80, 80, 50],
            ],
            index=["HP", "MP", "ATK", "DEF", "SP.ATK", "SP.DEF", "SPD"],
            columns=["Hero", "Warrior", "Wizard"],
        )
    usage 1: only plot one column
        pie(
            df,
            columns="Wizard",
            width=0.6,
            show_label=False,
            fmt=".0f",
        )
    usage 2: 
        pie(df,columns=["Hero", "Warrior"],show_label=False)
    usage 3: set different width
        pie(df,
            columns=["Hero", "Warrior", "Wizard"],
            width=[0.3, 0.2, 0.2],
            show_label=False,
            fmt=".0f",
            )
    usage 4: set width the same for all columns
        pie(df,
            columns=["Hero", "Warrior", "Wizard"],
            width=0.2,
            show_label=False,
            fmt=".0f",
            )
    usage 5: adjust the labels' offset
        pie(df, columns="Wizard", width=0.6, show_label=False, fmt=".6f", labeldistance=1.2)

    usage 6: 
        nexttile = subplot(1, 2)
        radar(data=df, columns="Wizard", ax=nexttile(projection="polar"))
        pie(data=df, columns="Wizard", ax=nexttile(), width=0.5, pctdistance=0.7)
    """
        print(usage_)
    # Convert data to a Pandas Series if needed
    if isinstance(data, dict):
        data = pd.DataFrame(pd.Series(data))
    if ~isinstance(data, pd.DataFrame):
        data=pd.DataFrame(data)

    if isinstance(data, pd.DataFrame):
        data=data.select_dtypes(include=np.number)
    if isinstance(columns,str):
        columns=[columns]
    if columns is None:
        columns = list(data.columns)
    # data=data[columns]
    # columns = list(data.columns)
    # print(columns)
    # 选择部分数据
    df=data[columns]

    if not isinstance(explode, list):
        explode=[explode]
    if explode == [None]:
        explode=[0]

    if width is None:
        if df.shape[1]>1:
            width=1/(df.shape[1]+2)
        else:
            width=1
    if isinstance(width,(float,int)):
        width=[width]
    if len(width)<df.shape[1]:
        width=width*df.shape[1]
    if isinstance(radius,(float,int)):
        radius=[radius]
    radius_tile=[1]*df.shape[1]
    radius=radius_tile.copy()
    for i in range(1,df.shape[1]):
        radius[i]=radius_tile[i]-np.sum(width[:i])

    # colors
    if facecolor is not None:
        if not isinstance(facecolor,list):
            facecolor=[facecolor]
        colors = facecolor
    else:
        colors = (
            get_color(data.shape[0])
            if cmap is None
            else plt.get_cmap(cmap)(np.linspace(0, 1, data.shape[0]))
        )
    # to check if facecolor is nested list or not
    is_nested = True if any(isinstance(i, list) for i in colors) else False
    inested = 0
    for column_,width_,radius_ in zip(columns, width,radius):
        if column_!=columns[0]:
            labels = data.index if show_label else None
        else:
            labels = data.index if show_label is not None else None
        data = df[column_]
        labels_legend=data.index
        sizes = data.values
        
        # Set wedge and text properties if none are provided
        kws_wedge = kws_wedge or {"edgecolor": edgecolor, "linewidth": edgewidth}
        kws_wedge.update({"width":width_})
        fontcolor=kws_text.get("color",fontcolor)
        fontsize=kws_text.get("fontsize",fontsize)
        kws_text.update({"color": fontcolor, "fontsize": fontsize})

        if ax is None: 
            ax=plt.gca()
        if len(explode)<len(labels_legend):
            explode.extend([0]*(len(labels_legend)-len(explode)))
        print(explode)
        if fmt:
            if not fmt.startswith("%"):
                autopct =f"%{fmt}%%"
        else:
            autopct=None

        if show_value is None:
            result = ax.pie(
                sizes,
                labels=labels,
                autopct= None,
                startangle=startangle + rotation_correction,
                explode=explode,
                colors=colors[inested] if is_nested else colors,
                shadow=shadow,
                pctdistance=pctdistance,
                labeldistance=labeldistance,
                wedgeprops=kws_wedge,
                textprops=kws_text,
                center=center,
                radius=radius_,
                frame=frame,
                **kwargs
            )
        else:
            result = ax.pie(
                sizes,
                labels=labels,
                autopct=autopct if autopct else None,
                startangle=startangle + rotation_correction,
                explode=explode,
                colors=colors[inested] if is_nested else colors,
                shadow=shadow,#shadow,
                pctdistance=pctdistance,
                labeldistance=labeldistance,
                wedgeprops=kws_wedge,
                textprops=kws_text,
                center=center,
                radius=radius_,
                frame=frame,
                **kwargs
            )
        if len(result) == 3:
            wedges, texts, autotexts = result
        elif len(result) == 2:
            wedges, texts = result
            autotexts = None 
        #! adjust_text
        if autotexts or texts:
            all_texts = []
            if autotexts and show_value:
                all_texts.extend(autotexts)
            if texts and show_label:
                all_texts.extend(texts)
                
            adjust_text(
                all_texts,
                ax=ax,
                arrowprops=kws_arrow,#dict(arrowstyle="-", color="gray", lw=0.5), 
                bbox=kws_bbox if kws_bbox else None,
                expand=expand_label,
                fontdict={
                        "fontsize": fontsize,
                        "color": fontcolor,
                    },
            )
            # Show exact values on wedges if show_value is True
            if show_value:
                for i, (wedge, txt) in enumerate(zip(wedges, texts)):
                    angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
                    x = np.cos(np.radians(angle)) * (pctdistance ) * radius_
                    y = np.sin(np.radians(angle)) * (pctdistance ) * radius_
                    if not fmt.startswith("{"):
                        value_text = f"{sizes[i]:{fmt}}"
                    else:
                        value_text = fmt.format(sizes[i]) 
                    ax.text(x, y, value_text, ha="center", va="center", fontsize=fontsize,color=fontcolor)
            inested+=1
    # Customize the legend
    if show_legend:
        ax.legend(
            wedges,
            labels_legend,
            loc=legend_loc,
            bbox_to_anchor=bbox_to_anchor,
            fontsize=legend_fontsize,
            title_fontsize=legend_fontsize,
        ) 
    ax.set(aspect="equal")
    return ax

def ellipse(
    data,
    x=None,
    y=None,
    hue=None,
    n_std=1.5,
    ax=None,
    confidence=0.95,
    annotate_center=False,
    palette=None,
    facecolor=None,
    edgecolor=None,
    label:bool=True,
    **kwargs,
):
    """
    Plot advanced ellipses representing covariance for different groups
    # simulate data:
                control = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], size=50)
                patient = np.random.multivariate_normal([2, 1], [[1, -0.3], [-0.3, 1]], size=50)
                df = pd.DataFrame(
                    {
                        "Dim1": np.concatenate([control[:, 0], patient[:, 0]]),
                        "Dim2": np.concatenate([control[:, 1], patient[:, 1]]),
                        "Group": ["Control"] * 50 + ["Patient"] * 50,
                    }
                )
                plotxy(
                    data=df,
                    x="Dim1",
                    y="Dim2",
                    hue="Group",
                    kind_="scatter",
                    palette=get_color(8),
                )
                ellipse(
                    data=df,
                    x="Dim1",
                    y="Dim2",
                    hue="Group",
                    palette=get_color(8),
                    alpha=0.1,
                    lw=2,
                )
    Parameters:
        data (DataFrame): Input DataFrame with columns for x, y, and hue.
        x (str): Column name for x-axis values.
        y (str): Column name for y-axis values.
        hue (str, optional): Column name for group labels.
        n_std (float): Number of standard deviations for the ellipse (overridden if confidence is provided).
        ax (matplotlib.axes.Axes, optional): Matplotlib Axes object to plot on. Defaults to current Axes.
        confidence (float, optional): Confidence level (e.g., 0.95 for 95% confidence interval).
        annotate_center (bool): Whether to annotate the ellipse center (mean).
        palette (dict or list, optional): A mapping of hues to colors or a list of colors.
        **kwargs: Additional keyword arguments for the Ellipse patch.

    Returns:
        list: List of Ellipse objects added to the Axes.
    """
    from matplotlib.patches import Ellipse
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    from scipy.stats import chi2

    if ax is None:
        ax = plt.gca()

    # Validate inputs
    if x is None or y is None:
        raise ValueError(
            "Both `x` and `y` must be specified as column names in the DataFrame."
        )
    if not isinstance(data, pd.DataFrame):
        raise ValueError("`data` must be a pandas DataFrame.")

    # Prepare data for hue-based grouping
    ellipses = []
    if hue is not None:
        groups = data[hue].unique()
        colors = sns.color_palette(palette or "husl", len(groups))
        color_map = dict(zip(groups, colors))
    else:
        groups = [None]
        color_map = {None: kwargs.get("edgecolor", "blue")}
    alpha = kwargs.pop("alpha", 0.2)
    edgecolor=kwargs.pop("edgecolor", None)
    facecolor=kwargs.pop("facecolor", None)
    for group in groups:
        group_data = data[data[hue] == group] if hue else data

        # Extract x and y columns for the group
        group_points = group_data[[x, y]].values

        # Compute mean and covariance matrix
        # # 标准化处理
        # group_points = group_data[[x, y]].values
        # group_points -= group_points.mean(axis=0)
        # group_points /= group_points.std(axis=0)

        cov = np.cov(group_points.T)
        mean = np.mean(group_points, axis=0)

        # Eigenvalues and eigenvectors
        eigvals, eigvecs = np.linalg.eigh(cov)
        order = eigvals.argsort()[::-1]
        eigvals, eigvecs = eigvals[order], eigvecs[:, order]

        # Rotation angle and ellipse dimensions
        angle = np.degrees(np.arctan2(*eigvecs[:, 0][::-1]))
        if confidence:
            n_std = np.sqrt(chi2.ppf(confidence, df=2))  # Chi-square quantile
        width, height = 2 * n_std * np.sqrt(eigvals)

        # Create and style the ellipse
        if facecolor is None:
            facecolor_ = color_map[group]
        if edgecolor is None:
            edgecolor_ = color_map[group]
        ellipse = Ellipse(
            xy=mean,
            width=width,
            height=height,
            angle=angle,
            edgecolor=edgecolor_,
            facecolor=(facecolor_, alpha), #facecolor_, # only work on facecolor
            # alpha=alpha,
            label=group if (hue and label) else None,
            **kwargs,
        )
        ax.add_patch(ellipse)
        ellipses.append(ellipse)

        # Annotate center
        if annotate_center:
            ax.annotate(
                f"Mean\n({mean[0]:.2f}, {mean[1]:.2f})",
                xy=mean,
                xycoords="data",
                fontsize=10,
                ha="center",
                color=ellipse_color,
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    edgecolor="gray",
                    facecolor="white",
                    alpha=0.8,
                ),
            )

    return ax

def ppi(
    interactions,
    player1="preferredName_A",
    player2="preferredName_B",
    weight="score",
    n_layers=None,  # Number of concentric layers
    n_rank=[5, 10],  # Nodes in each rank for the concentric layout
    dist_node = 10,  # Distance between each rank of circles
    layout="degree", 
    size=None,#700,
    sizes=(50,500),# min and max of size
    facecolor="skyblue",
    cmap='coolwarm',
    edgecolor="k",
    edgelinewidth=1.5,
    alpha=.5,
    alphas=(0.1, 1.0),# min and max of alpha
    marker="o",
    node_hideticks=True,
    linecolor="gray",
    line_cmap='coolwarm',
    linewidth=1.5,
    linewidths=(0.5,5),# min and max of linewidth
    linealpha=1.0,
    linealphas=(0.1,1.0),# min and max of linealpha
    linestyle="-",
    line_arrowstyle='-',
    fontsize=10,
    fontcolor="k",
    ha:str="center",
    va:str="center",
    figsize=(12, 10),
    k_value=0.3,    
    bgcolor="w",
    dir_save="./ppi_network.html",
    physics=True,
    notebook=False,
    scale=1,
    ax=None,
    **kwargs
):
    """
    Plot a Protein-Protein Interaction (PPI) network with adjustable appearance.

    ppi(
        interactions_sort.iloc[:1000, :],
        player1="player1",
        player2="player2",
        weight="count",
        layout="spring",
        n_layers=13,
        fontsize=1,
        n_rank=[5, 10, 20, 40, 80, 80, 80, 80, 80, 80, 80, 80],
    )
    """
    from pyvis.network import Network
    import networkx as nx 
    from IPython.display import IFrame
    from matplotlib.colors import Normalize
    from matplotlib import cm
    from . import ips

    if run_once_within():
        usage_str="""
        ppi(
            interactions,
            player1="preferredName_A",
            player2="preferredName_B",
            weight="score",
            n_layers=None,  # Number of concentric layers
            n_rank=[5, 10],  # Nodes in each rank for the concentric layout
            dist_node = 10,  # Distance between each rank of circles
            layout="degree", 
            size=None,#700,
            sizes=(50,500),# min and max of size
            facecolor="skyblue",
            cmap='coolwarm',
            edgecolor="k",
            edgelinewidth=1.5,
            alpha=.5,
            alphas=(0.1, 1.0),# min and max of alpha
            marker="o",
            node_hideticks=True,
            linecolor="gray",
            line_cmap='coolwarm',
            linewidth=1.5,
            linewidths=(0.5,5),# min and max of linewidth
            linealpha=1.0,
            linealphas=(0.1,1.0),# min and max of linealpha
            linestyle="-",
            line_arrowstyle='-',
            fontsize=10,
            fontcolor="k",
            ha:str="center",
            va:str="center",
            figsize=(12, 10),
            k_value=0.3,    
            bgcolor="w",
            dir_save="./ppi_network.html",
            physics=True,
            notebook=False,
            scale=1,
            ax=None,
            **kwargs
        ):
        """
        print(usage_str)
    
    # Check for required columns in the DataFrame
    for col in [player1, player2, weight]:
        if col not in interactions.columns:
            raise ValueError(f"Column '{col}' is missing from the interactions DataFrame.")
    interactions.sort_values(by=[weight], inplace=True)
    # Initialize Pyvis network
    net = Network(height="750px", width="100%", bgcolor=bgcolor, font_color=fontcolor)
    net.force_atlas_2based(
        gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.1
    ) 
    net.toggle_physics(physics)

    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break

    # Create a NetworkX graph from the interaction data
    G = nx.Graph()
    for _, row in interactions.iterrows():
        G.add_edge(row[player1], row[player2], weight=row[weight])
    # G = nx.from_pandas_edgelist(interactions, source=player1, target=player2, edge_attr=weight)


    # Calculate node degrees
    degrees = dict(G.degree())
    norm = Normalize(vmin=min(degrees.values()), vmax=max(degrees.values()))
    colormap = cm.get_cmap(cmap)  # Get the 'coolwarm' colormap

    if not ips.isa(facecolor, 'color'):
        print("facecolor: based on degrees")
        facecolor = [colormap(norm(deg)) for deg in degrees.values()]  # Use colormap
    num_nodes = G.number_of_nodes()
    #* size
    # Set properties based on degrees
    if not isinstance(size, (int,float,list)):
        print("size: based on degrees")
        size = [deg * 50 for deg in degrees.values()]  # Scale sizes
    size = (size[:num_nodes] if len(size) > num_nodes else size) if isinstance(size, list) else [size] * num_nodes
    if isinstance(size, list) and len(ips.flatten(size,verbose=False))!=1:
        # Normalize sizes
        min_size, max_size = sizes  # Use sizes tuple for min and max values
        min_degree, max_degree = min(size), max(size)
        if max_degree > min_degree:  # Avoid division by zero
            size = [
                min_size + (max_size - min_size) * (sz - min_degree) / (max_degree - min_degree)
                for sz in size
            ]
        else:
            # If all values are the same, set them to a default of the midpoint
            size = [(min_size + max_size) / 2] * len(size)

    #* facecolor
    facecolor = (facecolor[:num_nodes] if len(facecolor) > num_nodes else facecolor) if isinstance(facecolor, list) else [facecolor] * num_nodes
    # * facealpha
    if isinstance(alpha, list):
        alpha = (alpha[:num_nodes] if len(alpha) > num_nodes else alpha + [alpha[-1]] * (num_nodes - len(alpha)))
        min_alphas, max_alphas = alphas  # Use alphas tuple for min and max values
        if len(alpha) > 0:
            # Normalize alpha based on the specified min and max
            min_alpha, max_alpha = min(alpha), max(alpha)
            if max_alpha > min_alpha:  # Avoid division by zero
                alpha = [
                    min_alphas + (max_alphas - min_alphas) * (ea - min_alpha) / (max_alpha - min_alpha)
                    for ea in alpha
                ]
            else:
                # If all alpha values are the same, set them to the average of min and max
                alpha = [(min_alphas + max_alphas) / 2] * len(alpha)
        else:
            # Default to a full opacity if no edges are provided
            alpha = [1.0] * num_nodes  
    else:
        # If alpha is a single value, convert it to a list and normalize it
        alpha = [alpha] * num_nodes  # Adjust based on alphas

    for i, node in enumerate(G.nodes()):
        net.add_node(
            node,
            label=node,
            size=size[i],
            color=facecolor[i],
            alpha=alpha[i],
            font={"size": fontsize, "color": fontcolor},
        )
    print(f'nodes number: {i+1}')

    for edge in G.edges(data=True):
        net.add_edge(
            edge[0],
            edge[1],
            weight=edge[2]["weight"],
            color=edgecolor,
            width=edgelinewidth * edge[2]["weight"],
        )

    layouts = [
        "spring",
        "circular",
        "kamada_kawai",
        "random",
        "shell",
        "planar",
        "spiral",
        "degree"
    ]
    layout = ips.strcmp(layout, layouts)[0]
    print(f"layout:{layout}, or select one in {layouts}")
    
    # Choose layout
    if layout == "spring":
        pos = nx.spring_layout(G, k=k_value)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G)
    elif layout == "spectral":
        pos = nx.spectral_layout(G)
    elif layout == "random":
        pos = nx.random_layout(G)
    elif layout == "shell":
        pos = nx.shell_layout(G)
    elif layout == "planar":
        if nx.check_planarity(G)[0]:
            pos = nx.planar_layout(G)
        else:
            print("Graph is not planar; switching to spring layout.")
            pos = nx.spring_layout(G, k=k_value)
    elif layout == "spiral":
        pos = nx.spiral_layout(G)
    elif layout=='degree':
        # Calculate node degrees and sort nodes by degree
        degrees = dict(G.degree())
        sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        norm = Normalize(vmin=min(degrees.values()), vmax=max(degrees.values()))
        colormap = cm.get_cmap(cmap)
        
        # Create positions for concentric circles based on n_layers and n_rank
        pos = {}
        n_layers=len(n_rank)+1 if n_layers is None else n_layers
        for rank_index in range(n_layers):
            if rank_index < len(n_rank):
                nodes_per_rank = n_rank[rank_index]
                rank_nodes = sorted_nodes[sum(n_rank[:rank_index]): sum(n_rank[:rank_index + 1])]
            else:
                # 随机打乱剩余节点的顺序
                remaining_nodes = sorted_nodes[sum(n_rank[:rank_index]):]
                random_indices = np.random.permutation(len(remaining_nodes)) 
                rank_nodes = [remaining_nodes[i] for i in random_indices]

            radius = (rank_index + 1) * dist_node  # Radius for this rank

            # Arrange nodes in a circle for the current rank
            for i, (node, degree) in enumerate(rank_nodes):
                angle = (i / len(rank_nodes)) * 2 * np.pi  # Distribute around circle
                pos[node] = (radius * np.cos(angle), radius * np.sin(angle))

    else:
        print(f"Unknown layout '{layout}', defaulting to 'spring',or可以用这些: {layouts}")
        pos = nx.spring_layout(G, k=k_value)

    for node, (x, y) in pos.items():
        net.get_node(node)["x"] = x * scale
        net.get_node(node)["y"] = y * scale

    # If ax is None, use plt.gca()
    if ax is None:
        fig, ax = plt.subplots(1,1,figsize=figsize) 
    
    # Draw nodes, edges, and labels with customization options
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_size=size,
        node_color=facecolor,
        linewidths=edgelinewidth,
        edgecolors=edgecolor,
        alpha=alpha,
        hide_ticks=node_hideticks,
        node_shape=marker
    )

    #* linewidth
    if not isinstance(linewidth, list):
        linewidth = [linewidth] * G.number_of_edges()
    else:
        linewidth = (linewidth[:G.number_of_edges()] if len(linewidth) > G.number_of_edges() else linewidth + [linewidth[-1]] * (G.number_of_edges() - len(linewidth)))
        # Normalize linewidth if it is a list
        if isinstance(linewidth, list):
            min_linewidth, max_linewidth = min(linewidth), max(linewidth)
            vmin, vmax = linewidths  # Use linewidths tuple for min and max values
            if max_linewidth > min_linewidth:  # Avoid division by zero
                # Scale between vmin and vmax
                linewidth = [
                    vmin + (vmax - vmin) * (lw - min_linewidth) / (max_linewidth - min_linewidth)
                    for lw in linewidth
                ]
            else:
                # If all values are the same, set them to a default of the midpoint
                linewidth = [(vmin + vmax) / 2] * len(linewidth)
        else:
            # If linewidth is a single value, convert it to a list of that value
            linewidth = [linewidth] * G.number_of_edges()
    #* linecolor 
    if not isinstance(linecolor, str):  
        weights = [G[u][v]["weight"] for u, v in G.edges()]
        norm = Normalize(vmin=min(weights), vmax=max(weights))
        colormap = cm.get_cmap(line_cmap)
        linecolor = [colormap(norm(weight)) for weight in weights]
    else:
        linecolor = [linecolor] * G.number_of_edges()

    # * linealpha
    if isinstance(linealpha, list):
        linealpha = (linealpha[:G.number_of_edges()] if len(linealpha) > G.number_of_edges() else linealpha + [linealpha[-1]] * (G.number_of_edges() - len(linealpha)))
        min_alpha, max_alpha = linealphas  # Use linealphas tuple for min and max values
        if len(linealpha) > 0:
            min_linealpha, max_linealpha = min(linealpha), max(linealpha)
            if max_linealpha > min_linealpha:  # Avoid division by zero
                linealpha = [
                    min_alpha + (max_alpha - min_alpha) * (ea - min_linealpha) / (max_linealpha - min_linealpha)
                    for ea in linealpha
                ]
            else:
                linealpha = [(min_alpha + max_alpha) / 2] * len(linealpha)
        else:
            linealpha = [1.0] * G.number_of_edges() # 如果设置有误,则将它设置成1.0
    else:
        linealpha = [linealpha] * G.number_of_edges()  # Convert to list if single value
    nx.draw_networkx_edges(
        G, 
        pos, 
        ax=ax, 
        edge_color=linecolor, 
        width=linewidth,
        style=linestyle,
        arrowstyle=line_arrowstyle, 
        alpha=linealpha
    )
 
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=fontsize, font_color=fontcolor,horizontalalignment=ha,verticalalignment=va
    )
    figsets(ax=ax,**kws_figsets)
    ax.axis("off")
    if dir_save:
        if not os.path.basename(dir_save):
            dir_save="_.html"
        net.write_html(dir_save)
        nx.write_graphml(G, dir_save.replace(".html",".graphml"))  # Export to GraphML
        print(f"could be edited in Cytoscape \n{dir_save.replace(".html",".graphml")}")
        ips.figsave(dir_save.replace(".html",".pdf"))
    return G,ax