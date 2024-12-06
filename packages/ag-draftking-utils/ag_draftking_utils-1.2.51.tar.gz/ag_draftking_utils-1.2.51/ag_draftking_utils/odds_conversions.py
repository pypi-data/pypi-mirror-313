import numpy as np

def american_odds_to_breakeven_probability(ml):
    """
    Takes in the American Odds and returns the breakeven 
    probability necessary to win a bet
    :param ml - int: the moneyline (-100, -200, +110, +100, etc)
    """
    assert ml >= 100 or ml <= -100
    if ml < 0:
        return -ml / (-ml + 100)
    return 100 / (100 + ml)

def american_odds_to_payout(american_odds, did_win_bet, bet_size=100):
    """
    Determines the payout of the bet based on the win/loss and the odds.

    :param american_odds - int: the moneyline (-100, -200, +110, +100, etc)
    :param did_win_bet - bool: whether or not the bet pays-out
    :param bet_size - float: amount bet on the game
    """
    if not did_win_bet:
        return -bet_size
    if american_odds < 0:
        return (100/(-american_odds)) * bet_size
    else:
        return bet_size * american_odds/100

def american_odds_to_payout_vectorized(df, bet_size=100, price_col='price', won_bet_col='won_bet'):
    return np.where(
        df[won_bet_col].isna(),
        0,
        np.where(
            df[won_bet_col],
            np.where(
                df[price_col] < 0, 
                (100 / (-df[price_col])) * bet_size,
                bet_size*df[price_col] / 100
            ),
            -bet_size
        )
    )

def american_odds_to_breakeven_probability_vectorized(df, price_col='price'):
    odds = df[price_col]
    # Calculate the breakeven probability in a vectorized way
    return np.where(odds < 0, -odds / (-odds + 100), 100 / (100 + odds))