# Patch to correct analyzer logic for XtremeReversal strategy
# File: analyzer.py (partial snippet)

# Assuming necessary imports and utilities are defined above

def analyze_chart(candles):
    trigger_base_found = False
    reversal_buffer_found = False
    tb_direction = None
    entry_signal = None
    
    last_tb_index = find_last_trigger_base(candles)
    current_index = len(candles) - 1
    
    # --- Logic A: Check for Trigger Base after 30 bars ---
    if last_tb_index is not None and (current_index - last_tb_index) >= 30:
        opposite_tb = find_opposite_trigger_base(candles[last_tb_index + 1:])
        if opposite_tb:
            entry_signal = opposite_tb['direction']
            return f"{entry_signal.upper()} Signal (Confirmed)"

    # --- Logic B: No opposite TB, Check for Reversal Buffer after 40 bars ---
    if last_tb_index is not None and (current_index - last_tb_index) >= 40:
        if not find_opposite_trigger_base(candles[last_tb_index + 1:]):
            if is_reversal_buffer_forming(candles[-5:]):
                return "Buy Setup Forming (Reversal Buffer)" if is_downtrend(candles) else "Sell Setup Forming (Reversal Buffer)"
            if is_reversal_buffer_confirmed(candles[-3:]):
                entry_signal = "Buy" if is_downtrend(candles) else "Sell"
                return f"{entry_signal.upper()} Signal (Confirmed)"

    # --- Logic C: Setup still forming ---
    if is_m4_outside_bb(candles[-1]):
        return "Setup Forming"

    return "Invalid"

# Note: Supporting functions like `find_last_trigger_base`, `find_opposite_trigger_base`,
# `is_reversal_buffer_forming`, `is_reversal_buffer_confirmed`, `is_m4_outside_bb`, `is_downtrend`
# are assumed to be defined and working correctly.
