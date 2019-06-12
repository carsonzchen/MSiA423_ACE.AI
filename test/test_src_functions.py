from src.preprocess import *

import pytest
import pandas as pd

### Tests for functions in preprocess.py ###
# def test_trim_columns():
#     """ Test if trim_columns() returns accurate results """

#     df_input = {'player': ['Nadal R.', ' Federer R.', 'Murray A. ', 'Wawrinka S.  '], 
#     'court': ["Clay ", "Grass", "Hard", " Hard"],
#     }
#     df_badinput = {'player': ['Nadal R.', ' Federer R.', 'Murray A. ', 'Wawrinka S.  '], 
#     'court': [1, 2, 3, 4],
#     }
#     df = pd.DataFrame(data=df_input)
#     df_bad = pd.DataFrame(data=df_badinput)

#     expected = {'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
#     'court': ["Clay", "Grass", "Hard", "Hard"],
#     }
#     expected_bad = {'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
#     'court': [1, 2, 3, 4],
#     }
    
#     expected_df = pd.DataFrame(data=expected)
#     expected_bad_df = pd.DataFrame(data=expected_bad)

#     # Check expected output
#     assert expected_df.equals(trim_columns(df, df.columns.values))

#     # Check expected bad output error handling
#     assert expected_bad_df.equals(trim_columns(df_bad, df_bad.columns.values))

# def test_select_columns():
#     """ Test if select_columns() returns accurate results """
    
#     df_input = {'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
#     'court': ["Clay", "Grass", "Hard", "Hard"],
#     'matchnumber': [1, 2, 3, 4]
#     }
#     cols_good = ['player', 'court']
#     cols_bad = ['player', 'result']
#     df = pd.DataFrame(data=df_input)

#     expected = {'index': [0, 1, 2, 3],
#     'player': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
#     'court': ["Clay", "Grass", "Hard", "Hard"],
#     }
#     expected_df = pd.DataFrame(data=expected)

#     # Check expected output
#     assert expected_df.equals(select_columns(df, cols_good))

#     # Check expected bad output error handling
#     with pytest.raises(Exception) as excinfo:
#         select_columns(df, cols_bad)
#     assert str(excinfo.value) == "Error: columns not entirely found in the dataset" 

# def test_gen_rankings_static():
#     """ Test if gen_rankings_static() returns accurate results """
    
#     df_input = {'Winner': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
#     'Loser': ['Federer R.', 'Murray A.', 'Wawrinka S.', 'Nadal R.'],
#     'Date': ["2011", "2012", "2013", "2014"],
#     'WRank': [2, 4, 6, 8],
#     'LRank': [1, 5, 3, 7]
#     }
#     df_bad = {'Winner': ['Nadal R.', 'Federer R.', 'Murray A.', 'Wawrinka S.'], 
#     'Loser': ['Federer R.', 'Murray A.', 'Wawrinka S.', 'Nadal R.'],
#     'Date_New': ["2011", "2012", "2013", "2014"],
#     }
#     dfg = pd.DataFrame(data=df_input)
#     dfb = pd.DataFrame(data=df_bad)

#     expected = {'Player': ['Federer R.', 'Murray A.', 'Nadal R.', 'Wawrinka S.'], 
#     'Rank': [4, 6, 7, 8],
#     }
#     expected_df = pd.DataFrame(data=expected)

#     # Check expected output
#     assert expected_df.equals(gen_rankings_static(dfg))

#     # Check expected bad output error handling
#     with pytest.raises(Exception) as excinfo:
#         gen_rankings_static(dfb)
#     assert str(excinfo.value) == "Required columns not present" 

# def test_calculate_h2h():
#     """ Test if calculate_h2h() returns accurate results """
    
#     df_input = {'Winner': ['Nadal R.', 'Federer R.', 'Nadal R.', 'Nadal R.'], 
#     'Loser': ['Federer R.', 'Nadal R.', 'Federer R.', 'Federer R.'],
#     'Score': ["3-0", "3-2", "3-1", "3-0"]
#     }
#     dfg = pd.DataFrame(data=df_input)
#     df_bad = {'Player1': ['Nadal R.', 'Federer R.', 'Nadal R.', 'Nadal R.'], 
#     'Player2': ['Federer R.', 'Nadal R.', 'Federer R.', 'Federer R.'],
#     'Score': ["3-0", "3-2", "3-1", "3-0"]
#     }
#     dfb = pd.DataFrame(data=df_bad)

#     expected = {'Winner': ['Federer R.', 'Nadal R.'],
#     'Loser': ['Nadal R.', 'Federer R.'], 
#     'h2h_win': [1.0, 3.0],
#     'h2h_lost': [3.0, 1.0],
#     'totalPlayed': [4.0, 4.0],
#     'h2h_win_pct': [0.25, 0.75]
#     }
#     expected_df = pd.DataFrame(data=expected)

#     # Check expected output
#     assert expected_df.equals(calculate_h2h(dfg))

#     # Check expected bad output error handling
#     with pytest.raises(Exception) as excinfo:
#         calculate_h2h(dfb)
#     assert str(excinfo.value) == "Required columns not present" 

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