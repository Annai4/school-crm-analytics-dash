import pandas as pd

class DataFinalizer:
    def __init__(self, raw_tables, clean_tables):
        self.raw = raw_tables
        self.clean = clean_tables
        
        for key, df in clean_tables.items():
            setattr(self, key, df)

    def get_data_hygiene_report(self):
        report_list = []
        mapping = {'Deals': 'd1', 'Spend': 'd2', 'Calls': 'd3', 'Contacts': 'd4'}
        
        for label, key in mapping.items():
            raw_df = self.raw.get(key)
            clean_df = self.clean.get(key)
            
            if raw_df is not None and clean_df is not None:
                clean_cols = clean_df.columns.tolist()
                
                for col in raw_df.columns:
                    fill_rate = (raw_df[col].notnull().mean()) * 100
                    clean_name = col.lower().replace(' ', '_').replace('(', '').replace(')', '')
    
                    if (col in clean_cols or clean_name in clean_cols):
                        status = 'left'
                    else:
                        status = 'removed'
                    
                    report_list.append({
                        'Table': label, 
                        'Column': col, 
                        'Filling_%': round(fill_rate, 2), 
                        'Status': status
                    })
                    
        return pd.DataFrame(report_list)