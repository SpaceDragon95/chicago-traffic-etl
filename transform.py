"""
Canonical transform functions for Chicago traffic ETL.
"""

# ====================
# Schema/ columns groups
# ====================

STRING_COLUMNS =
NUMERIC_TEXT_COLUMNS =
INT_COLUMNS =
DATETIME_COLUMNS =
CONVERT_DT_COLUMNS =

# ====================
# Transform functions
# ====================

def canonicalize_ids(df):
    # ---- Guardrails

    # ----- Universal ID cleanup
 
    # ----- Parse ID text

    # ----- Cast ID column
    pass

def standardize_strings(df):
    # ---- Guardrails
   
    # ----- Universal string cleanup
    
    # ----- Column-specific casing
    pass

def cast_numeric(df):
    # ---- Guardrails

    # ----- Universal numeric cleanup

    # ----- Parse numeric text

    # ----- Cast integer columns
    pass

def parse_datetimes(df):
    # ---- Guardrails

    # ----- Universal datetime cleanup
    
    # ----- Parse datetime text
    pass

# ====================
# Pipeline execution
# ====================

#df = standardize_strings(df)
#df = cast_numeric(df)
#df = parse_datetimes(df)
#df = canonicalize_ids(df)
