import os
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "bookings.csv"

def load_data():
    if not os.path.exists(FILE_NAME):
        print(f"Error: File '{FILE_NAME}' not found.")
        return None

    try:
        df = pd.read_csv(FILE_NAME)
    except Exception as error:
        print(f"Error while reading CSV: {error}")
        return None

    required_columns = ["PNR", "Train", "Class", "Fare", "Status"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print("Error: Missing column(s):", ", ".join(missing_columns))
        return None

    df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")

    invalid_rows = df[df["Fare"].isna()]
    for _, row in invalid_rows.iterrows():
        print(f"Warning: Row with PNR {row['PNR']} skipped - invalid fare.")

    return df.dropna(subset=["Fare"]).copy()

def show_bookings_per_train(df):
    booking_count = df.groupby("Train").size().sort_values(ascending=False)

    print("\nBookings per train:")
    for train, count in booking_count.items():
        print(f"{train} : {int(count)}")

    print(f"Total bookings: {len(df)}")

    booking_count.plot(kind="bar", title="Bookings per Train")
    plt.xlabel("Train")
    plt.ylabel("Number of Bookings")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def show_confirmed_revenue(df):
    confirmed = df[
        df["Status"].astype(str).str.strip().str.lower() == "confirmed"
    ]

    revenue = confirmed.groupby("Train")["Fare"].sum().sort_values(ascending=False)

    print("\nRevenue per train (Confirmed only):")
    for train, amount in revenue.items():
        print(f"{train} : Rs. {amount:.0f}")

    print(f"Total confirmed revenue: Rs. {revenue.sum():.0f}")

    revenue.plot(kind="bar", title="Confirmed Revenue per Train")
    plt.xlabel("Train")
    plt.ylabel("Revenue (Rs.)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def main():
    print("===== Railway Reservation Analyzer =====")
    df = load_data()

    if df is None:
        return

    print(f"\nValid records: {len(df)}")

    while True:
        print("\nMenu:")
        print("1. Bookings per train")
        print("2. Revenue per train (Confirmed only)")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_bookings_per_train(df)
        elif choice == "2":
            show_confirmed_revenue(df)
        elif choice == "3":
            print("Program ended.")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()
