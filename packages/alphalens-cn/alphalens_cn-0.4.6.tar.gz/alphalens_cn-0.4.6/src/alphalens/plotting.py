#
# Copyright 2017 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

import seaborn as sns
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from functools import wraps

from . import utils
from . import performance as perf

DECIMAL_TO_BPS = 10000


def customize(func):
    """
    Decorator to set plotting context and axes style during function call.
    装饰器，用于在函数调用期间设置绘图上下文和轴样式。
    """

    @wraps(func)
    def call_w_context(*args, **kwargs):
        set_context = kwargs.pop("set_context", True)
        if set_context:
            color_palette = sns.color_palette("colorblind")
            with plotting_context(), axes_style(), color_palette:
                sns.despine(left=True)
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return call_w_context


def plotting_context(context="notebook", font_scale=1.5, rc=None):
    """
    Create alphalens default plotting style context.

    Under the hood, calls and returns seaborn.plotting_context() with
    some custom settings. Usually you would use in a with-context.

    Parameters
    ----------
    context : str, optional
        Name of seaborn context.
    font_scale : float, optional
        Scale font by factor font_scale.
    rc : dict, optional
        Config flags.
        By default, {'lines.linewidth': 1.5}
        is being used and will be added to any
        rc passed in, unless explicitly overriden.

    Returns
    -------
    seaborn plotting context

    Example
    -------
    with alphalens.plotting.plotting_context(font_scale=2):
        alphalens.create_full_tear_sheet(..., set_context=False)

    See also
    --------
    For more information, see seaborn.plotting_context().
    创建 alphalens 默认绘图样式上下文。

    在底层，调用并返回 seaborn.plotting_context()
    一些自定义设置。通常你会在上下文中使用。

    参数
    ----------
    context : 字符串，可选
        名称为 seaborn 上下文。
        字体缩放：float，可选
        按字体缩放因子 font_scale 缩放字体。
    rc : 字典，可选
        配置标志。
        默认情况下，{'lines.linewidth': 1.5}
        正在使用并将添加到任何
        rc 已传入，除非明确覆盖。

    返回
    -------
    seaborn 绘图上下文

    示例
    -------
    在 alphalens.plotting.plotting_context(font_scale=2) 下：
    alphalens.create_full_tear_sheet(..., set_context=False)

    参见
    --------
    有关更多信息，请参阅 seaborn.plotting_context()。
    """
    if rc is None:
        rc = {}

    rc_default = {"lines.linewidth": 1.5}

    # Add defaults if they do not exist
    for name, val in rc_default.items():
        rc.setdefault(name, val)

    return sns.plotting_context(context=context, font_scale=font_scale, rc=rc)


def axes_style(style="darkgrid", rc=None):
    """Create alphalens default axes style context.

    Under the hood, calls and returns seaborn.axes_style() with
    some custom settings. Usually you would use in a with-context.

    Parameters
    ----------
    style : str, optional
        Name of seaborn style.
    rc : dict, optional
        Config flags.

    Returns
    -------
    seaborn plotting context

    Example
    -------
    with alphalens.plotting.axes_style(style='whitegrid'):
        alphalens.create_full_tear_sheet(..., set_context=False)

    See also
    --------
    For more information, see seaborn.plotting_context().
    创建 alphalens 默认轴样式上下文。

    在底层，调用并返回 seaborn.axes_style()
    
    参数
    ----------
    样式：str，可选

    一些自定义设置。通常你会在上下文中使用。
    seaborn 风格名称。

    rc : 字典，可选

    配置标志。
    返回
    -------

    seaborn 绘图上下文
    示例
    -------
    alphalens.create_full_tear_sheet(..., set_context=False)

    参见
    --------
    有关更多信息，请参阅 seaborn.plotting_context()。
    """
    if rc is None:
        rc = {}

    rc_default = {}

    # Add defaults if they do not exist
    for name, val in rc_default.items():
        rc.setdefault(name, val)

    return sns.axes_style(style=style, rc=rc)


def plot_returns_table(
    alpha_beta, mean_ret_quantile, mean_ret_spread_quantile, return_df=False
):
    returns_table = pd.DataFrame()
    returns_table = pd.concat([returns_table, alpha_beta])
    #returns_table.loc["Mean Period Wise Return Top Quantile (bps)"] = (
    returns_table.loc["周期性回报顶部分位数的平均值（基点）"] = (
        mean_ret_quantile.iloc[-1] * DECIMAL_TO_BPS
    )
    #returns_table.loc["Mean Period Wise Return Bottom Quantile (bps)"] = (
    returns_table.loc["周期性回报底部分位数的平均值（基点）"] = (
        mean_ret_quantile.iloc[0] * DECIMAL_TO_BPS
    )
    #returns_table.loc["Mean Period Wise Spread (bps)"] = (
    returns_table.loc["周期性价差的平均值（基点）[分位收益差，越大越好]"] = (
        mean_ret_spread_quantile.mean() * DECIMAL_TO_BPS
    )

    if return_df:
        return returns_table
    else:
        print("Returns Analysis")
        utils.print_table(returns_table.apply(lambda x: x.round(3)))


