from src.preprocess import *
from src.generate_features import *
#from src.train_model import *
from src.helpers.helpers import *

import pytest
import pandas as pd
import numpy as np

## Tests for functions in preprocess.py ###
def test_trim_columns():
    """ Test if trim_columns() returns accurate results """

    df_input = {'player': ['Nadal R.', ' Federer R.', 'Murray A. ', 'Wawrinka S.  '], 
    'court': ["Clay ", "Grass", "Hard", " Hard"],
    }
    df_badinput = {'player': ['Nadal R.', ' Federer R.', 'Murray A. ', 'Wawrinka S.  '], 
    'court': [1, 2, 3, 4],
    }
    df = pd.DataFrame(data=df_input)
    df_bad = pd.DataFrame(data=df_badinput)

    expected = {'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
    'court': ["Clay", "Grass", "Hard", "Hard"],
    }
    expected_bad = {'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
    'court': [1, 2, 3, 4],
    }
    
    expected_df = pd.DataFrame(data=expected)
    expected_bad_df = pd.DataFrame(data=expected_bad)

    # Check expected output
    assert expected_df.equals(trim_columns(df, df.columns.values))

    # Check expected bad output error handling
    assert expected_bad_df.equals(trim_columns(df_bad, df_bad.columns.values))

def test_select_columns():
    """ Test if select_columns() returns accurate results """
    
    df_input = {'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
    'court': ["Clay", "Grass", "Hard", "Hard"],
    'matchnumber': [1, 2, 3, 4]
    }
    cols_good = ['player', 'court']
    cols_bad = ['player', 'result']
    df = pd.DataFrame(data=df_input)

    expected = {'index': [0, 1, 2, 3],
    'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
    'court': ["Clay", "Grass", "Hard", "Hard"],
    }
    expected_df = pd.DataFrame(data=expected)

    # Check expected output
    assert expected_df.equals(select_columns(df, cols_good))

    # Check expected bad output error handling
    with pytest.raises(Exception) as excinfo:
        select_columns(df, cols_bad)
    assert str(excinfo.value) == "Error: columns not entirely found in the dataset" 

def test_gen_rankings_static():
    """ Test if gen_rankings_static() returns accurate results """
    
    df_input = {'Winner': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
    'Loser': ['Federer R.', 'Murray A.', 'Wawrinka S.', 'Nadal R.'],
    'Date': ["2011", "2012", "2013", "2014"],
    'WRank': [2, 4, 6, 8],
    'LRank': [1, 5, 3, 7]
    }
    df_bad = {'Winner': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
    'Loser': ['Federer R.', 'Murray A.', 'Wawrinka S.', 'Nadal R.'],
    'Date_New': ["2011", "2012", "2013", "2014"],
    }
    dfg = pd.DataFrame(data=df_input)
    dfb = pd.DataFrame(data=df_bad)

    expected = {'Player': ['Federer R.', 'Murray A.', 'Nadal R.', 'Wawrinka S.'], 
    'Rank': [4, 6, 7, 8],
    }
    expected_df = pd.DataFrame(data=expected)

    # Check expected output
    assert expected_df.equals(gen_rankings_static(dfg))

    # Check expected bad output error handling
    with pytest.raises(Exception) as excinfo:
        gen_rankings_static(dfb)
    assert str(excinfo.value) == "Required columns not present" 

def test_calculate_h2h():
    """ Test if calculate_h2h() returns accurate results """
    
    df_input = {'Winner': ['Nadal R.', 'Federer R.', 'Nadal R.', 'Nadal R.'], 
    'Loser': ['Federer R.', 'Nadal R.', 'Federer R.', 'Federer R.'],
    'Score': ["3-0", "3-2", "3-1", "3-0"]
    }
    dfg = pd.DataFrame(data=df_input)
    df_bad = {'Player1': ['Nadal R.', 'Federer R.', 'Nadal R.', 'Nadal R.'], 
    'Player2': ['Federer R.', 'Nadal R.', 'Federer R.', 'Federer R.'],
    'Score': ["3-0", "3-2", "3-1", "3-0"]
    }
    dfb = pd.DataFrame(data=df_bad)

    expected = {'Winner': ['Federer R.', 'Nadal R.'],
    'Loser': ['Nadal R.', 'Federer R.'], 
    'h2h_win': [1.0, 3.0],
    'h2h_lost': [3.0, 1.0],
    'totalPlayed': [4.0, 4.0],
    'h2h_win_pct': [0.25, 0.75]
    }
    expected_df = pd.DataFrame(data=expected)

    # Check expected output
    assert expected_df.equals(calculate_h2h(dfg))

    # Check expected bad output error handling
    with pytest.raises(Exception) as excinfo:
        calculate_h2h(dfb)
    assert str(excinfo.value) == "Required columns not present" 

