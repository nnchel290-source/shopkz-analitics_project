
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine


DB_USER = "postgres"
DB_PASSWORD = "koksoker"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "shop_analytics"

engine = create_engine(
    f"postgresql+psycopg2://postgres:koksoker@localhost:5432/kzshop_db"
)


query = """
    SELECT sale_date, total_amount
    FROM sales
    ORDER BY sale_date;
"""

df = pd.read_sql(query, engine)
df["sale_date"] = pd.to_datetime(df["sale_date"])
df = df.set_index("sale_date")


# Метрика 1
daily_revenue = df["total_amount"].resample("D").sum()

# Метрика 2
cumulative_revenue = daily_revenue.cumsum()

# Метрика 3
rolling_avg = daily_revenue.rolling(7).mean()

print("=== Первые 5 строк ежедневной выручки ===")
print(daily_revenue.head())
print(f"\nОбщая выручка: {cumulative_revenue.iloc[-1]:,.0f} тг")
print(f"Средняя дневная выручка: {daily_revenue.mean():,.0f} тг")


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle("shop_analytics — Дашборд продаж 2023–2024", fontsize=16, fontweight="bold", y=0.98)


ax1.bar(
    daily_revenue.index,
    daily_revenue.values,
    color="#4C72B0",
    alpha=0.5,
    label="Күнделікті түсім / Дневная выручка",
    width=1
)
ax1.plot(
    rolling_avg.index,
    rolling_avg.values,
    color="#C44E52",
    linewidth=2,
    label="7 күндік орта / 7-дн. скользящее среднее"
)
ax1.set_title("Күнделікті түсім және тренд / Дневная выручка и тренд", fontsize=13)
ax1.set_xlabel("Күні / Дата")
ax1.set_ylabel("Түсім (тг) / Выручка (тг)")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.tick_params(axis="x", rotation=45)
ax1.legend(loc="upper left")
ax1.grid(axis="y", alpha=0.3)


ax2.plot(
    cumulative_revenue.index,
    cumulative_revenue.values,
    color="#2ca02c",
    linewidth=2,
    label="Жинақталған түсім / Накопленная выручка"
)
ax2.fill_between(
    cumulative_revenue.index,
    cumulative_revenue.values,
    alpha=0.25,
    color="#2ca02c"
)
ax2.set_title("Жинақталған қорытынды / Накопленная выручка", fontsize=13)
ax2.set_xlabel("Күні / Дата")
ax2.set_ylabel("Жалпы түсім (тг) / Итого (тг)")
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.tick_params(axis="x", rotation=45)
ax2.legend(loc="upper left")
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nДашборд сохранён в dashboard.png")
