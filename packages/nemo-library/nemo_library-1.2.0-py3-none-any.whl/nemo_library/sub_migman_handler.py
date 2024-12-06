import pandas as pd

class MigManHandler:
    
    def loadTemplate(self,project:str):
    
        filename = f"./nemo_library/migmantemplates/Template {project} MAIN.csv"
        print(filename)
        df = pd.read_csv(filename)
        print(df)