def plot_turnover_table(autocorrelation_data, quantile_turnover, return_df=False):
    turnover_table = pd.DataFrame()
    for period in sorted(quantile_turnover.keys()):
        for quantile, p_data in quantile_turnover[period].items():
            turnover_table.loc[
                "分位数 {} 的平均换手率 ".format(quantile),
                "{}D".format(period),
            ] = p_data.mean()
    auto_corr = pd.DataFrame()
    for period, p_data in autocorrelation_data.items():
        auto_corr.loc[
            "因子排名自相关性的平均值", "{}D".format(period)
        ] = p_data.mean()

    if return_df:
        return turnover_table, auto_corr
    else:
        print("Turnover Analysis")
        utils.print_table(turnover_table.apply(lambda x: x.round(3)))
        utils.print_table(auto_corr.apply(lambda x: x.round(3)))


def plot_information_table(ic_data, return_df=False):
    ic_summary_table = pd.DataFrame()
    ic_summary_table["IC 均值"] = ic_data.mean()
    ic_summary_table["IC 标准差"] = ic_data.std()
    ic_summary_table["风险调整 IC"] = ic_data.mean() / ic_data.std()
    t_stat, p_value = stats.ttest_1samp(ic_data, 0)
    ic_summary_table["t统计量(IC)[越大越好]"] = t_stat
    ic_summary_table["p值(IC)[越小越好]"] = p_value
    ic_summary_table["IC 偏度"] = stats.skew(ic_data)
    ic_summary_table["IC 峰度"] = stats.kurtosis(ic_data)

    if return_df:
        return ic_summary_table
    else:
        print("Information Analysis")
        utils.print_table(ic_summary_table.apply(lambda x: x.round(3)).T)


def plot_quantile_statistics_table(factor_data, return_df=False):
    quantile_stats = factor_data.groupby("factor_quantile")["factor"].agg(
        ["min", "max", "mean", "std", "count"]
    )

    quantile_stats["count %"] = (
        quantile_stats["count"] / quantile_stats["count"].sum() * 100.0
    )

    if return_df:
        return quantile_stats
    else:
        print("Quantiles Statistics")
        utils.print_table(quantile_stats)


def plot_ic_ts(ic, ax=None):
    """
    Plots Spearman Rank Information Coefficient and IC moving
    average for a given factor.
    绘制给定因子的Spearman秩信息系数及其移动平均线
    Spearman秩信息系数（Spearman Rank Information Coefficient, IC）: 这是一种衡量因子预测能力的方法，通过计算因子值与未来回报之间的Spearman秩相关系数来实现。

    移动平均线（Moving Average）: 这是一种平滑数据的方法，通过计算一定窗口期内的平均值来减少短期波动的影响。
    Parameters
    ----------
    ic : pd.DataFrame
        DataFrame indexed by date, with IC for each forward return.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on. 
    绘制给定因子的Spearman秩信息系数及其移动平均线

    参数
    ic: pd.DataFrame

    按日期索引的DataFrame，包含每个前瞻性回报的IC。

    ax: matplotlib.Axes, 可选

    用于绘图的坐标轴。

    返回值
    ax: matplotlib.Axes

    绘图所用的坐标轴。

    详细解释

    Spearman秩信息系数（Spearman Rank Information Coefficient, IC）: 这是一种衡量因子预测能力的方法，通过计算因子值与未来回报之间的Spearman秩相关系数来实现。

    移动平均线（Moving Average）: 这是一种平滑数据的方法，通过计算一定窗口期内的平均值来减少短期波动的影响。
    """
    ic = ic.copy()

    num_plots = len(ic.columns)
    if ax is None:
        f, ax = plt.subplots(num_plots, 1, figsize=(18, num_plots * 7))
        ax = np.asarray([ax]).flatten()

    ymin, ymax = (None, None)
    for a, (period_num, ic) in zip(ax, ic.items()):
        ic.plot(alpha=0.7, ax=a, lw=0.7, color="steelblue")
        ic.rolling(window=22).mean().plot(ax=a, color="forestgreen", lw=2, alpha=0.8)

        a.set(ylabel="IC", xlabel="")
        a.set_title(
            "{} Period Forward Return Information Coefficient (IC)".format(period_num)
        )
        a.axhline(0.0, linestyle="-", color="black", lw=1, alpha=0.8)
        a.legend(["IC", "1 month moving avg"], loc="upper right")
        a.text(
            0.05,
            0.95,
            "Mean %.3f \n Std. %.3f" % (ic.mean(), ic.std()),
            fontsize=16,
            bbox={"facecolor": "white", "alpha": 1, "pad": 5},
            transform=a.transAxes,
            verticalalignment="top",
        )

        curr_ymin, curr_ymax = a.get_ylim()
        ymin = curr_ymin if ymin is None else min(ymin, curr_ymin)
        ymax = curr_ymax if ymax is None else max(ymax, curr_ymax)

    for a in ax:
        a.set_ylim([ymin, ymax])

    return ax


