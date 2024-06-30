import pandas as pd
import kivy
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
#from android.os import Environment

kivy.require('1.0.7')

KV = '''
<Tabela>:
    viewclass: 'CustomLabel'
    RecycleGridLayout:
        id: layout
        default_size: None, dp(24)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(2)

<CustomLabel@Label>:
    font_size: '14sp'
    halign: 'right'
    valign: 'middle'
    text_size: self.size

BoxLayout:
    orientation: 'vertical'
    FileChooserListView:
        id: filechooser
        filters: ['*.csv']
        on_selection: app.load_csv(filechooser.selection)
    Button:
        text: 'Carregar Arquivo CSV'
        size_hint_y: None
        height: 50
        on_release: app.load_csv(filechooser.selection)
    Tabela:
        id: tabela
'''

class Tabela(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_data(self, data, num_cols):
        self.ids.layout.cols = num_cols
        self.data = [{'text': f'{value:>10}' if isinstance(value, str) else f'{value:>10.2f}'} for row in data for value in row]

class TabelaApp(App):
    def build(self):
        self.title = 'PolôSTAT'
#        downloads_path = Environment.getExternalStoragePublicDirectory(
#                        Environment.DIRECTORY_DOWNLOADS
#                        ).getAbsolutePath()

        return Builder.load_string(KV)

    def load_csv(self, selection):
        if selection:

            file_path = selection[0]

            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, sep=";")
                describe_df = df.describe(include='all').reset_index()

                # Tradução dos cabeçalhos da tabela
                traducoes = {
                    'index': 'campo',
                    'count': 'contagem',
                    'mean': 'média',
                    'std': 'desvio padrão',
                    'min': 'mínimo',
                    '25%': '25%',
                    '50%': '50%',
                    '75%': '75%',
                    'max': 'máximo'
                }

                # Renomear os cabeçalhos e a primeira coluna
                describe_df.rename(columns=traducoes, inplace=True)
                describe_df['campo'] = describe_df['campo'].map(traducoes).fillna(describe_df['campo'])

                # Convertendo o DataFrame em uma lista de listas e incluindo os cabeçalhos
                data = [describe_df.columns.to_list()] + describe_df.values.tolist()

                num_cols = len(describe_df.columns)
                tabela = self.root.ids.tabela
                tabela.update_data(data, num_cols)

if __name__ == '__main__':
    TabelaApp().run()
