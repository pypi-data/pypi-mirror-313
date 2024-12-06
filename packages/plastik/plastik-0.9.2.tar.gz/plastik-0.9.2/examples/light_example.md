---
title: "plastik"
kind: beamer
fontsize: 8pt
...

# Imports

```python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import plastik
```

# Log tick format 1

```python
a = np.exp(np.linspace(-3, 5, 100))
base = 2  # Default is 10, but 2 works equally well
plt.figure()
plastik.log_tick_format(plt.gca(), "x", base=base)
plt.plot(a)
plt.show()
```
\hfill![](figures/log_tick_format1.png){width=70%}\hfill\hfill

# Log tick format 2

```python
a = np.exp(np.linspace(-3, 5, 100))
base = 2  # Default is 10, but 2 works equally well
fig = plt.figure()
ax = fig.add_subplot(111)
ax.loglog()
plastik.log_tick_format(ax, "both", base=base)
ax.plot(a)
plt.show()
```
\hfill![](figures/log_tick_format2.png){width=70%}\hfill\hfill

# Log tick format 3

```python
a = np.exp(np.linspace(-3, 5, 100))
fig = plt.figure()
ax = fig.add_subplot(111)
ax = plastik.log_tick_format(ax, "y")
# If you do:
ax.semilogy(a)
# the axis will be re-set, in which case you will have to run
plastik.log_tick_format(ax, "y")
# again. (But just use plt.plot(), so much easier.)
plt.show()
```
\vspace{-5mm}
\hfill![](figures/log_tick_format3.png){width=70%}\hfill\hfill

# Topside legends 1

```python
a = np.linspace(-3, 5, 100)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(a, label="Topside legend 1")
ax.plot(a + 1, label="Topside legend 2")
ax.plot(a + 2, label="Topside legend 3")
ax.plot(a + 3, label="Topside legend 4")
plastik.topside_legends(ax, c_max=2, side="bottom", alpha=0.2)
plt.show()
```
\vspace{-5mm}
\hfill![](figures/topside_legends1.png){width=70%}\hfill\hfill

# Topside legends 2

```python
a = np.linspace(-3, 5, 100)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(a, label="Topside legend 1")
ax.plot(a + 1, label="Topside legend 2")
ax.plot(a + 2, label="Topside legend 3")
ax.plot(a + 3, label="Topside legend 4")
plastik.topside_legends(ax, c_max=3, side="top right", alpha=1)
plt.show()
```
\vspace{-5mm}
\hfill![](figures/topside_legends2.png){width=70%}\hfill\hfill

# Ridge plot (prep)

```python
# Set up
x = np.linspace(1e-1, 3e1, 1000) ** 2


def func(x, s):
    return 10 / ((x - s) ** 2 + 1)


dt = [
    func(x, 3), func(x, 1), func(x, 0),
    func(x, 100), func(x, 300), func(x, 500)
]
dta = [(x, a) for a in dt]

lab = [f"{i}" for i in range(6)]
```

# Ridge plot 1

::: columns

:::: {.column width=40%}

```python
r = plastik.Ridge(
    dta,
    "gsz",
    xlabel="bottom",
    ylabel="xlabel",
)
r.main()
f = r.figure
l = r.lines
a = r.top_axes
axs = r.all_axes
a.legend(l, lab)
plt.show()
```

::::

:::: {.column width=60%}

\hfill![](figures/ridge1.png){width=75%}

::::

:::

# Ridge plot 2

::: columns

:::: {.column width=45%}

```python
r = plastik.Ridge(
    dta,
    "gs",
    ylabel="xlabel",
)
r.main()
f = r.figure
l = r.lines
a = r.top_axes
axs = r.all_axes
a.legend(l, lab)
plastik.topside_legends(
    a, l, c_max=6, side="right"
)
for ax in axs:
    plastik.log_tick_format(ax, which="y")
plt.show()
```

::::

:::: {.column width=55%}

\hfill![](figures/ridge2.png){width=85%}

::::

:::

# Ridge plot 3

::: columns

:::: {.column width=40%}

```python
r = plastik.Ridge(
    dta,
    "s",
    xlabel="bottom axis label",
    ylabel="xlabel",
    pltype="semilogx",
)
r.main()
f = r.figure
l = r.lines
a = r.top_axes
axs = r.all_axes
a.legend(l, lab)
plastik.topside_legends(
    a, l, c_max=5, side="right"
)
for ax in axs:
    plastik.log_tick_format(ax, which="x")
plt.show()
```

::::

:::: {.column width=60%}

\hfill![](figures/ridge3.png){width=75%}

::::

:::
# Ridge plot 4

::: columns

:::: {.column width=40%}

```python
r = plastik.Ridge(
    dta,
    "bz",
    ylabel="xlabel",
    pltype="loglog",
)
r.main()
f = r.figure
l = r.lines
a = r.bottom_axes
axs = r.all_axes
for ax in axs:
    plastik.log_tick_format(ax, which="both")
plt.show()
```

::::

:::: {.column width=60%}

\hfill![](figures/ridge4.png){width=75%}

::::

:::
