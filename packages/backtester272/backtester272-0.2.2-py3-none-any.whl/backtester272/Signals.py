import requests
import pandas as pd
import time
from pandas.tseries.offsets import DateOffset

from DataBase import DataBase


class Signals:
    """
    Classe pour analyser les signaux de trading à partir d'un fichier CSV contenant des données de crypto-monnaies.
    """

    def __init__(self, file_path, alpha=1.0, verbose=False):
        """
        Initialise la classe avec le chemin du fichier et les paramètres de configuration.

        :param file_path: Chemin vers le fichier CSV contenant les données.
        :param alpha: Coefficient qui permet de calculer le risque du portefeuille.
        :param verbose: Booléen pour activer les messages d'information.
        """
        self.file_path = file_path
        self.alpha = alpha
        self.verbose = verbose
        self.database = self.load_data()
        self.monthly_returns = self.Value_strat()

    def load_data(self):
        """
        Charge le fichier CSV et prétraité les données.

        :return: DataFrame contenant les données prétraitées.
        """
        # Charger le CSV
        database = pd.read_csv(self.file_path)
        database = database[["Date", "ID", "Close"]]

        # Convertir la colonne 'Date' en format datetime
        database['Date'] = pd.to_datetime(database['Date'], format='%Y-%m-%d')
        
        return database

    def Value_strat(self): # Return sur 1 mois
        """
        Calcule les retours mensuels et les pondérations.

        :return: DataFrame contenant les retours mensuels, les rangs et les pondérations.
        """
        # Obtenir la date la plus récente dans la colonne 'Date'
        most_recent_date = self.database['Date'].max()

        # Calculer un mois en arrière
        one_month_ago = most_recent_date - DateOffset(months=1)

        # Filtrer les données pour ne garder que celles entre un mois en arrière et la date la plus récente
        filtered_data = self.database[(self.database['Date'] > one_month_ago) & (self.database['Date'] <= most_recent_date)]

        # Calculer les returns (pourcentage de changement quotidien)
        filtered_data['returns'] = filtered_data['Close'].pct_change()

        # Extraire l'année et le mois de la colonne 'Date'
        filtered_data['Month'] = filtered_data['Date'].dt.to_period('M')

        # Ne garder que les données du mois le plus récent
        latest_month = filtered_data['Month'].max()
        filtered_data = filtered_data[filtered_data['Month'] == latest_month]

        # Grouper par 'ID' (actif) et calculer la moyenne des returns
        monthly_returns = filtered_data.groupby(['ID', 'Month'])['returns'].mean().reset_index().sort_values(by='returns', ascending=False).reset_index(drop=True)

        # Calculer le rank des returns (du plus grand au plus petit)
        monthly_returns['Rank'] = monthly_returns['returns'].rank(ascending=False)

        # Calculer la somme des ranks
        sum_ranks = monthly_returns['Rank'].sum()

        # Calculer le nombre d'actifs uniques
        num_assets = monthly_returns['ID'].nunique()

        # Calculer la pondération
        monthly_returns['Weight'] = self.alpha * (monthly_returns['Rank'] - (sum_ranks / num_assets))

        return monthly_returns

    def display_results(self):
        """
        Affiche les résultats des retours mensuels, rangs et pondérations.
        """
        print(self.monthly_returns[['ID', 'Rank', 'Weight']])
    
    def calculate_returns(self, period):
        """
        Calcule les retours d'une période donnée.

        :param period: La période sur laquelle calculer les retours (en mois).
        :return: DataFrame contenant les retours moyens par actif.
        """
        # Obtenir la date la plus récente
        most_recent_date = self.database['Date'].max()
        start_date = most_recent_date - DateOffset(months=period)

        # Filtrer les données pour la période souhaitée
        filtered_data = self.database[(self.database['Date'] >= start_date) & (self.database['Date'] <= most_recent_date)].copy()

        # Calculer les retours
        filtered_data['returns'] = filtered_data['Close'].pct_change()

        # Grouper par 'ID' (actif) et calculer la moyenne des retours
        returns_mean = filtered_data.groupby('ID')['returns'].mean().reset_index()
        returns_mean.columns = ['ID', f'returns_{period}_months']  # Renommer la colonne

        return returns_mean

    
    def Trend(self):
        """
        Calcule les rendements sur 1 mois, 6 mois et 1 an,
        puis applique la stratégie de Trend following.

        :return: DataFrame avec les actifs à acheter ou vendre.
        """
        # Calculer les retours pour les trois périodes
        returns_1m = self.calculate_returns(1)
        returns_6m = self.calculate_returns(6)
        returns_12m = self.calculate_returns(12)

        # Fusionner les données de retours
        trend_data = returns_1m.merge(returns_6m, on='ID', how='outer').merge(returns_12m, on='ID', how='outer')

        # Calculer la moyenne des retours sur les trois périodes
        trend_data['average_returns'] = trend_data[['returns_1_months', 'returns_6_months', 'returns_12_months']].mean(axis=1)

        # Séparer les actifs à acheter et à vendre
        to_buy = trend_data[trend_data['average_returns'] > 0]
        to_sell = trend_data[trend_data['average_returns'] <= 0]

        if self.verbose:
            print("Assets to Buy:")
            print(to_buy)
            print("\nAssets to Sell:")
            print(to_sell)

        return to_buy, to_sell
    