def plot_ic_hist(ic, ax=None):
    """
    Plots Spearman Rank Information Coefficient histogram for a given factor.
    绘制给定因子的Spearman秩信息系数直方图
    详细解释

    Spearman秩信息系数（Spearman Rank Information Coefficient, IC）: 这是一种衡量因子预测能力的方法，通过计算因子值与未来回报之间的Spearman秩相关系数来实现。

    直方图（Histogram）: 这是一种统计图表，用于展示数据分布的频率。通过直方图，可以直观地看到Spearman秩信息系数在不同区间的分布情况。
    Parameters
    ----------
    ic : pd.DataFrame
        DataFrame indexed by date, with IC for each forward return.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    绘制给定因子的Spearman秩信息系数直方图

    参数
    ic: pd.DataFrame

    按日期索引的DataFrame，包含每个前瞻性回报的IC。

    ax: matplotlib.Axes, 可选

    用于绘图的坐标轴。

    返回值
    ax: matplotlib.Axes

    绘图所用的坐标轴
    """

    ic = ic.copy()

    num_plots = len(ic.columns)

    v_spaces = ((num_plots - 1) // 3) + 1

    if ax is None:
        f, ax = plt.subplots(v_spaces, 3, figsize=(18, v_spaces * 6))
        ax = ax.flatten()

    for a, (period_num, ic) in zip(ax, ic.items()):
        sns.histplot(ic.replace(np.nan, 0.0), kde=True, ax=a)
        a.set(title="%s Period IC" % period_num, xlabel="IC")
        a.set_xlim([-1, 1])
        a.text(
            0.05,
            0.95,
            "Mean %.3f \n Std. %.3f" % (ic.mean(), ic.std()),
            fontsize=16,
            bbox={"facecolor": "white", "alpha": 1, "pad": 5},
            transform=a.transAxes,
            verticalalignment="top",
        )
        a.axvline(ic.mean(), color="w", linestyle="dashed", linewidth=2)

    if num_plots < len(ax):
        ax[-1].set_visible(False)

    return ax


def plot_ic_qq(ic, theoretical_dist=stats.norm, ax=None):
    """
    Plots Spearman Rank Information Coefficient "Q-Q" plot relative to
    a theoretical distribution.
    绘制给定因子的Spearman秩信息系数相对于理论分布的Q-Q图
    Q-Q图（Quantile-Quantile Plot）: 这是一种统计图表，用于比较两个分布的分位数。通过Q-Q图，可以直观地看到实际数据分布与理论分布之间的差异。

    理论分布（Theoretical Distribution）: 这里指的是用于比较的参考分布，例如正态分布或t分布。
    Parameters
    ----------
    ic : pd.DataFrame
        DataFrame indexed by date, with IC for each forward return.
    theoretical_dist : scipy.stats._continuous_distns
        Continuous distribution generator. scipy.stats.norm and
        scipy.stats.t are popular options.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    绘制给定因子的Spearman秩信息系数相对于理论分布的Q-Q图

    参数
    ic: pd.DataFrame

    按日期索引的DataFrame，包含每个前瞻性回报的IC。

    theoretical_dist: scipy.stats._continuous_distns

    连续分布生成器。常见的选项包括scipy.stats.norm（正态分布）和scipy.stats.t（t分布）。

    ax: matplotlib.Axes, 可选

    用于绘图的坐标轴。

    返回值
    ax: matplotlib.Axes

    绘图所用的坐标轴。

    Q-Q图（Quantile-Quantile Plot）: 这是一种统计图表，用于比较两个分布的分位数。通过Q-Q图，可以直观地看到实际数据分布与理论分布之间的差异。

    理论分布（Theoretical Distribution）: 这里指的是用于比较的参考分布，例如正态分布或t分布。
    """

    ic = ic.copy()

    num_plots = len(ic.columns)

    v_spaces = ((num_plots - 1) // 3) + 1

    if ax is None:
        f, ax = plt.subplots(v_spaces, 3, figsize=(18, v_spaces * 6))
        ax = ax.flatten()

    if isinstance(theoretical_dist, stats.norm.__class__):
        dist_name = "Normal"
    elif isinstance(theoretical_dist, stats.t.__class__):
        dist_name = "T"
    else:
        dist_name = "Theoretical"

    for a, (period_num, ic) in zip(ax, ic.items()):
        sm.qqplot(
            ic.replace(np.nan, 0.0).values,
            theoretical_dist,
            fit=True,
            line="45",
            ax=a,
        )
        a.set(
            title="{} Period IC {} Dist. Q-Q".format(period_num, dist_name),
            ylabel="Observed Quantile",
            xlabel="{} Distribution Quantile".format(dist_name),
        )

    return ax


def plot_quantile_returns_bar(
    mean_ret_by_q, by_group=False, ylim_percentiles=None, ax=None
):
    """
    Plots mean period wise returns for factor quantiles.
    绘制因子分位数的周期性回报的平均值
    详细解释

    因子分位数（Factor Quantiles）: 在多因子模型中，因子值通常被分为不同的分位数（例如，第1分位数、第2分位数等），以评估不同分位数对投资组合表现的影响。

    周期性回报（Period Wise Returns）: 指在特定周期内（如日、周、月等）的回报。

    平均值（Mean）: 这里指的是周期性回报的平均值。
    Parameters
    ----------
    mean_ret_by_q : pd.DataFrame
        DataFrame with quantile, (group) and mean period wise return values.
    by_group : bool
        Disaggregated figures by group.
    ylim_percentiles : tuple of integers
        Percentiles of observed data to use as y limits for plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    绘制因子分位数的周期性回报的平均值

    参数
    mean_ret_by_q: pd.DataFrame

    包含分位数、组别和周期性回报平均值的DataFrame。

    by_group: bool

    是否按组别细分数据。

    ylim_percentiles: tuple of integers

    用于设置y轴范围的观测数据百分位数。

    ax: matplotlib.Axes, 可选

    用于绘图的坐标轴。

    返回值
    ax: matplotlib.Axes

    绘图所用的坐标轴
    """

    mean_ret_by_q = mean_ret_by_q.copy()

    if ylim_percentiles is not None:
        ymin = (
            np.nanpercentile(mean_ret_by_q.values, ylim_percentiles[0]) * DECIMAL_TO_BPS
        )
        ymax = (
            np.nanpercentile(mean_ret_by_q.values, ylim_percentiles[1]) * DECIMAL_TO_BPS
        )
    else:
        ymin = None
        ymax = None

    if by_group:
        num_group = len(mean_ret_by_q.index.get_level_values("group").unique())

        if ax is None:
            v_spaces = ((num_group - 1) // 2) + 1
            f, ax = plt.subplots(
                v_spaces,
                2,
                sharex=False,
                sharey=True,
                figsize=(18, 6 * v_spaces),
            )
            ax = ax.flatten()

        for a, (sc, cor) in zip(ax, mean_ret_by_q.groupby(level="group")):
            (
                cor.xs(sc, level="group")
                .multiply(DECIMAL_TO_BPS)
                .plot(kind="bar", title=sc, ax=a)
            )

            a.set(xlabel="", ylabel="Mean Return (bps)", ylim=(ymin, ymax))

        if num_group < len(ax):
            ax[-1].set_visible(False)

        return ax

    else:
        if ax is None:
            f, ax = plt.subplots(1, 1, figsize=(18, 6))

        (
            mean_ret_by_q.multiply(DECIMAL_TO_BPS).plot(
                kind="bar",
                title="Mean Period Wise Return By Factor Quantile",
                ax=ax,
            )
        )
        ax.set(xlabel="", ylabel="Mean Return (bps)", ylim=(ymin, ymax))

        return ax


def plot_quantile_returns_violin(return_by_q, ylim_percentiles=None, ax=None):
    """
    Plots a violin box plot of period wise returns for factor quantiles.
    绘制因子分位数的周期性回报的小提琴箱线图

    因子分位数（Factor Quantiles）: 在多因子模型中，因子值通常被分为不同的分位数（例如，第1分位数、第2分位数等），以评估不同分位数对投资组合表现的影响。

    周期性回报（Period Wise Returns）: 指在特定周期内（如日、周、月等）的回报。

    小提琴箱线图（Violin Box Plot）: 这是一种结合了小提琴图和箱线图的图表。小提琴图展示了数据的密度分布，而箱线图则展示了数据的四分位数和中位数，帮助更全面地理解数据的分布情况。
    Parameters
    ----------
    return_by_q : pd.DataFrame - MultiIndex
        DataFrame with date and quantile as rows MultiIndex,
        forward return windows as columns, returns as values.
    ylim_percentiles : tuple of integers
        Percentiles of observed data to use as y limits for plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    return_by_q = return_by_q.copy()

    if ylim_percentiles is not None:
        ymin = (
            np.nanpercentile(return_by_q.values, ylim_percentiles[0]) * DECIMAL_TO_BPS
        )
        ymax = (
            np.nanpercentile(return_by_q.values, ylim_percentiles[1]) * DECIMAL_TO_BPS
        )
    else:
        ymin = None
        ymax = None

    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))

    unstacked_dr = return_by_q.multiply(DECIMAL_TO_BPS)
    unstacked_dr.columns = unstacked_dr.columns.set_names("forward_periods")
    unstacked_dr = unstacked_dr.stack()
    unstacked_dr.name = "return"
    unstacked_dr = unstacked_dr.reset_index()

    sns.violinplot(
        data=unstacked_dr,
        x="factor_quantile",
        hue="forward_periods",
        y="return",
        orient="v",
        cut=0,
        inner="quartile",
        ax=ax,
    )
    ax.set(
        xlabel="",
        ylabel="Return (bps)",
        title="Period Wise Return By Factor Quantile",
        ylim=(ymin, ymax),
    )

    ax.axhline(0.0, linestyle="-", color="black", lw=0.7, alpha=0.6)

    return ax


def plot_mean_quantile_returns_spread_time_series(
    mean_returns_spread, std_err=None, bandwidth=1, ax=None
):
    """
    Plots mean period wise returns for factor quantiles.
    绘制因子分位数的周期性回报的平均值
    因子分位数（Factor Quantiles）: 在多因子模型中，因子值通常被分为不同的分位数（例如，第1分位数、第2分位数等），以评估不同分位数对投资组合表现的影响。

    周期性回报（Period Wise Returns）: 指在特定周期内（如日、周、月等）的回报。

    平均值（Mean）: 这里指的是周期性回报的平均值。
    Parameters
    ----------
    mean_returns_spread : pd.Series
        Series with difference between quantile mean returns by period.
    std_err : pd.Series
        Series with standard error of difference between quantile
        mean returns each period.
    bandwidth : float
        Width of displayed error bands in standard deviations.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if isinstance(mean_returns_spread, pd.DataFrame):
        if ax is None:
            ax = [None for a in mean_returns_spread.columns]

        ymin, ymax = (None, None)
        for (i, a), (name, fr_column) in zip(
            enumerate(ax), mean_returns_spread.items()
        ):
            stdn = None if std_err is None else std_err[name]
            a = plot_mean_quantile_returns_spread_time_series(
                fr_column, std_err=stdn, ax=a
            )
            ax[i] = a
            curr_ymin, curr_ymax = a.get_ylim()
            ymin = curr_ymin if ymin is None else min(ymin, curr_ymin)
            ymax = curr_ymax if ymax is None else max(ymax, curr_ymax)

        for a in ax:
            a.set_ylim([ymin, ymax])

        return ax

    if mean_returns_spread.isnull().all():
        return ax

    periods = mean_returns_spread.name
    title = (
        "Top Minus Bottom Quantile Mean Return "
        "({} Period Forward Return)".format(periods if periods is not None else "")
    )

    if ax is None:
        f, ax = plt.subplots(figsize=(18, 6))

    mean_returns_spread_bps = mean_returns_spread * DECIMAL_TO_BPS

    mean_returns_spread_bps.plot(alpha=0.4, ax=ax, lw=0.7, color="forestgreen")
    mean_returns_spread_bps.rolling(window=22).mean().plot(
        color="orangered", alpha=0.7, ax=ax
    )
    ax.legend(["mean returns spread", "1 month moving avg"], loc="upper right")

    if std_err is not None:
        std_err_bps = std_err * DECIMAL_TO_BPS
        upper = mean_returns_spread_bps.values + (std_err_bps * bandwidth)
        lower = mean_returns_spread_bps.values - (std_err_bps * bandwidth)
        ax.fill_between(
            mean_returns_spread.index,
            lower,
            upper,
            alpha=0.3,
            color="steelblue",
        )

    ylim = np.nanpercentile(abs(mean_returns_spread_bps.values), 95)
    ax.set(
        ylabel="Difference In Quantile Mean Return (bps)",
        xlabel="",
        title=title,
        ylim=(-ylim, ylim),
    )
    ax.axhline(0.0, linestyle="-", color="black", lw=1, alpha=0.8)

    return ax


def plot_ic_by_group(ic_group, ax=None):
    """
    Plots Spearman Rank Information Coefficient for a given factor over
    provided forward returns. Separates by group.
    绘制给定因子在提供的前瞻性回报上的Spearman秩信息系数，并按组别进行分离

    详细解释

    Spearman秩信息系数（Spearman Rank Information Coefficient, IC）: 这是一种衡量因子预测能力的方法，通过计算因子值与未来回报之间的Spearman秩相关系数来实现。

    前瞻性回报（Forward Returns）: 指未来的回报，通常用于评估因子对未来表现的预测能力。

    按组别分离（Separates by Group）: 这意味着将数据按不同的组别进行分类，并在图表中分别展示每个组别的Spearman秩信息系数。


    Parameters
    ----------
    ic_group : pd.DataFrame
        group-wise mean period wise returns.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))
    ic_group.plot(kind="bar", ax=ax)

    ax.set(title="Information Coefficient By Group", xlabel="")
    ax.set_xticklabels(ic_group.index, rotation=45)

    return ax


def plot_factor_rank_auto_correlation(factor_autocorrelation, period=1, ax=None):
    """
    Plots factor rank autocorrelation over time.
    See factor_rank_autocorrelation for more details.
    绘制因子排名自相关性随时间的变化

    详细解释

    因子排名（Factor Rank）: 在多因子模型中，各个因子根据其对投资组合表现的影响力进行的排名。

    自相关性（Autocorrelation）: 指时间序列数据中，某一时刻的值与之前时刻的值之间的相关性。

    随时间的变化（Over Time）: 这意味着图表将展示因子排名自相关性在不同时间点的变化情况。
    Parameters
    ----------
    factor_autocorrelation : pd.Series
        Rolling 1 period (defined by time_rule) autocorrelation
        of factor values.
    period: int, optional
        Period over which the autocorrelation is calculated
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))

    factor_autocorrelation.plot(
        title="{}D Period Factor Rank Autocorrelation".format(period), ax=ax
    )
    ax.set(ylabel="Autocorrelation Coefficient", xlabel="")
    ax.axhline(0.0, linestyle="-", color="black", lw=1)
    ax.text(
        0.05,
        0.95,
        "Mean %.3f" % factor_autocorrelation.mean(),
        fontsize=16,
        bbox={"facecolor": "white", "alpha": 1, "pad": 5},
        transform=ax.transAxes,
        verticalalignment="top",
    )

    return ax


def plot_top_bottom_quantile_turnover(quantile_turnover, period=1, ax=None):
    """
    Plots period wise top and bottom quantile factor turnover.
    绘制周期性最高和最低分位数的因子换手率

    详细解释

    周期性（Period Wise）: 指在特定周期内（如日、周、月等）的换手率。

    最高分位数（Top Quantile）: 通常指因子值最高的部分（例如最高的25%或10%）。

    最低分位数（Bottom Quantile）: 通常指因子值最低的部分（例如最低的25%或10%）。

    因子换手率（Factor Turnover）: 指在一定时间内资产或证券的交易量占总量的比例。
    Parameters
    ----------
    quantile_turnover: pd.Dataframe
        Quantile turnover (each DataFrame column a quantile).
    period: int, optional
        Period over which to calculate the turnover.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))

    max_quantile = quantile_turnover.columns.max()
    min_quantile = quantile_turnover.columns.min()
    turnover = pd.DataFrame()
    turnover["top quantile turnover"] = quantile_turnover[max_quantile]
    turnover["bottom quantile turnover"] = quantile_turnover[min_quantile]
    turnover.plot(
        title="{}D Period Top and Bottom Quantile Turnover".format(period),
        ax=ax,
        alpha=0.6,
        lw=0.8,
    )
    ax.set(ylabel="Proportion Of Names New To Quantile", xlabel="")

    return ax


def plot_monthly_ic_heatmap(mean_monthly_ic, ax=None):
    """
    Plots a heatmap of the information coefficient or returns by month.
    绘制信息系数或回报按月份的热力图

    详细解释

    信息系数（Information Coefficient, IC）: 这是一种衡量因子预测能力的方法，通常通过计算因子值与未来回报之间的相关系数来实现。

    回报（Returns）: 指投资组合或资产在特定时间段内的收益。

    按月份（By Month）: 这意味着数据将按月份进行分类和展示。

    热力图（Heatmap）: 这是一种图表，通过颜色深浅来展示数据的分布和强度。在热力图中，颜色越深表示值越大，颜色越浅表示值越小。
    Parameters
    ----------
    mean_monthly_ic : pd.DataFrame
        The mean monthly IC for N periods forward.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    mean_monthly_ic = mean_monthly_ic.copy()

    num_plots = len(mean_monthly_ic.columns)

    v_spaces = ((num_plots - 1) // 3) + 1

    if ax is None:
        f, ax = plt.subplots(v_spaces, 3, figsize=(18, v_spaces * 6))
        ax = ax.flatten()

    new_index_year = []
    new_index_month = []
    for date in mean_monthly_ic.index:
        new_index_year.append(date.year)
        new_index_month.append(date.month)

    mean_monthly_ic.index = pd.MultiIndex.from_arrays(
        [new_index_year, new_index_month], names=["year", "month"]
    )

    for a, (periods_num, ic) in zip(ax, mean_monthly_ic.items()):
        sns.heatmap(
            ic.unstack(),
            annot=True,
            alpha=1.0,
            center=0.0,
            annot_kws={"size": 7},
            linewidths=0.01,
            linecolor="white",
            cmap=cm.coolwarm_r,
            cbar=False,
            ax=a,
        )
        a.set(ylabel="", xlabel="")

        a.set_title("Monthly Mean {} Period IC".format(periods_num))

    if num_plots < len(ax):
        ax[-1].set_visible(False)

    return ax


def plot_cumulative_returns(factor_returns, period, freq=None, title=None, ax=None):
    """
    Plots the cumulative returns of the returns series passed in.
    绘制传入的回报序列的累积回报

    详细解释

    回报序列（Returns Series）: 指在特定时间段内的一系列回报数据。

    累积回报（Cumulative Returns）: 指从初始时间点到当前时间点的总回报，通常通过将每个时间点的回报累加得到。
    Parameters
    ----------
    factor_returns : pd.Series
        Period wise returns of dollar neutral portfolio weighted by factor
        value.
    period : pandas.Timedelta or string
        Length of period for which the returns are computed (e.g. 1 day)
        if 'period' is a string it must follow pandas.Timedelta constructor
        format (e.g. '1 days', '1D', '30m', '3h', '1D1h', etc)
    freq : pandas DateOffset
        Used to specify a particular trading calendar e.g. BusinessDay or Day
        Usually this is inferred from utils.infer_trading_calendar, which is
        called by either get_clean_factor_and_forward_returns or
        compute_forward_returns
    title: string, optional
        Custom title
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))

    factor_returns = perf.cumulative_returns(factor_returns)

    factor_returns.plot(ax=ax, lw=3, color="forestgreen", alpha=0.6)
    ax.set(
        ylabel="Cumulative Returns",
        title=(
            "Portfolio Cumulative Return ({} Fwd Period)".format(period)
            if title is None
            else title
        ),
        xlabel="",
    )
    ax.axhline(1.0, linestyle="-", color="black", lw=1)

    return ax


def plot_cumulative_returns_by_quantile(quantile_returns, period, freq=None, ax=None):
    """
    Plots the cumulative returns of various factor quantiles.
    绘制各种因子分位数的累积回报

    详细解释

    因子分位数（Factor Quantiles）: 在多因子模型中，因子值通常被分为不同的分位数（例如，第1分位数、第2分位数等），以评估不同分位数对投资组合表现的影响。

    累积回报（Cumulative Returns）: 指从初始时间点到当前时间点的总回报，通常通过将每个时间点的回报累加得到。
    Parameters
    ----------
    quantile_returns : pd.DataFrame
        Returns by factor quantile
    period : pandas.Timedelta or string
        Length of period for which the returns are computed (e.g. 1 day)
        if 'period' is a string it must follow pandas.Timedelta constructor
        format (e.g. '1 days', '1D', '30m', '3h', '1D1h', etc)
    freq : pandas DateOffset
        Used to specify a particular trading calendar e.g. BusinessDay or Day
        Usually this is inferred from utils.infer_trading_calendar, which is
        called by either get_clean_factor_and_forward_returns or
        compute_forward_returns
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
    """

    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))

    ret_wide = quantile_returns.unstack("factor_quantile")

    cum_ret = ret_wide.apply(perf.cumulative_returns)

    cum_ret = cum_ret.loc[:, ::-1]  # we want negative quantiles as 'red'

    cum_ret.plot(lw=2, ax=ax, cmap=cm.coolwarm)
    ax.legend()
    ymin, ymax = cum_ret.min().min(), cum_ret.max().max()
    ax.set(
        ylabel="Log Cumulative Returns",
        title="""Cumulative Return by Quantile
                    ({} Period Forward Return)""".format(
            period
        ),
        xlabel="",
        yscale="symlog",
        yticks=np.linspace(ymin, ymax, 5),
        ylim=(ymin, ymax),
    )

    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.axhline(1.0, linestyle="-", color="black", lw=1)

    return ax


def plot_quantile_average_cumulative_return(
    avg_cumulative_returns,
    by_quantile=False,
    std_bar=False,
    title=None,
    ax=None,
):
    """
    Plots sector-wise mean daily returns for factor quantiles
    across provided forward price movement columns.
    绘制因子分位数在不同行业中的每日平均回报，并考虑提供的前瞻性价格变动列

    详细解释

    因子分位数（Factor Quantiles）: 在多因子模型中，因子值通常被分为不同的分位数（例如，第1分位数、第2分位数等），以评估不同分位数对投资组合表现的影响。

    行业（Sector）: 指不同的行业或部门，通常用于分析不同行业的表现差异。

    每日平均回报（Mean Daily Returns）: 指在特定时间段内（通常是每日）的平均回报。

    前瞻性价格变动列（Forward Price Movement Columns）: 指未来的价格变动数据，通常用于评估因子对未来表现的预测能力。
    Parameters
    ----------
    avg_cumulative_returns: pd.Dataframe
        The format is the one returned by
        performance.average_cumulative_return_by_quantile
    by_quantile : boolean, optional
        Disaggregated figures by quantile (useful to clearly see std dev bars)
    std_bar : boolean, optional
        Plot standard deviation plot
    title: string, optional
        Custom title
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
    """

    avg_cumulative_returns = avg_cumulative_returns.multiply(DECIMAL_TO_BPS)
    quantiles = len(avg_cumulative_returns.index.levels[0].unique())
    palette = [cm.coolwarm(i) for i in np.linspace(0, 1, quantiles)]
    palette = palette[::-1]  # we want negative quantiles as 'red'

    if by_quantile:

        if ax is None:
            v_spaces = ((quantiles - 1) // 2) + 1
            f, ax = plt.subplots(
                v_spaces,
                2,
                sharex=False,
                sharey=False,
                figsize=(18, 6 * v_spaces),
            )
            ax = ax.flatten()

        for i, (quantile, q_ret) in enumerate(
            avg_cumulative_returns.groupby(level="factor_quantile")
        ):

            mean = q_ret.loc[(quantile, "mean")]
            mean.name = "Quantile " + str(quantile)
            mean.plot(ax=ax[i], color=palette[i])
            ax[i].set_ylabel("Mean Return (bps)")

            if std_bar:
                std = q_ret.loc[(quantile, "std")]
                ax[i].errorbar(
                    std.index,
                    mean,
                    yerr=std,
                    fmt="none",
                    ecolor=palette[i],
                    label="none",
                )

            ax[i].axvline(x=0, color="k", linestyle="--")
            ax[i].legend()
            i += 1

    else:

        if ax is None:
            f, ax = plt.subplots(1, 1, figsize=(18, 6))

        for i, (quantile, q_ret) in enumerate(
            avg_cumulative_returns.groupby(level="factor_quantile")
        ):

            mean = q_ret.loc[(quantile, "mean")]
            mean.name = "Quantile " + str(quantile)
            mean.plot(ax=ax, color=palette[i])

            if std_bar:
                std = q_ret.loc[(quantile, "std")]
                ax.errorbar(
                    std.index,
                    mean,
                    yerr=std,
                    fmt="none",
                    ecolor=palette[i],
                    label="none",
                )
            i += 1

        ax.axvline(x=0, color="k", linestyle="--")
        ax.legend()
        ax.set(
            ylabel="Mean Return (bps)",
            title=(
                "Average Cumulative Returns by Quantile" if title is None else title
            ),
            xlabel="Periods",
        )

    return ax


def plot_events_distribution(events, num_bars=50, ax=None):
    """
    Plots the distribution of events in time.
    绘制事件在时间上的分布

    详细解释

    事件（Events）: 指在特定时间点发生的特定事件或数据点。

    时间上的分布（Distribution in Time）: 这意味着图表将展示事件在不同时间点的分布情况。
    Parameters
    ----------
    events : pd.Series
        A pd.Series whose index contains at least 'date' level.
    num_bars : integer, optional
        Number of bars to plot
    ax : matplotlib.Axes, optional
        Axes upon which to plot.

    Returns
    -------
    ax : matplotlib.Axes
    """

    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))

    start = events.index.get_level_values("date").min()
    end = events.index.get_level_values("date").max()
    group_interval = (end - start) / num_bars
    grouper = pd.Grouper(level="date", freq=group_interval)
    events.groupby(grouper).count().plot(kind="bar", grid=False, ax=ax)
    ax.set(
        ylabel="Number of events",
        title="Distribution of events in time",
        xlabel="Date",
    )

    return ax
