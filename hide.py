import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import warnings
import datetime

warnings.filterwarnings('ignore')

def create_sample_data(symbol):
    np.random.seed(abs(hash(symbol)) % 1000)
    base_prices = {
        'AAPL': 175, 'GOOGL': 140, 'MSFT': 380,
        'TSLA': 200, 'AMZN': 170, 'META': 450, 'NVDA': 850,
    }
    base = base_prices.get(symbol, 100)
    dates = pd.date_range(end=datetime.datetime.now(), periods=180)
    changes = np.random.normal(0, 2, 180)
    prices = base + np.cumsum(changes)
    return pd.DataFrame({'Close': prices}, index=dates)

def predict_stock(symbol):
    try:
        try:
            df = yf.download(symbol, period="6mo", progress=False, timeout=10)
        except Exception as e:
            print(f"Download error: {e}")
            df = pd.DataFrame()

        if df is None or df.empty:
            print(f"No data for {symbol}, using sample data")
            df = create_sample_data(symbol)
            data = df[['Close']].copy()
        else:
            # MultiIndex fix
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Close column dhundo
            close_col = None
            for col in df.columns:
                if str(col).lower() == 'close':
                    close_col = col
                    break

            if close_col is None:
                df = create_sample_data(symbol)
                data = df[['Close']].copy()
            else:
                data = df[[close_col]].copy()
                data.columns = ['Close']

        data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
        data.dropna(inplace=True)

        if len(data) < 15:
            return None

        for i in range(1, 11):
            data[f'Day_{i}'] = data['Close'].shift(i)
        data['Target'] = data['Close'].shift(-1)
        data.dropna(inplace=True)

        feature_cols = [f'Day_{i}' for i in range(1, 11)]
        X = data[feature_cols]
        y = data['Target']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X_train, y_train)

        current_price = float(data['Close'].iloc[-1])
        last_sequence = X.iloc[-1:].values
        tomorrow_price = float(model.predict(last_sequence)[0])

        change = tomorrow_price - current_price
        percent = round((change / current_price) * 100, 2)

        return {
            'symbol': symbol,
            'current_price': round(current_price, 2),
            'predicted_price': round(tomorrow_price, 2),
            'percent_change': percent,
            'history_prices': [round(float(x), 2) for x in data['Close'].tail(7).tolist()],
            'history_dates': [str(d.strftime('%d %b')) for d in data.index[-7:]],
        }

    except Exception as e:
        print(f"Error: {e}")
        return None