def test_calculate_surface_winpct():
    """ Test if calculate_surface_winpct() returns accurate results """
    
    df_input = {'Winner': ['Nadal R.', 'Federer R.', 'Nadal R.', 'Nadal R.'], 
    'Loser': ['Federer R.', 'Nadal R.', 'Federer R.', 'Federer R.'],
    'Surface': ["Clay", "Grass", "Clay", "Grass"],
    'Score': ["3-0", "3-2", "3-1", "3-0"]
    }
    dfg = pd.DataFrame(data=df_input)
    df_bad = {'Player1': ['Nadal R.', 'Federer R.', 'Nadal R.', 'Nadal R.'], 
    'Player2': ['Federer R.', 'Nadal R.', 'Federer R.', 'Federer R.'],
    'Score': ["3-0", "3-2", "3-1", "3-0"]
    }
    dfb = pd.DataFrame(data=df_bad)

    expected = {'Player': ['Federer R.', 'Nadal R.', 'Nadal R.', 'Federer R.'],
    'Surface': ["Grass", "Clay", "Grass", "Clay"],
    'surf_matches': [2.0, 2.0, 2.0, 2.0],
    'surf_winpct': [0.5, 1.0, 0.5, 0.0]
    }
    expected_df = pd.DataFrame(data=expected)

    # Check expected output
    assert expected_df.equals(calculate_surface_winpct(dfg))

    # Check expected bad output error handling
    with pytest.raises(Exception) as excinfo:
        calculate_surface_winpct(dfb)
    assert str(excinfo.value) == "Required columns not present" 

## Tests for functions in generate_features.py ###

def test_fewGamesCorrection():
    """ Test if fewGamesCorrection() returns accurate results """
    
    df_input = {'p1': ['A', 'B', 'C', 'D'], 
    'p2': ['B', 'C', 'D', 'E'],
    'totalPlayed': [0, 1, 20, 10],
    'winPct': [0.0, 1.0, 0.7, 0.4]
    }
    df = pd.DataFrame(data=df_input)

    expected = {'p1': ['A', 'B', 'C', 'D'], 
    'p2': ['B', 'C', 'D', 'E'],
    'totalPlayed': [0.0, 1.0, 20.0, 10.0],
    'winPct': [0.5, 0.5, 0.7, 0.4]
    }
    expected_df = pd.DataFrame(data=expected)

    # Check expected bad output would return original dataset as desired
    assert df.equals(fewGamesCorrection(df, ['winPct'], 'ClayPlayed', 2.0, 0.5))

    # Check expected output
    assert expected_df.equals(fewGamesCorrection(df, ['winPct'], 'totalPlayed', 2.0, 0.5))

def test_add_h2h():
    """ Test if add_h2h() returns accurate results """
    
    df_input = {'Winner': ['Nadal R.', 'Federer R.'],
    'Loser': ['Federer R.', 'Nadal R.'],
    'Rank': [1, 2]
    }
    df = pd.DataFrame(data=df_input)
    h2h = {'Winner': ['Federer R.', 'Nadal R.', 'Nadal R.'],
    'Loser': ['Nadal R.', 'Federer R.', 'Murray A.'], 
    'h2h_win': [1.0, 3.0, 4.0],
    'h2h_lost': [3.0, 1.0, 2.0],
    'totalPlayed': [4.0, 4.0, 6.0],
    'h2h_win_pct': [0.25, 0.75, 0.66]
    }
    df_h2h = pd.DataFrame(data=h2h)
    h2h_bad = {'Winner': ['Federer R.', 'Nadal R.', 'Nadal R.'],
    'h2h_count': [2, 2, 4]
    }
    df_h2h_bad = pd.DataFrame(data=h2h_bad)

    expected = {'Winner': ['Nadal R.', 'Federer R.'], 
    'Loser': ['Federer R.', 'Nadal R.'],
    'Rank': [1, 2],
    'h2h_win': [3.0, 1.0],
    'h2h_lost': [1.0, 3.0],
    'totalPlayed': [4.0, 4.0],
    'h2h_win_pct': [0.75, 0.25]
    }
    expected_df = pd.DataFrame(data=expected)

    # Check expected bad input returns orginal df
    assert df.equals(add_h2h(df, df_h2h_bad))

    # Check expected output
    assert expected_df.equals(add_h2h(df, df_h2h))