class Momentum:
        """
        Calcule les rendements sur 1 mois, 1 an,
        puis applique la stratégie de Momentum qui consite à acheter les cryptos au plus haut rendement et vendre celles qui ont les rendements les plus faibles .

        :return: DataFrame avec les actifs et leur rank.
        """
        
        def __init__(self, historical_data, num_assets=8, lookback_period=180):
            self.historical_data = pd.read_csv(historical_data)
            self.num_assets = num_assets
            self.lookback_period = lookback_period
            self.historical_data['Date']  = pd.to_datetime(self.historical_data['Date'])
            self.historical_data.set_index('Date', inplace=True)
        # Calculer les retours pour les trois périodes

        def calculate_return(self):
            self.returns = self.historical_data.pct_change()
            
            
        def calculate_volatility(self):
            self.volatility = self.returns.rolling(window=365, min_periods=1).std().mean()
            
            
        def select_assets(self):
            """ periode de lookback - la periode la plus récente
            """
            self.total_returns = self.returns.rolling(window=self.lookback_period).apply(lambda x: (1 + x).prod() - 1)
            # Sélectionner les actifs avec les meilleurs rendements
            self.top_assets = self.total_returns.iloc[-1].nlargest(self.num_assets).index.tolist()
            # Sélectionner les actifs avec les pires rendements
            self.bottom_assets = self.total_returns.iloc[-1].nsmallest(self.num_assets).index.tolist()

        def calculate_weights(self):
            """Calcule les poids des actifs basés sur la variation de la performance.
                on prends la valeur absolue de car on veux buy les meilleurs et short les moins bonnes
                c'est pour ca qu'on *-1 pour self.relative_weights_bottom_assets pour s'assurer qu'on est des chiffres négatifs et qu'on short
            """
            # Calculer la variation quotidienne de la performance pour les actifs sélectionnés
            daily_variation_top_assets = self.returns[self.top_assets].diff().abs()
            
            # Calculer les poids relatifs en divisant la variation quotidienne de chaque actif par la variation totale
            self.relative_weights_top_assets = daily_variation_top_assets.div(daily_variation_top_assets.sum(axis=1), axis=0)
            self.relative_weights_top_assets = self.relative_weights_top_assets.iloc[-1]
            
            # Calculer la variation quotidienne de la performance pour les actifs sélectionnés
            daily_variation_botom_assets = self.returns[self.bottom_assets].diff().abs()
            
            # Calculer les poids relatifs en divisant la variation quotidienne de chaque actif par la variation totale
            self.relative_weights_bottom_assets = daily_variation_botom_assets.div(daily_variation_botom_assets.sum(axis=1), axis=0)
            self.relative_weights_bottom_assets = self.relative_weights_bottom_assets.iloc[-1] * -1
            
            self.total_weights = pd.concat([self.relative_weights_top_assets, self.relative_weights_bottom_assets])


        def run_strat(self):
            self.calculate_return()
            self.select_assets()
            self.calculate_weights()
            
            
            return self.total_weights