def test_add_surface_winpct():
    """ Test if calculate_surface_winpct() returns accurate results """
    
    df_input = {'Winner': ['Nadal R.', 'Federer R.'], 
    'Loser': ['Federer R.', 'Nadal R.'],
    'Surface': ["Clay", "Clay"],
    }
    df = pd.DataFrame(data=df_input)
    surf = {'Player': ['Federer R.', 'Nadal R.', 'Nadal R.'],
    'Surface': ["Clay", "Clay", "Glass"],
    'surf_matches': [20, 30, 15],
    'surf_winpct':  [0.8, 0.9, 0.7]
    }
    df_surf = pd.DataFrame(data=surf)
    surf_bad = {'Player': ['Federer R.', 'Nadal R.', 'Nadal R.'],
    'surf_matches': [20, 30, 15],
    'surf_winpct':  [0.8, 0.9, 0.7]
    }
    df_surf_bad = pd.DataFrame(data=surf)

    expected = {'Winner': ['Nadal R.', 'Federer R.'], 
    'Loser': ['Federer R.', 'Nadal R.'],
    'Surface': ["Clay", "Clay"],
    'surf_matches_x': [30, 20],
    'surf_winpct_x':  [0.9, 0.8],
    'surf_matches_y': [20, 30],
    'surf_winpct_y':  [0.8, 0.9]
    }
    expected_df = pd.DataFrame(data=expected)

    # Check expected bad input returns orginal df
    assert df.equals(add_h2h(df, df_surf_bad))

    # Check expected output
    assert expected_df.equals(add_surface_winpct(df, df_surf))

def test_flip_records():
    """ Test if flip_records() returns accurate results """
    
    df_input = {'Winner': ['Nadal R.'], 'Loser': ['Federer R.'],
    'WRank': [1], 'LRank':[2], 'Wsets': [3], 'Lsets':[2], 'h2h_win_pct':[0.6],
    'h2h_win': [10], 'h2h_lost': [5], 'surf_matches_x': [20], 'surf_matches_y': [10],
    'surf_winpct_x': [0.9], 'surf_winpct_y': [0.7], 'index':[0]}
    df = pd.DataFrame(data=df_input)

    expected = df_input = {'Player1': ['Federer R.'], 'Player2': ['Nadal R.'],
    'Rank_P1': [2], 'Rank_P2': [1], 'Sets_P1':[2], 'Sets_P2':[3], 'h2h_win_pct':[0.4],
    'h2hwin_P1': [5], 'h2hwin_P2': [10], 'index':[0], 'matchresult': ['L'],
    'mp_surface_P1': [10], 'mp_surface_P2': [20],
    'winpct_surface_P1': [0.7], 'winpct_surface_P2': [0.9], }
    expected_df = pd.DataFrame(data=expected)

    # Check expected output
    assert expected_df.equals(flip_records(df, seednumber=4))

# def test_choose_features():
#     """ Test if choose_features() returns accurate results """
    
#     df_input = {'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
#     'court': ["Clay", "Grass", "Hard", "Hard"],
#     'matchnumber': [1, 2, 3, 4]
#     }
#     df = pd.DataFrame(data=df_input)

#     expected = {'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
#     'court': ["Clay", "Grass", "Hard", "Hard"],
#     }
#     expected_df = pd.DataFrame(data=expected)

#     # Check expected output
#     assert expected_df.equals(choose_features(df, features_to_use=['player'], target='court'))

# def test_split_train_test():
#     """ Test if choose_features() returns accurate results """
    
#     df_input = {'feature': [1, 2, 3, 4], 
#     'target': [10, 12, 14, 16],
#     }
#     df = pd.DataFrame(data=df_input)
#     result = split_train_test(df, 'target', test_size = 0.25, random_state = 42)

#     # Check expected output has the correct dimensions
#     assert len(result[0]) == 3
#     assert len(result[1]) == 1
#     assert len(result[2]) == 3
#     assert len(result[3]) == 1

### test_fit_xgboost: This is just a wrapper function for fitting the XGBoost model,
### there is no way to check this model without involving manual handling of the data

## Tests for functions in helpers.helpers.py ###
def test_setFeatureType():
    """ Test if setFeatureType convert columns to accurate types """
    
    df_input1 = {'target': [10, 12, 14, 16]}
    df_input2 = {'target': ['10', '12', 'k', '16']}
    df1 = pd.DataFrame(data=df_input1)
    df2 = pd.DataFrame(data=df_input2)
    
    exp_output1 = {'target': ['10', '12', '14', '16']}
    exp_output2 = {'target': ['10', '12', 'k', '16']}
    ef1 = pd.DataFrame(data=exp_output1)
    ef2 = pd.DataFrame(data=exp_output2)

    # Check expected output
    setFeatureType(df1, ['target'], 'str')
    assert ef1.equals(df1)

    # Check expected bad input returns orginal df
    setFeatureType(df2, ['target'], 'int') # df2 should not convert
    assert ef2.equals(df2)

def test_fillColumnNAs():
    """ Test if fillColumnNAs replaces missing values with specified values """
    
    df_input = {'target1': [10.0, 12.0, 14.0, np.nan],
    'target2': [1.0, np.nan, 3.0, np.nan]}
    df = pd.DataFrame(data=df_input)

    expected_output = {'target1': [10.0, 12.0, 14.0, 0.0],
    'target2': [1.0, 0.0, 3.0, 0.0]}
    ef = pd.DataFrame(data=expected_output)

    # Check expected output
    fillColumnNAs(df, df.columns, 0)
    assert ef.equals(df)

### Other functions involving loading/writing files or database operations are not tested